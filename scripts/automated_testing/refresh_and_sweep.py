#!/usr/bin/env python3
"""Refresh the course manifest when needed and then run the full sweep.

This helper keeps the annual refresh flow simple:

1. Rebuild the structured manual manifest if the PDF is newer.
2. Run the full course sweep.

The script intentionally does not parse the PDF itself at runtime; it uses the
project's structured manifest and the existing validation runners.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from generate_manual_manifest import main as generate_manifest_main
from run_full_course_sweep import main as sweep_main

REPO_ROOT = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh the manual manifest if needed, then run the full course sweep.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Path to the course repo root.",
    )
    parser.add_argument(
        "--exercise",
        choices=["ex01", "ex02", "ex03", "ex04", "ex05", "ex06", "ex07", "ex08", "ex09", "all"],
        default="all",
        help="Exercise validation profile to pass through to the full-sweep runner.",
    )
    parser.add_argument(
        "--headed-ui",
        action="store_true",
        help="Pass headed UI mode through to the exercise validation phase.",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop at the first failing step.",
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


def main() -> int:
    args = parse_args()

    # Refresh the manifest first if the PDF is newer than the generated JSON.
    # This keeps the workflow lightweight and avoids PDF parsing in the runtime
    # validation stage.
    manifest_result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).resolve().parent / "generate_manual_manifest.py"),
            "--repo-root",
            str(args.repo_root),
        ],
        cwd=str(args.repo_root),
        check=False,
    )
    if manifest_result.returncode != 0:
        return manifest_result.returncode

    # Run the sweep with the same flags as the main validation entry point.
    sweep_args = [
        "--exercise",
        args.exercise,
    ]
    if args.headed_ui:
        sweep_args.append("--headed-ui")
    if args.fail_fast:
        sweep_args.append("--fail-fast")
    if args.skip_exercise_validation:
        sweep_args.append("--skip-exercise-validation")
    if args.skip_slide_validation:
        sweep_args.append("--skip-slide-validation")

    original_argv = sys.argv[:]
    try:
        sys.argv = ["run_full_course_sweep.py", *sweep_args]
        return sweep_main()
    finally:
        sys.argv = original_argv


if __name__ == "__main__":
    raise SystemExit(main())
