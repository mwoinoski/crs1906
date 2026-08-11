#!/usr/bin/env python3
"""Run attendee-path validation for course exercises.

This runner validates exercise template implementations (not solution projects).
It starts with Exercise 1.1 and is designed to be extended exercise by exercise.

Typical usage:
    D:/mikew/Software/python-3.14/python.exe scripts/automated_testing/run_exercise_validation.py
    D:/mikew/Software/python-3.14/python.exe scripts/automated_testing/run_exercise_validation.py --exercise ex01
"""

from __future__ import annotations

import argparse
import os
import re
import socket
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

AUTOMATED_TESTING_DIR = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PY314 = Path(r"D:\mikew\Software\python-3.14\python.exe")
WORKSPACE_PYTHON = Path(sys.executable)


@dataclass
class StepResult:
    name: str
    status: str  # PASS | FAIL | SKIP
    code: int
    duration_s: float
    note: str = ""


@dataclass
class Step:
    name: str
    cwd: Path
    cmd: list[str]
    note: str = ""
    precheck: Optional[Callable[[], tuple[bool, str]]] = None
    env: Optional[dict[str, str]] = None
    allowed_codes: Optional[set[int]] = None


def q(arg: str) -> str:
    return f'"{arg}"' if " " in arg else arg


def run_cmd(step: Step) -> StepResult:
    if step.precheck is not None:
        ok, reason = step.precheck()
        if not ok:
            return StepResult(step.name, "SKIP", 0, 0.0, reason)

    print("\n" + "=" * 88)
    print(step.name)
    print("=" * 88)
    if step.note:
        print(step.note)
    print(f"cwd: {step.cwd}")
    print("cmd:", " ".join(q(str(part)) for part in step.cmd))
    print("-" * 88)

    start = time.perf_counter()
    try:
        env = os.environ.copy()
        if step.env:
            env.update(step.env)
        cp = subprocess.run(step.cmd, cwd=step.cwd, check=False, env=env)
    except FileNotFoundError as exc:
        elapsed = time.perf_counter() - start
        return StepResult(step.name, "FAIL", 127, elapsed, f"Missing file/executable: {exc}")

    elapsed = time.perf_counter() - start
    allowed_codes = step.allowed_codes if step.allowed_codes is not None else {0}
    status = "PASS" if cp.returncode in allowed_codes else "FAIL"
    note = ""
    if cp.returncode != 0 and status == "PASS":
        note = f"Non-zero exit accepted for this diagnostic step (code={cp.returncode})"
    return StepResult(step.name, status, cp.returncode, elapsed, note)


def check_exists(path: Path, label: str) -> Callable[[], tuple[bool, str]]:
    def _inner() -> tuple[bool, str]:
        if path.exists():
            return True, ""
        return False, f"{label} not found: {path}"

    return _inner


def can_connect(host: str, port: int, timeout: float = 1.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def wait_port(host: str, port: int, timeout_s: float) -> bool:
    end = time.time() + timeout_s
    while time.time() < end:
        if can_connect(host, port, timeout=0.75):
            return True
        time.sleep(0.2)
    return False


def stop_process(proc: Optional[subprocess.Popen], timeout: float = 5) -> None:
    if proc is None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()


def start_flask_server(cwd: Path, module_file: str, port: int) -> subprocess.Popen:
    env = os.environ.copy()
    code = (
        "import importlib.util; "
        f"spec=importlib.util.spec_from_file_location('srv','{module_file}'); "
        "m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); "
        f"m.app.run(debug=False, port={port})"
    )
    return subprocess.Popen(
        [str(WORKSPACE_PYTHON), "-c", code],
        cwd=cwd,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        sock.listen(1)
        return int(sock.getsockname()[1])


def start_pserve_server(project_root: Path, port: int) -> tuple[subprocess.Popen, Path]:
    pserve_exe = project_root / "venv" / "Scripts" / "pserve.exe"
    if not pserve_exe.exists():
        raise FileNotFoundError(f"pserve executable not found: {pserve_exe}")

    source_ini = project_root / "development.ini"
    if not source_ini.exists():
        raise FileNotFoundError(f"development.ini not found: {source_ini}")

    ini_text = source_ini.read_text(encoding="utf-8")
    if "port = 6543" not in ini_text:
        raise RuntimeError(f"Could not locate default port setting in {source_ini}")

    # Force pserve to import the app from the local exercise folder rather than
    # any globally editable install path.
    ini_text = re.sub(
        r"^use\s*=\s*egg:Exercise_[^\r\n]+$",
        "use = call:ticketmanor:main",
        ini_text,
        flags=re.MULTILINE,
    )
    ini_text = ini_text.replace("port = 6543", f"port = {port}", 1)

    fd, temp_name = tempfile.mkstemp(prefix="copilot_pserve_", suffix=".ini", dir=str(project_root))
    os.close(fd)
    temp_ini = Path(temp_name)
    temp_ini.write_text(ini_text, encoding="utf-8")

    proc = subprocess.Popen(
        [str(pserve_exe), str(temp_ini)],
        cwd=project_root,
        env={
            **os.environ,
            "PYTHONPATH": (
                f"{project_root}{os.pathsep}{os.environ['PYTHONPATH']}"
                if os.environ.get("PYTHONPATH")
                else str(project_root)
            ),
        },
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return proc, temp_ini


def build_steps(exercise: str) -> list[Step]:
    ex01 = REPO_ROOT / "exercises" / "ex01_inheritance"
    ex02 = REPO_ROOT / "exercises" / "ex02_template_method"
    ex03_1 = REPO_ROOT / "exercises" / "ex03_unit_testing"
    ex03_2 = REPO_ROOT / "exercises" / "ex03_with_mocks"
    ex04 = REPO_ROOT / "exercises" / "ex04_debugging"
    ex05 = REPO_ROOT / "exercises" / "ex05_performance"
    ex06 = REPO_ROOT / "exercises" / "ex06_design_patterns"
    ex07 = REPO_ROOT / "exercises" / "ex07_distributing"
    ex08_1 = REPO_ROOT / "exercises" / "ex08_concurrency"
    ex08_2 = REPO_ROOT / "exercises" / "ex08_multiprocessing"
    ex09 = REPO_ROOT / "exercises" / "ex09_rest_services"
    ex01_py = ex01 / "venv" / "Scripts" / "python.exe"
    ex02_py = ex02 / "venv" / "Scripts" / "python.exe"
    ex03_1_py = ex03_1 / "venv" / "Scripts" / "python.exe"
    ex03_2_py = ex03_2 / "venv" / "Scripts" / "python.exe"
    ex08_1_py = ex08_1 / "venv" / "Scripts" / "python.exe"
    ex08_2_py = ex08_2 / "venv" / "Scripts" / "python.exe"
    py314 = DEFAULT_PY314

    ex01_steps = [
        Step(
            name="Ex 1.1 python basics review script",
            cwd=ex01,
            cmd=[str(py314), "python_basics_review.py"],
            precheck=check_exists(py314, "Python 3.14 executable"),
        ),
        Step(
            name="Ex 1.1 full pytest suite",
            cwd=ex01,
            cmd=[str(ex01_py), "-m", "pytest", "-q", "tests"],
            precheck=check_exists(ex01_py, "Ex 1.1 venv python"),
        ),
    ]

    ex02_steps = [
        Step(
            name="Ex 2.1 full pytest suite",
            cwd=ex02,
            cmd=[str(ex02_py), "-m", "pytest", "-q", "tests"],
            precheck=check_exists(ex02_py, "Ex 2.1 venv python"),
        ),
    ]

    ex03_steps = [
        Step(
            name="Ex 3.1 target tests",
            cwd=ex03_1,
            cmd=[
                str(ex03_1_py),
                "-m",
                "pytest",
                "-q",
                "person/test_person.py",
                "tests/rest_services/test_rss_news_feed_parser.py",
                "tests/rest_services/test_rss_news_feed_parser_no_class.py",
            ],
            precheck=check_exists(ex03_1_py, "Ex 3.1 venv python"),
        ),
        Step(
            name="Ex 3.2 target tests",
            cwd=ex03_2,
            cmd=[
                str(ex03_2_py),
                "-m",
                "pytest",
                "-q",
                "tests/rest_services/test_feed_reader.py",
                "tests/rest_services/test_user_service.py",
            ],
            precheck=check_exists(ex03_2_py, "Ex 3.2 venv python"),
            note="Starter project does not include tests/rest_services/test_user_service_unittest.py",
        ),
    ]

    ex04_steps = [
        Step(
            name="Ex 4.1 non-demo target tests",
            cwd=ex04 / "sample_unit_tests",
            cmd=[
                str(py314),
                "-m",
                "pytest",
                "-q",
                "test_business_object.py",
                "test_business_object_patch.py",
                "test_business_object_sentinel.py",
            ],
            precheck=check_exists(py314, "Python 3.14 executable"),
        ),
    ]

    ex05_steps = [
        Step(
            name="Ex 5.1 func_stats script",
            cwd=ex05,
            cmd=[str(py314), "func_stats.py"],
            precheck=check_exists(py314, "Python 3.14 executable"),
        ),
        Step(
            name="Ex 5.1 sudoku script",
            cwd=ex05,
            cmd=[str(py314), "sudoku.py", "sudoku_input.txt"],
            precheck=check_exists(py314, "Python 3.14 executable"),
            note="Using bundled input file sudoku_input.txt",
        ),
    ]

    ex06_steps = [
        Step(
            name="Ex 6.1 observer pattern test",
            cwd=ex06,
            cmd=[str(py314), "-m", "pytest", "-q", "test_chat_observer.py"],
            precheck=check_exists(py314, "Python 3.14 executable"),
        ),
    ]

    ex07_steps = [
        Step(
            name="Ex 7.1 tz package tests",
            cwd=ex07 / "distributing_project",
            cmd=[str(py314), "-m", "pytest", "-q", "tests/test_tz.py"],
            precheck=check_exists(py314, "Python 3.14 executable"),
            env={"PYTHONPATH": "src"},
        ),
    ]

    ex08_steps = [
        Step(
            name="Ex 8.1 full pytest suite",
            cwd=ex08_1,
            cmd=[str(ex08_1_py), "-m", "pytest", "-q", "tests"],
            precheck=check_exists(ex08_1_py, "Ex 8.1 venv python"),
        ),
        Step(
            name="Ex 8.2 pi_monte_carlo script",
            cwd=ex08_2 / "pi_monte_carlo",
            cmd=[str(ex08_2_py), "pi.py"],
            precheck=check_exists(ex08_2_py, "Ex 8.2 venv python"),
        ),
    ]

    ex09_steps = [
        Step(
            name="Ex 9.1 local rest_server integration",
            cwd=ex09 / "user_service",
            cmd=[str(WORKSPACE_PYTHON), "-m", "pytest", "-q", "test_rest_server.py"],
            precheck=lambda: (can_connect("localhost", 5000), "rest_server.py is not listening on localhost:5000"),
        ),
        Step(
            name="Ex 9.1 desktop Tk widget smoke",
            cwd=REPO_ROOT,
            cmd=[
                str(WORKSPACE_PYTHON),
                str(AUTOMATED_TESTING_DIR / "user_gui_smoke.py"),
                "--ex09-root",
                str(ex09),
            ],
            precheck=lambda: (can_connect("localhost", 5001), "user_server.py is not listening on localhost:5001"),
        ),
        Step(
            name="Ex 9.1 user_ui service REST smoke",
            cwd=REPO_ROOT,
            cmd=[
                str(WORKSPACE_PYTHON),
                "-c",
                "import requests; r=requests.get('http://localhost:5001/rest/users', auth=('admin','adminpw'), timeout=10); print('status', r.status_code); raise SystemExit(0 if r.status_code==200 else 1)",
            ],
            precheck=lambda: (can_connect("localhost", 5001), "user_server.py is not listening on localhost:5001"),
        ),
    ]

    if exercise == "ex01":
        return ex01_steps
    if exercise == "ex02":
        return ex02_steps
    if exercise == "ex03":
        return ex03_steps
    if exercise == "ex04":
        return ex04_steps
    if exercise == "ex05":
        return ex05_steps
    if exercise == "ex06":
        return ex06_steps
    if exercise == "ex07":
        return ex07_steps
    if exercise == "ex08":
        return ex08_steps
    if exercise == "ex09":
        return ex09_steps
    if exercise == "all":
        return (
            ex01_steps
            + ex02_steps
            + ex03_steps
            + ex04_steps
            + ex05_steps
            + ex06_steps
            + ex07_steps
            + ex08_steps
            + ex09_steps
        )

    raise ValueError(f"Unsupported exercise code: {exercise}")


def print_summary(results: list[StepResult]) -> None:
    print("\n" + "#" * 88)
    print("Summary")
    print("#" * 88)
    for result in results:
        extra = f" | {result.note}" if result.note else ""
        print(f"[{result.status}] {result.name} ({result.duration_s:.2f}s){extra}")

    print("-" * 88)
    passed = sum(1 for result in results if result.status == "PASS")
    failed = sum(1 for result in results if result.status == "FAIL")
    skipped = sum(1 for result in results if result.status == "SKIP")
    print(f"PASS={passed}  FAIL={failed}  SKIP={skipped}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run attendee exercise validation checks.")
    parser.add_argument(
        "--exercise",
        choices=["ex01", "ex02", "ex03", "ex04", "ex05", "ex06", "ex07", "ex08", "ex09", "all"],
        default="all",
        help="Exercise validation profile to run (default: all)",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop at the first failing step.",
    )
    parser.add_argument(
        "--headed-ui",
        action="store_true",
        help="Run TicketManor Playwright browser checks in headed mode.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rest_server_proc: Optional[subprocess.Popen] = None
    user_server_proc: Optional[subprocess.Popen] = None
    ui_smoke_script = AUTOMATED_TESTING_DIR / "ticketmanor_ui_smoke.py"

    results: list[StepResult] = []

    if args.exercise in {"ex01", "ex02", "ex03", "ex08", "all"}:
        ui_checks: list[tuple[str, Path, bool, str]] = []
        if args.exercise in {"ex01", "all"}:
            ui_checks.append(("Ex 1.1 TicketManor UI smoke", REPO_ROOT / "exercises" / "ex01_inheritance", False, "ex01"))
        if args.exercise in {"ex02", "all"}:
            ui_checks.append(("Ex 2.1 TicketManor UI smoke", REPO_ROOT / "exercises" / "ex02_template_method", False, "ex02"))
        if args.exercise in {"ex03", "all"}:
            ui_checks.append(("Ex 3.1 TicketManor UI smoke", REPO_ROOT / "exercises" / "ex03_unit_testing", False, "ex03"))
        if args.exercise in {"ex08", "all"}:
            ui_checks.extend([
                ("Ex 8.1 TicketManor UI smoke", REPO_ROOT / "exercises" / "ex08_concurrency", False, "ex08_1"),
                ("Ex 8.2 TicketManor UI smoke", REPO_ROOT / "exercises" / "ex08_multiprocessing", True, "ex08_2"),
            ])

        for label, project_root, check_all_news, scenario in ui_checks:
            if not (project_root / "venv" / "Scripts" / "pserve.exe").exists():
                results.append(StepResult(label, "SKIP", 0, 0.0, f"pserve not found in {project_root}"))
                continue

            ui_port = find_free_port()
            server, temp_ini = start_pserve_server(project_root, ui_port)
            try:
                if not wait_port("127.0.0.1", ui_port, timeout_s=15):
                    results.append(StepResult(label, "FAIL", 2, 0.0, f"{project_root} did not open port {ui_port}"))
                    if args.fail_fast:
                        print_summary(results)
                        return 1
                    continue

                cmd = [
                    str(WORKSPACE_PYTHON),
                    str(ui_smoke_script),
                    "--base-url",
                    f"http://127.0.0.1:{ui_port}/static/#/home",
                    "--no-start-server",
                    "--scenario",
                    scenario,
                    "--browser-channel",
                    "chrome",
                ]
                if args.headed_ui:
                    cmd.append("--headed")
                if check_all_news:
                    cmd.append("--check-all-news")

                ui_result = run_cmd(
                    Step(
                        name=label,
                        cwd=REPO_ROOT,
                        cmd=cmd,
                        note=f"Temporary server: {project_root}",
                    )
                )
                results.append(ui_result)
                if args.fail_fast and ui_result.status == "FAIL":
                    print_summary(results)
                    return 1
            finally:
                stop_process(server)
                temp_ini.unlink(missing_ok=True)

    if args.exercise in {"ex09", "all"}:
        ex09_root = REPO_ROOT / "exercises" / "ex09_rest_services"
        rest_server_dir = ex09_root / "user_service"
        user_server_dir = ex09_root / "user_ui"

        if not can_connect("127.0.0.1", 5000):
            rest_server_proc = start_flask_server(rest_server_dir, "rest_server.py", 5000)
            if not wait_port("127.0.0.1", 5000, timeout_s=12):
                stop_process(rest_server_proc)
                print("ERROR: could not start Ex 9.1 rest_server.py on port 5000")
                return 2

        if not can_connect("127.0.0.1", 5001):
            user_server_proc = start_flask_server(user_server_dir, "user_server.py", 5001)
            if not wait_port("127.0.0.1", 5001, timeout_s=12):
                stop_process(rest_server_proc)
                stop_process(user_server_proc)
                print("ERROR: could not start Ex 9.1 user_server.py on port 5001")
                return 2

    steps = build_steps(args.exercise)
    try:
        for step in steps:
            result = run_cmd(step)
            results.append(result)
            if result.status == "FAIL" and args.fail_fast:
                break
    finally:
        stop_process(rest_server_proc)
        stop_process(user_server_proc)

    print_summary(results)
    return 1 if any(result.status == "FAIL" for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
