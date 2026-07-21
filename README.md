# 🏈 Fantasy Football League Handbook

A Python-powered, static-site generator that turns a simple JSON data file into a clean, mobile-friendly fantasy football league handbook — hosted for free on GitHub Pages.

> **Goal:** No databases, no complicated frameworks. Just edit a JSON file, run one command, and share the link.

---

## 📁 Project Structure

```
FantasyFootballLeague/
├── data/
│   └── league.json        # ← Edit this file to update your league info
├── templates/
│   └── handbook.html      # Jinja2 HTML template (design lives here)
├── docs/
│   └── index.html         # Generated output — served by GitHub Pages
├── generate.py            # The script that builds the page
├── requirements.txt       # Python dependencies (just Jinja2)
├── .gitignore             # Files Git should ignore
└── README.md              # This file
```

**Why each file/folder exists:**

| Path | Purpose |
|---|---|
| `data/league.json` | Single source of truth for all league info. Edit this to update the site. |
| `templates/handbook.html` | HTML + CSS template. Jinja2 fills in the data placeholders. |
| `docs/index.html` | The final generated webpage. GitHub Pages serves this publicly. |
| `generate.py` | Reads the data, renders the template, writes `docs/index.html`. |
| `requirements.txt` | Tells Python what packages to install (`python -m pip install -r requirements.txt`). |

---

## 🚀 Local Setup (Step by Step)

> These instructions work for macOS, Linux, and Ubuntu-based WSL.

### 1. Prerequisites

Make sure you have **Python 3.8+** installed. Check with:

```bash
python3 --version
```

If your system also has a `python` command, that is fine too. In this guide, `python` commands are run from inside a virtual environment.

### 2. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/FantasyFootballLeague.git
cd FantasyFootballLeague
```

### 3. Create a virtual environment (recommended)

A virtual environment keeps your project's dependencies separate from the rest of your system.

```bash
python3 -m venv .venv
```

Activate it:

```bash
# macOS/Linux/WSL
source .venv/bin/activate
```

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bat
:: Windows Command Prompt (cmd)
.venv\Scripts\activate.bat
```

After activation, your shell prompt should show something like `(.venv)`.

### 4. Install dependencies

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

> Why this works better: some Linux/WSL installs block global `pip install` (PEP 668). Installing inside `.venv` avoids that problem.

### 5. Edit your league data

Open `data/league.json` in any text editor and update it with your league's real information. The file contains sample data for all sections:

- **league** — Name, season, commissioner, platform
- **members** — Each owner's name, team name, and emoji
- **draft** — Date, time, type, order, location
- **prizes** — Entry fee, total pool, prize breakdown
- **rules** — Organized by category
- **voting** — Past league votes and results
- **playoffs** — Bracket format and tiebreaker rules
- **champions** — Year-by-year past champions
- **records** — All-time league records

### 6. Generate the page

```bash
python generate.py
```

### 7. Preview locally

#### macOS

```bash
open docs/index.html
```

#### Linux desktop (with GUI browser installed)

```bash
xdg-open docs/index.html
```

#### WSL (Ubuntu on Windows)

Use Windows to open the generated file:

```bash
explorer.exe docs/index.html
```

If needed, use an absolute Windows path:

```bash
explorer.exe "$(wslpath -w "$PWD/docs/index.html")"
```

#### Fallback option (works everywhere)

Run a tiny local web server:

```bash
python -m http.server 8000 --directory docs
```

Then open:

- `http://localhost:8000` (from your browser on the same machine)

---

## 📡 Publishing with GitHub Pages

GitHub Pages hosts your site for free directly from this repository.

### Step 1: Push your changes to GitHub

```bash
git add .
git commit -m "Update league data for 2025 season"
git push origin main
```

### Step 2: Enable GitHub Pages

1. Go to your repository on GitHub.
2. Click **Settings** → **Pages** (in the left sidebar).
3. Under **Source**, select **Deploy from a branch**.
4. Set **Branch** to `main` and **Folder** to `/docs`.
5. Click **Save**.

### Step 3: Access your live site

After a minute or two, your handbook will be live at:

```
https://YOUR_USERNAME.github.io/FantasyFootballLeague/
```

Share this link with your league members!

---

## 🔄 Making Updates

Whenever you need to update the handbook (new draft order, rule changes, etc.):

1. Edit `data/league.json`
2. Run `python generate.py`
3. Commit and push:
   ```bash
   git add .
   git commit -m "Update draft order for 2025"
   git push origin main
   ```

GitHub Pages will automatically redeploy your updated page within a minute.

---

## ❗ Common Troubleshooting

### `Command 'python' not found`

Use `python3` to create the environment:

```bash
python3 -m venv .venv
```

Then activate it and use `python ...` commands from inside `.venv`.

### `error: externally-managed-environment` during `pip install`

You are likely installing outside a virtual environment on Linux/WSL. Activate `.venv` and run:

```bash
python -m pip install -r requirements.txt
```

### `py generate.py` fails on Linux/WSL

Use:

```bash
python generate.py
```

The `py` launcher is mainly a Windows workflow and may behave differently on Linux.

### `xdg-open` cannot open `docs/index.html` in WSL

WSL usually has no Linux GUI browser installed. Use:

```bash
explorer.exe docs/index.html
```

or run a local server (`python -m http.server 8000 --directory docs`) and open `http://localhost:8000` in Windows.

---

## 💡 Future Feature Ideas

Here are some ways you could expand this project as you learn more:

| Feature | What You'd Learn |
|---|---|
| **Multiple seasons** — Store each season in a separate JSON file | File organization, data modeling |
| **Dark mode toggle** — Add a button to switch themes | JavaScript, CSS variables |
| **Standings table** — Pull in weekly win/loss records | Python data manipulation |
| **Search/filter** — Filter records by year or owner | JavaScript DOM manipulation |
| **Automatic rebuild** — Use GitHub Actions to auto-run `generate.py` on push | CI/CD, GitHub Actions |
| **Trade log** — Track every trade with date, teams, and players | JSON data design |
| **Charts** — Visualize points scored over the season | Python `matplotlib` or Chart.js |
| **Email/SMS notifications** — Notify owners of waiver claims | Python `smtplib`, APIs |

---

## 🛠️ Tech Stack

- **Python 3** — Generator script logic
- **Jinja2** — HTML templating engine
- **HTML5 / CSS3** — Mobile-friendly, responsive design (no external dependencies)
- **JSON** — Human-readable data storage
- **GitHub Pages** — Free static site hosting
