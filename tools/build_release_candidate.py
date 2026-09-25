#!/usr/bin/env python3
"""Build one public Skill release candidate ZIP without publishing anything."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
DIST = ROOT / "dist"
SKILL_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
VERSION_RE = re.compile(r"^v?[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.-]+)?$")

SKIP_NAMES = {".DS_Store"}
SKIP_PARTS = {"__pycache__"}
SKIP_SUFFIXES = {".pyc", ".pyo"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a versioned Skill release candidate")
    parser.add_argument("skill", help="Skill directory name under skills/")
    parser.add_argument("version", help="Version such as v1.0.1")
    args = parser.parse_args()

    skill = args.skill.strip()
    version = args.version.strip()
    if not SKILL_RE.fullmatch(skill):
        print("ERROR: invalid Skill name")
        return 2
    if not VERSION_RE.fullmatch(version):
        print("ERROR: invalid version; expected semantic form such as v1.0.1")
        return 2
    if not version.startswith("v"):
        version = "v" + version

    source = SKILLS / skill
    if not source.is_dir() or not (source / "SKILL.md").is_file():
        print(f"ERROR: Skill not found or missing SKILL.md: {skill}")
        return 2

    DIST.mkdir(exist_ok=True)
    archive = DIST / f"{skill}-{version}-release.zip"
    if archive.exists():
        archive.unlink()

    added = 0
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(source.rglob("*")):
            if path.is_symlink() or not path.is_file():
                continue
            if path.name in SKIP_NAMES:
                continue
            if any(part in SKIP_PARTS for part in path.parts):
                continue
            if path.suffix.lower() in SKIP_SUFFIXES:
                continue
            arcname = Path(skill) / path.relative_to(source)
            zf.write(path, arcname.as_posix())
            added += 1

    if added == 0:
        print("ERROR: release ZIP would be empty")
        return 1

    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum = archive.with_suffix(archive.suffix + ".sha256")
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="utf-8")

    print(f"BUILT={archive.relative_to(ROOT)}")
    print(f"FILES={added}")
    print(f"SHA256={digest}")
    print(f"CHECKSUM_FILE={checksum.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
