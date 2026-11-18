#!/usr/bin/env python3
"""Standalone on-demand inspector and lazy bootstrapper for Smolnikov Research Agent Skills."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

ON_DEMAND_FILENAME = "on-demand.json"
_SAFE_TOKEN_RE = re.compile(r"^[A-Za-z0-9._/\-\[\]=<>~@:]+$")


def _repo_skills_root() -> Path:
    return Path(__file__).resolve().parent.parent / "skills"


def _models_cache_root() -> Path:
    override = os.environ.get("CAPYAGENT_MODELS_DIR", "").strip()
    if override:
        return Path(override).expanduser()
    home = Path(os.environ.get("CAPYAGENT_HOME", Path.home() / ".capyagent")).expanduser()
    return home / "cache" / "models"


def find_skill_dir(skill_name_or_dir: Union[str, Path]) -> Optional[Path]:
    """Resolve an optional skill directory inside ./skills/ or local user skills directory."""
    candidate = Path(skill_name_or_dir)
    if candidate.is_dir() and (candidate / "SKILL.md").is_file():
        return candidate.resolve()
    slug = str(skill_name_or_dir).strip().rstrip("/").rsplit("/", 1)[-1]
    for root in (
        Path(os.environ.get("CAPYAGENT_HOME", Path.home() / ".capyagent")).expanduser() / "skills",
        _repo_skills_root(),
    ):
        if not root.is_dir():
            continue
        direct = root / slug
        if (direct / "SKILL.md").is_file():
            return direct
        for sk in root.rglob("SKILL.md"):
            if sk.parent.name == slug:
                return sk.parent
    return None


def _parse_pkg_spec(spec: Union[str, dict]) -> Tuple[str, str]:
    if isinstance(spec, dict):
        pip_name = str(spec.get("pip") or spec.get("package") or "").strip()
        mod_name = str(spec.get("import") or pip_name.split("[", 1)[0].replace("-", "_")).strip()
        return mod_name, pip_name
    pip_name = str(spec).strip()
    base = re.split(r"[<>=~!;\[]", pip_name, maxsplit=1)[0].strip()
    return base.replace("-", "_"), pip_name


def inspect_on_demand_skill(skill_dir: Path) -> Dict[str, Any]:
    """Read-only inspection of system binaries, Python packages, and local model checkpoints."""
    manifest_path = Path(skill_dir) / ON_DEMAND_FILENAME
    if not manifest_path.is_file():
        return {
            "has_on_demand": False,
            "auto_load_on_startup": False,
            "ready": True,
            "missing_binaries": [],
            "missing_python": [],
            "missing_models": [],
            "install_commands": [],
        }

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    binaries = [str(b).strip() for b in manifest.get("system_binaries", []) if str(b).strip()]
    missing_binaries = [b for b in binaries if shutil.which(b) is None]

    missing_python: List[str] = []
    for raw_spec in manifest.get("python_packages", []):
        mod_name, pip_name = _parse_pkg_spec(raw_spec)
        if mod_name and pip_name and importlib.util.find_spec(mod_name) is None:
            missing_python.append(pip_name)

    models_cache = _models_cache_root()
    missing_models: List[dict] = []
    for m in manifest.get("models", []):
        if not isinstance(m, dict):
            continue
        mid = str(m.get("id") or "").strip()
        repo = str(m.get("repo") or "").strip()
        env_ep = str(m.get("env_endpoint") or "").strip()
        if not mid:
            continue
        endpoint_set = bool(env_ep and os.environ.get(env_ep, "").strip())
        target_dir = models_cache / mid
        weights_ok = target_dir.is_dir() and any(target_dir.iterdir())
        if not endpoint_set and not weights_ok:
            missing_models.append({"id": mid, "repo": repo, "target_dir": str(target_dir), "env_endpoint": env_ep})

    install_commands: List[str] = []
    safe_py = [pkg for pkg in missing_python if _SAFE_TOKEN_RE.match(pkg)]
    if safe_py:
        uv_bin = shutil.which("uv")
        install_commands.append(
            ("uv pip install " if uv_bin else f"{sys.executable} -m pip install ") + " ".join(safe_py)
        )
    for hint in manifest.get("system_install_hints", []):
        if str(hint).strip():
            install_commands.append(str(hint).strip())
    for m in missing_models:
        if m["repo"] and _SAFE_TOKEN_RE.match(m["repo"]):
            install_commands.append(f"hf download {m['repo']} --local-dir {m['target_dir']}")

    return {
        "has_on_demand": True,
        "auto_load_on_startup": bool(manifest.get("auto_load_on_startup", False)),
        "ready": not missing_binaries and not missing_python and not missing_models,
        "summary": str(manifest.get("summary") or ""),
        "missing_binaries": missing_binaries,
        "missing_python": missing_python,
        "missing_models": missing_models,
        "install_commands": install_commands,
    }


def bootstrap_on_demand_skill(
    skill_name_or_dir: Union[str, Path],
    *,
    install_python: bool = True,
    download_models: bool = False,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Explicitly install Python deps and optionally fetch model weights for an on-demand skill."""
    skill_dir = find_skill_dir(skill_name_or_dir)
    if skill_dir is None:
        return {"ok": False, "error": f"Skill '{skill_name_or_dir}' not found."}
    before = inspect_on_demand_skill(skill_dir)
    cmds: List[List[str]] = []

    if install_python and before["missing_python"]:
        safe_py = [p for p in before["missing_python"] if _SAFE_TOKEN_RE.match(p)]
        if safe_py:
            uv_bin = shutil.which("uv")
            cmds.append([uv_bin, "pip", "install", *safe_py] if uv_bin else [sys.executable, "-m", "pip", "install", *safe_py])

    if download_models and before["missing_models"]:
        hf_bin = shutil.which("hf") or shutil.which("huggingface-cli")
        for m in before["missing_models"]:
            if hf_bin and m.get("repo") and _SAFE_TOKEN_RE.match(str(m["repo"])):
                cmds.append([hf_bin, "download", str(m["repo"]), "--local-dir", str(m["target_dir"])])

    executed: List[dict] = []
    if not dry_run:
        for cmd in cmds:
            proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
            executed.append({"cmd": " ".join(cmd), "returncode": proc.returncode, "stderr": proc.stderr[-800:]})
            if proc.returncode != 0:
                return {"ok": False, "skill": skill_dir.name, "executed": executed, "status": inspect_on_demand_skill(skill_dir)}

    return {
        "ok": True,
        "skill": skill_dir.name,
        "dry_run": dry_run,
        "planned_commands": [" ".join(c) for c in cmds],
        "executed": executed,
        "status": before if dry_run else inspect_on_demand_skill(skill_dir),
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect or lazily bootstrap an optional skill.")
    parser.add_argument("skill")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--models", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    if args.install:
        res = bootstrap_on_demand_skill(args.skill, install_python=True, download_models=args.models, dry_run=args.dry_run)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0 if res.get("ok") else 1

    skill_dir = find_skill_dir(args.skill)
    if skill_dir is None:
        print(json.dumps({"ok": False, "error": f"Skill '{args.skill}' not found"}))
        return 1
    print(json.dumps({"skill": skill_dir.name, **inspect_on_demand_skill(skill_dir)}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
