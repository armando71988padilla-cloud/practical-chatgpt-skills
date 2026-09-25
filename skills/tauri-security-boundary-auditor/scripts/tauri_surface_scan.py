#!/usr/bin/env python3
"""Read-only static inventory for common Tauri v2 security surfaces.

The scanner never runs project code, build tools, package managers, or network
requests. Findings are heuristic review signals, not vulnerability claims.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    import tomllib
except ImportError:
    tomllib = None

TEXT_SUFFIXES = {".json", ".toml", ".rs", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}
MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_FINDINGS = 500

MARKERS = {
    "shell_plugin_dependency": ["tauri-plugin-shell", "@tauri-apps/plugin-shell"],
    "process_plugin_dependency": ["tauri-plugin-process", "@tauri-apps/plugin-process"],
    "filesystem_plugin_dependency": ["tauri-plugin-fs", "@tauri-apps/plugin-fs"],
    "http_plugin_dependency": ["tauri-plugin-http", "@tauri-apps/plugin-http"],
    "localhost_plugin_dependency": ["tauri-plugin-localhost", "@tauri-apps/plugin-localhost"],
    "updater_plugin_dependency": ["tauri-plugin-updater", "@tauri-apps/plugin-updater"],
    "shell_execute_permission": ["shell:allow-execute", "shell:allow-spawn", "shell:default"],
    "filesystem_write_permission": [
        "fs:allow-write",
        "fs:allow-write-file",
        "fs:allow-write-text-file",
        "fs:allow-create",
        "fs:allow-remove",
        "fs:allow-rename",
        "fs:allow-copy-file",
    ],
    "http_permission": ["http:allow-fetch", "http:default"],
    "updater_install_permission": [
        "updater:allow-install",
        "updater:allow-download-and-install",
        "updater:default",
    ],
    "dangerous_remote_ipc": ["dangerousRemoteDomainIpcAccess", "dangerous_remote_domain_ipc_access"],
}

RUST_PROCESS_PATTERNS = [
    re.compile(r"std::process::Command\s*::\s*new"),
    re.compile(r"tokio::process::Command\s*::\s*new"),
]

FRONTEND_INVOKE_RE = re.compile(r"\binvoke\s*\(")
TAURI_COMMAND_RE = re.compile(r"#\s*\[\s*tauri::command")
INVOKE_HANDLER_RE = re.compile(r"\.invoke_handler\s*\(")


def read_text(path: Path) -> str:
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return ""
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def add_finding(findings: list[dict], finding: dict) -> None:
    if len(findings) < MAX_FINDINGS:
        findings.append(finding)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="strict"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None


def load_toml(path: Path):
    if tomllib is None:
        return None
    try:
        return tomllib.loads(path.read_text(encoding="utf-8", errors="strict"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError):
        return None


def collect_candidate_files(project_root: Path, src_tauri: Path) -> list[Path]:
    candidates: set[Path] = set()
    for path in [
        src_tauri / "tauri.conf.json",
        src_tauri / "Cargo.toml",
        project_root / "package.json",
        project_root / "package-lock.json",
        project_root / "pnpm-lock.yaml",
        project_root / "yarn.lock",
        project_root / "bun.lockb",
    ]:
        if path.is_file():
            candidates.add(path)

    for folder_name in ("capabilities", "permissions"):
        folder = src_tauri / folder_name
        if folder.is_dir():
            for path in folder.rglob("*"):
                if path.is_file() and path.suffix.lower() in {".json", ".toml"}:
                    candidates.add(path)

    rust_src = src_tauri / "src"
    if rust_src.is_dir():
        for path in rust_src.rglob("*.rs"):
            if path.is_file():
                candidates.add(path)

    for frontend_dir in (project_root / "src", project_root / "app", project_root / "frontend"):
        if frontend_dir.is_dir():
            for path in frontend_dir.rglob("*"):
                if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                    candidates.add(path)

    return sorted(candidates)


def inspect_config(path: Path, root: Path, findings: list[dict], metadata: dict) -> None:
    config = load_json(path)
    if config is None:
        add_finding(findings, {
            "category": "tauri_config_parse",
            "classification": "unproven",
            "file": rel(path, root),
            "note": "tauri.conf.json could not be parsed as strict JSON",
        })
        return

    build = config.get("build", {}) if isinstance(config, dict) else {}
    app = config.get("app", {}) if isinstance(config, dict) else {}
    bundle = config.get("bundle", {}) if isinstance(config, dict) else {}

    if isinstance(build, dict):
        metadata["dev_url"] = build.get("devUrl")
        metadata["frontend_dist"] = build.get("frontendDist")
        if build.get("devUrl"):
            add_finding(findings, {
                "category": "development_url_present",
                "classification": "informational",
                "file": rel(path, root),
                "value": str(build.get("devUrl")),
            })

    security = app.get("security", {}) if isinstance(app, dict) else {}
    if isinstance(security, dict):
        csp = security.get("csp", "__missing__")
        metadata["csp_state"] = "missing" if csp == "__missing__" else ("null" if csp is None else "configured")
        if csp is None:
            add_finding(findings, {
                "category": "csp_disabled",
                "classification": "review_required",
                "file": rel(path, root),
            })
        elif csp == "__missing__":
            add_finding(findings, {
                "category": "csp_missing",
                "classification": "review_required",
                "file": rel(path, root),
            })
        else:
            csp_text = json.dumps(csp, sort_keys=True)
            if "*" in csp_text:
                add_finding(findings, {
                    "category": "csp_wildcard_marker",
                    "classification": "review_required",
                    "file": rel(path, root),
                })
            if "unsafe-eval" in csp_text:
                add_finding(findings, {
                    "category": "csp_unsafe_eval",
                    "classification": "review_required",
                    "file": rel(path, root),
                })

    plugins = config.get("plugins", {}) if isinstance(config, dict) else {}
    updater = plugins.get("updater", {}) if isinstance(plugins, dict) else {}
    if isinstance(updater, dict) and updater:
        metadata["updater_present"] = True
        metadata["updater_endpoints"] = updater.get("endpoints")
        metadata["updater_pubkey_present"] = bool(updater.get("pubkey"))
        if updater.get("dangerousInsecureTransportProtocol") is True:
            add_finding(findings, {
                "category": "updater_insecure_transport_enabled",
                "classification": "review_required",
                "file": rel(path, root),
            })
        if not updater.get("pubkey"):
            add_finding(findings, {
                "category": "updater_pubkey_not_found_in_config",
                "classification": "unproven",
                "file": rel(path, root),
                "note": "Verify whether updater signing/public-key configuration is supplied elsewhere.",
            })

    if isinstance(bundle, dict) and bundle.get("createUpdaterArtifacts"):
        metadata["create_updater_artifacts"] = bundle.get("createUpdaterArtifacts")


def inspect_capability(path: Path, root: Path, findings: list[dict], capability_summary: list[dict]) -> None:
    data = load_json(path) if path.suffix.lower() == ".json" else load_toml(path)
    summary = {"file": rel(path, root), "parsed": data is not None}
    if not isinstance(data, dict):
        capability_summary.append(summary)
        return

    for key in ("identifier", "description", "windows", "webviews", "platforms", "remote"):
        if key in data:
            summary[key] = data.get(key)

    permissions = data.get("permissions", [])
    summary["permission_count"] = len(permissions) if isinstance(permissions, list) else None
    capability_summary.append(summary)

    if data.get("remote"):
        add_finding(findings, {
            "category": "remote_capability_present",
            "classification": "review_required",
            "file": rel(path, root),
        })

    text = read_text(path)
    if "**" in text or '"*"' in text or ' = "*"' in text:
        add_finding(findings, {
            "category": "capability_wildcard_marker",
            "classification": "review_required",
            "file": rel(path, root),
        })

    if re.search(r'"args"\s*:\s*true', text) or re.search(r"\bargs\s*=\s*true", text):
        add_finding(findings, {
            "category": "shell_args_unconstrained_marker",
            "classification": "review_required",
            "file": rel(path, root),
        })


def scan(root: Path) -> dict:
    root = root.resolve()
    src_tauri = root / "src-tauri" if (root / "src-tauri").is_dir() else root
    project_root = src_tauri.parent if src_tauri.name == "src-tauri" else root

    findings: list[dict] = []
    metadata: dict = {"updater_present": False}
    capability_summary: list[dict] = []
    files = collect_candidate_files(project_root, src_tauri)
    files_inspected: list[str] = []
    command_files: list[str] = []
    invoke_handler_files: list[str] = []
    frontend_invoke_files: list[str] = []
    direct_process_files: list[str] = []

    for path in files:
        text = read_text(path)
        files_inspected.append(rel(path, project_root))

        for category, markers in MARKERS.items():
            hits = [marker for marker in markers if marker in text]
            if hits:
                add_finding(findings, {
                    "category": category,
                    "classification": "review_required",
                    "file": rel(path, project_root),
                    "markers": hits,
                })

        if path.name == "tauri.conf.json":
            inspect_config(path, project_root, findings, metadata)

        if "capabilities" in path.parts or "permissions" in path.parts:
            inspect_capability(path, project_root, findings, capability_summary)

        if path.suffix.lower() == ".rs":
            if TAURI_COMMAND_RE.search(text):
                command_files.append(rel(path, project_root))
            if INVOKE_HANDLER_RE.search(text):
                invoke_handler_files.append(rel(path, project_root))
            if any(pattern.search(text) for pattern in RUST_PROCESS_PATTERNS):
                direct_process_files.append(rel(path, project_root))
                add_finding(findings, {
                    "category": "direct_rust_process_execution",
                    "classification": "review_required",
                    "file": rel(path, project_root),
                })
        elif path.suffix.lower() in {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}:
            if FRONTEND_INVOKE_RE.search(text):
                frontend_invoke_files.append(rel(path, project_root))

    return {
        "ok": True,
        "scanner": "tauri-security-boundary-surface-scan",
        "read_only": True,
        "executes_project_code": False,
        "network_used": False,
        "project_root": str(project_root),
        "src_tauri": str(src_tauri),
        "metadata": metadata,
        "files_inspected": files_inspected,
        "capabilities": capability_summary,
        "tauri_command_files": command_files,
        "invoke_handler_files": invoke_handler_files,
        "frontend_invoke_files": frontend_invoke_files,
        "direct_process_files": direct_process_files,
        "findings": findings,
        "finding_count": len(findings),
        "note": "Heuristic findings require manual review and are not proof of a vulnerability.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Tauri v2 security surface inventory")
    parser.add_argument("root", help="Tauri project root or src-tauri directory")
    args = parser.parse_args()
    root = Path(args.root)
    if not root.exists():
        print(json.dumps({"ok": False, "error": "root_not_found", "root": str(root)}, indent=2))
        return 2

    try:
        result = scan(root)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": "scan_failed", "detail": str(exc)}, indent=2))
        return 1

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
