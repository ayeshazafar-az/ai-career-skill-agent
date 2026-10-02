<p align="center">
  <h1 align="center">⚡ NeuralCore OS — AI Career Agent</h1>
  <p align="center">
    <strong>Next-Generation Autonomous Career Intelligence Platform</strong>
  </p>
  <p align="center">
    An AI-powered career gap analysis tool that compares your resume skills against real-world job market demands using Google Gemini, generates actionable project-based learning roadmaps, and provides an interactive AI career coach — all within a premium Streamlit dashboard.
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-1.36-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Google%20Gemini-LLM-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini" />
  <img src="https://img.shields.io/badge/Supabase-Auth%20%26%20DB-3FCF8E?style=for-the-badge&logo=supabase&logoColor=white" alt="Supabase" />
  <img src="https://img.shields.io/badge/Plotly-Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly" />
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the App](#running-the-app)
- [Usage Workflow](#-usage-workflow)
- [Module Deep Dive](#-module-deep-dive)
- [Admin Panel](#-admin-panel)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🧠 Overview

**NeuralCore OS** is an end-to-end AI career intelligence platform that helps job seekers understand exactly where they stand relative to the market. Instead of guessing which skills to learn next, the platform:

1. **Extracts** skills from your resume (PDF or raw text) using Google Gemini's structured JSON output.
2. **Analyzes** target job descriptions (pre-loaded industry presets or custom-pasted JDs) to identify market-demanded skills and their frequency.
3. **Computes** a mathematical gap matrix that scores each skill as *Demonstrated*, *Theoretical*, or *Missing*, weighted by market demand frequency.
4. **Generates** a personalized, project-first learning roadmap powered by Gemini to close the most critical gaps.
5. **Provides** an interactive AI Career Coach chatbot grounded in your actual gap analysis data.

---

## ✨ Key Features

### 🎯 Precision Skill Extraction
- Parses resumes from **PDF upload** or **raw text paste**.
- Uses Gemini's strict JSON output mode to normalize skills (e.g., `Postgres` → `PostgreSQL`, `React.js` → `React`).
- Assigns evidence levels: **Demonstrated** (backed by projects/metrics) vs. **Theoretical** (only listed, no proof).

### 🔗 Live GitHub Portfolio Integration
- Optionally attach a GitHub profile URL.
- Fetches the 5 most recently updated public repositories via GitHub's public API.
- Injects repository context (name, description, primary language) directly into the AI analysis pipeline for more accurate skill evidence detection.

### 📊 Market Intelligence Dashboard
- **Radar/Spider Chart**: Visual comparison of candidate proficiency vs. market demand (top 10 skills) using Plotly.
- **Readiness Score Gauge**: A single percentage metric quantifying your overall market readiness.
- **Color-Coded Gap Matrix Table**: Sortable, styled DataFrame showing every skill, its market frequency, your status (Demonstrated/Theoretical/Missing), and evidence details.
- **High Priority Alerts**: Automatically flags skills with ≥50% market frequency that you haven't demonstrated.

### 🗺️ AI-Powered Roadmap Generation
- Generates a **3-step project-based learning roadmap** focusing on prerequisite logic (learn languages before frameworks).
- Each step includes a specific, actionable **micro-project** that serves as portfolio proof.
- Powered by Gemini with full gap context.

### 💬 Interactive AI Career Coach
- A conversational chatbot embedded directly in the roadmap tab.
- Fully grounded in your gap matrix data — ask questions like *"Why is Docker high priority?"* or *"What project should I build to prove React skills?"*.
- Maintains conversation history within the session.

### 🔐 Authentication & Role-Based Access Control (RBAC)
- Full **Sign Up / Login / Admin** authentication flow via Supabase Auth.
- Three access levels:
  - **Candidate**: Standard dashboard with full analysis capabilities.
  - **Administrator**: Access to the NeuralCore Command Center with telemetry and dataset management.
- Admin access controlled via environment variable (`ADMIN_SECRET_KEY`) or email matching (`ADMIN_EMAIL`).

### 🛡️ Admin Command Center
- Live telemetry: total analyses, unique users, system status.
- **Global Dataset Registry**: Live JSON editor to manage pre-loaded industry presets (job descriptions).
- Changes deploy instantly and affect the inference pipeline for all users.

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        STREAMLIT UI LAYER                       │
│  ┌──────────┐  ┌──────────────┐  ┌──────────┐  ┌────────────┐  │
│  │ Auth Page│  │  Dashboard   │  │  Charts  │  │Admin Panel │  │
│  └────┬─────┘  └──────┬───────┘  └────┬─────┘  └─────┬──────┘  │
│       │               │               │               │         │
├───────┴───────────────┴───────────────┴───────────────┴─────────┤
│                       SERVICE LAYER                             │
│  ┌────────────────┐  ┌───────────┐  ┌──────────────────────┐    │
│  │ Gemini Service │  │Gap Engine │  │  Roadmap Service     │    │
│  │ (Skill Extract)│  │(Math Core)│  │  (Roadmap + Chat)    │    │
│  └───────┬────────┘  └─────┬─────┘  └──────────┬───────────┘    │
│          │                 │                    │                │
│  ┌───────┴─────┐    ┌─────┴──────┐    ┌────────┴───────┐       │
│  │GitHub Svc   │    │ Supabase   │    │ Google Gemini  │       │
│  │(Portfolio)  │    │ Client     │    │ API            │       │
│  └─────────────┘    └────────────┘    └────────────────┘       │
├─────────────────────────────────────────────────────────────────┤
│                     EXTERNAL SERVICES                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ GitHub API   │  │ Supabase    │  │ Google Gemini 3.5    │   │
│  │ (Public)     │  │ (Auth + DB) │  │ Flash Lite           │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Resume (PDF/Text)  ──►  Gemini: Extract & Normalize Candidate Skills
                                         │
                                         ▼
Job Descriptions   ──►  Gemini: Extract & Normalize Market Skills
                                         │
                                         ▼
                        Gap Engine: Frequency Calculation
                        + Candidate ↔ Market Comparison
                                         │
                      ┌──────────────────┼──────────────────┐
                      ▼                  ▼                  ▼
              Readiness Score     Gap Matrix Table    AI Roadmap
                 (Gauge)          (Color-coded)     (Project-first)
                                                         │
                                                         ▼
                                                    AI Career Coach
                                                    (Context-aware Chat)
```

---

## 🛠 Tech Stack

| Layer         | Technology                   | Purpose                                   |
|---------------|------------------------------|-------------------------------------------|
| **Frontend**  | Streamlit 1.36               | Interactive web dashboard with custom CSS |
| **AI/LLM**    | Google Gemini 3.5 Flash Lite | Skill extraction, roadmap, chatbot        |
| **Auth & DB** | Supabase                     | User authentication, profile storage      |
| **Charts**    | Plotly 5.22                  | Radar charts, interactive visualizations  |
| **Data**      | Pandas 2.2                   | DataFrame manipulation, styled tables     |
| **PDF**       | pypdf 4.2                    | Resume PDF text extraction                |
| **Config**    | python-dotenv                | Environment variable management           |

---

## 📁 Project Structure

```
career-agent/
│
├── app.py                          # Main entry point — auth flow + routing
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (API keys, secrets)
│
├── .streamlit/
│   └── config.toml                 # Streamlit theme (dark mode, colors, fonts)
│
├── src/
│   ├── data/
│   │   └── presets.json            # Pre-loaded industry JD presets (Full-Stack, Data Scientist)
│   │
│   ├── db/
│   │   └── supabase_client.py      # Supabase connection + profile persistence
│   │
│   ├── services/
│   │   ├── gemini_service.py       # Gemini API: skill extraction (candidate + market)
│   │   ├── gap_engine.py           # Mathematical gap analysis engine
│   │   ├── roadmap_service.py      # AI roadmap generation + career coach chatbot
│   │   └── github_service.py       # GitHub API: portfolio context fetcher
│   │
│   └── ui/
│       ├── dashboard.py            # Main candidate dashboard (4-tab layout)
│       ├── admin_dashboard.py      # Admin command center (telemetry + dataset editor)
│       └── charts.py               # Plotly radar chart, readiness gauge, gap matrix table
│
├── extractor.py                    # (Reserved) Future module
├── gap_engine.py                   # (Reserved) Future module
├── roadmap.py                      # (Reserved) Future module
├── schemas.py                      # (Reserved) Future module
│
└── venv/                           # Python virtual environment
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** installed on your system
- A **Google Gemini API Key** (get one from [Google AI Studio](https://aistudio.google.com/))
- A **Supabase** project (optional — app works in demo mode without it)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/career-agent.git
   cd career-agent
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Supabase Configuration (Optional — app works without it in demo mode)
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_KEY="your-supabase-anon-key"

# Gemini API Configuration (Required)
GEMINI_API_KEY="your-gemini-api-key"

# Admin Configuration
ADMIN_SECRET_KEY="your-admin-secret"
ADMIN_EMAIL="admin@example.com"       # Optional — email-based admin detection
```

> **⚠️ Important:** Never commit your `.env` file to version control. Add it to `.gitignore`.

### Running the App

```bash
streamlit run app.py
```

The app will launch at `http://localhost:8501` by default.

---

## 📖 Usage Workflow

### For Candidates

1. **Register or Log In** on the authentication page.
2. Navigate to the **Engine Ingestion** tab:
   - **Phase 1 — Market Baseline**: Load a pre-built industry preset (Full-Stack Developer or Data Scientist) or paste a custom job description.
   - **Phase 2 — Candidate Context**: Upload your resume as a PDF or paste it as raw text.
   - *(Optional)* Attach your GitHub profile URL for richer analysis.
3. Click **"INITIALIZE CORE INFERENCE PIPELINE"** to run the analysis.
4. Explore results across three tabs:
   - **📊 Market Intel**: Radar chart + readiness score.
   - **🧩 Gap Matrix**: Full skill-by-skill breakdown with evidence levels and priorities.
   - **🗺️ Autonomous Action Plan**: AI-generated project roadmap + interactive career coach chatbot.

### For Administrators

1. Log in via the **Administrator** tab using the root secret key.
2. Access the **NeuralCore Command Center**:
   - View live telemetry (total analyses, unique users, system status).
   - Edit the **Global Dataset Registry** (preset job descriptions) via the live JSON editor.
   - Deploy updates that immediately affect the inference pipeline.

---

## 🔬 Module Deep Dive

### `gemini_service.py` — AI Skill Extraction

| Function                   | Purpose                                                              |
|----------------------------|----------------------------------------------------------------------|
| `get_gemini_client()`      | Configures and returns a Gemini model with strict JSON output mode   |
| `extract_candidate_skills()` | Extracts, normalizes, and categorizes skills from resume text      |
| `extract_market_skills()`  | Extracts required/preferred skills from multiple job descriptions    |
| `clean_json_response()`    | Strips markdown fences from Gemini responses before JSON parsing     |

**Key Design Decision:** The Gemini model is configured with `response_mime_type: "application/json"` to force structured output, eliminating the need for fragile regex parsing.

### `gap_engine.py` — Mathematical Analysis Core

| Function                       | Purpose                                                           |
|--------------------------------|-------------------------------------------------------------------|
| `calculate_market_frequencies()` | Computes skill appearance frequency (%) across all job descriptions |
| `analyze_gaps()`               | Cross-references candidate skills with market demands; computes readiness score |

**Readiness Score Formula:**
```
readiness = (Σ frequency × evidence_level) / (Σ frequency × 2) × 100
```
Where `evidence_level` is 0 (Missing), 1 (Theoretical), or 2 (Demonstrated), and 2 is the maximum.

**High Priority Logic:** A skill is flagged as high priority if its market frequency is ≥ 50% AND the candidate's evidence level is < 2 (not yet demonstrated).

### `roadmap_service.py` — Roadmap + Chat

| Function              | Purpose                                                                  |
|-----------------------|--------------------------------------------------------------------------|
| `generate_roadmap()`  | Creates a 3-step project-based roadmap from high-priority gaps           |
| `get_chat_response()` | Powers the AI career coach with full gap matrix context in the system prompt |

### `github_service.py` — Portfolio Evidence

| Function                          | Purpose                                              |
|-----------------------------------|------------------------------------------------------|
| `extract_github_username()`       | Parses GitHub username from a profile URL            |
| `fetch_github_portfolio_context()`| Fetches top 5 repos and formats them for AI ingestion|

> Uses GitHub's public API (60 req/hr rate limit, no auth token required).

---

## 🛡️ Admin Panel

The admin panel (`/admin`) is accessible via:

1. **Root Secret Key**: Enter the `ADMIN_SECRET_KEY` from `.env` in the Administrator tab.
2. **Email Match**: If `ADMIN_EMAIL` is set in `.env`, users with that email automatically see the admin view.
3. **Fallback**: If neither is configured, any email containing `"admin"` triggers admin mode.

### Admin Capabilities

| Feature                  | Description                                                        |
|--------------------------|--------------------------------------------------------------------|
| **Telemetry Dashboard**  | Total analyses, unique users, system connection status             |
| **System Operations Log**| Visual display of auth, Gemini, Supabase, and cache status         |
| **Dataset Registry**     | Live JSON editor for `presets.json` — deploy changes in real-time  |

---

## 🎨 Screenshots

> *Run the app locally to see the premium dark-mode UI with glassmorphism effects, gradient buttons, animated hover cards, and the full radar chart visualization.*

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request.

---

## 📄 License

This project is open-source. See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <strong>Built with ❤️ using Streamlit, Google Gemini, and Supabase</strong>
</p>
