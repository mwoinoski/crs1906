#!/usr/bin/env python3
"""Command-line smoke automation for Exercise 4.1 unittestgui.

This validates that the Tk/unit-test workflow can be driven from a normal
command line without relying on PyCharm. It opens the GUI in a hidden state,
programmatically performs the discover/run steps, and verifies that the log
file was updated.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EXERCISE_DIR = REPO_ROOT / "exercises" / "solution_ex04_debugging"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Exercise 4.1 unittestgui smoke automation.")
    parser.add_argument(
        "--exercise-dir",
        default=str(DEFAULT_EXERCISE_DIR),
        help="Path to the ex04_debugging solution folder (default: solution_ex04_debugging).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    exercise_dir = Path(args.exercise_dir).resolve()
    sample_dir = exercise_dir / "sample_unit_tests"
    log_file = exercise_dir / "unittestgui.log"

    if not exercise_dir.exists():
        print(f"ERROR: exercise directory not found: {exercise_dir}")
        return 1
    if not sample_dir.exists():
        print(f"ERROR: sample tests directory not found: {sample_dir}")
        return 1

    before_size = log_file.stat().st_size if log_file.exists() else 0

    original_cwd = Path.cwd()
    root = None
    try:
        os.chdir(exercise_dir)
        if str(exercise_dir) not in sys.path:
            sys.path.insert(0, str(exercise_dir))

        import importlib
        import tkinter as tk

        unittestgui = importlib.import_module("unittestgui")

        root = tk.Tk()
        root.withdraw()

        runner = unittestgui.TkTestRunner(root, "")
        runner.getDirectoryToDiscover = lambda: str(sample_dir)

        runner.discoverClicked()
        if not runner.test_suite:
            print("ERROR: unittestgui did not discover a test suite.")
            return 1

        discovered = runner.test_suite.countTestCases()
        runner.runClicked()
        root.update_idletasks()

        summary = {
            "discovered": discovered,
            "run": runner.runCountVar.get(),
            "failures": runner.failCountVar.get(),
            "errors": runner.errorCountVar.get(),
            "skipped": runner.skipCountVar.get(),
            "remaining": runner.remainingCountVar.get(),
        }

        if summary["discovered"] <= 0:
            print(f"ERROR: expected discovered tests, got: {summary}")
            return 1
        if summary["run"] != summary["discovered"]:
            print(f"ERROR: not all discovered tests were run: {summary}")
            return 1
        if summary["remaining"] != 0:
            print(f"ERROR: GUI still reports remaining tests after run: {summary}")
            return 1
        if summary["failures"] + summary["errors"] <= 0:
            print(f"ERROR: expected at least one failure/error from the demo suite: {summary}")
            return 1

        if not log_file.exists():
            print(f"ERROR: log file was not created: {log_file}")
            return 1

        added_text = log_file.read_text(encoding="utf-8", errors="replace")
        if before_size:
            added_text = added_text[before_size:]

        if "selected directory =" not in added_text or "sample_unit_tests" not in added_text:
            print("ERROR: expected discovery log output was not written to unittestgui.log")
            return 1

        print("PASS: command-line unittestgui smoke automation succeeded")
        print(summary)
        return 0
    finally:
        if root is not None:
            try:
                root.destroy()
            except Exception:
                pass
        os.chdir(original_cwd)


if __name__ == "__main__":
    raise SystemExit(main())
