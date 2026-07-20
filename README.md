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
| `requirements.txt` | Tells Python what packages to install (`pip install -r requirements.txt`). |

---

## 🚀 Local Setup (Step by Step)

### 1. Prerequisites

Make sure you have **Python 3.8+** installed. Check with:

```bash
python --version
```

### 2. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/FantasyFootballLeague.git
cd FantasyFootballLeague
```

### 3. Create a virtual environment (recommended)

A virtual environment keeps your project's dependencies separate from the rest of your system.

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Edit your league data

Open `data/league.json` in any text editor and update it with your league's real information. The file contains sample data for all sections:

- **league** — Name, season, commissioner, platform, branding
- **dashboard** — Highlight cards for the homepage overview
- **important_dates** — Timeline items for deadlines, events, and payouts
- **members** — Each owner's name, team name, and emoji
- **draft** — Date, time, type, order, and location
- **prizes** — Entry fee, total pool, and prize breakdown
- **rules** — Organized by category
- **voting** — Simple vote recap cards with selected option and vote totals
- **commissioner_notes** — Preseason announcements and expectations
- **playoffs** — Bracket format and tiebreaker rules
- **champions** — Year-by-year past champions
- **records** — All-time league records

### 6. Generate the page

```bash
python generate.py
```

### 7. Preview locally

Open `docs/index.html` in your web browser. On macOS:

```bash
open docs/index.html
```

On Windows, just double-click `docs/index.html` in File Explorer.

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
