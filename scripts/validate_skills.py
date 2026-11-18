#!/usr/bin/env python3
"""Clean-room repository validator for Smolnikov Research Agent Skills."""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETING_RE = re.compile(r"\b(powerful|comprehensive|seamless|revolutionary|cutting-edge|state-of-the-art)\b", re.IGNORECASE)
SECRET_RE = re.compile(r"(-----BEGIN [A-Z ]*PRIVATE " + r"KEY-----|sk-[A-Za-z0-9]{24,}|gh[po]_[A-Za-z0-9]{20,}|glpat-[A-Za-z0-9_-]{20,})")
MACHINE_PATH_RE = re.compile(r"(?:/home/(?!runner\b)[a-z0-9_-]+/|/root/|[A-Z]:\\\\Users\\\\)")


def validate_repo() -> None:
    skill_dirs = sorted(p.parent for p in (ROOT / "skills").glob("*/SKILL.md"))
    assert len(skill_dirs) == 15, f"Expected 15 skills, found {len(skill_dirs)}"

    groupings = json.loads((ROOT / "skills.sh.json").read_text(encoding="utf-8"))["groupings"]
    grouped_names = {name for g in groupings for name in g["skills"]}
    actual_names = {d.name for d in skill_dirs}
    assert grouped_names == actual_names, f"skills.sh.json mismatch: {grouped_names ^ actual_names}"

    for sdir in skill_dirs:
        raw = (sdir / "SKILL.md").read_text(encoding="utf-8")
        assert raw.startswith("---\n"), f"{sdir.name}: missing YAML frontmatter"
        header = raw.split("---", 2)[1]
        assert f"name: {sdir.name}\n" in header, f"{sdir.name}: name mismatch"
        assert "author: Smolnikov Research\n" in header, f"{sdir.name}: wrong author"
        m_desc = re.search(r'^description:\s*"?(.+?)"?\s*$', header, re.MULTILINE)
        assert m_desc, f"{sdir.name}: missing description"
        desc = m_desc.group(1).strip()
        assert len(desc) <= 60 and desc.endswith("."), f"{sdir.name}: invalid description {desc!r}"
        assert not MARKETING_RE.search(desc), f"{sdir.name}: banned marketing term in {desc!r}"

        od_path = sdir / "on-demand.json"
        assert od_path.is_file(), f"{sdir.name}: missing on-demand.json"
        od = json.loads(od_path.read_text(encoding="utf-8"))
        assert od.get("auto_load_on_startup") is False, f"{sdir.name}: auto_load_on_startup must be false"

        for py in sdir.rglob("*.py"):
            ast.parse(py.read_text(encoding="utf-8"), filename=str(py))

    for p in ROOT.rglob("*"):
        if not p.is_file() or ".git" in p.parts or p.suffix in {".png", ".mp4", ".wav", ".pyc"}:
            continue
        txt = p.read_text(encoding="utf-8", errors="ignore")
        rel = p.relative_to(ROOT).as_posix()
        if rel != "scripts/validate_skills.py":
            assert not SECRET_RE.search(txt), f"Secret-shaped token in {rel}"
            assert not MACHINE_PATH_RE.search(txt), f"Internal machine path in {rel}"

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "\u2014" not in readme and "\u2013" not in readme, "Long dash found in README.md"
    print(f"Validated {len(skill_dirs)} clean-room skills successfully.")


if __name__ == "__main__":
    validate_repo()
