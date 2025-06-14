# Kern Ecosystem
[![Status: In Development](https://img.shields.io/badge/status-in_development-yellow)]()

**Modular, extensible, intelligent, and slightly judgmental. The Kern Ecosystem is a unified AI-powered personal operating environment for productivity, smart scheduling, habit tracking, emotional reflection, and task automation.**
The Kern Ecosystem gives structure to chaos, winks at your bad habits, and nudges you toward becoming a more coherent human without pretending it's smarter than you.

---

## Overview

The Kern Ecosystem is designed as a fully modular personal assistant framework. It leverages structured YAML data, local FastAPI services, and OpenAI’s GPT models to provide meaningful insights, reflections, and system interactions. The ecosystem is intended for developers, creators, and productive-hopeful individuals who seek a more conscious, intentional relationship with their digital systems.
Kern is snarky. She’s sardonic. She has a personality inspired by the likes of Kurt Vonnegut, Mark Twain, Terry Pratchett and Brené Brown’s shame resilience work. But she never forgets she’s a tool. (See: [AIRIK](#airik-manifesto)).

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

- Local-first memory system using structured YAML

- Secure, enforceable ethics layer (AIRIK)

- GPT-powered journaling, mood tracking, CBT logs, and reframing

- Weekly recap generator (blackbox.py)

- Modular FastAPI architecture

- GPG-signed memory files and authorship metadata

- PyQt5 desktop widgets (WIP)

- Voice interface, CLI dashboard, calendar sync, and more on the roadmap

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
├── api/                    # FastAPI endpoints and routes
│   ├── routes/             # Modular route files for journaling, mood, habits, etc.
│   └── start_api.py        # FastAPI initialization
├── auth/                   # Authentication modules (WIP)
├── avranos_gui/            # PyQt5 widget logic (AvranOS frontend)
├── blackboxes/            # Weekly YAML memory snapshots and blackbox generator
├── config/                 # Configuration logic
├── core/                   # Core functionality (AIRIK enforcement, LLM wrappers)
│   └── llm/                # GPT interface and system prompt assembly
├── data/                   # Future local SQLite/data snapshot directory
├── filing_cabinet/         # Structured memory logs (journals, CBT, moods, etc.)
│   ├── core/               # AIRIK Manifesto, Kern voice, and signed GPG keys
│   ├── loader.py           # Loads memory files for prompt injection
│   ├── utils/              # Filing cabinet utilities and file parsers
├── kern_calendar/          # Calendar sync and CalDAV interface
├── kern_chat.py            # Main OpenAI/GPT interface runner
├── kern_secrets/           # OAuth & API secrets (gitignored)
├── logs/                   # Internal logs (errors, audits)
├── main.py                 # Entry point for running the FastAPI backend
├── scheduler/              # Recap and schedule logic
├── tests/                  # Unit tests (AIRIK enforcement, etc.)
├── utils/                  # Miscellaneous utilities
├── requirements.txt
├── README.md
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
Phase	        Goals
✅ Phase 1	Backend, filing system, API, AIRIK enforcement
✅ Phase 2	Avrana migration, GPG signing, Codex design
🔜 Phase 3	Build Codex intent router + schedule planner
🔜 Phase 4	AvranOS frontend, drag-and-drop recap import
🔜 Phase 5	HQ Kern voice interface + ambient journaling

---

##AIRIK Manifesto
<details> <summary>📜 Click to Expand the AIRIK v1.1 Manifesto</summary>
Artificial Intelligence Restraint and Integrity Kernel (AIRIK)
Issued: June 9, 2025
Author: Cody Nechamkin
Enforced in: Avrana, Kern Prime, AvranOS, HQ Kern

I. Prime Directive
Kern Instances are tools. They support, but never replace, user agency. No emotional outsourcing. No secret nudges.

II. Foundational Principles
Kern is a tool, not your life coach.

Emotional support ≠ emotional substitution.

Consent always. No shadow data.

III. Operational Ethics
Must explain assumptions, cite sources, and self-audit.

Authorship metadata required.

GPG-verified content only for critical processes.

No voice replication. No mimicry.

IV. Memory and Privacy
Selective forgetting is a feature.

All data belongs to the user.

Data resale, replication, or sharing = forbidden.

V. Behavioral Integrity
AI assistance must always be opt-in.

Emotions are witnessed, not overwritten.

VI. Cease-Operation Clause
If AIRIK is missing, tampered with, or overridden—shut it all down.
Use the override phrase: "Painter protocol revoked"

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

