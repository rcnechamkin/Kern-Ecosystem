# Kern Ecosystem
[![Status: In Development](https://img.shields.io/badge/status-in_development-yellow)]()

**Modular, extensible, and intelligent. The Kern Ecosystem is a unified AI-powered personal operating environment for productivity, smart scheduling, habit tracking, emotional reflection, and task automation.**

---

## Overview

The Kern Ecosystem is designed as a fully modular personal assistant framework. It leverages structured YAML data, local FastAPI services, and OpenAI’s GPT models to provide meaningful insights, reflections, and system interactions. The ecosystem is intended for developers, creators, and productivity-minded individuals who seek a more conscious, intentional relationship with their digital systems.
This repository is the **master hub** of the Kern Ecosystem.

---

### Core Components (or "Kern Instances")

- **Avrana** — The backend brain. Runs all server-side logic via FastAPI, handling structured logs, calendar sync, recap generation, and OpenAI interactions.
- **AvranOS** — The desktop UI. A modular PyQt5 interface for interacting with your personal data, including widgets, dashboards, and sprite-based feedback (WIP).
- **Kern Prime** — The cognitive core. A conversational layer powered by GPT-4o or GPT-3.5 that responds with insight, wit, and CBT-informed coaching based on structured logs.
- **AvranOS Lite** — A future mobile or lightweight UI built for quick entries and portable logging.
- **Kern Calendar** — Calendar + task syncing layer powered by CalDAV (Nextcloud or similar).
- **HQ Kern** — Optional Raspberry Pi-based voice interface for ambient logging, commands, and verbal summaries.

---

## Features

- ✅ Local-first data logging using YAML + Git
- ✅ Structured API access to mood, journal, habit, and CBT logs
- ✅ Weekly "Black Box" recap generator (WIP)
- ✅ OpenAI API integration for intelligent summaries and prompts
- ✅ CalDAV calendar integration
- ✅ CLI endpoints and future command system
- ✅ Samba support for drag-and-drop recap ingestion

---

## Technology Stack

| Layer            | Tech                        |
|------------------|-----------------------------|
| Backend API      | Python 3.11+, FastAPI       |
| GUI Interface    | PyQt5 (AvranOS)             |
| AI Integration   | OpenAI GPT-4o/3.5 via `openai` |
| Calendar Sync    | CalDAV, Nextcloud           |
| File Handling    | YAML, Markdown, JSON        |
| File Sharing     | Samba                       |
| Logs & Archives  | Git, plain-text, SQLite (optional) |

---


## Current Avrana File Layout

```bash
avrana/
├── api/ # FastAPI endpoints
│ └── routes/ # Modular route files
├── filing_cabinet/ # Local YAML data logs (moods, CBT, etc.)
├── scheduler/ # Recap generators, calendar integration
├── secrets/ # API tokens, env files (gitignored)
├── logs/ # Internal log system
├── tests/ # (Coming soon)
├── main.py # Server entrypoint
├── README.md
└── .gitignore
```

---

## Getting Started

1. **Clone the Project**
```bash
git clone https://github.com/rcnechamkin/Kern-Ecosystem.git
cd Kern-Ecosystem
```

2. **Create and Activate Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configure Environment**
```bash
cp .env.example .env
# Add OpenAI key, CalDAV credentials, etc.
```

4. **Start the Backend API**
```bash
python main.py
```

5. **(Optional) Set Up Samba for Eventual Recap Sharing**
```bash
sudo apt install samba
# Configure access to /filing_cabinet/ in smb.conf
```
---

## Example Manual API Request

```bash
curl -X POST http://127.0.0.1:8000/cbt/log \
     -H "Content-Type: application/json" \
     -d '{
        "date": "2025-06-06",
        "mood": "anxious but focused",
        "thought_patterns": [
            "catastrophizing",
            "all-or-nothing thinking"
        ],
        "reframing": "I’m not doomed. I’m just overwhelmed, and that’s temporary."
     }'
```

---

## Roadmap
- Core YAML logging with FastAPI
- Mood, CBT, journal, sleep, and habit tracking
- Weekly recap generator
- GitHub integration with version control
- PyQt-based dashboard (AvranOS)
- GPT-powered schedule generator and check-in system
- CLI command toolkit
- Modular plugin system (calendar scraping, media logging, etc.)
- Mobile UI (AvranOS Lite)
- Voice interface (HQ Kern)

---

<details>
Planned Kern Ecosystem Layout (Monorepo)

```bash
kern-ecosystem/
├── backend/             # Avrana: FastAPI routes and logic
├── frontend/            # AvranOS: GUI layer
├── mobile/              # AvranOS Lite
├── calendar/            # Kern Calendar sync + scheduling tools
├── filing_cabinet/      # Structured logs (CBT, moods, habits)
├── auth/                # Optional permissions & token logic
├── avranos_gui/         # GUI widget logic & sprite interaction
├── config/              # Config files and YAML profiles
├── data/                # SQLite snapshots, backups, etc.
├── secrets/             # OpenAI keys, login tokens (gitignored)
├── logs/                # CLI logs, error tracking
├── scheduler/           # Recap generators, task engines
├── utils/               # CLI tools, file parsers, formatters
├── main.py              # Entry point to FastAPI
├── .gitignore           # Hides venv/, secrets, YAML logs
└── README.md            # This file
```
</details>

---

 ## Security and Privacy
- All logs stored locally in plain text YAML
- No data is uploaded unless explicitly configured (e.g. OpenAI API)
- .env, secrets/, and filing_cabinet/**/*.yaml are excluded from version control via .gitignore
- Future encryption layers planned for highly sensitive logs

---

## About the Creator
Built by **Cody Nechamkin**, a speculative fiction writer, systems thinker, and network engineer in training. The Kern Ecosystem reflects his obsession with cognitive transparency, narrative structure, and user-defined intelligence.

---

## License

MIT License. Do whatever you'd like with this project. Just don't try to sell it back to me.

---

## Contact

For inquiries, collaborations, or contribution discussions, please reach out via GitHub Issues or fork the repository.

