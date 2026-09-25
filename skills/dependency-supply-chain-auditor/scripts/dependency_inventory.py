#!/usr/bin/env python3
"""Read-only inventory of dependency manifests, locks, and source-risk markers.

The scanner never runs package managers, project code, builds, install hooks, or
network requests. It avoids printing dependency URL/index values that may contain
credentials and reports source types, package names, counts, and line numbers instead.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None

MAX_DEPTH = 4
MAX_FILES = 250
SKIP_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "target", "dist", "build",
    ".venv", "venv", "env", "__pycache__", ".tox", ".nox", ".cache",
}
JS_LOCKS = ("package-lock.json", "npm-shrinkwrap.json", "pnpm-lock.yaml", "yarn.lock")
PY_LOCKS = ("uv.lock", "poetry.lock", "Pipfile.lock")

SPECIAL_JS_PREFIXES = ("git+", "git:", "http:", "https:", "file:", "link:", "workspace:")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def depth_from(root: Path, path: Path) -> int:
    try:
        return len(path.relative_to(root).parts) - 1
    except ValueError:
        return MAX_DEPTH + 1


def walk_manifests(root: Path) -> list[Path]:
    wanted_exact = {"package.json", "Cargo.toml", "pyproject.toml", "Pipfile"}
    found: list[Path] = []
    for path in root.rglob("*"):
        if len(found) >= MAX_FILES:
            break
        if not path.is_file():
            continue
        try:
            parts = path.relative_to(root).parts
        except ValueError:
            continue
        if any(part in SKIP_DIRS for part in parts[:-1]):
            continue
        if depth_from(root, path) > MAX_DEPTH:
            continue
        if path.name in wanted_exact or (path.name.startswith("requirements") and path.suffix == ".txt"):
            found.append(path)
    return sorted(set(found))


def js_selector_class(spec: str) -> str:
    s = spec.strip().lower()
    if s in {"", "*", "latest"}:
        return "non_deterministic_selector"
    if s.startswith(("git+", "git:")):
        return "vcs"
    if s.startswith(("http:", "https:")):
        return "url"
    if s.startswith("file:"):
        return "local_file"
    if s.startswith("link:"):
        return "local_link"
    if s.startswith("workspace:"):
        return "workspace"
    if s.startswith("npm:"):
        return "package_alias"
    return "registry_selector"


def npm_summary(path: Path, root: Path) -> dict:
    try:
        data = json.loads(read_text(path))
    except Exception as exc:
        return {"parse_error": type(exc).__name__}

    direct: list[dict] = []
    special: list[dict] = []
    for section_name in ("dependencies", "devDependencies", "optionalDependencies", "peerDependencies"):
        section = data.get(section_name, {})
        if not isinstance(section, dict):
            continue
        for name, raw_spec in sorted(section.items()):
            spec = str(raw_spec)
            kind = js_selector_class(spec)
            direct.append({"name": name, "section": section_name, "selector_class": kind})
            if kind != "registry_selector":
                special.append({"name": name, "section": section_name, "selector_class": kind})

    scripts = data.get("scripts", {}) if isinstance(data.get("scripts"), dict) else {}
    lifecycle = sorted(k for k in scripts if k in {"preinstall", "install", "postinstall", "prepare"})
    overrides = data.get("overrides")
    resolutions = data.get("resolutions")
    manager = data.get("packageManager")

    parent = path.parent
    locks = [name for name in JS_LOCKS if (parent / name).is_file()]
    return {
        "manifest": rel(path, root),
        "package_manager_hint": str(manager) if manager else None,
        "direct_dependency_count": len(direct),
        "direct_dependencies": direct,
        "special_source_or_selector_entries": special,
        "lifecycle_script_names": lifecycle,
        "overrides_present": bool(overrides),
        "resolutions_present": bool(resolutions),
        "lockfiles": locks,
        "multiple_lockfiles": len(locks) > 1,
    }


def cargo_dependency_tables(data: dict) -> list[tuple[str, dict]]:
    tables: list[tuple[str, dict]] = []
    for key in ("dependencies", "dev-dependencies", "build-dependencies"):
        section = data.get(key)
        if isinstance(section, dict):
            tables.append((key, section))
    target = data.get("target")
    if isinstance(target, dict):
        for target_name, target_data in target.items():
            if not isinstance(target_data, dict):
                continue
            for key in ("dependencies", "dev-dependencies", "build-dependencies"):
                section = target_data.get(key)
                if isinstance(section, dict):
                    tables.append((f"target:{target_name}:{key}", section))
    return tables


def cargo_summary(path: Path, root: Path) -> dict:
    text = read_text(path)
    data = None
    if tomllib is not None:
        try:
            data = tomllib.loads(text)
        except Exception:
            data = None

    special: list[dict] = []
    direct_count = None
    wildcard: list[dict] = []
    if isinstance(data, dict):
        direct_count = 0
        for table_name, section in cargo_dependency_tables(data):
            for name, spec in sorted(section.items()):
                direct_count += 1
                if isinstance(spec, dict):
                    if "git" in spec:
                        special.append({"name": name, "table": table_name, "source_type": "vcs"})
                    if "path" in spec:
                        special.append({"name": name, "table": table_name, "source_type": "local_path"})
                    if "registry" in spec:
                        special.append({"name": name, "table": table_name, "source_type": "custom_registry"})
                    version = spec.get("version")
                    if isinstance(version, str) and version.strip() == "*":
                        wildcard.append({"name": name, "table": table_name})
                elif isinstance(spec, str) and spec.strip() == "*":
                    wildcard.append({"name": name, "table": table_name})

    line_markers = {"git": [], "path": [], "registry": []}
    for idx, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if re.search(r"\bgit\s*=", line):
            line_markers["git"].append(idx)
        if re.search(r"\bpath\s*=", line):
            line_markers["path"].append(idx)
        if re.search(r"\bregistry\s*=", line) or "replace-with" in line:
            line_markers["registry"].append(idx)

    return {
        "manifest": rel(path, root),
        "direct_dependency_count": direct_count,
        "special_dependencies": special,
        "wildcard_version_entries": wildcard,
        "source_marker_lines": line_markers,
        "lockfiles": ["Cargo.lock"] if (path.parent / "Cargo.lock").is_file() else [],
    }


def sanitize_req_name(line: str) -> str:
    work = line.strip()
    if work.startswith("-e "):
        work = work[3:].strip()
    egg = re.search(r"[#&]egg=([A-Za-z0-9_.-]+)", work)
    if egg:
        return egg.group(1)
    if " @ " in work:
        return work.split(" @ ", 1)[0].strip()
    if work.startswith(("git+", "http://", "https://", "file:")):
        return "direct-source-requirement"
    return re.split(r"[<>=!~\[\s]", work, maxsplit=1)[0] or "unknown"


def requirements_summary(path: Path, root: Path) -> dict:
    entries = 0
    special: list[dict] = []
    unpinned: list[dict] = []
    index_directives: list[dict] = []
    hash_entries = 0

    for idx, raw in enumerate(read_text(path).splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "--hash=" in line:
            hash_entries += 1

        if line.startswith("--index-url"):
            index_directives.append({"line": idx, "type": "index_url"})
            continue
        if line.startswith("--extra-index-url"):
            index_directives.append({"line": idx, "type": "extra_index_url"})
            continue
        if line.startswith("--trusted-host"):
            index_directives.append({"line": idx, "type": "trusted_host"})
            continue

        entries += 1
        lower = line.lower()
        source_type = None
        if lower.startswith("-e "):
            source_type = "editable"
        elif lower.startswith("git+"):
            source_type = "vcs"
        elif lower.startswith(("http://", "https://")) or " @ http://" in lower or " @ https://" in lower:
            source_type = "url"
        elif lower.startswith(("file:", "./", "../", "/")) or " @ file:" in lower:
            source_type = "local_path"
        if source_type:
            special.append({"line": idx, "name": sanitize_req_name(line), "source_type": source_type})

        if not line.startswith("-") and not source_type and not any(op in line for op in ("==", "===", " @ ")):
            name = sanitize_req_name(line)
            if name:
                unpinned.append({"line": idx, "name": name})

    return {
        "manifest": rel(path, root),
        "dependency_entry_count": entries,
        "special_dependencies": special,
        "unpinned_entries": unpinned,
        "index_directives": index_directives,
        "entries_with_hash_marker": hash_entries,
    }


def pyproject_summary(path: Path, root: Path) -> dict:
    text = read_text(path)
    data = None
    if tomllib is not None:
        try:
            data = tomllib.loads(text)
        except Exception:
            data = None

    result = {
        "manifest": rel(path, root),
        "project_dependency_count": None,
        "direct_url_dependencies": [],
        "build_system_requirement_count": None,
        "custom_source_markers": [],
        "lockfiles": [name for name in PY_LOCKS if (path.parent / name).is_file()],
    }
    if not isinstance(data, dict):
        result["parse_error"] = True
        return result

    project = data.get("project")
    if isinstance(project, dict):
        deps = project.get("dependencies", [])
        if isinstance(deps, list):
            result["project_dependency_count"] = len(deps)
            for dep in deps:
                if isinstance(dep, str) and (" @ " in dep or "git+" in dep or "http://" in dep or "https://" in dep):
                    result["direct_url_dependencies"].append({"name": sanitize_req_name(dep)})

    build = data.get("build-system")
    if isinstance(build, dict) and isinstance(build.get("requires"), list):
        result["build_system_requirement_count"] = len(build.get("requires", []))

    tool = data.get("tool")
    if isinstance(tool, dict):
        # Report presence only. Source values may contain internal/private endpoints.
        for tool_name in ("poetry", "pdm", "uv"):
            tool_data = tool.get(tool_name)
            if isinstance(tool_data, dict):
                for key in ("source", "sources", "index", "indexes"):
                    if key in tool_data:
                        result["custom_source_markers"].append({"tool": tool_name, "key": key})
    return result


def pipfile_summary(path: Path, root: Path) -> dict:
    text = read_text(path)
    markers: list[dict] = []
    for idx, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip().lower()
        if line.startswith("url ="):
            markers.append({"line": idx, "type": "source_url"})
        if "git =" in line:
            markers.append({"line": idx, "type": "vcs_dependency"})
        if "path =" in line:
            markers.append({"line": idx, "type": "local_path_dependency"})
    return {
        "manifest": rel(path, root),
        "source_or_special_markers": markers,
        "lockfiles": ["Pipfile.lock"] if (path.parent / "Pipfile.lock").is_file() else [],
    }


def scan(root: Path) -> dict:
    root = root.resolve()
    manifests = walk_manifests(root)
    projects: list[dict] = []
    ecosystems: set[str] = set()

    for path in manifests:
        if path.name == "package.json":
            ecosystems.add("javascript")
            projects.append({"ecosystem": "javascript", **npm_summary(path, root)})
        elif path.name == "Cargo.toml":
            ecosystems.add("cargo")
            projects.append({"ecosystem": "cargo", **cargo_summary(path, root)})
        elif path.name == "pyproject.toml":
            ecosystems.add("python")
            projects.append({"ecosystem": "python", **pyproject_summary(path, root)})
        elif path.name == "Pipfile":
            ecosystems.add("python")
            projects.append({"ecosystem": "python", **pipfile_summary(path, root)})
        elif path.name.startswith("requirements") and path.suffix == ".txt":
            ecosystems.add("python")
            projects.append({"ecosystem": "python", **requirements_summary(path, root)})

    return {
        "ok": True,
        "scanner": "dependency-supply-chain-inventory",
        "read_only": True,
        "network_used": False,
        "runs_package_managers": False,
        "executes_project_code": False,
        "project_root": str(root),
        "ecosystems": sorted(ecosystems),
        "manifest_count": len(manifests),
        "projects": projects,
        "truncated_manifest_discovery": len(manifests) >= MAX_FILES,
        "note": "Static inventory only. Vulnerability, maintainer, license, ownership, and registry claims require current external evidence.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only dependency supply-chain inventory")
    parser.add_argument("root", help="Project or repository root")
    args = parser.parse_args()
    root = Path(args.root)
    if not root.exists() or not root.is_dir():
        print(json.dumps({"ok": False, "error": "root_not_found", "root": str(root)}, indent=2))
        return 2
    try:
        result = scan(root)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": "scan_failed", "detail": type(exc).__name__}, indent=2))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
