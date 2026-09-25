#!/usr/bin/env python3
"""Read-only heuristic scanner for pasted shell command text.

The script never executes reviewed commands and never echoes source lines. It reports
rule identifiers, severity, and line numbers only so suspected secrets are not copied
into output.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RULES = [
    ("unresolved_placeholder", "high", re.compile(r"<[^>\n]{1,80}>")),
    ("recursive_delete_unix", "high", re.compile(r"\brm\s+[^\n]*-[^\n]*r[^\n]*f|\brm\s+-rf\b|\brm\s+-fr\b", re.I)),
    ("recursive_delete_powershell", "high", re.compile(r"\bRemove-Item\b[^\n]*(?:-Recurse[^\n]*-Force|-Force[^\n]*-Recurse)", re.I)),
    ("recursive_delete_cmd", "high", re.compile(r"\b(?:del|rd|rmdir)\b[^\n]*/[sq][^\n]*/[sq]", re.I)),
    ("disk_write_or_format", "high", re.compile(r"\b(?:mkfs(?:\.[a-z0-9]+)?|diskpart|format\s+[A-Za-z]:|dd\s+[^\n]*\bof=)\b", re.I)),
    ("recursive_permission_change", "high", re.compile(r"\b(?:chmod|chown)\b[^\n]*\s-R\b|\b(?:chmod|chown)\b\s+-R\b", re.I)),
    ("world_writable_permissions", "high", re.compile(r"\bchmod\b[^\n]*\b777\b", re.I)),
    ("download_to_shell", "high", re.compile(r"\b(?:curl|wget)\b[^\n]*\|\s*(?:sudo\s+)?(?:sh|bash|zsh)\b", re.I)),
    ("powershell_download_execute", "high", re.compile(r"\b(?:irm|Invoke-RestMethod|iwr|Invoke-WebRequest)\b[^\n]*\|\s*(?:iex|Invoke-Expression)\b", re.I)),
    ("encoded_powershell", "high", re.compile(r"\b(?:powershell|pwsh)\b[^\n]*(?:-enc|-encodedcommand)\b", re.I)),
    ("dynamic_eval", "high", re.compile(r"(?:^|[;&|\s])(?:eval|iex|Invoke-Expression)\b", re.I)),
    ("git_hard_reset", "high", re.compile(r"\bgit\s+reset\s+--hard\b", re.I)),
    ("git_aggressive_clean", "high", re.compile(r"\bgit\s+clean\s+[^\n]*-[a-z]*f[a-z]*[^\n]*[dx]|\bgit\s+clean\s+[^\n]*-[a-z]*[dx][a-z]*[^\n]*f", re.I)),
    ("git_force_push", "high", re.compile(r"\bgit\s+push\b[^\n]*(?:--force(?:-with-lease)?|-f)\b", re.I)),
    ("privilege_elevation", "medium", re.compile(r"(?:^|[;&|\s])sudo\b|\bStart-Process\b[^\n]*-Verb\s+RunAs\b", re.I)),
    ("tls_verification_disabled", "medium", re.compile(r"\b(?:curl|wget)\b[^\n]*(?:-k\b|--insecure\b|--no-check-certificate\b)", re.I)),
    ("ssh_host_key_check_disabled", "medium", re.compile(r"StrictHostKeyChecking\s*=\s*no", re.I)),
    ("execution_policy_weakened", "medium", re.compile(r"\bSet-ExecutionPolicy\b[^\n]*(?:Bypass|Unrestricted)\b", re.I)),
    ("possible_inline_secret", "medium", re.compile(r"\b(?:password|passwd|token|secret|api[_-]?key)\b\s*[=:]\s*[^\s]+", re.I)),
    ("force_overwrite_redirect", "medium", re.compile(r"(?<!>)>(?!>)\s*[^|&;\n]+")),
]


def scan(text: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for rule_id, severity, pattern in RULES:
            if pattern.search(line):
                findings.append({"rule": rule_id, "severity": severity, "line": lineno})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only heuristic scan of shell command text")
    parser.add_argument("path", nargs="?", help="Text file to scan; read stdin when omitted")
    args = parser.parse_args()

    if args.path:
        text = Path(args.path).read_text(encoding="utf-8", errors="replace")
    else:
        text = sys.stdin.read()

    findings = scan(text)
    counts = {"high": 0, "medium": 0}
    for finding in findings:
        severity = str(finding["severity"])
        counts[severity] = counts.get(severity, 0) + 1

    print(json.dumps({
        "scanner": "copy-paste-guard-command-risk-scan",
        "read_only": True,
        "executes_input": False,
        "finding_count": len(findings),
        "severity_counts": counts,
        "findings": findings,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
