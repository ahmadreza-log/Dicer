# 🤝 Contributing to Dicer

Thank you for helping improve **Dicer**! This document explains how to contribute and keep the project healthy.

---

## 📋 Before You Start

1. 📖 Read the [README](README.md) to understand the project goals
2. 🔍 Check [existing issues](https://github.com/ahmadreza-log/Dicer/issues) to avoid duplicate work
3. 📝 For large changes, open an issue first to discuss the approach

---

## 🛠️ Development Setup

```bash
# Clone the repository
git clone https://github.com/ahmadreza-log/Dicer.git
cd Dicer

# Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# Run the server (CLI panel)
cd server
python main.py

# Or web dashboard + auto-start TCP
cd server
python main.py --dash

# Run the client (separate terminal)
cd client
python main.py
```

Local settings are written to `server/config/stored.json` and `client/stored.json` — both are **gitignored**. Mail **test mode** (Dash → Mail) is enough for registration without SMTP.

---

## 📁 Project Structure

```
Dicer/
├── server/          # Central TCP server, Dash board, MySQL, mail
│   ├── config/      # Defaults and stored.json (local)
│   ├── cli/         # CLI panel and Manager
│   ├── board/       # Plotly Dash dashboard
│   ├── network/     # Socket server, handlers, protocol
│   ├── database/    # Users, campaigns, activation codes
│   ├── mail/        # SMTP and test-mode sender
│   ├── room/        # In-memory game rooms
│   └── logger/
├── client/          # CustomTkinter GUI (auth, rooms, i18n)
│   ├── screens/
│   ├── network/
│   └── i18n/
└── docs/            # Additional documentation (if added)
```

---

## 📏 Coding Standards

All contributions must follow these rules:

| Rule | Description |
|------|-------------|
| 💬 **Comments** | Full explanations in **English** |
| 📂 **File split** | Keep files small and focused for easier development |
| 🔤 **PascalCase** | Classes, methods, and file names |
| 1️⃣ **Single-word names** | Files, classes, and variables (no single-letter names) |
| 📁 **Folders** | Group related files into dedicated folders |
| 📄 **File names** | Always single-word (e.g. `Server.py`, not `central_server.py`) |

### Example

```python
# ✅ Good
class Handler:
    def Run(self) -> None:
        peer = self.peer

# ❌ Avoid
class client_handler:
    def run_client(self):
        s = self.s
```

---

## 📝 Documentation Maintenance

> ⚠️ **Required:** When you change behavior, you **must** update the related docs in the same pull request.

| Change type              | Files to update                          |
|--------------------------|------------------------------------------|
| New feature              | `README.md`, `CHANGELOG.md`              |
| Bug fix                  | `CHANGELOG.md`                           |
| Breaking change          | `README.md`, `CHANGELOG.md`, migration notes |
| Security fix             | `SECURITY.md`, `CHANGELOG.md`            |
| Coding standard change   | `CONTRIBUTING.md`, `README.md`           |

---

## 🔀 Pull Request Process

1. 🌿 Create a branch from `main` (e.g. `feature/client-connect`)
2. ✏️ Make focused changes with clear commits
3. 📋 Update `CHANGELOG.md` under `[Unreleased]`
4. 📖 Update `README.md` if setup or usage changed
5. 🚀 Open a pull request using the [PR template](.github/PULL_REQUEST_TEMPLATE.md)
6. ✅ Wait for review and address feedback

---

## 🐛 Bug Reports

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md) and include:

- Steps to reproduce
- Expected vs actual behavior
- Server logs from `server/logs/dicer.log`
- Python version and OS

---

## 💡 Feature Requests

Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md).

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
