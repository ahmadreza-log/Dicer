# 🎲 Dicer

A tabletop hub where clients connect through a **central TCP server** — game rooms, campaigns, and user accounts, built in Python with sockets and CustomTkinter.

---

## 🏗️ Architecture

```
┌──────────┐       ┌─────────────────┐       ┌──────────┐
│ Client 1 │──────▶│  Central Server │◀──────│ Client 2 │
│ (GUI)    │       │   (server/)     │       │ (GUI)    │
└──────────┘       │  TCP :12055     │       └──────────┘
                   │  Dash :8050     │
                   └────────▲────────┘
                            │
                   ┌────────┴────────┐
                   │    Client 3     │
                   └─────────────────┘
```

| Component | Folder    | Status         | Description                              |
|-----------|-----------|----------------|------------------------------------------|
| 🖥️ Server | `server/` | ✅ In progress | Central TCP hub, MySQL, Dash dashboard   |
| 📱 Client | `client/` | ✅ In progress | CustomTkinter GUI — auth, rooms, i18n  |

---

## ✨ Features

### Server
- 🔌 **TCP socket server** — multi-client, threaded connections (port **12055**)
- 🎲 **Game rooms** — 10-character room IDs; DM, player, and spectator roles
- 👤 **User accounts** — registration, login, email verification (6-digit codes)
- ✉️ **Mail** — SMTP delivery or **test mode** (codes logged locally, no SMTP required)
- 🗄️ **MySQL** — users, campaigns, activation codes; auto-connect and schema bootstrap
- 📈 **Plotly Dash dashboard** — live metrics, controls, users/mail settings (port **8050**)
- 📊 **Logging** — console + rotating file logs under `server/logs/`
- ⚙️ **CLI + web settings** — persist to `server/config/stored.json`

### Client
- 🔐 **Sign-in on startup** — register, verify email, then main menu
- 🏠 **Rooms** — DM creates/joins campaigns; players join by room ID (copy/paste)
- 🌐 **English / Persian** — RTL-aware UI with locale persisted in `client/stored.json`
- 📡 **Live presence** — authenticated clients stay connected as **Guest** until a game role is chosen

---

## 🚀 Quick Start

### 📋 Requirements

- Python **3.10+**
- **MySQL** 8.x (recommended — database is enabled by default)
- Dependencies in `requirements.txt`

### 📦 Setup

```bash
git clone https://github.com/ahmadreza-log/Dicer.git
cd Dicer

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

### ▶️ Run the Server

**Web dashboard (recommended for development):**

```bash
cd server
python main.py --dash
```

Open **http://127.0.0.1:8050**. The TCP server auto-starts when `AutoStart` is enabled (default).

**Interactive CLI panel:**

```bash
cd server
python main.py
```

**Headless TCP only:**

```bash
python main.py --headless
```

### ✉️ Email verification (development)

1. Open Dash → **Mail**
2. Enable **Test mode** (verification codes print to the server console and `server/logs/test-mail.log`)
3. Save settings

No real SMTP is required for local registration testing.

### 📱 Run the Client

```bash
cd client
python main.py
```

1. **Sign in** or **Create account**
2. Enter the 6-digit code from the server log (test mode) or your email (SMTP)
3. Use **Start** to create or join a room

Client network target: **Settings → Network** (default `127.0.0.1:12055`).

### 🧪 Test TCP

```bash
python -c "import socket; p=socket.create_connection(('127.0.0.1',12055)); print(p.recv(1024).decode()); p.close()"
```

Expected: `Connected to Dicer server`

---

## 📈 Web Dashboard

| Page / widget | Description |
|---------------|-------------|
| Dashboard | Server state, uptime, client count, **last 10** chart samples |
| Clients | Active TCP connections (Guest until a game role is registered) |
| Users | Registered MySQL accounts |
| Mail | SMTP + test mode for verification emails |
| Settings | Network, database, logging, save/load `stored.json` |

```bash
python main.py --dash --dash-host 127.0.0.1 --dash-port 8050
```

---

## ⚙️ CLI Options

| Flag           | Default      | Description                              |
|----------------|--------------|------------------------------------------|
| `--host`       | `127.0.0.1`  | Bind address (headless)                  |
| `--level`      | `INFO`       | Log level (`DEBUG` … `CRITICAL`)         |
| `--headless`   | off          | TCP server only (no panel)               |
| `--dash`       | off          | Plotly Dash web dashboard                |
| `--dash-host`  | `127.0.0.1`  | Dash bind address                        |
| `--dash-port`  | `8050`       | Dash HTTP port                           |

TCP game port is fixed at **12055**.

---

## 📁 Project Structure

```
Dicer/
├── server/
│   ├── main.py
│   ├── config/          # Network defaults, stored.json
│   ├── cli/             # Panel, Manager, arguments
│   ├── board/           # Dash dashboard
│   ├── network/         # TCP server, Handler, Protocol
│   ├── database/        # Engine, users, campaigns, activation_codes
│   ├── mail/            # SMTP + test mode sender
│   ├── security/        # Password hashing (PBKDF2)
│   ├── room/            # Live game rooms in memory
│   └── logger/
├── client/
│   ├── main.py
│   ├── App.py
│   ├── screens/         # Auth, Menu, Start, Room, Join, Settings…
│   ├── network/         # Session, Protocol
│   ├── i18n/            # en, fa locales
│   └── stored.json      # Local settings (gitignored)
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
└── LICENSE
```

---

## 🗄️ Database (MySQL)

| Setting   | Default       | Description              |
|-----------|---------------|--------------------------|
| Enabled   | `true`        | Auto-connect on server start |
| Host      | `127.0.0.1`   | MySQL server address     |
| Port      | `3306`        | MySQL port               |
| User      | `root`        | MySQL username           |
| Name      | `dicer`       | Schema name (auto-created) |

Configure in Dash → **Settings → Database** or CLI settings hub. Credentials persist in `server/config/stored.json` (gitignored).

---

## 📊 Logging

Logs go to the terminal and `server/logs/dicer.log` when file logging is enabled in settings.

| Path | Purpose |
|------|---------|
| `server/logs/dicer.log` | Server log (rotating) |
| `server/logs/test-mail.log` | Verification codes in mail test mode |

---

## 🔒 Local files (not committed)

| File | Purpose |
|------|---------|
| `server/config/stored.json` | Server settings |
| `client/stored.json` | Client locale, host, signed-in user |
| `server/logs/` | Runtime logs |
| `.env` | Secrets (if used) |

See `.gitignore` for the full list.

---

## 🗺️ Roadmap

- [x] Central TCP server with socket connections
- [x] Game rooms and campaign storage
- [x] User registration, login, and email verification
- [x] CustomTkinter client with i18n
- [x] Plotly Dash dashboard
- [ ] In-room chat and message relay
- [ ] Production deployment (public IP / hosting)

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Update **README.md** and **CHANGELOG.md** when behavior changes.

---

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md).

---

## 🔒 Security

Report vulnerabilities privately — see [SECURITY.md](SECURITY.md).

---

## 📜 License

[MIT License](LICENSE)
