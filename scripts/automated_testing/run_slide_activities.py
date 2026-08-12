#!/usr/bin/env python3
"""Automated validation for the requested Course 1906 slide activities.

This runner automates as much of the slide-based material as is practical in a
local workspace. GUI-only demos that are not reliably automatable are reported
as SKIP with a reason.
"""

from __future__ import annotations

import argparse
import os
import socket
import subprocess
import sys
import tempfile
import textwrap
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional


REPO_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_PYTHON = Path(sys.executable)
AUTOMATED_TESTING_DIR = REPO_ROOT / "scripts" / "automated_testing"


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
        return StepResult(step.name, step.section, "FAIL", 127, elapsed, f"Missing file/executable: {exc}")

    elapsed = time.perf_counter() - start
    allowed_codes = step.allowed_codes if step.allowed_codes is not None else {0}
    status = "PASS" if cp.returncode in allowed_codes else "FAIL"
    note = ""
    if cp.returncode != 0 and status == "PASS":
        note = f"Non-zero exit accepted for this diagnostic step (code={cp.returncode})"
    return StepResult(step.name, step.section, status, cp.returncode, elapsed, note)


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


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        sock.listen(1)
        return int(sock.getsockname()[1])


def start_flask_server(cwd: Path, module_file: str, port: int) -> subprocess.Popen:
    code = (
        "import importlib.util; "
        f"spec=importlib.util.spec_from_file_location('srv','{module_file}'); "
        "m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); "
        f"m.app.run(debug=False, port={port})"
    )
    return subprocess.Popen(
        [str(WORKSPACE_PYTHON), '-c', code],
        cwd=cwd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


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


def print_summary(results: list[StepResult]) -> None:
    print("\n" + "#" * 88)
    print("Summary")
    print("#" * 88)
    for result in results:
        extra = f" | {result.note}" if result.note else ""
        print(f"[{result.status}] {result.name} ({result.duration_s:.2f}s){extra}")
    print("-" * 88)
    print(
        f"PASS={sum(r.status == 'PASS' for r in results)}  "
        f"FAIL={sum(r.status == 'FAIL' for r in results)}  "
        f"SKIP={sum(r.status == 'SKIP' for r in results)}"
    )


def build_steps() -> list[Step]:
    ex01 = REPO_ROOT / "exercises" / "solution_ex01_inheritance"
    ex04 = REPO_ROOT / "exercises" / "solution_ex04_debugging"
    ex05 = REPO_ROOT / "exercises" / "solution_ex05_performance"
    ex08_1 = REPO_ROOT / "exercises" / "solution_ex08_concurrency"
    ex08_2 = REPO_ROOT / "exercises" / "solution_ex08_multiprocessing"

    ch02 = REPO_ROOT / "examples" / "ch02_examples"
    ch05 = REPO_ROOT / "examples" / "ch05_examples"
    ch06 = REPO_ROOT / "examples" / "ch06_examples"
    ch07 = REPO_ROOT / "examples" / "ch07_examples"
    ch07_distribution = ch07 / "distribution_demo"
    ch07_rich_wheelhouse = ch07 / "rich_wheelhouse"
    ch08 = REPO_ROOT / "examples" / "ch08_examples"
    ch08_images_in = ch08 / "imagescale_in"
    ch09 = REPO_ROOT / "examples" / "ch09_examples" / "todo-api"

    py314 = WORKSPACE_PYTHON
    pypy = Path(r"D:\mikew\Software\pypy\pypy.exe")
    ch09_test_with_server = textwrap.dedent(
        """
        import importlib
        import socket
        import subprocess
        import sys
        import time
        import unittest

        host = '127.0.0.1'

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, 0))
            s.listen(1)
            port = s.getsockname()[1]

        def wait_port(timeout_s=10.0):
            end = time.time() + timeout_s
            while time.time() < end:
                try:
                    with socket.create_connection((host, port), timeout=0.5):
                        return True
                except OSError:
                    time.sleep(0.2)
            return False

        server = subprocess.Popen(
            [
                sys.executable,
                '-c',
                f"import rest_server_json as srv; srv.app.run(debug=False, host='{host}', port={port})",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            if not wait_port():
                raise SystemExit('REST server did not start in time')

            tests_mod = importlib.import_module('test_rest_server')
            tests_mod.base_url = f'http://{host}:{port}/todo/api/v1.0/tasks'
            suite = unittest.defaultTestLoader.loadTestsFromModule(tests_mod)
            result = unittest.TextTestRunner(verbosity=1).run(suite)
            raise SystemExit(0 if result.wasSuccessful() else 1)
        finally:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
        """
    ).strip()

    return [
        Step(
            name="Do Now slide 1-22",
            section="Do Now slide 1-22",
            cwd=ex01,
            cmd=[str(py314), "python_basics_review.py"],
            precheck=check_exists(ex01 / "python_basics_review.py", "python basics review script"),
        ),
        Step(
            name="Do Now slides 2-10 and 2-11",
            section="Do Now slides 2-10 and 2-11",
            cwd=ch02,
            cmd=[
                str(py314),
                "-c",
                textwrap.dedent(
                    """
                    import json
                    import threading
                    import urllib.parse
                    import urllib.request
                    from http.server import HTTPServer
                    import http_server

                    server = HTTPServer(('127.0.0.1', 0), http_server.AddUserFormProcessor)
                    port = server.server_port
                    thread = threading.Thread(target=server.serve_forever, daemon=True)
                    thread.start()
                    try:
                        base = f'http://127.0.0.1:{port}/adduser'
                        with urllib.request.urlopen(base + '?name=Homer&job=Chaos', timeout=5) as response:
                            assert response.status == 200
                            assert json.loads(response.read().decode('utf-8')) == {'name': 'Homer', 'job': 'Chaos'}
                        post_data = urllib.parse.urlencode({'name': 'Marge', 'job': 'Manager'}).encode('utf-8')
                        request = urllib.request.Request(base, data=post_data, method='POST')
                        with urllib.request.urlopen(request, timeout=5) as response:
                            assert response.status == 201
                            assert json.loads(response.read().decode('utf-8')) == {'name': 'Marge', 'job': 'Manager'}
                    finally:
                        server.shutdown()
                        server.server_close()
                    """
                ).strip(),
            ],
            precheck=check_exists(ch02 / "http_server.py", "chapter 2 HTTP server demo"),
        ),
        Step(
            name="Instructor demo slide 4-10",
            section="Instructor demo slide 4-10",
            cwd=REPO_ROOT,
            cmd=[str(py314), str(AUTOMATED_TESTING_DIR / "unittestgui_smoke.py"), "--exercise-dir", str(ex04)],
            precheck=check_exists(AUTOMATED_TESTING_DIR / "unittestgui_smoke.py", "unittestgui smoke script"),
        ),
        Step(
            name="Instructor demo slide 5-18",
            section="Instructor demo slide 5-18",
            cwd=ex05,
            cmd=[str(py314), "func_stats.py"],
            precheck=check_exists(ex05 / "func_stats.py", "func_stats.py"),
        ),
        Step(
            name="Verify slide 5-33 commands and timings",
            section="Verify slide 5-33 commands and timings",
            cwd=ch05,
            cmd=[
                str(py314),
                "-c",
                textwrap.dedent(
                    f"""
                    import pathlib
                    import subprocess
                    import time

                    workdir = pathlib.Path(r'{ch05}')

                    def measure(executable):
                        start = time.perf_counter()
                        cp = subprocess.run([executable, 'primes_python.py'], cwd=workdir, capture_output=True, text=True)
                        elapsed = time.perf_counter() - start
                        print(cp.stdout, end='')
                        if cp.returncode != 0:
                            print(cp.stderr)
                            raise SystemExit(cp.returncode)
                        return elapsed

                    python_elapsed = measure(r'{py314}')
                    pypy_elapsed = measure(r'{pypy}')
                    print(f'Python elapsed: {{python_elapsed:.2f}}s')
                    print(f'PyPy elapsed: {{pypy_elapsed:.2f}}s')
                    if not pypy_elapsed < python_elapsed:
                        raise SystemExit('PyPy did not run faster than Python for primes_python.py')
                    """
                ).strip(),
            ],
            precheck=check_exists(ch05 / "primes_python.py", "primes_python.py"),
        ),
        Step(
            name="Do Now slides 6-11 and 6-12",
            section="Do Now slides 6-11 and 6-12",
            cwd=ch06,
            cmd=[
                str(py314),
                "-c",
                textwrap.dedent(
                    """
                    import subprocess
                    import sys

                    cp = subprocess.run([sys.executable, 'observer.py'], capture_output=True, text=True)
                    print(cp.stdout, end='')
                    if cp.returncode != 0:
                        print(cp.stderr)
                        raise SystemExit(cp.returncode)
                    if 'observer1.update() called' not in cp.stdout or 'observer2.update() called' not in cp.stdout:
                        raise SystemExit('observer demo did not emit the expected notifications')
                    """
                ).strip(),
            ],
            precheck=check_exists(ch06 / "observer.py", "observer.py"),
        ),
        Step(
            name="Do Now slides 6-21 and 6-22",
            section="Do Now slides 6-21 and 6-22",
            cwd=ch06,
            cmd=[
                str(py314),
                "-c",
                textwrap.dedent(
                    """
                    import subprocess
                    import sys

                    cp = subprocess.run([sys.executable, '-m', 'decorators.logging_demo'], capture_output=True, text=True)
                    print(cp.stdout, end='')
                    if cp.returncode != 0:
                        print(cp.stderr)
                        raise SystemExit(cp.returncode)
                    if 'fibonacci(20, debug=True): enter' not in cp.stdout or 'nsum(1000000): exit' not in cp.stdout:
                        raise SystemExit('logging demo output missing decorator traces')
                    """
                ).strip(),
            ],
            precheck=check_exists(ch06 / "decorators" / "logging_demo.py", "logging_demo.py"),
        ),
        Step(
            name="Do Now slide 6-30",
            section="Do Now slide 6-30",
            cwd=ch06,
            cmd=[
                str(py314),
                "-c",
                textwrap.dedent(
                    """
                    import subprocess
                    import sys

                    cp = subprocess.run([sys.executable, 'image_proxy.py'], capture_output=True, text=True)
                    print(cp.stdout, end='')
                    if cp.returncode != 0:
                        print(cp.stderr)
                        raise SystemExit(cp.returncode)
                    if 'LazyLoadingImage.__init__' not in cp.stdout or 'ConcreteImage.__init__' in cp.stdout:
                        raise SystemExit('image proxy demo did not show lazy loading only')
                    """
                ).strip(),
            ],
            precheck=check_exists(ch06 / "image_proxy.py", "image_proxy.py"),
        ),
        Step(
            name="Do Now slide 7-9",
            section="Do Now slide 7-9",
            cwd=ch07,
            cmd=[
                str(py314),
                "-c",
                textwrap.dedent(
                    f"""
                    import pathlib
                    import subprocess
                    import sys
                    import tempfile

                    wheelhouse = pathlib.Path(r'{ch07_rich_wheelhouse}')
                    with tempfile.TemporaryDirectory(prefix='course1906_rich_') as tmpdir:
                        venv_dir = pathlib.Path(tmpdir) / 'venv'
                        subprocess.run([sys.executable, '-m', 'venv', str(venv_dir)], check=True)
                        py = venv_dir / 'Scripts' / 'python.exe'
                        subprocess.run([str(py), '-m', 'pip', 'install', '--no-index', '--find-links', str(wheelhouse), 'rich'], check=True)
                        cp = subprocess.run(
                            [
                                str(py),
                                '-c',
                                "from rich.console import Console; Console().print('rich install OK')",
                            ],
                            capture_output=True,
                            text=True,
                        )
                        print(cp.stdout, end='')
                        if cp.returncode != 0:
                            print(cp.stderr)
                            raise SystemExit(cp.returncode)
                    """
                ).strip(),
            ],
            precheck=check_exists(ch07_rich_wheelhouse / "rich-13.9.4-py3-none-any.whl", "rich wheelhouse"),
        ),
        Step(
            name="Instructor demo slide 7-15",
            section="Instructor demo slide 7-15",
            cwd=ch07,
            cmd=[
                str(py314),
                "-c",
                textwrap.dedent(
                    """
                    import pathlib
                    import subprocess
                    import sys
                    import tempfile

                    with tempfile.TemporaryDirectory(prefix='course1906_venv_') as tmpdir:
                        venv_dir = pathlib.Path(tmpdir) / 'new_venv'
                        subprocess.run([sys.executable, '-m', 'venv', str(venv_dir)], check=True)
                        py = venv_dir / 'Scripts' / 'python.exe'
                        cp = subprocess.run([str(py), '--version'], capture_output=True, text=True)
                        print(cp.stdout.strip() or cp.stderr.strip())
                        if cp.returncode != 0:
                            raise SystemExit(cp.returncode)
                    """
                ).strip(),
            ],
        ),
        Step(
            name="Do Now slide 7-16",
            section="Do Now slide 7-16",
            cwd=ch07,
            cmd=[
                str(py314),
                "-c",
                textwrap.dedent(
                    """
                    import pathlib
                    import subprocess
                    import sys
                    import tempfile

                    with tempfile.TemporaryDirectory(prefix='course1906_venv_create_') as tmpdir:
                        venv_dir = pathlib.Path(tmpdir) / 'new_venv'
                        subprocess.run([sys.executable, '-m', 'venv', str(venv_dir)], check=True)
                        contents = sorted(path.name for path in venv_dir.iterdir())
                        print(contents)
                        assert 'Scripts' in contents
                        assert 'Lib' in contents
                    """
                ).strip(),
            ],
        ),
        Step(
            name="Instructor demo slides 7-25 through 7-27",
            section="Instructor demo slides 7-25 through 7-27",
            cwd=ch07_distribution,
            cmd=[
                str(py314),
                "-c",
                textwrap.dedent(
                    """
                    import pathlib
                    import subprocess
                    import sys
                    import tempfile

                    project_dir = pathlib.Path.cwd()
                    with tempfile.TemporaryDirectory(prefix='course1906_dist_') as tmpdir:
                        venv_dir = pathlib.Path(tmpdir) / 'testenv'
                        subprocess.run([sys.executable, '-m', 'build'], cwd=project_dir, check=True)
                        subprocess.run([sys.executable, '-m', 'venv', str(venv_dir)], check=True)
                        py = venv_dir / 'Scripts' / 'python.exe'
                        wheel = sorted((project_dir / 'dist').glob('setup_example-*.whl'))[-1]
                        subprocess.run([str(py), '-m', 'pip', 'install', str(wheel)], check=True)
                        cp = subprocess.run([str(py), '-c', 'from setup_example.sample_mod1 import func1; func1()'], capture_output=True, text=True)
                        print(cp.stdout, end='')
                        if cp.returncode != 0:
                            print(cp.stderr)
                            raise SystemExit(cp.returncode)
                    """
                ).strip(),
            ],
            precheck=check_exists(ch07_distribution / "pyproject.toml", "distribution demo project"),
        ),
        Step(
            name="Do Now slide 8-9",
            section="Do Now slide 8-9",
            cwd=ch08,
            cmd=[str(py314), "-c", "import sys; print('Skipping GUI turtle demo automation'); raise SystemExit(0)"],
            precheck=(lambda: (False, "GUI turtle demo is intentionally skipped in automated validation")),
        ),
        Step(
            name="Do Now slide 8-28",
            section="Do Now slide 8-28",
            cwd=ch08,
            cmd=[
                str(py314),
                "-c",
                textwrap.dedent(
                    f"""
                    import pathlib
                    import subprocess
                    import sys
                    import tempfile

                    src_dir = pathlib.Path(r'{ch08_images_in}')
                    if not src_dir.exists():
                        raise SystemExit('imagescale input directory not found')
                    with tempfile.TemporaryDirectory(prefix='course1906_imagescale_') as tmpdir:
                        dest_dir = pathlib.Path(tmpdir) / 'imagescale_out'
                        cp = subprocess.run([sys.executable, 'imagescale-q-m.py', str(src_dir), str(dest_dir), '-n', '2'], capture_output=True, text=True)
                        print(cp.stdout, end='')
                        if cp.returncode != 0:
                            print(cp.stderr)
                            raise SystemExit(cp.returncode)
                        if not any(dest_dir.iterdir()):
                            raise SystemExit('imagescale demo did not create any output images')
                    """
                ).strip(),
            ],
            precheck=check_exists(ch08_images_in, "imagescale input directory"),
        ),
        Step(
            name="Do Now slide 9-8",
            section="Do Now slide 9-8",
            cwd=ch09,
            cmd=[str(py314), "-c", ch09_test_with_server],
            precheck=check_exists(ch09 / "test_rest_server.py", "todo-api integration tests"),
        ),
        Step(
            name="Do Now slides 9-27 through 9-31",
            section="Do Now slides 9-27 through 9-31",
            cwd=ch09,
            cmd=[str(py314), "-c", ch09_test_with_server],
            precheck=check_exists(ch09 / "test_rest_server.py", "todo-api integration tests"),
        ),
    ]

    return steps


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run automated checks for the requested slide activities.")
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop at the first failing step.",
    )
    return parser.parse_args()


def main() -> int:
    _ = parse_args()
    results: list[StepResult] = []
    for step in build_steps():
        result = run_cmd(step)
        results.append(result)
    print_summary(results)
    return 1 if any(result.status == "FAIL" for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())