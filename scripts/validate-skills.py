#!/usr/bin/env python3
"""Validate the skill collection before committing.

Checks:
  - every skills/<id>/SKILL.md has YAML frontmatter with name and description
  - the frontmatter parses as YAML (when PyYAML is installed), catching
    unquoted colons and other syntax a real loader would reject
  - the directory name is a valid lowercase kebab-case skill ID
  - skill IDs are unique
  - relative Markdown links resolve to files or directories
  - no references to retired upstream skill IDs or harness prefixes survive

Exit code 1 on any error.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # PyYAML is optional; the strict parse is skipped without it.
    yaml = None

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
RETIRED = {
    "superpowers:",
    "/setup-matt-pocock-skills",
    "ask-matt",
    "setup-matt-pocock-skills",
    "requesting-code-review",
    "receiving-code-review",
    "subagent-driven-development",
    "diagnosing-bugs",
    "writing-skills",
    "to-tickets",
    "to-spec",
    "implement-spec",
    "grill-me",
    "grill-with-docs",
}
# These appear legitimately in prose as concepts; only flag them when used as a skill ID.
RETIRED_CONTEXT = re.compile(
    r"(Skill tool with [\"']?(?:brainstorming|grilling|writing-plans|tdd|claude-handoff)"
    r"|superpowers:)"
)


def frontmatter_body(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    return text[4:end]


def parse_frontmatter(text: str) -> dict[str, str] | None:
    body = frontmatter_body(text)
    if body is None:
        return None
    data: dict[str, str] = {}
    for line in body.splitlines():
        m = re.match(r"^([A-Za-z0-9_/-]+):\s*(.*)$", line)
        if m:
            value = m.group(2).strip().strip('"').strip("'")
            data[m.group(1)] = value
    return data


def check_links(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for raw in LINK_RE.findall(text):
        target = raw.strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = target.split("#", 1)[0]
        if not target:
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)}: broken link -> {raw}")


def main() -> int:
    errors: list[str] = []
    skill_dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir()) if SKILLS.exists() else []

    if not skill_dirs:
        errors.append("skills/: no skill directories found")

    seen: dict[str, Path] = {}
    for skill_dir in skill_dirs:
        skill_id = skill_dir.name
        if not ID_RE.match(skill_id):
            errors.append(f"{skill_id}: directory name is not lowercase kebab-case")
        if skill_id in seen:
            errors.append(f"{skill_id}: duplicate skill ID ({seen[skill_id]} and {skill_dir})")
        seen[skill_id] = skill_dir

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            errors.append(f"{skill_id}: missing SKILL.md")
            continue

        text = skill_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if fm is None:
            errors.append(f"{skill_id}: missing or malformed frontmatter")
        else:
            if not fm.get("name"):
                errors.append(f"{skill_id}: frontmatter missing name")
            if not fm.get("description"):
                errors.append(f"{skill_id}: frontmatter missing description")
            elif len(fm["description"]) > 1024:
                errors.append(f"{skill_id}: description longer than 1024 characters")
            if yaml is not None:
                body = frontmatter_body(text)
                if body is not None:
                    try:
                        yaml.safe_load(body)
                    except yaml.YAMLError as exc:
                        detail = str(exc).splitlines()[0]
                        errors.append(f"{skill_id}: frontmatter is not valid YAML ({detail})")

        for needle in RETIRED:
            if needle in text:
                # Allow attribution prose that names the upstream skill explicitly.
                if "upstream" in text.lower() or "derived from" in text.lower():
                    continue
                errors.append(f"{skill_id}: retired reference {needle!r}")

        if RETIRED_CONTEXT.search(text):
            errors.append(f"{skill_id}: stale cross-skill invocation")

        for md in skill_dir.rglob("*.md"):
            check_links(md, errors)

    # Root documents too.
    for md in [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "ATTRIBUTION.md"]:
        if md.exists():
            check_links(md, errors)

    if errors:
        print("Validation failed:\n")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"OK: {len(skill_dirs)} skills validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
