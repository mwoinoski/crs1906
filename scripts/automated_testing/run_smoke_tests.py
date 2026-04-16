#!/usr/bin/env python3
"""Incremental smoke-test runner for the Course 1906 repository.

This script is intentionally small and conservative. It provides a repeatable
starting point for automation:

- standalone Python scripts run with the interpreter that launches this file
  (for this workspace, that is typically Python 3.14)
- TicketManor/Pyramid tests run with the project-local Python 3.13 virtualenv

Examples
--------
    py -3.14 scripts\automated_testing\run_smoke_tests.py --list
    py -3.14 scripts\automated_testing\run_smoke_tests.py baseline
    py -3.14 scripts\automated_testing\run_smoke_tests.py ticketmanor-api
    py -3.14 scripts\automated_testing\run_smoke_tests.py all
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

AUTOMATED_TESTING_DIR = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_PYTHON = Path(sys.executable)


@dataclass(frozen=True)
class Job:
    name: str
    description: str
    cwd: Path
    cmd: list[str]


def quote(arg: str) -> str:
    return f'"{arg}"' if " " in arg else arg


def run_job(job: Job) -> int:
    print("\n" + "=" * 78)
    print(job.name)
    print("=" * 78)
    print(job.description)
    print(f"cwd: {job.cwd}")
    print("cmd:", " ".join(quote(part) for part in job.cmd))
    print("-" * 78)

    start = time.perf_counter()
    try:
        completed = subprocess.run(job.cmd, cwd=job.cwd, check=False)
    except FileNotFoundError as exc:
        print(f"ERROR: missing executable or file: {exc}")
        return 1

    elapsed = time.perf_counter() - start
    status = "PASS" if completed.returncode == 0 else "FAIL"
    print("-" * 78)
    print(f"{status}: exit code {completed.returncode} in {elapsed:.2f}s")
    return completed.returncode


EX01_ROOT = REPO_ROOT / "exercises" / "solution_ex01_inheritance"
EX01_VENV_PYTHON = EX01_ROOT / "venv" / "Scripts" / "python.exe"
BASELINE_SCRIPT = EX01_ROOT / "python_basics_review.py"
TICKETMANOR_ROOT = REPO_ROOT / "exercises" / "ticketmanor_webapp"
TICKETMANOR_PYTHON = TICKETMANOR_ROOT / "venv" / "Scripts" / "python.exe"
TICKETMANOR_UI_SCRIPT = AUTOMATED_TESTING_DIR / "ticketmanor_ui_smoke.py"
PYTEST_WARNING_FILTER = "ignore::DeprecationWarning"


SUITES: dict[str, list[Job]] = {
    "baseline": [
        Job(
            name="Baseline script: python_basics_review.py",
            description=(
                "Runs the simplest smoke-test target with the interpreter used "
                "to launch this runner."
            ),
            cwd=BASELINE_SCRIPT.parent,
            cmd=[str(WORKSPACE_PYTHON), str(BASELINE_SCRIPT.name)],
        ),
    ],
    "ex01-pytest": [
        Job(
            name="solution_ex01_inheritance pytest suite",
            description=(
                "Runs the full test suite for the inheritance exercise solution "
                "with its Python 3.13 virtualenv."
            ),
            cwd=EX01_ROOT,
            cmd=[
                str(EX01_VENV_PYTHON),
                "-m",
                "pytest",
                "-W",
                PYTEST_WARNING_FILTER,
                "tests",
                "-q",
            ],
        ),
    ],
    "ticketmanor-api": [
        Job(
            name="TicketManor EventService integration tests",
            description=(
                "Runs Pyramid/WebTest integration tests against the project-local "
                "Python 3.13 virtualenv and temporary SQLite test DB."
            ),
            cwd=TICKETMANOR_ROOT,
            cmd=[
                str(TICKETMANOR_PYTHON),
                "-m",
                "pytest",
                "-W",
                PYTEST_WARNING_FILTER,
                "tests/rest_services/test_event_service_integration.py",
                "-q",
            ],
        ),
        Job(
            name="TicketManor UserService integration tests",
            description=(
                "Runs API integration tests using the TicketManor project's own "
                "Python 3.13 virtualenv."
            ),
            cwd=TICKETMANOR_ROOT,
            cmd=[
                str(TICKETMANOR_PYTHON),
                "-m",
                "pytest",
                "-W",
                PYTEST_WARNING_FILTER,
                "tests/rest_services/test_user_service_integration.py",
                "-q",
            ],
        ),
    ],
    "ticketmanor-pytest": [
        Job(
            name="ticketmanor_webapp full pytest suite",
            description=(
                "Runs the full TicketManor test suite with the project-local "
                "Python 3.13 virtualenv."
            ),
            cwd=TICKETMANOR_ROOT,
            cmd=[
                str(TICKETMANOR_PYTHON),
                "-m",
                "pytest",
                "-W",
                PYTEST_WARNING_FILTER,
                "tests",
                "-q",
            ],
        ),
    ],
    "ticketmanor-ui": [
        Job(
            name="TicketManor Playwright UI smoke test",
            description=(
                "Runs the browser-based Concerts search smoke test using the "
                "workspace Python and Playwright."
            ),
            cwd=REPO_ROOT,
            cmd=[str(WORKSPACE_PYTHON), str(TICKETMANOR_UI_SCRIPT)],
        ),
    ],
}


def iter_jobs(suite_name: str) -> Iterable[Job]:
    if suite_name == "all":
        for name in (
            "baseline",
            "ex01-pytest",
            "ticketmanor-api",
            "ticketmanor-pytest",
            "ticketmanor-ui",
        ):
            yield from SUITES[name]
    else:
        yield from SUITES[suite_name]


def validate_environment(suite_name: str) -> int:
    if not BASELINE_SCRIPT.exists():
        print(f"ERROR: baseline script not found: {BASELINE_SCRIPT}")
        return 1

    if suite_name in {"ex01-pytest", "all"} and not EX01_VENV_PYTHON.exists():
        print("ERROR: solution_ex01_inheritance venv python not found:")
        print(f"  {EX01_VENV_PYTHON}")
        print("Create the exercise virtualenv first with Python 3.13.")
        return 1

    if suite_name in {"ticketmanor-api", "ticketmanor-pytest", "all"} and not TICKETMANOR_PYTHON.exists():
        print("ERROR: TicketManor venv python not found:")
        print(f"  {TICKETMANOR_PYTHON}")
        print("Create the TicketManor virtualenv first with Python 3.13.")
        return 1

    if suite_name in {"ticketmanor-ui", "all"} and not TICKETMANOR_UI_SCRIPT.exists():
        print("ERROR: TicketManor UI smoke script not found:")
        print(f"  {TICKETMANOR_UI_SCRIPT}")
        return 1

    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run incremental smoke tests for crs1906.")
    parser.add_argument(
        "suite",
        nargs="?",
        default="baseline",
        choices=["baseline", "ex01-pytest", "ticketmanor-api", "ticketmanor-pytest", "ticketmanor-ui", "all"],
        help="Which test suite to run (default: baseline).",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List the available suites and exit.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.list:
        print("Available suites:")
        print("  baseline           - simple standalone script smoke test (Python 3.14)")
        print("  ex01-pytest        - full solution_ex01_inheritance test suite (Python 3.13 venv)")
        print("  ticketmanor-api    - focused TicketManor API integration checks (Python 3.13 venv)")
        print("  ticketmanor-pytest - full TicketManor test suite (Python 3.13 venv)")
        print("  ticketmanor-ui     - browser-based TicketManor search smoke test (Playwright)")
        print("  all                - run all currently configured suites")
        return 0

    rc = validate_environment(args.suite)
    if rc:
        return rc

    failures = 0
    for job in iter_jobs(args.suite):
        rc = run_job(job)
        if rc != 0:
            failures += 1
            break

    if failures:
        print(f"\nSmoke test run finished with {failures} failure(s).")
        return 1

    print("\nSmoke test run finished successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
