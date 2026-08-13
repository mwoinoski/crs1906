#!/usr/bin/env python3
"""Run a full course sweep for Course 1906.

This aggregator runs the two validation layers used in this repo:

1. attendee/starter exercise validation
2. slide/demo validation that exercises the solution projects and demo scripts

Typical usage:
    D:/mikew/Software/python-3.14/python.exe scripts/automated_testing/run_full_course_sweep.py
    D:/mikew/Software/python-3.14/python.exe scripts/automated_testing/run_full_course_sweep.py --headed-ui --fail-fast
    D:/mikew/Software/python-3.14/python.exe scripts/automated_testing/run_full_course_sweep.py --exercise ex08
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from manual_manifest import ensure_manifest, validate_manifest

REPO_ROOT = Path(__file__).resolve().parents[2]
AUTOMATED_TESTING_DIR = Path(__file__).resolve().parent
EXERCISE_VALIDATOR = AUTOMATED_TESTING_DIR / "run_exercise_validation.py"
SLIDE_VALIDATOR = AUTOMATED_TESTING_DIR / "run_slide_activities.py"
MANIFEST_PATH = AUTOMATED_TESTING_DIR / "course_manual_manifest.json"


def find_placeholder_violations(repo_root: Path | None = None) -> list[str]:
    """Return any Python source placeholders left behind in solution directories.

    Student exercise templates intentionally keep placeholder values like "...."
    so the interpreter will fail until the student replaces them. Solution files,
    however, should never keep those placeholders in place.
    """
    if repo_root is None:
        repo_root = REPO_ROOT

    exercises_dir = repo_root / "exercises"
    if not exercises_dir.exists():
        return []

    violations: list[str] = []
    for solution_dir in sorted(exercises_dir.iterdir()):
        if not solution_dir.is_dir() or not solution_dir.name.startswith("solution_"):
            continue

        for py_file in sorted(solution_dir.rglob("*.py")):
            try:
                lines = py_file.read_text(encoding="utf-8").splitlines()
            except UnicodeDecodeError:
                try:
                    lines = py_file.read_text(encoding="utf-8", errors="replace").splitlines()
                except OSError:
                    continue
            for line_no, line in enumerate(lines, start=1):
                if "...." in line:
                    violations.append(f"{py_file.relative_to(repo_root)}:{line_no}: contains '....'")
    return violations


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a full Course 1906 sweep.")
    parser.add_argument(
        "--exercise",
        choices=["ex01", "ex02", "ex03", "ex04", "ex05", "ex06", "ex07", "ex08", "ex09", "all"],
        default="all",
        help="Exercise validation profile to run in the starter exercise validator (default: all).",
    )
    parser.add_argument(
        "--headed-ui",
        action="store_true",
        help="Pass headed UI mode through to the starter exercise validation step.",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop each validation phase at the first failing step.",
    )
    parser.add_argument(
        "--skip-exercise-validation",
        action="store_true",
        help="Skip the starter exercise validation phase.",
    )
    parser.add_argument(
        "--skip-slide-validation",
        action="store_true",
        help="Skip the slide/demo validation phase.",
    )
    return parser.parse_args()


def run_phase(label: str, script: Path, extra_args: list[str]) -> int:
    cmd = [sys.executable, str(script), *extra_args]
    print(f"\n{'=' * 96}\n{label}\n{'=' * 96}")
    print(f"cwd: {REPO_ROOT}")
    print("cmd:", " ".join(f'"{part}"' if " " in part else part for part in cmd))
    print("-" * 96)
    return subprocess.run(cmd, cwd=REPO_ROOT, check=False).returncode


def main() -> int:
    args = parse_args()

    ensure_manifest(REPO_ROOT, MANIFEST_PATH)
    manifest_errors = validate_manifest(REPO_ROOT, MANIFEST_PATH)
    if manifest_errors:
        print("ERROR: manual manifest validation failed:")
        for error in manifest_errors:
            print(f"  {error}")
        return 1

    placeholder_violations = find_placeholder_violations()
    if placeholder_violations:
        print("ERROR: solution files contain '....' placeholders:")
        for violation in placeholder_violations:
            print(f"  {violation}")
        return 1

    if args.skip_exercise_validation and args.skip_slide_validation:
        print("ERROR: both validation phases were skipped.")
        return 2

    overall_rc = 0

    if not args.skip_exercise_validation:
        exercise_args: list[str] = ["--exercise", args.exercise]
        if args.headed_ui:
            exercise_args.append("--headed-ui")
        if args.fail_fast:
            exercise_args.append("--fail-fast")

        exercise_rc = run_phase("Exercise validation phase", EXERCISE_VALIDATOR, exercise_args)
        overall_rc = exercise_rc or overall_rc
        if exercise_rc != 0 and args.fail_fast:
            print("\nExercise validation failed; stopping full sweep early.")
            return exercise_rc

    if not args.skip_slide_validation:
        slide_args: list[str] = []
        if args.fail_fast:
            slide_args.append("--fail-fast")

        slide_rc = run_phase("Slide/demo validation phase", SLIDE_VALIDATOR, slide_args)
        overall_rc = slide_rc or overall_rc
        if slide_rc != 0 and args.fail_fast:
            print("\nSlide/demo validation failed; stopping full sweep early.")
            return slide_rc

    if overall_rc == 0:
        print("\nFull course sweep completed successfully.")
    else:
        print(f"\nFull course sweep finished with failures (exit code {overall_rc}).")
    return overall_rc


if __name__ == "__main__":
    raise SystemExit(main())
