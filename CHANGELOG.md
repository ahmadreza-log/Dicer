# 📋 Changelog

All notable changes to **Dicer** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> ⚠️ **Maintenance rule:** Update this file with every meaningful change before merging.

---

## [Unreleased]

### ✨ Added
- 🔐 **Client auth gate** — sign-in / register on startup; email verification with 6-digit codes
- 👤 **User accounts** — MySQL `users` table with PBKDF2-SHA256 passwords and `activation_codes`
- ✉️ **Mail service** — SMTP settings plus **test mode** (codes logged to console and `server/logs/test-mail.log`)
- 📊 **Dashboard Users & Mail pages** — registered accounts and SMTP/test-mail configuration
- 🏠 **Room flow** — DM campaign picker, room screen, copy/paste room ID, join as player/spectator
- 🌐 **Client i18n** — English and Persian with RTL-aware layout
- 📱 **Client presence** — authenticated clients keep a live TCP connection (shown as Guest until a game role is chosen)
- 📈 Plotly Dash 4.x web dashboard (`server/board/`) — live status, server controls, client chart, MySQL panel
- 🗄️ MySQL database layer with pluggable `database/Engine.py` facade and auto-connect on server start
- 🎲 **Game rooms** — 10-character room IDs, DM/player/spectator roles
- 💾 **Campaign storage** — save/list campaigns per user in MySQL
- 📊 Dash sidebar panel — full settings forms, storage overview boxes, activity feed
- 🖥️ CustomTkinter client GUI (`client/`)
- ⌨️ CLI flags `--dash`, `--dash-host`, `--dash-port`, `--headless`

### 🔧 Changed
- 📈 Dashboard client chart now keeps only the **last 10** samples (cleaner x-axis)
- 🗄️ Database is **enabled by default**; schema `dicer` and tables are created automatically when MySQL is reachable
- 🔄 Campaign ownership uses `user_id` instead of device `owner_id`
- 💾 Client settings persist to `client/stored.json` (locale, network host, signed-in user)
- 🔌 TCP game port fixed at **12055** (Dash HTTP port remains **8050**)

### 🚧 Planned
- In-room chat and message relay between clients
- Logout and session refresh on the client
- Production deployment (public IP / hosting)

---

## [0.1.0] - 2026-06-06

### ✨ Added
- 🖥️ **Central TCP server** (`server/`) — socket-based hub for client connections
- 🧵 **Multi-client support** — threaded handler per connection
- 📁 **Modular server architecture** — split into `config`, `cli`, `network`, `hooks`, and `logger` folders
- 📊 **Logging system** — detailed console and rotating file logs under `server/logs/`
- ⚙️ **CLI arguments** — `--host`, `--level`, `--headless`, `--dash`
- 🛑 **Graceful shutdown** — SIGINT / SIGTERM signal handling

### 📌 Defaults
- Host: `127.0.0.1` (local development)
- TCP port: `12055`
- Log level: `INFO`

---

## Version History Summary

| Version | Date       | Highlights                          |
|---------|------------|-------------------------------------|
| Unreleased | —       | Auth, users, mail test mode, rooms, i18n client |
| 0.1.0   | 2026-06-06 | Initial central server + logging    |

[Unreleased]: https://github.com/ahmadreza-log/Dicer/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/ahmadreza-log/Dicer/releases/tag/v0.1.0
