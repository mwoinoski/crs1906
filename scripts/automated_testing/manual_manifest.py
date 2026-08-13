#!/usr/bin/env python3
"""Exercise-manifest helpers for the Course 1906 validation workflow.

This module intentionally does not parse PDF files at runtime. The annual course
refresh process is expected to generate a structured manifest from the revised
exercise manual once, and then the runtime validation scripts simply read that
manifest on each run.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

AUTOMATED_TESTING_DIR = Path(__file__).resolve().parent
DEFAULT_MANIFEST_PATH = AUTOMATED_TESTING_DIR / "course_manual_manifest.json"


def build_default_manifest(repo_root: Path) -> dict[str, Any]:
    """Build the default structured manifest used when no PDF-derived manifest exists.

    This is deliberately simple but practical: it records the expected exercise
    folders and the files that should exist for each project. The real refresh
    process can replace this with a richer manifest generated from the PDF, but
    the runtime validator remains manifest-driven and does not parse PDFs.
    """
    exercises_root = repo_root / "exercises"
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "generated_from": "static-template-manifest",
        "entries": [],
    }

    if not exercises_root.exists():
        return manifest

    for exercise_dir in sorted(exercises_root.iterdir()):
        if not exercise_dir.is_dir():
            continue

        name = exercise_dir.name
        if name.startswith("solution_"):
            kind = "solution"
        elif name.startswith("ex") or name.startswith("app"):
            kind = "starter"
        else:
            continue

        files: list[str] = []
        for child in sorted(exercise_dir.rglob("*")):
            if child.is_file():
                rel = child.relative_to(repo_root).as_posix()
                files.append(rel)

        entry = {
            "exercise": name,
            "kind": kind,
            "files": files,
            "must_contain": [],
        }
        manifest["entries"].append(entry)

    return manifest


def find_recent_manual_pdf(repo_root: Path) -> Path | None:
    candidates = [p for p in repo_root.rglob("*.pdf") if "manual" in p.name.lower() or "exercise" in p.name.lower() or "slides" in p.name.lower()]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def should_refresh_manifest(manifest_path: Path, repo_root: Path) -> bool:
    if not manifest_path.exists():
        return True

    pdf_path = find_recent_manual_pdf(repo_root)
    if pdf_path is None:
        return False

    return pdf_path.stat().st_mtime > manifest_path.stat().st_mtime


def write_manifest(manifest: dict[str, Any], manifest_path: Path) -> None:
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_manifest(manifest_path: Path) -> dict[str, Any]:
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def ensure_manifest(repo_root: Path, manifest_path: Path | None = None) -> Path:
    if manifest_path is None:
        manifest_path = DEFAULT_MANIFEST_PATH

    if should_refresh_manifest(manifest_path, repo_root):
        write_manifest(build_default_manifest(repo_root), manifest_path)

    if not manifest_path.exists():
        write_manifest(build_default_manifest(repo_root), manifest_path)

    return manifest_path


def validate_manifest(repo_root: Path, manifest_path: Path | None = None) -> list[str]:
    """Validate the current repo against the manifest entries.

    The manifest is intentionally simple: each project entry lists expected files.
    Runtime validation then ensures those files exist in the repo. This provides a
    lightweight manual-as-spec layer without parsing PDFs at runtime.
    """
    if manifest_path is None:
        manifest_path = DEFAULT_MANIFEST_PATH

    if not manifest_path.exists():
        return [f"Manifest is missing: {manifest_path}"]

    try:
        manifest = load_manifest(manifest_path)
    except json.JSONDecodeError as exc:
        return [f"Manifest is not valid JSON: {manifest_path}: {exc}"]

    errors: list[str] = []
    entries = manifest.get("entries", [])
    if not isinstance(entries, list):
        return [f"Manifest does not contain an entries list: {manifest_path}"]

    for entry in entries:
        exercise = entry.get("exercise")
        files = entry.get("files", [])
        if not exercise or not isinstance(files, list):
            errors.append(f"Manifest entry is missing exercise/files: {entry}")
            continue

        project_dir = repo_root / "exercises" / exercise
        if not project_dir.exists():
            errors.append(f"Manifest references missing project directory: {project_dir}")
            continue

        for rel_path in files:
            full_path = repo_root / rel_path
            if not full_path.exists():
                errors.append(f"Manifest expects file to exist: {rel_path}")

    return errors
