#!/usr/bin/env python3
"""Browser smoke automation for the Exercise 5.1 SnakeViz workflow.

This script starts a local SnakeViz server for a profiling file, opens the page
in a browser via Playwright, and verifies that the profile graph is visible.
It does not attempt to interpret the graph or table contents.
"""

from __future__ import annotations

import argparse
import contextlib
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PROFILE = REPO_ROOT / "exercises" / "solution_ex05_performance" / "sudoku.prof"
DEFAULT_WORK_DIR = DEFAULT_PROFILE.parent
WORKSPACE_PYTHON = Path(sys.executable)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a SnakeViz graph-presence smoke test.")
    parser.add_argument(
        "--profile-path",
        default=str(DEFAULT_PROFILE),
        help="Path to the .prof file to visualize.",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host interface for the SnakeViz server.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8087,
        help="Preferred port for the SnakeViz server.",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Show the browser window instead of running headless.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Seconds to wait for the server and page to load.",
    )
    return parser.parse_args()


def can_connect(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def choose_port(host: str, preferred_port: int) -> int:
    if not can_connect(host, preferred_port, timeout=0.25):
        return preferred_port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return int(sock.getsockname()[1])


def ensure_profile_exists(profile_path: Path) -> None:
    if profile_path.exists():
        return

    work_dir = profile_path.parent
    subprocess.run(
        [str(WORKSPACE_PYTHON), "-m", "cProfile", "-o", str(profile_path), "sudoku.py", "sudoku_input.txt"],
        cwd=work_dir,
        check=True,
    )


def start_server(profile_path: Path, host: str, port: int) -> subprocess.Popen[str]:
    return subprocess.Popen(
        [str(WORKSPACE_PYTHON), "-m", "snakeviz", "-s", "-H", host, "-p", str(port), str(profile_path)],
        cwd=profile_path.parent,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def wait_for_server(url: str, server_process: subprocess.Popen[str], timeout: float) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1.5) as response:
                if response.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError, ValueError):
            pass

        if server_process.poll() is not None:
            output = ""
            if server_process.stdout is not None:
                output = server_process.stdout.read()
            raise RuntimeError(
                f"SnakeViz server exited early with code {server_process.returncode}.\n{output}"
            )
        time.sleep(0.25)

    raise TimeoutError(f"Timed out waiting for SnakeViz to start at {url}")


def run_browser_check(url: str, headed: bool) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=not headed)
        page = browser.new_page(viewport={"width": 1440, "height": 1080})
        try:
            page.goto(url, wait_until="domcontentloaded")
            page.get_by_role("heading", name="SnakeViz").wait_for(state="visible", timeout=10_000)
            page.get_by_role("button", name="Call Stack").wait_for(state="visible", timeout=10_000)

            graph = page.locator("img, svg, canvas").first
            graph.wait_for(state="visible", timeout=10_000)

            print("PASS: SnakeViz page loaded and a graph element is visible in the browser.")
        finally:
            browser.close()


def main() -> int:
    args = parse_args()
    profile_path = Path(args.profile_path).resolve()

    try:
        ensure_profile_exists(profile_path)
    except Exception as exc:
        print(f"ERROR: could not prepare profile file: {exc}")
        return 1

    if not profile_path.exists():
        print(f"ERROR: profile file not found: {profile_path}")
        return 1

    port = choose_port(args.host, args.port)
    encoded_profile = urllib.parse.quote(str(profile_path))
    url = f"http://{args.host}:{port}/snakeviz/{encoded_profile}"
    server_process: subprocess.Popen[str] | None = None

    try:
        server_process = start_server(profile_path, args.host, port)
        wait_for_server(url, server_process, args.timeout)
        run_browser_check(url, args.headed)
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1
    finally:
        if server_process is not None and server_process.poll() is None:
            with contextlib.suppress(Exception):
                server_process.terminate()
                server_process.wait(timeout=10)


if __name__ == "__main__":
    raise SystemExit(main())
