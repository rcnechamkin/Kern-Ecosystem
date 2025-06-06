# Kern Ecosystem

**Modular, extensible, and intelligent. The Kern Ecosystem is a unified AI-powered personal operating environment for productivity, habit tracking, emotional reflection, and task automation.**

---

## Overview

The Kern Ecosystem is designed as a fully modular personal assistant framework. It leverages structured YAML data, local FastAPI services, and OpenAI’s GPT models to provide meaningful insights, reflections, and system interactions. The ecosystem is intended for developers, creators, and productivity-minded individuals who seek a more conscious, intentional relationship with their digital systems.

### Core Components

- **Avrana** – The backend brain. Runs all server-side logic including data logging, scheduling, calendar synchronization, and API serving.
- **AvranOS** – The user interface. A GUI built in Python (PyQt5 or equivalent) that interacts with Avrana and presents insights through a modular dashboard.
- **Kern Prime** – The conversational layer. Built on OpenAI's GPT-4o or GPT-3.5, this module provides coaching, conversational logging, and CBT-informed reflection tools.

---

## Features

- ✅ Local-first design using YAML logs and open protocols
- ✅ Modular backend API with FastAPI
- ✅ Calendar sync with Nextcloud (CalDAV)
- ✅ Mood and journal tracking
- ✅ Automated weekly recap generation
- ✅ Optional Samba-based drag-and-drop recap ingestion
- ✅ Extensible plugin system under development

---

## Technology Stack

- **Python 3.11+**
- **FastAPI** for backend services
- **PyQt5** for GUI (AvranOS)
- **OpenAI GPT APIs** (via `openai` Python package)
- **CalDAV** for calendar synchronization
- **Samba** for local network sharing
- **Markdown/YAML** for readable, version-controlled logs

---

## Project Structure

```bash
kern-ecosystem/
├── api/               # FastAPI backend exposing data to GUI or clients
├── auth/              # (Optional) Permissions, token handling
├── avranos_gui/       # GUI logic (PyQt5, sprite widgets, dashboards)
├── config/            # YAML config files for local vs remote instances
├── data/              # Metadata dumps, backups, or SQLite snapshots
├── filing_cabinet/    # Logs, journals, moods, habits, CBT notes
├── logs/              # System logs and alerts
├── scheduler/         # Recap builder, calendar sync, digest exports
├── secrets/           # Encrypted credentials (never committed)
├── utils/             # Shared tools, file watchers, CLI commands
├── README.md          # Project overview
└── .gitignore         # Hides secrets and system files
```

---

## Getting Started

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure Environment Variables**
```bash
cp .env.example .env
# Add OpenAI key, Nextcloud credentials, and any necessary paths
```

3. **Start Backend Services**
```bash
python main.py
```

4. **Optional: Enable Samba Sharing**
```bash
sudo apt install samba
# Configure access to the /filing_cabinet/ directory for drag-and-drop support
```

---

## Roadmap

- [x] FastAPI backend with structured logging
- [x] Local mood & journal entry support
- [x] Calendar integration with CalDAV
- [ ] Full-featured GUI dashboard (AvranOS)
- [ ] Plugin system for modular task extensions
- [ ] CLI tools for remote control and summary logging
- [ ] Voice interface integration
- [ ] Personal data archive for long-term digital memory

---

## License

MIT License

---

## Contact

For inquiries, collaborations, or contribution discussions, please reach out via GitHub Issues or fork the repository.

