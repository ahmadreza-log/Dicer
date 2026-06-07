import smtplib
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path

from logger.Logger import Logger
from mail.Settings import Settings


class Sender:
    logger = Logger.Get("Mail")
    TestLogName = "test-mail.log"

    @classmethod
    def Send(cls, to_address: str, subject: str, body: str) -> tuple[bool, str]:
        address = to_address.strip()

        if not address:
            return False, "Recipient email is required."

        if Settings.TestMode:
            return cls._SendTest(address, subject, body)

        if not Settings.Enabled:
            cls.logger.warning(
                "Mail disabled | to=%s | subject=%s | body=%s",
                address,
                subject,
                body.replace("\n", " "),
            )
            return False, "Email service is not configured."

        try:
            message = EmailMessage()
            message["Subject"] = subject
            message["From"] = f"{Settings.FromName} <{Settings.FromAddress}>"
            message["To"] = address
            message.set_content(body)

            with smtplib.SMTP(Settings.Host, Settings.Port, timeout=20) as client:
                if Settings.UseTls:
                    client.starttls()

                if Settings.Username:
                    client.login(Settings.Username, Settings.Password)

                client.send_message(message)

            cls.logger.info("Mail sent | to=%s | subject=%s", address, subject)
            return True, ""
        except OSError as error:
            cls.logger.error("Mail failed | to=%s | reason=%s", address, error)
            return False, f"Could not send email: {error}"

    @classmethod
    def SendActivationCode(cls, to_address: str, username: str, code: str) -> tuple[bool, str]:
        subject = "Verify your Dicer account"
        body = (
            f"Hello {username},\n\n"
            f"Your Dicer verification code is: {code}\n\n"
            "Enter this 6-digit code in the app to verify your email.\n"
            "The code expires in 15 minutes.\n\n"
            "If you did not create an account, you can ignore this message."
        )
        return cls.Send(to_address, subject, body)

    @classmethod
    def _SendTest(cls, to_address: str, subject: str, body: str) -> tuple[bool, str]:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        entry = (
            f"[{timestamp}]\n"
            f"TO: {to_address}\n"
            f"SUBJECT: {subject}\n"
            f"{body}\n"
            f"{'=' * 60}\n"
        )
        banner = (
            "\n"
            "===== DICER TEST MAIL (SMTP skipped) =====\n"
            f"{entry}"
            "==========================================\n"
        )

        cls.logger.warning("TEST MAIL | to=%s | subject=%s", to_address, subject)
        print(banner, flush=True)
        cls._AppendTestLog(entry)
        return True, ""

    @classmethod
    def _AppendTestLog(cls, entry: str) -> None:
        log_dir = Path(__file__).resolve().parent.parent / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / cls.TestLogName

        try:
            with log_path.open("a", encoding="utf-8") as handle:
                handle.write(entry)
        except OSError as error:
            cls.logger.error("Test mail log failed | reason=%s", error)
