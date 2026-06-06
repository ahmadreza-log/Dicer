# 🎲 Dicer

A peer-to-peer networking platform where users connect through a **central TCP server**. Clients join the hub and communicate with each other via the server — built in Python with sockets.

---

## 🏗️ Architecture

```
┌──────────┐       ┌─────────────────┐       ┌──────────┐
│ Client 1 │──────▶│  Central Server │◀──────│ Client 2 │
└──────────┘       │   (server/)     │       └──────────┘
                   └────────▲────────┘
                            │
                   ┌────────┴────────┐
                   │    Client 3     │
                   └─────────────────┘
```

| Component | Folder    | Status         | Description                              |
|-----------|-----------|----------------|------------------------------------------|
| 🖥️ Server | `server/` | ✅ In progress | Central TCP hub — accepts client connections |
| 📱 Client | `client/` | 🚧 Planned     | User application that connects to the server |

---

## ✨ Features (Server)

- 🔌 **TCP socket server** — multi-client, threaded connections
- 🗄️ **MySQL database layer** — pluggable engine with CLI settings (disabled by default)
- 📈 **Plotly Dash dashboard** — web UI for server status, controls, and live charts (Dash 4.x)
- 📊 **Detailed logging** — console + rotating file logs
- ⚙️ **CLI configuration** — host, port, and log level
- 🛑 **Graceful shutdown** — clean exit on Ctrl+C
- 📁 **Modular codebase** — split by responsibility for easy growth

---

## 🚀 Quick Start

### 📋 Requirements

- Python **3.10+**
- **MySQL** 8.x (optional, when database is enabled)
- Dependencies listed in `requirements.txt`

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

```bash
cd server
python main.py
```

This opens the **interactive management panel** and **starts the server automatically**:

| Option | Action |
|--------|--------|
| `1` | ⏯️ Toggle — Start or Stop the server (label changes with state) |
| `2` | 🔄 Restart the server |
| `3` | 📊 View detailed status (Screen 3) |
| `4` | 👥 List connected clients (Screen 3) |
| `5` | ⚙️ Settings — full settings hub (see below) |
| `0` | ❌ Exit and shut down |

After each action, a **message box** (Screen 2) or **detail screen** (Screen 3) is shown, then the main menu returns — no "Press Enter" step.

### ⚙️ Settings Hub (`[5]`)

| Option | Section |
|--------|---------|
| `1` | 🌐 **Network** — Host, Port, Listen Mode, Max Clients, Auto Start |
| `2` | 📊 **Logging** — Enable, Level, Console/File, Directory, Rotation |
| `3` | 🔗 **Connection** — Welcome Message, Buffer, Idle Timeout, Max/IP |
| `4` | 🔒 **Security** — Password, Allowed IPs, Blocked IPs |
| `5` | 🗄️ **Database** — MySQL host, port, user, password, test connection |
| `6` | 💾 **Save / Load / Reset** — persists to `config/stored.json` |
| `7` | 📋 **View All Settings** — full overview on Screen 3 |

For direct server start without the panel:

```bash
python main.py --headless
```

### 📈 Web Dashboard (Plotly Dash 4.x)

Run the browser-based management dashboard instead of the CLI panel:

```bash
python main.py --dash
```

Open **http://127.0.0.1:8050** (default). The TCP server auto-starts when `AutoStart` is enabled in settings.

| Widget | Description |
|--------|-------------|
| Status cards | Server state, host, uptime, client count |
| Controls | Start, Stop, Restart |
| Live chart | Connected clients over time |
| Client table | Active connection addresses |
| Database | MySQL connect, test, disconnect |

```bash
python main.py --dash --dash-host 127.0.0.1 --dash-port 8050
```

Built with [Plotly Dash 4.x](https://dash.plotly.com) and `dash-bootstrap-components` (CYBORG theme).

### 🧪 Test a Connection

```bash
python -c "import socket; p=socket.create_connection(('127.0.0.1',5555)); print(p.recv(1024).decode()); p.close()"
```

Expected output:

```
Connected to Dicer server
```

---

## ⚙️ CLI Options

| Flag           | Default      | Description                              |
|----------------|--------------|------------------------------------------|
| `--host`       | `127.0.0.1`  | Address the server binds to            |
| `--port`       | `5555`       | TCP port to listen on                    |
| `--level`      | `INFO`       | Log level (`DEBUG` … `CRITICAL`)         |
| `--headless`   | off          | Start TCP server only (no panel)         |
| `--dash`       | off          | Start Plotly Dash web dashboard          |
| `--dash-host`  | `127.0.0.1`  | Dash bind address                        |
| `--dash-port`  | `8050`       | Dash HTTP port                           |

```bash
python main.py --host 127.0.0.1 --port 5555 --level DEBUG
```

---

## 📁 Project Structure

```
Dicer/
├── server/
│   ├── main.py              # 🚀 Entry point
│   ├── config/
│   │   └── Settings.py      # 🌐 Network defaults
│   ├── cli/
│   │   └── Arguments.py     # ⌨️ CLI parsing
│   ├── board/
│   │   ├── App.py           # 📈 Dash application entry
│   │   ├── Layout.py        # 🎨 Dashboard layout
│   │   ├── Callbacks.py     # 🔄 Live updates & controls
│   │   ├── Bridge.py        # 🔗 Manager ↔ Dash bridge
│   │   └── Settings.py      # ⚙️ Dash host/port defaults
│   ├── network/
│   │   ├── Server.py        # 🖥️ TCP listener
│   │   ├── Handler.py       # 🔗 Per-client handler
│   │   └── Registry.py      # 📋 Active connections
│   ├── hooks/
│   │   └── Shutdown.py      # 🛑 Signal handling
│   ├── database/
│   │   ├── Engine.py        # 🗄️ Database facade
│   │   ├── Base.py          # 🔌 Driver interface
│   │   ├── Settings.py      # ⚙️ DB config
│   │   └── mysql/
│   │       └── Driver.py    # 🐬 MySQL driver
│   └── logger/
│       ├── Logger.py        # 📊 Logging facade
│       ├── Format.py        # 📝 Log format
│       ├── File.py          # 💾 File output
│       ├── Console.py       # 🖥️ Terminal output
│       ├── Level.py         # 📶 Level parsing
│       └── Settings.py      # ⚙️ Log config
├── client/                  # 🚧 Coming soon
├── requirements.txt         # 📦 Python dependencies
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

---

## 🗄️ Database (MySQL)

> ⏸️ **Disabled by default** — enable from **Settings → Database** in the management panel.

| Setting   | Default       | Description              |
|-----------|---------------|--------------------------|
| Type      | `MySQL`       | Engine type (extensible) |
| Host      | `127.0.0.1`   | MySQL server address     |
| Port      | `3306`        | MySQL port               |
| User      | `root`        | MySQL username           |
| Name      | `dicer`       | Database schema name     |

The `database/Engine.py` facade uses a driver pattern — MySQL now, stronger databases later.

---

## 📊 Logging

> ⏸️ **Temporarily disabled** — set `Enabled = True` in `server/logger/Settings.py` when logging is ready.

When enabled, logs are written to **both** the terminal and `server/logs/dicer.log`.

Example line:

```
2026-06-06 12:17:36.783 | INFO | Dicer.Server:Start:32 | MainThread | Server listening | host=127.0.0.1 | port=5555
```

| Setting   | Location                    | Default   |
|-----------|-----------------------------|-----------|
| Log file  | `server/logs/dicer.log`     | —         |
| Max size  | `logger/Settings.py`        | 5 MB      |
| Backups   | `logger/Settings.py`        | 5 files   |

---

## 🗺️ Roadmap

- [x] Central TCP server with socket connections
- [x] Multi-client threading
- [x] Structured logging system
- [x] MySQL database layer (pluggable drivers)
- [x] Plotly Dash 4.x web dashboard (`python main.py --dash`)
- [ ] Client application (`client/`)
- [ ] User registration and discovery
- [ ] Message relay between clients
- [ ] Production deployment (public IP / hosting)

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for coding standards and the documentation update policy.

Please note that this project follows the [Code of Conduct](CODE_OF_CONDUCT.md).

---

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history. **Update it with every release.**

---

## 🔒 Security

Report vulnerabilities privately — see [SECURITY.md](SECURITY.md).

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
