#!/usr/bin/env python3
"""Validate public Skill source without network access or repository mutation."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
RELEASES_DIR = ROOT / "docs" / "releases"
TESTS_DIR = ROOT / "tests"

DENIED_SUFFIXES = {
    ".exe", ".dll", ".so", ".dylib", ".bin", ".class", ".pyc", ".pyo",
    ".jar", ".app", ".msi", ".dmg", ".iso",
}
DENIED_NAMES = {".DS_Store"}
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
NAME_RE = re.compile(r"(?m)^name:\s*([^\n#]+?)\s*$")
DESCRIPTION_RE = re.compile(r"(?m)^description:\s*(.+?)\s*$")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_python(path: Path, errors: list[str]) -> None:
    try:
        source = path.read_text(encoding="utf-8")
        compile(source, str(path), "exec")
    except Exception as exc:
        fail(errors, f"{path.relative_to(ROOT)}: Python syntax error: {exc}")


def validate_skill(skill_dir: Path, errors: list[str]) -> None:
    skill_name = skill_dir.name
    root_skill = skill_dir / "SKILL.md"
    skill_files = list(skill_dir.rglob("SKILL.md"))

    if len(skill_files) != 1:
        fail(errors, f"{skill_name}: expected exactly one SKILL.md, found {len(skill_files)}")
        return

    if not root_skill.is_file():
        fail(errors, f"{skill_name}: SKILL.md must be at the Skill directory root")
        return

    text = root_skill.read_text(encoding="utf-8")
    frontmatter = FRONTMATTER_RE.match(text)
    if not frontmatter:
        fail(errors, f"{skill_name}: missing YAML-style frontmatter in SKILL.md")
    else:
        block = frontmatter.group(1)
        name_match = NAME_RE.search(block)
        description_match = DESCRIPTION_RE.search(block)

        if not name_match:
            fail(errors, f"{skill_name}: frontmatter is missing name")
        elif name_match.group(1).strip().strip('"\'') != skill_name:
            fail(
                errors,
                f"{skill_name}: frontmatter name must match directory name "
                f"(found {name_match.group(1).strip()!r})",
            )

        if not description_match or not description_match.group(1).strip():
            fail(errors, f"{skill_name}: frontmatter is missing description")

    agent = skill_dir / "agents" / "openai.yaml"
    if agent.exists():
        agent_text = agent.read_text(encoding="utf-8")
        if "display_name:" not in agent_text:
            fail(errors, f"{skill_name}: agents/openai.yaml missing display_name")
        if "short_description:" not in agent_text:
            fail(errors, f"{skill_name}: agents/openai.yaml missing short_description")

    for path in skill_dir.rglob("*"):
        if path.is_symlink():
            fail(errors, f"{path.relative_to(ROOT)}: symlinks are not allowed in public Skill source")
            continue
        if not path.is_file():
            continue
        if path.name in DENIED_NAMES:
            fail(errors, f"{path.relative_to(ROOT)}: generated OS metadata file is not allowed")
        if path.suffix.lower() in DENIED_SUFFIXES:
            fail(errors, f"{path.relative_to(ROOT)}: compiled/binary artifact is not allowed")
        if "__pycache__" in path.parts:
            fail(errors, f"{path.relative_to(ROOT)}: __pycache__ is not allowed")
        if path.suffix.lower() == ".py":
            validate_python(path, errors)

    release_docs = list(RELEASES_DIR.glob(f"{skill_name}-v*.md"))
    if not release_docs:
        fail(errors, f"{skill_name}: no release documentation found under docs/releases/")

    test_candidates = list(TESTS_DIR.glob(f"{skill_name}*"))
    if not test_candidates:
        fail(errors, f"{skill_name}: no public test fixture/case found under tests/")


def main() -> int:
    errors: list[str] = []

    if not SKILLS_DIR.is_dir():
        print("ERROR: skills/ directory not found")
        return 1

    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    if not skill_dirs:
        print("ERROR: no Skill directories found")
        return 1

    for path in ROOT.rglob("*"):
        if "__pycache__" in path.parts:
            fail(errors, f"{path.relative_to(ROOT)}: __pycache__ is not allowed")
        if path.is_file() and path.suffix.lower() in {".pyc", ".pyo"}:
            fail(errors, f"{path.relative_to(ROOT)}: compiled Python artifact is not allowed")

    for skill_dir in skill_dirs:
        validate_skill(skill_dir, errors)

    if errors:
        print(f"VALIDATION FAILED: {len(errors)} problem(s)")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"VALIDATION PASSED: {len(skill_dirs)} public Skill(s)")
    for skill_dir in skill_dirs:
        print(f" - {skill_dir.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
