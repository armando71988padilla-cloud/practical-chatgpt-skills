#!/usr/bin/env python3
"""Read-only concise Git state report with secret-safe path warnings.

The script runs only local, read-only Git and filesystem queries. It does not fetch,
stage, modify, commit, reset, clean, switch, merge, rebase, or push.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
from pathlib import Path

RISK_NAME = re.compile(
    r"(^|/)(?:\.env(?:\.|$)|id_rsa(?:\.|$)|id_ed25519(?:\.|$)|"
    r".*(?:secret|token|credential|cookie|session|private[_-]?key|service[_-]?account).*)",
    re.I,
)
BACKUP_NAME = re.compile(r"(?:\.bak(?:[._-]|$)|\.old(?:[._-]|$)|~$|\.sw[op]$|backup|copy[-_ ]?of)", re.I)
GENERATED_NAME = re.compile(
    r"(^|/)(?:node_modules|dist|build|target|coverage|\.cache|__pycache__)(/|$)|"
    r"\.(?:log|tmp|cache|pyc|class)$",
    re.I,
)
BINARY_OR_ARCHIVE = re.compile(
    r"\.(?:zip|tar|tgz|gz|7z|rar|iso|dmg|exe|msi|appimage|db|sqlite(?:3)?|pkl|pt|pth|ckpt|onnx)$",
    re.I,
)
LARGE_BYTES = 10 * 1024 * 1024
MAX_LIST = 200


def run(repo: Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=15,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
    )
    if check and proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout.strip()


def sanitize_remote(text: str) -> str:
    text = re.sub(r"(https?://)[^/@\s]+@", r"\1", text)
    text = re.sub(r"(https?://)([^/:\s]+):[^/@\s]+@", r"\1", text)
    return text


def list_paths(repo: Path, args: list[str], limit: int = MAX_LIST) -> tuple[list[str], bool]:
    out = run(repo, *args, check=False)
    items = [line for line in out.splitlines() if line]
    return items[:limit], len(items) > limit


def print_paths(label: str, paths: list[str], truncated: bool) -> None:
    print(f"{label}_COUNT_SHOWN={len(paths)}")
    print(f"{label}_TRUNCATED={'YES' if truncated else 'NO'}")
    for path in paths[:50]:
        print(f"{label}: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Report concise read-only Git state")
    parser.add_argument("repo", help="Concrete candidate repository directory")
    args = parser.parse_args()

    candidate = Path(args.repo).expanduser().resolve()
    if not candidate.exists():
        print(f"STOP: candidate does not exist: {candidate}")
        return 2

    try:
        root = Path(run(candidate, "rev-parse", "--show-toplevel")).resolve()
    except Exception as exc:
        print(f"STOP: not a git repository: {exc}")
        return 2

    branch = run(root, "branch", "--show-current", check=False) or "DETACHED"
    commit = run(root, "rev-parse", "--verify", "HEAD", check=False) or "UNBORN"
    upstream = run(root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}", check=False)

    ahead = behind = None
    if upstream:
        counts = run(root, "rev-list", "--left-right", "--count", f"{upstream}...HEAD", check=False).split()
        if len(counts) == 2 and all(item.isdigit() for item in counts):
            behind, ahead = map(int, counts)

    staged, staged_trunc = list_paths(root, ["diff", "--cached", "--name-only"])
    unstaged, unstaged_trunc = list_paths(root, ["diff", "--name-only"])
    untracked, untracked_trunc = list_paths(root, ["ls-files", "--others", "--exclude-standard"])
    ignored, ignored_trunc = list_paths(root, ["ls-files", "--others", "--ignored", "--exclude-standard"])
    remotes = sanitize_remote(run(root, "remote", "-v", check=False))
    submodules = run(root, "submodule", "status", "--recursive", check=False)
    worktrees = run(root, "worktree", "list", "--porcelain", check=False)
    porcelain = run(root, "status", "--porcelain=v1", "--branch", check=False)

    print("READ_ONLY=YES")
    print("NETWORK_USED=NO")
    print(f"ROOT={root}")
    print(f"BRANCH={branch}")
    print(f"COMMIT={commit}")
    print(f"UPSTREAM={upstream or 'NONE'}")
    print(f"AHEAD={ahead if ahead is not None else 'UNPROVEN'}")
    print(f"BEHIND={behind if behind is not None else 'UNPROVEN'}")
    print("REMOTE_FRESHNESS=UNPROVEN_LOCAL_REFS_ONLY")
    print("REMOTES_BEGIN")
    print(remotes or "NONE")
    print("REMOTES_END")

    print_paths("STAGED", staged, staged_trunc)
    print_paths("UNSTAGED", unstaged, unstaged_trunc)
    print_paths("UNTRACKED", untracked, untracked_trunc)
    print_paths("IGNORED", ignored, ignored_trunc)

    print(f"SUBMODULES_PRESENT={'YES' if submodules else 'NO'}")
    if submodules:
        for line in submodules.splitlines()[:50]:
            print(f"SUBMODULE: {line}")

    worktree_count = sum(1 for line in worktrees.splitlines() if line.startswith("worktree "))
    print(f"WORKTREE_COUNT={worktree_count}")
    print(f"STATUS_PORCELAIN_NONEMPTY={'YES' if porcelain else 'NO'}")

    all_paths = sorted(set(staged + unstaged + untracked))
    warnings = 0
    for rel in all_paths:
        full = root / rel
        if RISK_NAME.search(rel):
            print(f"RISK_NAME: {rel}")
            warnings += 1
        if BACKUP_NAME.search(rel):
            print(f"BACKUP_RISK: {rel}")
            warnings += 1
        if GENERATED_NAME.search(rel):
            print(f"GENERATED_RISK: {rel}")
            warnings += 1
        if BINARY_OR_ARCHIVE.search(rel):
            print(f"BINARY_OR_ARCHIVE_RISK: {rel}")
            warnings += 1
        try:
            if full.is_file() and full.stat().st_size > LARGE_BYTES:
                print(f"LARGE_FILE_RISK: {rel} size_bytes={full.stat().st_size}")
                warnings += 1
        except OSError:
            pass

    git_dir = Path(run(root, "rev-parse", "--git-dir", check=False))
    if not git_dir.is_absolute():
        git_dir = root / git_dir
    in_progress = []
    markers = {
        "MERGE": ["MERGE_HEAD"],
        "REBASE": ["rebase-merge", "rebase-apply"],
        "CHERRY_PICK": ["CHERRY_PICK_HEAD"],
        "REVERT": ["REVERT_HEAD"],
        "BISECT": ["BISECT_LOG"],
    }
    for label, names in markers.items():
        if any((git_dir / name).exists() for name in names):
            in_progress.append(label)
    print("IN_PROGRESS=" + (",".join(in_progress) if in_progress else "NONE"))
    print(f"RISK_WARNING_COUNT={warnings}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
