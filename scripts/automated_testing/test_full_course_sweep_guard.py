from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import manual_manifest
import run_full_course_sweep as sweep


def test_manifest_generator_and_refresh_logic(tmp_path: Path) -> None:
    ex_dir = tmp_path / "exercises" / "ex01_inheritance"
    ex_dir.mkdir(parents=True)
    (ex_dir / "sample.py").write_text("print('ok')\n", encoding="utf-8")

    pdf = tmp_path / "exercise_manual.pdf"
    pdf.write_bytes(b"pdf")
    manifest_path = tmp_path / "course_manual_manifest.json"

    manual_manifest.write_manifest(manual_manifest.build_default_manifest(tmp_path), manifest_path)
    old_mtime = manifest_path.stat().st_mtime

    # Force the manifest to refresh when the PDF is newer.
    import time
    time.sleep(0.05)
    pdf.touch()
    assert manual_manifest.should_refresh_manifest(manifest_path, tmp_path) is True

    refreshed = manual_manifest.ensure_manifest(tmp_path, manifest_path)
    assert refreshed.exists()
    assert refreshed.stat().st_mtime >= old_mtime


def test_manifest_validation_checks_expected_files(tmp_path: Path) -> None:
    ex_dir = tmp_path / "exercises" / "ex01_inheritance"
    ex_dir.mkdir(parents=True)
    (ex_dir / "sample.py").write_text("print('ok')\n", encoding="utf-8")

    manifest = manual_manifest.build_default_manifest(tmp_path)
    manifest["entries"] = [{
        "exercise": "ex01_inheritance",
        "kind": "starter",
        "files": ["exercises/ex01_inheritance/sample.py"],
        "must_contain": [],
    }]

    manifest_path = tmp_path / "manual_manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    assert manual_manifest.validate_manifest(tmp_path, manifest_path) == []


def test_placeholder_guard_flags_solution_files_only(tmp_path: Path) -> None:
    starter = tmp_path / "exercises" / "ex01_inheritance"
    starter.mkdir(parents=True)
    (starter / "starter.py").write_text("x = ....\n", encoding="utf-8")

    solution = tmp_path / "exercises" / "solution_ex01_inheritance"
    solution.mkdir(parents=True)
    (solution / "solved.py").write_text("result = ....\n", encoding="utf-8")
    (solution / "data.txt").write_text("....\n", encoding="utf-8")

    violations = sweep.find_placeholder_violations(tmp_path)

    assert len(violations) == 1
    assert "solution_ex01_inheritance" in violations[0]
    assert "solved.py" in violations[0]


def test_placeholder_guard_ignores_non_python_files_and_data(tmp_path: Path) -> None:
    solution = tmp_path / "exercises" / "solution_appA_extending_python"
    solution.mkdir(parents=True)
    (solution / "module.py").write_text("value = 42\n", encoding="utf-8")
    (solution / "puzzle.txt").write_text("....\n", encoding="utf-8")

    assert sweep.find_placeholder_violations(tmp_path) == []


def test_manifest_guard_allows_template_placeholders(tmp_path: Path) -> None:
    starter = tmp_path / "exercises" / "ex01_inheritance"
    starter.mkdir(parents=True)
    (starter / "starter.py").write_text("x = ....\n", encoding="utf-8")

    assert sweep.find_placeholder_violations(tmp_path) == []
