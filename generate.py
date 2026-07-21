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
import sys
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
DATA_FILE     = os.path.join(BASE_DIR, "data", "league.json")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
OUTPUT_DIR    = os.path.join(BASE_DIR, "docs")
OUTPUT_FILE   = os.path.join(OUTPUT_DIR, "index.html")


class ValidationError(ValueError):
    """Raised when the league data file is missing, malformed, or incorrectly typed."""


def load_data(path: str) -> dict:
    """Load and return the JSON data file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_type(value, expected_type, path: str) -> None:
    """Ensure a value matches the expected type."""
    if not isinstance(value, expected_type):
        expected_name = (
            " or ".join(t.__name__ for t in expected_type)
            if isinstance(expected_type, tuple)
            else expected_type.__name__
        )
        actual_name = type(value).__name__
        raise ValidationError(f"{path} must be {expected_name}, got {actual_name}.")


def require_field(mapping: dict, field: str, expected_type, path: str) -> None:
    """Ensure a required field exists and matches the expected type."""
    if field not in mapping:
        raise ValidationError(f"{path}.{field} is required.")
    validate_type(mapping[field], expected_type, f"{path}.{field}")


def validate_string_list(values: list, path: str) -> None:
    """Ensure every item in a list is a string."""
    validate_type(values, list, path)
    for index, item in enumerate(values):
        validate_type(item, str, f"{path}[{index}]")


def validate_members(members: list) -> None:
    """Validate member entries."""
    validate_type(members, list, "members")
    for index, member in enumerate(members):
        path = f"members[{index}]"
        validate_type(member, dict, path)
        require_field(member, "name", str, path)
        require_field(member, "team_name", str, path)
        require_field(member, "emoji", str, path)


def validate_draft(draft: dict) -> None:
    """Validate draft information when present."""
    validate_type(draft, dict, "draft")
    for field in ("date", "time", "type", "location"):
        if field in draft:
            validate_type(draft[field], str, f"draft.{field}")
    for field in ("rounds", "seconds_per_pick"):
        if field in draft:
            validate_type(draft[field], int, f"draft.{field}")
    if "order" in draft:
        validate_string_list(draft["order"], "draft.order")
    if "note" in draft:
        validate_type(draft["note"], str, "draft.note")


def validate_prizes(prizes: dict) -> None:
    """Validate prize information when present."""
    validate_type(prizes, dict, "prizes")
    for field in ("entry_fee", "total_pool"):
        if field in prizes:
            validate_type(prizes[field], (int, float), f"prizes.{field}")
    if "breakdown" in prizes:
        validate_type(prizes["breakdown"], list, "prizes.breakdown")
        for index, prize in enumerate(prizes["breakdown"]):
            path = f"prizes.breakdown[{index}]"
            validate_type(prize, dict, path)
            require_field(prize, "place", str, path)
            require_field(prize, "amount", (int, float), path)
            require_field(prize, "description", str, path)
    if "notes" in prizes:
        validate_type(prizes["notes"], str, "prizes.notes")


def validate_rules(rules: list) -> None:
    """Validate rule categories."""
    validate_type(rules, list, "rules")
    for index, rule_section in enumerate(rules):
        path = f"rules[{index}]"
        validate_type(rule_section, dict, path)
        require_field(rule_section, "category", str, path)
        require_field(rule_section, "entries", list, path)
        validate_string_list(rule_section["entries"], f"{path}.entries")


def validate_voting(voting: list) -> None:
    """Validate voting history."""
    validate_type(voting, list, "voting")
    for index, vote in enumerate(voting):
        path = f"voting[{index}]"
        validate_type(vote, dict, path)
        require_field(vote, "date", str, path)
        require_field(vote, "topic", str, path)
        require_field(vote, "result", str, path)
        if "notes" in vote:
            validate_type(vote["notes"], str, f"{path}.notes")


def validate_playoffs(playoffs: dict) -> None:
    """Validate playoff information when present."""
    validate_type(playoffs, dict, "playoffs")
    for field in ("format", "weeks", "byes", "tiebreaker"):
        if field in playoffs:
            validate_type(playoffs[field], str, f"playoffs.{field}")
    if "bracket" in playoffs:
        validate_type(playoffs["bracket"], list, "playoffs.bracket")
        for index, round_info in enumerate(playoffs["bracket"]):
            path = f"playoffs.bracket[{index}]"
            validate_type(round_info, dict, path)
            require_field(round_info, "round", str, path)
            require_field(round_info, "matchups", list, path)
            validate_string_list(round_info["matchups"], f"{path}.matchups")


def validate_champions(champions: list) -> None:
    """Validate champion rows."""
    validate_type(champions, list, "champions")
    for index, champion in enumerate(champions):
        path = f"champions[{index}]"
        validate_type(champion, dict, path)
        require_field(champion, "season", (int, str), path)
        require_field(champion, "champion", str, path)
        require_field(champion, "team", str, path)
        require_field(champion, "record", str, path)
        require_field(champion, "points", (int, float), path)


def validate_records(records: list) -> None:
    """Validate record rows."""
    validate_type(records, list, "records")
    for index, record in enumerate(records):
        path = f"records[{index}]"
        validate_type(record, dict, path)
        require_field(record, "category", str, path)
        require_field(record, "holder", str, path)
        require_field(record, "value", str, path)
        if "season" in record:
            validate_type(record["season"], (int, str), f"{path}.season")


def validate_data(data: dict) -> None:
    """Validate the league data file and allow optional sections to be omitted."""
    validate_type(data, dict, "root")
    require_field(data, "league", dict, "root")

    league = data["league"]
    require_field(league, "name", str, "league")
    require_field(league, "season", (int, str), "league")
    for field in ("platform", "commissioner", "tagline"):
        if field in league:
            validate_type(league[field], str, f"league.{field}")
    if "founded" in league:
        validate_type(league["founded"], (int, str), "league.founded")

    validators = {
        "members": validate_members,
        "draft": validate_draft,
        "prizes": validate_prizes,
        "rules": validate_rules,
        "voting": validate_voting,
        "playoffs": validate_playoffs,
        "champions": validate_champions,
        "records": validate_records,
    }
    for section, validator in validators.items():
        if section in data:
            validator(data[section])


def build_context(data: dict) -> dict:
    """Build a render context with safe defaults for optional sections."""
    return {
        "league": data["league"],
        "members": data.get("members"),
        "draft": data.get("draft"),
        "prizes": data.get("prizes"),
        "rules": data.get("rules"),
        "voting": data.get("voting"),
        "playoffs": data.get("playoffs"),
        "champions": data.get("champions"),
        "records": data.get("records"),
        "generated_on": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
    }


def render_template(data: dict, templates_dir: str) -> str:
    """Render the handbook template with the provided data."""
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template("handbook.html")
    return template.render(**build_context(data))


def write_output(html: str, output_dir: str, output_file: str) -> None:
    """Write the rendered HTML to the output file."""
    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)


def main() -> None:
    print("🏈  Fantasy Football League Handbook Generator")
    print("─" * 44)

    print(f"📂  Loading data from  : {os.path.relpath(DATA_FILE)}")
    try:
        data = load_data(DATA_FILE)
    except json.JSONDecodeError as exc:
        print(f"❌  Invalid JSON      : {exc}")
        sys.exit(1)
    try:
        validate_data(data)
    except ValidationError as exc:
        print(f"❌  Validation error   : {exc}")
        sys.exit(1)

    league_name = data["league"]["name"]
    season      = data["league"]["season"]
    print(f"✅  League            : {league_name} ({season})")

    print(f"🎨  Rendering template: templates/handbook.html")
    html = render_template(data, TEMPLATES_DIR)

    print(f"💾  Writing output to : {os.path.relpath(OUTPUT_FILE)}")
    write_output(html, OUTPUT_DIR, OUTPUT_FILE)

    print()
    print("✅  Done! Open docs/index.html in your browser to preview.")


if __name__ == "__main__":
    main()
