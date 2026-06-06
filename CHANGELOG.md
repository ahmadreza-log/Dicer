# 📋 Changelog

All notable changes to **Dicer** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> ⚠️ **Maintenance rule:** Update this file with every meaningful change before merging.

---

## [Unreleased]

### ✨ Added
- 🗄️ MySQL database layer with pluggable `database/Engine.py` facade and `mysql/Driver.py`
- ⚙️ Database settings submenu — enable, host, port, user, password, test, connect/disconnect
- 📦 `requirements.txt` with `mysql-connector-python`

### 🔧 Changed
- 🗄️ Fix database menu — lazy MySQL import, direct toggle, test works without enabling first
- 🖥️ Interactive management CLI panel added (`cli/Menu.py`, `cli/Panel.py`, `cli/Manager.py`) — auto-starts server on launch
- ⚙️ Full Settings hub with Network, Logging, Connection, Security, and Save/Load/Reset submenus
- 💾 Settings persistence via `config/stored.json`
- 🔒 IP allow/block list enforcement on incoming connections

### 🚧 Planned
- Client application (`client/`)
- User-to-user messaging through the central server
- Authentication and session management

---

## [0.1.0] - 2026-06-06

### ✨ Added
- 🖥️ **Central TCP server** (`server/`) — socket-based hub for client connections
- 🧵 **Multi-client support** — threaded handler per connection
- 📁 **Modular server architecture** — split into `config`, `cli`, `network`, `hooks`, and `logger` folders
- 📊 **Logging system** — detailed console and rotating file logs under `server/logs/`
- ⚙️ **CLI arguments** — `--host`, `--port`, and `--level`
- 🛑 **Graceful shutdown** — SIGINT / SIGTERM signal handling

### 📌 Defaults
- Host: `127.0.0.1` (local development)
- Port: `5555`
- Log level: `INFO`

---

## Version History Summary

| Version | Date       | Highlights                          |
|---------|------------|-------------------------------------|
| 0.1.0   | 2026-06-06 | Initial central server + logging    |

[Unreleased]: https://github.com/ahmadreza-log/Dicer/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/ahmadreza-log/Dicer/releases/tag/v0.1.0
