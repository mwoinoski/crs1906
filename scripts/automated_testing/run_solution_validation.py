#!/usr/bin/env python3
"""Run the solution-validation workflow for Course 1906.

This script reproduces the solution checks performed during the current review:
- Ex 01 through Ex 09 solution projects
- AppA solution scripts
- AppB is intentionally excluded from this validation scope

Design goals:
- one-command repeatability
- clear pass/fail/skip reporting
- minimal user interaction
- safe handling of optional/external dependencies

Typical usage:
    py -3.14 scripts\automated_testing\run_solution_validation.py
    py -3.14 scripts\automated_testing\run_solution_validation.py --include-external-6544
    py -3.14 scripts\automated_testing\run_solution_validation.py --fail-fast
"""

from __future__ import annotations

import argparse
import base64
import os
import shutil
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
WORKSPACE_PYTHON = Path(sys.executable)

FAST_SKIP_STEP_NAMES = {
    "Ex 3.1 coverage report (html)",
    "Ex 5.1 sudoku cProfile tottime",
    "Ex 5.1 sudoku cProfile ncalls",
    "Ex 5.1 sudoku cProfile output file",
    "Ex 7.1 build package dist artifacts",
    "Ex 7.1 bonus wheel install in clean venv",
}

REQUESTED_SECTIONS = [
    "Ex 1.1",
    "Ex 2.1 steps 8-11",
    "Ex 2.1 step 15",
    "Ex 3.1 steps 17-22",
    "Ex 4.1 steps 1-17",
    "Ex 4.1 steps 18-23",
    "Ex 4.1 steps 24-25",
    "Ex 5.1",
    "Ex 6.1",
    "Ex 7.1",
    "Ex 8.1 steps 12-19",
    "Ex 8.2 steps 11-13",
    "Ex 8.2 steps 14-17",
    "Ex 9.1 steps 1-14",
]

UI_SECTION_BY_LABEL = {
    "Ex 1.1 TicketManor UI smoke": "Ex 1.1",
    "Ex 2.1 TicketManor UI smoke": "Ex 2.1 steps 8-11",
    "Ex 3.1 TicketManor UI smoke": "Ex 3.1 steps 17-22",
    "Ex 8.1 TicketManor UI smoke": "Ex 8.1 steps 12-19",
    "Ex 8.2 TicketManor UI smoke": "Ex 8.2 steps 14-17",
}


@dataclass
class StepResult:
    name: str
    section: str
    status: str  # PASS | FAIL | SKIP
    code: int
    duration_s: float
    note: str = ""


@dataclass
class Step:
    name: str
    section: str
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
            return StepResult(step.name, step.section, "SKIP", 0, 0.0, reason)

    print("\n" + "=" * 88)
    print(step.name)
    print("=" * 88)
    if step.note:
        print(step.note)
    print(f"cwd: {step.cwd}")
    print("cmd:", " ".join(q(str(p)) for p in step.cmd))
    print("-" * 88)

    start = time.perf_counter()
    try:
        env = os.environ.copy()
        if step.env:
            env.update(step.env)
        cp = subprocess.run(step.cmd, cwd=step.cwd, check=False, env=env)
    except FileNotFoundError as exc:
        elapsed = time.perf_counter() - start
        return StepResult(step.name, step.section, "FAIL", 127, elapsed, f"Missing file/executable: {exc}")

    elapsed = time.perf_counter() - start
    allowed_codes = step.allowed_codes if step.allowed_codes is not None else {0}
    status = "PASS" if cp.returncode in allowed_codes else "FAIL"
    note = ""
    if cp.returncode != 0 and status == "PASS":
        note = f"Non-zero exit accepted for this diagnostic step (code={cp.returncode})"
    return StepResult(step.name, step.section, status, cp.returncode, elapsed, note)


def local_venv_python(path: Path) -> Path:
    return path / "venv" / "Scripts" / "python.exe"


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


def section_for_ui_label(label: str) -> str:
    return UI_SECTION_BY_LABEL.get(label, label)


def stop_process(proc: Optional[subprocess.Popen], timeout: float = 5) -> None:
    if proc is None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()


def restore_file_from_backup(target: Path) -> None:
    backup = target.parent / f"{target.name}.backup"
    if backup.exists():
        shutil.copy2(backup, target)


def restore_ex09_databases() -> None:
    restore_file_from_backup(REPO_ROOT / "exercises" / "solution_ex09_rest_services" / "user_service" / "users_db.sqlite")
    restore_file_from_backup(REPO_ROOT / "exercises" / "solution_ex09_rest_services" / "user_ui" / "users_db.sqlite")


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


def resolve_python314_exec() -> Optional[Path]:
    candidates = [
        Path(r"C:\python\python3.14\python.exe"),
        Path(r"D:\mikew\Software\python-3.14\python.exe"),
        WORKSPACE_PYTHON,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def resolve_python314t_exec() -> Optional[Path]:
    candidates = [
        Path(r"C:\python\python3.14\python3.14t.exe"),
        Path(r"D:\mikew\Software\python-3.14\python3.14t.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def resolve_pypy_exec() -> Optional[str]:
    path_candidates = [
        Path(r"C:\python\pypy\pypy.exe"),
        Path(r"D:\mikew\Software\pypy\pypy.exe"),
    ]
    for candidate in path_candidates:
        if candidate.exists():
            return str(candidate)

    fallback = shutil.which("pypy")
    if fallback:
        return fallback

    return None


def resolve_python27_exec() -> Optional[str]:
    path_candidates = [
        Path(r"C:\python\python2.7\python.exe"),
        Path(r"D:\mikew\Software\python-2.7\python.exe"),
    ]
    for candidate in path_candidates:
        if candidate.exists():
            return str(candidate)

    candidates = [
        shutil.which("python2.7"),
        shutil.which("python27"),
    ]
    for candidate in candidates:
        if candidate:
            return candidate

    # Final fallback: ask the py launcher for Python 2.7.
    cp = subprocess.run(
        ["py", "-2.7", "-c", "import sys; print(sys.executable)"],
        check=False,
        capture_output=True,
        text=True,
    )
    if cp.returncode == 0 and cp.stdout.strip():
        return cp.stdout.strip()

    return None


def is_module_importable(py_exe: Path, module_name: str) -> bool:
    cp = subprocess.run(
        [str(py_exe), "-c", f"import importlib.util, sys; sys.exit(0 if importlib.util.find_spec('{module_name}') else 1)"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return cp.returncode == 0


def has_6544_contract() -> tuple[bool, str]:
    if not can_connect("localhost", 6544):
        return False, "No listener on localhost:6544"

    # Probe: GET /rest/users with admin creds should return 200 on expected service.
    try:
        import urllib.request

        url = "http://localhost:6544/rest/users"
        req = urllib.request.Request(url, method="GET")
        req.add_header("Accept", "application/json")
        creds = base64.b64encode(b"admin:adminpw").decode("ascii")
        req.add_header("Authorization", f"Basic {creds}")
        with urllib.request.urlopen(req, timeout=3) as resp:
            if resp.status == 200:
                return True, ""
            return False, f"Unexpected status from 6544 probe: {resp.status}"
    except Exception as exc:  # pragma: no cover
        return False, f"6544 probe failed: {exc}"


def start_flask_server(cwd: Path, module_file: str, port: int) -> subprocess.Popen:
    env = os.environ.copy()
    # Disable reloader for clean lifecycle management.
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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        s.listen(1)
        return int(s.getsockname()[1])



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
    ini_text = ini_text.replace("port = 6543", f"port = {port}", 1)

    fd, temp_name = tempfile.mkstemp(prefix="copilot_pserve_", suffix=".ini", dir=str(project_root))
    os.close(fd)
    temp_ini = Path(temp_name)
    temp_ini.write_text(ini_text, encoding="utf-8")

    proc = subprocess.Popen(
        [str(pserve_exe), str(temp_ini)],
        cwd=project_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return proc, temp_ini


def wait_port(host: str, port: int, timeout_s: float) -> bool:
    end = time.time() + timeout_s
    while time.time() < end:
        if can_connect(host, port, timeout=0.75):
            return True
        time.sleep(0.2)
    return False


def include_step_for_profile(step: Step, profile: str) -> bool:
    return profile != "fast" or step.name not in FAST_SKIP_STEP_NAMES


def build_steps(include_external_6544: bool, profile: str) -> list[Step]:
    ex01 = REPO_ROOT / "exercises" / "solution_ex01_inheritance"
    ex02 = REPO_ROOT / "exercises" / "solution_ex02_template_method"
    ex03_1 = REPO_ROOT / "exercises" / "solution_ex03_unit_testing"
    ex03_2 = REPO_ROOT / "exercises" / "solution_ex03_with_mocks"
    ex04 = REPO_ROOT / "exercises" / "solution_ex04_debugging"
    ex05 = REPO_ROOT / "exercises" / "solution_ex05_performance"
    ex06 = REPO_ROOT / "exercises" / "solution_ex06_design_patterns"
    ex07 = REPO_ROOT / "exercises" / "solution_ex07_distributing" / "distributing_project"
    ex08_1 = REPO_ROOT / "exercises" / "solution_ex08_concurrency"
    ex08_2 = REPO_ROOT / "exercises" / "solution_ex08_multiprocessing"
    ex09 = REPO_ROOT / "exercises" / "solution_ex09_rest_services" / "user_service"
    appa = REPO_ROOT / "exercises" / "solution_appA_extending_python"
    py314 = resolve_python314_exec()
    py314t = resolve_python314t_exec()
    pypy = resolve_pypy_exec()
    py27 = resolve_python27_exec()

    ex01_py = local_venv_python(ex01)
    ex02_py = local_venv_python(ex02)
    ex03_1_py = local_venv_python(ex03_1)
    ex03_2_py = local_venv_python(ex03_2)
    ex08_1_py = local_venv_python(ex08_1)
    ex08_2_py = local_venv_python(ex08_2)

    steps: list[Step] = [
        Step(
            name="Ex 1.1 full pytest suite",
            section="Ex 1.1",
            cwd=ex01,
            cmd=[str(ex01_py), "-m", "pytest", "-q", "tests"],
            precheck=check_exists(ex01_py, "Ex 1.1 venv python"),
        ),
        Step(
            name="Ex 2.1 full pytest suite",
            section="Ex 2.1",
            cwd=ex02,
            cmd=[str(ex02_py), "-m", "pytest", "-q", "tests"],
            precheck=check_exists(ex02_py, "Ex 2.1 venv python"),
        ),
        Step(
            name="Ex 3.1 target tests",
            section="Ex 3.1",
            cwd=ex03_1,
            cmd=[
                str(ex03_1_py), "-m", "pytest", "-q",
                "person/test_person.py",
                "tests/rest_services/test_rss_news_feed_parser.py",
                "tests/rest_services/test_rss_news_feed_parser_no_class.py",
            ],
            precheck=check_exists(ex03_1_py, "Ex 3.1 venv python"),
        ),
        Step(
            name="Ex 3.1 coverage report (term)",
            section="Ex 3.1 steps 17-22",
            cwd=ex03_1,
            cmd=[
                str(ex03_1_py), "-m", "pytest",
                "--cov-report", "term",
                "--cov", "ticketmanor.rest_services.feed_reader",
                "tests/rest_services/test_rss_news_feed_parser.py",
            ],
            precheck=check_exists(ex03_1_py, "Ex 3.1 venv python"),
        ),
        Step(
            name="Ex 3.1 coverage report (term-missing)",
            section="Ex 3.1 steps 17-22",
            cwd=ex03_1,
            cmd=[
                str(ex03_1_py), "-m", "pytest",
                "--cov-report", "term-missing",
                "--cov", "ticketmanor.rest_services.feed_reader",
                "tests/rest_services/test_rss_news_feed_parser.py",
            ],
            precheck=check_exists(ex03_1_py, "Ex 3.1 venv python"),
        ),
        Step(
            name="Ex 3.1 coverage report (html)",
            section="Ex 3.1 steps 17-22",
            cwd=ex03_1,
            cmd=[
                str(ex03_1_py), "-m", "pytest",
                "--cov-report", "html",
                "--cov", "ticketmanor.rest_services.feed_reader",
                "tests/rest_services/test_rss_news_feed_parser.py",
            ],
            precheck=check_exists(ex03_1_py, "Ex 3.1 venv python"),
        ),
        Step(
            name="Ex 3.2 target tests",
            section="Ex 3.2",
            cwd=ex03_2,
            cmd=[
                str(ex03_2_py), "-m", "pytest", "-q",
                "tests/rest_services/test_feed_reader.py",
                "tests/rest_services/test_user_service.py",
                "tests/rest_services/test_user_service_unittest.py",
            ],
            precheck=check_exists(ex03_2_py, "Ex 3.2 venv python"),
        ),
        Step(
            name="Ex 4.1 unittestgui CLI smoke",
            section="Ex 4.1 steps 1-17",
            cwd=REPO_ROOT,
            cmd=[
                str(WORKSPACE_PYTHON),
                str(AUTOMATED_TESTING_DIR / "unittestgui_smoke.py"),
                "--exercise-dir",
                str(ex04),
            ],
        ),
        Step(
            name="Ex 4.1 non-demo tests",
            section="Ex 4.1 steps 1-17",
            cwd=ex04 / "sample_unit_tests",
            cmd=[
                str(WORKSPACE_PYTHON), "-m", "pytest", "-q",
                "test_business_object.py",
                "test_business_object_patch.py",
                "test_business_object_sentinel.py",
                "test_person.py::PersonTestCase::test_init",
                "test_person.py::PersonTestCase::test_eq_instances_equal",
                "test_person.py::PersonTestCase::test_eq_new_instances_equal",
                "test_person_nose.py::test_init",
                "test_person_nose.py::test_eq_instances_equal",
                "test_person_nose.py::test_eq_instances_not_equal",
                "test_person_nose.py::test_eq_new_instances_equal",
            ],
        ),
        Step(
            name="Ex 4.1 pylint baseline",
            section="Ex 4.1 steps 18-23",
            cwd=ex04,
            cmd=[str(WORKSPACE_PYTHON), "-m", "pylint", "unittestgui.py"],
            allowed_codes={0, 2, 4, 8, 16, 18, 20, 24, 26, 28, 30},
            note="Diagnostic lint output is expected for this manual exercise.",
        ),
        Step(
            name="Ex 4.1 pylint disable messages",
            section="Ex 4.1 steps 18-23",
            cwd=ex04,
            cmd=[
                str(WORKSPACE_PYTHON), "-m", "pylint",
                "--disable=fixme,invalid-name,unnecessary-pass",
                "unittestgui.py",
            ],
            allowed_codes={0, 2, 4, 8, 16, 18, 20, 24, 26, 28, 30},
            note="Diagnostic lint output is expected for this manual exercise.",
        ),
        Step(
            name="Ex 4.1 generate pylint rcfile",
            section="Ex 4.1 steps 24-25",
            cwd=ex04,
            cmd=[
                "cmd",
                "/c",
                f"{q(str(WORKSPACE_PYTHON))} -m pylint --disable=fixme,invalid-name,unnecessary-pass --generate-rcfile > ex04_pylintrc.generated",
            ],
        ),
        Step(
            name="Ex 4.1 pylint with generated rcfile",
            section="Ex 4.1 steps 24-25",
            cwd=ex04,
            cmd=[str(WORKSPACE_PYTHON), "-m", "pylint", "--rcfile", "ex04_pylintrc.generated", "unittestgui.py"],
            precheck=check_exists(ex04 / "ex04_pylintrc.generated", "generated pylint rcfile"),
            allowed_codes={0, 2, 4, 8, 16, 18, 20, 24, 26, 28, 30},
            note="Diagnostic lint output is expected for this manual exercise.",
        ),
        Step(
            name="Ex 5.1 func_stats",
            section="Ex 5.1",
            cwd=ex05,
            cmd=[str(WORKSPACE_PYTHON), "func_stats.py"],
        ),
        Step(
            name="Ex 5.1 sudoku manual input",
            section="Ex 5.1",
            cwd=ex05,
            cmd=[str(WORKSPACE_PYTHON), "sudoku.py", "sudoku_input.txt"],
        ),
        Step(
            name="Ex 5.1 sudoku cProfile tottime",
            section="Ex 5.1",
            cwd=ex05,
            cmd=[
                "cmd",
                "/c",
                f"{q(str(WORKSPACE_PYTHON))} -m cProfile -s tottime sudoku.py sudoku_input.txt > profile1.txt",
            ],
        ),
        Step(
            name="Ex 5.1 sudoku cProfile ncalls",
            section="Ex 5.1",
            cwd=ex05,
            cmd=[
                "cmd",
                "/c",
                f"{q(str(WORKSPACE_PYTHON))} -m cProfile -s ncalls sudoku.py sudoku_input.txt > profile2.txt",
            ],
        ),
        Step(
            name="Ex 5.1 sudoku cProfile output file",
            section="Ex 5.1",
            cwd=ex05,
            cmd=[str(WORKSPACE_PYTHON), "-m", "cProfile", "-o", "sudoku.prof", "sudoku.py", "sudoku_input.txt"],
        ),
        Step(
            name="Ex 5.1 SnakeViz graph smoke",
            section="Ex 5.1",
            cwd=REPO_ROOT,
            cmd=[
                str(WORKSPACE_PYTHON),
                str(AUTOMATED_TESTING_DIR / "snakeviz_smoke.py"),
                "--profile-path",
                str(ex05 / "sudoku.prof"),
            ],
            precheck=(lambda: (is_module_importable(WORKSPACE_PYTHON, "snakeviz"), "snakeviz module is not installed in the workspace Python environment")),
        ),
        Step(
            name="Ex 5.1 PyPy comparison",
            section="Ex 5.1",
            cwd=ex05,
            cmd=[str(pypy) if pypy else "pypy", "sudoku.py", "sudoku_input.txt"],
            precheck=(lambda: (pypy is not None, "PyPy executable not found at the standard workstation or instructor paths")),
        ),
        Step(
            name="Ex 5.1 sudoku",
            section="Ex 5.1",
            cwd=ex05,
            cmd=[str(WORKSPACE_PYTHON), "sudoku.py", "sudoku_input_easy_1011.txt"],
        ),
        Step(
            name="Ex 6.1 observer tests",
            section="Ex 6.1",
            cwd=ex06,
            cmd=[str(WORKSPACE_PYTHON), "-m", "pytest", "-q", "test_chat_observer.py"],
        ),
        Step(
            name="Ex 6.1 tkinter GUI interaction tests",
            section="Ex 6.1",
            cwd=REPO_ROOT,
            cmd=[str(WORKSPACE_PYTHON), "-m", "pytest", "-q", str(AUTOMATED_TESTING_DIR / "test_chat_gui_observer.py")],
        ),
        Step(
            name="Ex 6.1 sudoku with configurable decorator",
            section="Ex 6.1",
            cwd=ex06,
            cmd=[str(WORKSPACE_PYTHON), "sudoku.py", "sudoku_input.txt"],
        ),
        Step(
            name="Ex 7.1 package tests",
            section="Ex 7.1",
            cwd=ex07,
            cmd=[str(WORKSPACE_PYTHON), "-m", "pytest", "-q", "tests/test_tz.py"],
            note="Requires pytz import availability in the interpreter used to run this script.",
            env={"PYTHONPATH": str(ex07 / "src")},
        ),
        Step(
            name="Ex 7.1 verify build package",
            section="Ex 7.1",
            cwd=REPO_ROOT,
            cmd=[str(WORKSPACE_PYTHON), "-m", "pip", "show", "build"],
        ),
        Step(
            name="Ex 7.1 sudoku compatibility script",
            section="Ex 7.1",
            cwd=REPO_ROOT / "exercises" / "solution_ex07_distributing",
            cmd=[py27 if py27 else str(WORKSPACE_PYTHON), "sudoku.py", "sudoku_input.txt"],
            precheck=(lambda: (py27 is not None, "Python 2.7 interpreter not found; compatibility script is Python-2-only")),
        ),
        Step(
            name="Ex 7.1 build package dist artifacts",
            section="Ex 7.1",
            cwd=ex07,
            cmd=[str(WORKSPACE_PYTHON), "-m", "build"],
        ),
        Step(
            name="Ex 7.1 bonus wheel install in clean venv",
            section="Ex 7.1",
            cwd=ex07 / "dist",
            cmd=[str(WORKSPACE_PYTHON), "-c", "import subprocess, sys; subprocess.run([sys.executable, '-m', 'venv', 'venv_ex71_bonus_auto'], check=True); py='venv_ex71_bonus_auto\\\\Scripts\\\\python.exe'; subprocess.run([py, '-m', 'pip', 'install', 'simple_tz-1.0.0-py3-none-any.whl'], check=True); subprocess.run([py, '-c', \"from simple_tz import tz; print(tz.convert('2026-12-31 16:00:00','PST','CET'))\"], check=True)"],
            precheck=check_exists(ex07 / "dist" / "simple_tz-1.0.0-py3-none-any.whl", "simple_tz wheel in dist"),
        ),
        Step(
            name="Ex 8.1 core tests",
            section="Ex 8.1",
            cwd=ex08_1,
            cmd=[str(ex08_1_py), "-m", "pytest", "-q", "tests"],
            precheck=check_exists(ex08_1_py, "Ex 8.1 venv python"),
        ),
        Step(
            name="Ex 8.1 count_primes with Python 3.14",
            section="Ex 8.1",
            cwd=ex08_1,
            cmd=[str(py314) if py314 else str(WORKSPACE_PYTHON), "count_primes.py"],
            precheck=(lambda: (py314 is not None, "Python 3.14 executable not found")),
            env={"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"},
        ),
        Step(
            name="Ex 8.1 count_primes with Python 3.14t",
            section="Ex 8.1",
            cwd=ex08_1,
            cmd=[str(py314t) if py314t else str(WORKSPACE_PYTHON), "count_primes.py"],
            precheck=(lambda: (py314t is not None, "Python 3.14t executable not found (free-threading check skipped)")),
            env={"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"},
        ),
        Step(
            name="Ex 8.2 core tests",
            section="Ex 8.2",
            cwd=ex08_2,
            cmd=[str(ex08_2_py), "-m", "pytest", "-q", "tests", "-k", "not test_feed_reader"],
            precheck=check_exists(ex08_2_py, "Ex 8.2 venv python"),
        ),
        Step(
            name="Ex 8.2 pi_monte_carlo",
            section="Ex 8.2",
            cwd=ex08_2,
            cmd=[str(ex08_2_py), "pi_monte_carlo/pi.py"],
            precheck=check_exists(ex08_2_py, "Ex 8.2 venv python"),
        ),
        Step(
            name="Ex 8.2 pi_monte_carlo with Python 3.14t",
            section="Ex 8.2 steps 11-13",
            cwd=ex08_2 / "pi_monte_carlo",
            cmd=[str(py314t) if py314t else str(WORKSPACE_PYTHON), "pi.py"],
            precheck=(lambda: (py314t is not None, "Python 3.14t executable not found")),
        ),
        Step(
            name="Ex 9.1 local rest_server integration",
            section="Ex 9.1",
            cwd=ex09,
            cmd=[str(WORKSPACE_PYTHON), "-m", "pytest", "-q", "test_rest_server.py"],
        ),
        Step(
            name="Ex 9.1 desktop Tk widget smoke",
            section="Ex 9.1 steps 1-14",
            cwd=REPO_ROOT,
            cmd=[str(WORKSPACE_PYTHON), str(AUTOMATED_TESTING_DIR / "user_gui_smoke.py")],
            precheck=(lambda: (can_connect("localhost", 5001), "user_server.py is not listening on localhost:5001")),
        ),
        Step(
            name="Ex 9.1 user_ui service REST smoke",
            section="Ex 9.1 steps 1-14",
            cwd=REPO_ROOT,
            cmd=[str(WORKSPACE_PYTHON), "-c", "import requests; r=requests.get('http://localhost:5001/rest/users', auth=('admin','adminpw'), timeout=10); print('status', r.status_code); raise SystemExit(0 if r.status_code==200 else 1)"],
            precheck=(lambda: (can_connect("localhost", 5001), "user_server.py is not listening on localhost:5001")),
        ),
        Step(
            name="Ex 9.1 external 6544 json+urllib tests",
            section="Ex 9.1",
            cwd=ex09,
            cmd=[
                str(WORKSPACE_PYTHON), "-m", "pytest", "-q",
                "test_user_rest_service_json.py",
                "test_user_rest_service_urllib.py",
            ],
            precheck=(lambda: has_6544_contract()) if include_external_6544 else (lambda: (False, "Skipped unless --include-external-6544 is set")),
        ),
        Step(
            name="AppA pure Python mandelbrot",
            section="AppA",
            cwd=appa,
            cmd=[str(WORKSPACE_PYTHON), "mandelbrot.py", "100", "10", "-n"],
        ),
        Step(
            name="AppA ctypes mandelbrot",
            section="AppA",
            cwd=appa / "mandelbrot_ctypes",
            cmd=[str(WORKSPACE_PYTHON), "mandelbrot.py", "100", "10", "-n"],
        ),
        Step(
            name="AppA extension-module mandelbrot",
            section="AppA",
            cwd=appa / "mandelbrot_ext_module",
            cmd=[str(WORKSPACE_PYTHON), "mandelbrot.py", "100", "10", "-n"],
        ),
    ]

    # AppB is intentionally excluded from the current validation scope.
    return [s for s in steps if include_step_for_profile(s, profile)]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run reproducible validation for solution projects.")
    p.add_argument(
        "--include-external-6544",
        action="store_true",
        help="Run Ex 9 external tests on localhost:6544 when the service is available.",
    )
    p.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop on the first failing step.",
    )
    p.add_argument(
        "--profile",
        choices=("fast", "full", "strict"),
        default="full",
        help="Run profile: fast skips longer optional steps; full runs all configured checks; strict treats skips as failures.",
    )
    return p.parse_args()


def print_requested_section_report(results: list[StepResult]) -> None:
    status_by_requested = {name: "SKIP" for name in REQUESTED_SECTIONS}

    def mark(section: str, status: str) -> None:
        order = {"FAIL": 3, "PASS": 2, "SKIP": 1}
        current = status_by_requested.get(section, "SKIP")
        if order[status] > order[current]:
            status_by_requested[section] = status

    for result in results:
        if result.section in status_by_requested:
            mark(result.section, result.status)
        if result.name == "Ex 2.1 TicketManor UI smoke":
            mark("Ex 2.1 step 15", result.status)

    print("\n" + "#" * 88)
    print("Requested Manual-Step Coverage Report")
    print("#" * 88)
    for section in REQUESTED_SECTIONS:
        print(f"[{status_by_requested[section]}] {section}")


def main() -> int:
    args = parse_args()

    ex01_dir = REPO_ROOT / "exercises" / "solution_ex01_inheritance"
    ex02_dir = REPO_ROOT / "exercises" / "solution_ex02_template_method"
    ui_smoke_script = AUTOMATED_TESTING_DIR / "ticketmanor_ui_smoke.py"

    results: list[StepResult] = []

    ui_checks = [
        ("Ex 1.1 TicketManor UI smoke", ex01_dir),
        ("Ex 2.1 TicketManor UI smoke", ex02_dir),
    ]
    if args.profile != "fast":
        ui_checks.extend([
            ("Ex 3.1 TicketManor UI smoke", REPO_ROOT / "exercises" / "solution_ex03_unit_testing"),
            ("Ex 8.1 TicketManor UI smoke", REPO_ROOT / "exercises" / "solution_ex08_concurrency"),
            ("Ex 8.2 TicketManor UI smoke", REPO_ROOT / "exercises" / "solution_ex08_multiprocessing"),
        ])

    # Ex 1.1 and Ex 2.1 manual validation includes running the TicketManor web UI.
    for label, project_root in ui_checks:
        section = section_for_ui_label(label)
        if not (project_root / "venv" / "Scripts" / "pserve.exe").exists():
            results.append(StepResult(label, section, "SKIP", 0, 0.0, f"pserve not found in {project_root}"))
            continue

        ui_port = find_free_port()
        server, temp_ini = start_pserve_server(project_root, ui_port)
        try:
            if not wait_port("127.0.0.1", ui_port, timeout_s=15):
                results.append(StepResult(label, section, "FAIL", 2, 0.0, f"{project_root} did not open port {ui_port}"))
                if args.fail_fast:
                    break
                continue

            cmd = [
                str(WORKSPACE_PYTHON),
                str(ui_smoke_script),
                "--base-url",
                f"http://127.0.0.1:{ui_port}/static/#/home",
                "--no-start-server",
            ]
            if "8.2" in label:
                cmd.append("--check-all-news")

            ui_step = Step(
                name=label,
                section=section,
                cwd=REPO_ROOT,
                cmd=cmd,
                note=f"Temporary server: {project_root}",
            )
            ui_result = run_cmd(ui_step)
            results.append(ui_result)
            if args.fail_fast and ui_result.status == "FAIL":
                break
        finally:
            stop_process(server)
            if temp_ini.exists():
                temp_ini.unlink(missing_ok=True)

    # Stop early if fail-fast tripped during UI checks.
    if args.fail_fast and any(r.status == "FAIL" for r in results):
        print_summary(results)
        return 1

    ex09_root = REPO_ROOT / "exercises" / "solution_ex09_rest_services"
    ex09_dir = ex09_root / "user_service"
    ex09_user_ui_dir = ex09_root / "user_ui"
    server = start_flask_server(ex09_dir, "rest_server.py", 5000)
    user_ui_server: Optional[subprocess.Popen] = None

    if not can_connect("127.0.0.1", 5001):
        user_ui_server = start_flask_server(ex09_user_ui_dir, "user_server.py", 5001)
        wait_port("127.0.0.1", 5001, timeout_s=12)

    server_started = wait_port("127.0.0.1", 5000, timeout_s=12)
    if not server_started:
        stop_process(server)
        stop_process(user_ui_server)
        print("ERROR: could not start Ex 9 local rest_server on port 5000")
        return 2

    try:
        for step in build_steps(include_external_6544=args.include_external_6544, profile=args.profile):
            result = run_cmd(step)
            if args.profile == "strict" and result.status == "SKIP":
                result = StepResult(
                    result.name,
                    result.section,
                    "FAIL",
                    99,
                    result.duration_s,
                    f"Strict profile: skip treated as failure. Original reason: {result.note}",
                )
            results.append(result)

            print("-" * 88)
            print(f"{result.status}: {result.name} (code={result.code}, {result.duration_s:.2f}s)")
            if result.note:
                print(f"note: {result.note}")

            if args.fail_fast and result.status == "FAIL":
                break
    finally:
        stop_process(server)
        stop_process(user_ui_server)
        restore_ex09_databases()

    print_summary(results)
    failed = sum(1 for result in results if result.status == "FAIL")

    print_requested_section_report(results)

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
