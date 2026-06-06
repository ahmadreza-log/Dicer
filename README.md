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
- 📊 **Detailed logging** — console + rotating file logs
- ⚙️ **CLI configuration** — host, port, and log level
- 🛑 **Graceful shutdown** — clean exit on Ctrl+C
- 📁 **Modular codebase** — split by responsibility for easy growth

---

## 🚀 Quick Start

### 📋 Requirements

- Python **3.10+**
- No external dependencies (stdlib only)

### 📦 Setup

```bash
git clone https://github.com/ahmadreza-log/Dicer.git
cd Dicer

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
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
| `5` | 💾 **Save / Load / Reset** — persists to `config/stored.json` |
| `6` | 📋 **View All Settings** — full overview on Screen 3 |

For direct server start without the panel:

```bash
python main.py --headless
```

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

| Flag       | Default      | Description                    |
|------------|--------------|--------------------------------|
| `--host`   | `127.0.0.1`  | Address the server binds to    |
| `--port`   | `5555`       | TCP port to listen on          |
| `--level`  | `INFO`       | Log level (`DEBUG` … `CRITICAL`) |

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
│   ├── network/
│   │   ├── Server.py        # 🖥️ TCP listener
│   │   ├── Handler.py       # 🔗 Per-client handler
│   │   └── Registry.py      # 📋 Active connections
│   ├── hooks/
│   │   └── Shutdown.py      # 🛑 Signal handling
│   └── logger/
│       ├── Logger.py        # 📊 Logging facade
│       ├── Format.py        # 📝 Log format
│       ├── File.py          # 💾 File output
│       ├── Console.py       # 🖥️ Terminal output
│       ├── Level.py         # 📶 Level parsing
│       └── Settings.py      # ⚙️ Log config
├── client/                  # 🚧 Coming soon
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

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
