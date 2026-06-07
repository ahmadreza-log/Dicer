import socket
from collections.abc import Callable

from connection.Settings import Settings as Connection
from database.campaigns.Repository import Repository as Campaigns
from database.users.Repository import Repository as Users
from logger.Logger import Logger
from network.Entry import Entry
from network.Protocol import Protocol
from network.Registry import Registry
from room.Registry import Registry as RoomRegistry


class Handler:
    # Handles the full lifecycle of a single client connection:
    # welcome message, receive loop, cleanup on disconnect.

    def __init__(
        self,
        peer: socket.socket,
        address: tuple[str, int],
        registry: Registry,
        rooms: RoomRegistry,
        running: Callable[[], bool],
    ) -> None:
        self.peer = peer
        self.address = address
        self.registry = registry
        self.rooms = rooms
        self.running = running
        self.logger = Logger.Get("Handler")
        self.buffer = ""

    # Runs on a dedicated thread for each connected client.
    def Run(self) -> None:
        self.logger.debug(
            "Handler started | address=%s | port=%d",
            self.address[0],
            self.address[1],
        )

        self.registry.Add(self.peer, self.address)

        try:
            if Connection.Timeout > 0:
                self.peer.settimeout(float(Connection.Timeout))

            welcome = f"{Connection.Welcome}\n".encode("utf-8")
            self.peer.sendall(welcome)
            self.logger.debug(
                "Welcome message sent | address=%s | port=%d",
                self.address[0],
                self.address[1],
            )
            self.ReceiveLoop()
        except (ConnectionResetError, TimeoutError, OSError) as error:
            self.logger.warning(
                "Connection error | address=%s | port=%d | reason=%s",
                self.address[0],
                self.address[1],
                error,
            )
        finally:
            self.Disconnect()

    # Continuously reads incoming data until the client closes or the server stops.
    def ReceiveLoop(self) -> None:
        while self.running():
            try:
                payload = self.peer.recv(Connection.Buffer)
            except TimeoutError:
                self.logger.info(
                    "Client idle timeout | address=%s | port=%d",
                    self.address[0],
                    self.address[1],
                )
                break

            if not payload:
                self.logger.info(
                    "Client closed connection | address=%s | port=%d",
                    self.address[0],
                    self.address[1],
                )
                break

            text = payload.decode("utf-8", errors="replace")
            self.buffer += text
            self.ProcessBuffer()

    # Parses complete newline-delimited messages from the receive buffer.
    def ProcessBuffer(self) -> None:
        while "\n" in self.buffer:
            line, self.buffer = self.buffer.split("\n", 1)
            line = line.strip()

            if line:
                self.HandleLine(line)

    # Handles a single decoded client message.
    def HandleLine(self, line: str) -> None:
        self.logger.info(
            "Message received | address=%s | port=%d | text=%s",
            self.address[0],
            self.address[1],
            line,
        )

        message = Protocol.Parse(line)

        if message is None:
            self.Reply(Protocol.Error("Invalid message format."))
            return

        message_type = message.get("type")

        if message_type == "register":
            self.HandleRegister(message)
            return

        if message_type == "list_campaigns":
            self.HandleListCampaigns(message)
            return

        if message_type == "save_campaign":
            self.HandleSaveCampaign(message)
            return

        if message_type == "register_user":
            self.HandleRegisterUser(message)
            return

        if message_type == "login_user":
            self.HandleLoginUser(message)
            return

        if message_type == "verify_email":
            self.HandleVerifyEmail(message)
            return

        if message_type == "resend_activation":
            self.HandleResendActivation(message)
            return

        self.Reply(Protocol.Error("Unknown message type."))

    # Registers the client role sent after connect.
    def HandleRegister(self, message: dict) -> None:
        role = str(message.get("role", "")).strip().lower()

        if role not in Protocol.ValidRoles:
            self.Reply(Protocol.Registered(False, error="Invalid role."))
            return

        if role == "dm":
            success, reason, room_payload = self._RegisterDungeonMaster(message)

            if not success:
                self.Reply(Protocol.Registered(False, error=reason))
                return
        else:
            success, reason, room_payload = self._RegisterMember(message, role)

            if not success:
                self.Reply(Protocol.Registered(False, error=reason))
                return

        self.Reply(Protocol.Registered(True, role=role, room=room_payload))

    # Returns saved campaigns for the requesting client owner.
    def HandleListCampaigns(self, message: dict) -> None:
        user_id = Protocol.ParseUserId(message)

        if user_id is None:
            self.Reply(Protocol.Campaigns(False, error="User id is required."))
            return

        success, reason, items = Campaigns.ListByUser(user_id)

        if not success:
            self.Reply(Protocol.Campaigns(False, error=reason))
            return

        self.Reply(Protocol.Campaigns(True, items=items))

    # Persists a new campaign template for later reuse.
    def HandleSaveCampaign(self, message: dict) -> None:
        user_id = Protocol.ParseUserId(message)

        if user_id is None:
            self.Reply(Protocol.CampaignSaved(False, error="User id is required."))
            return

        name, capacity, is_private, password = Protocol.ParseCampaignForm(message)

        if not name:
            self.Reply(Protocol.CampaignSaved(False, error="Campaign name is required."))
            return

        if capacity <= 0:
            self.Reply(Protocol.CampaignSaved(False, error="Player count must be greater than zero."))
            return

        success, reason, campaign = Campaigns.Save(
            user_id=user_id,
            name=name,
            capacity=capacity,
            is_private=is_private,
            password=password,
        )

        if not success or campaign is None:
            self.Reply(Protocol.CampaignSaved(False, error=reason))
            return

        public_campaign = {
            "id": campaign["id"],
            "name": campaign["name"],
            "capacity": campaign["capacity"],
            "private": campaign["private"],
        }
        self.Reply(Protocol.CampaignSaved(True, campaign=public_campaign))

    # Authenticates a registered account by username or email.
    def HandleLoginUser(self, message: dict) -> None:
        login, password = Protocol.ParseLogin(message)

        if not login or not password:
            self.Reply(Protocol.UserLoggedIn(False, error="Username and password are required."))
            return

        success, reason, user = Users.Authenticate(login, password)

        if not success or user is None:
            self.Reply(Protocol.UserLoggedIn(False, error=reason))
            return

        self.Reply(Protocol.UserLoggedIn(True, user=Protocol.PublicUser(user)))

    # Creates a registered account and emails a verification code.
    def HandleRegisterUser(self, message: dict) -> None:
        username, email, password = Protocol.ParseCredentials(message)
        success, reason, user = Users.Register(username, email, password)

        if not success or user is None:
            self.Reply(Protocol.UserRegistered(False, error=reason))
            return

        self.Reply(Protocol.UserRegistered(True, user=Protocol.PublicUser(user)))

    # Verifies a user's email with a 6-digit activation code.
    def HandleVerifyEmail(self, message: dict) -> None:
        user_id = Protocol.ParseUserId(message)
        code = Protocol.ParseVerificationCode(message)

        if user_id is None:
            self.Reply(Protocol.EmailVerified(False, error="User id is required."))
            return

        success, reason, user = Users.VerifyEmail(user_id, code)

        if not success or user is None:
            self.Reply(Protocol.EmailVerified(False, error=reason))
            return

        self.Reply(Protocol.EmailVerified(True, user=Protocol.PublicUser(user)))

    # Sends a fresh activation code to the user's email.
    def HandleResendActivation(self, message: dict) -> None:
        user_id = Protocol.ParseUserId(message)

        if user_id is None:
            self.Reply(Protocol.ActivationSent(False, error="User id is required."))
            return

        success, reason = Users.ResendActivation(user_id)

        if not success:
            self.Reply(Protocol.ActivationSent(False, error=reason))
            return

        self.Reply(Protocol.ActivationSent(True))

    # Creates a room owned by a Dungeon Master connection.
    def _RegisterDungeonMaster(self, message: dict) -> tuple[bool, str, dict | None]:
        user_id = Protocol.ParseUserId(message)
        campaign_id = message.get("campaign_id")
        campaign_name = ""
        stored_campaign_id = None
        visibility = None
        password = None
        capacity = None

        if campaign_id is not None:
            if user_id is None:
                return False, "User id is required.", None

            try:
                resolved_id = int(campaign_id)
            except (TypeError, ValueError):
                return False, "Invalid campaign ID.", None

            campaign = Campaigns.Get(resolved_id, user_id)

            if campaign is None:
                return False, "Campaign not found.", None

            campaign_name = campaign["name"]
            stored_campaign_id = campaign["id"]
            visibility = "private" if campaign["private"] else "public"
            password = campaign["password"]
            capacity = campaign["capacity"]
        else:
            visibility, password, capacity, campaign_name = Protocol.ParseRoomSettings(
                message.get("room"),
            )

        dm_address = f"{self.address[0]}:{self.address[1]}"
        room = self.rooms.Create(
            host_peer=self.peer,
            dm_address=dm_address,
            visibility=visibility,
            password=password,
            capacity=capacity,
            campaign_name=campaign_name,
            campaign_id=stored_campaign_id,
        )

        success, reason = self.registry.Register(self.peer, "dm")

        if not success:
            self.rooms.Remove(room.id)
            return False, reason, None

        entry = self.registry.Find(self.peer)

        if entry is not None:
            entry.room_id = room.id

        label = campaign_name or room.id
        self._LogActivity(
            f"Room {room.id} created for campaign '{label}' by Dungeon Master from {dm_address}",
        )
        return True, "", room.ToDict(include_password=True)

    # Joins an existing room as a player or spectator.
    def _RegisterMember(self, message: dict, role: str) -> tuple[bool, str, dict | None]:
        room_id, password = Protocol.ParseJoin(message)

        if not room_id:
            return False, "Room ID is required.", None

        joined, reason, room = self.rooms.Join(room_id, self.peer, role, password)

        if not joined or room is None:
            return False, reason, None

        success, register_reason = self.registry.Register(self.peer, role)

        if not success:
            self.rooms.Leave(self.peer)
            return False, register_reason, None

        entry = self.registry.Find(self.peer)

        if entry is not None:
            entry.room_id = room.id

        client_address = f"{self.address[0]}:{self.address[1]}"
        self._LogActivity(
            f"{Entry.RoleLabel(role)} joined room {room.id} from {client_address}",
        )
        return True, "", room.ToDict()

    # Writes to the dashboard activity feed when the panel is active.
    def _LogActivity(self, message: str) -> None:
        try:
            from board.Bridge import Bridge

            Bridge.Log(message, "success")
        except ImportError:
            self.logger.info(message)

    # Sends a JSON response line to the client.
    def Reply(self, payload: dict) -> None:
        try:
            self.peer.sendall(Protocol.Encode(payload) + b"\n")
        except OSError as error:
            self.logger.warning(
                "Reply failed | address=%s | port=%d | reason=%s",
                self.address[0],
                self.address[1],
                error,
            )

    # Removes the client from the registry and closes its socket.
    def Disconnect(self) -> None:
        entry = self.registry.Find(self.peer)

        if entry is not None and entry.room_id:
            if entry.role == "dm":
                self.rooms.Remove(entry.room_id)
            else:
                self.rooms.Leave(self.peer)

        self.registry.Remove(self.peer)
        self.peer.close()
        self.logger.info(
            "Client disconnected | address=%s | port=%d",
            self.address[0],
            self.address[1],
        )
