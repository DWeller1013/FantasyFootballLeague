"""
generate.py — Fantasy Football League Handbook Generator

Reads league data from data/league.json, renders the Jinja2 template
in templates/handbook.html, and writes the final page to docs/index.html.

Usage:
    python generate.py

The output file (docs/index.html) is what GitHub Pages will serve publicly.
"""

import json
import os
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
DATA_FILE     = os.path.join(BASE_DIR, "data", "league.json")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
OUTPUT_DIR    = os.path.join(BASE_DIR, "docs")
OUTPUT_FILE   = os.path.join(OUTPUT_DIR, "index.html")


def load_data(path: str) -> dict:
    """Load and return the JSON data file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def render_template(data: dict, templates_dir: str) -> str:
    """Render the handbook template with the provided data."""
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template("handbook.html")

    context = {
        "league":       data["league"],
        "members":      data["members"],
        "draft":        data["draft"],
        "prizes":       data["prizes"],
        "rules":        data["rules"],
        "voting":       data["voting"],
        "playoffs":     data["playoffs"],
        "champions":    data["champions"],
        "records":      data["records"],
        "generated_on": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
    }

    return template.render(**context)


def write_output(html: str, output_dir: str, output_file: str) -> None:
    """Write the rendered HTML to the output file."""
    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)


def main() -> None:
    print("🏈  Fantasy Football League Handbook Generator")
    print("─" * 44)

    print(f"📂  Loading data from  : {os.path.relpath(DATA_FILE)}")
    data = load_data(DATA_FILE)

    league_name = data["league"]["name"]
    season      = data["league"]["season"]
    print(f"✅  League            : {league_name} ({season})")

    print(f"🎨  Rendering template: templates/handbook.html")
    html = render_template(data, TEMPLATES_DIR)

    print(f"💾  Writing output to : {os.path.relpath(OUTPUT_FILE)}")
    write_output(html, OUTPUT_DIR, OUTPUT_FILE)

    print()
    print("✅  Done! Open docs/index.html in your browser to preview.")
    print("📡  Push to GitHub and enable GitHub Pages (docs/ folder) to share.")


if __name__ == "__main__":
    main()
