#!/usr/bin/env python3
"""TicketManor browser smoke test.

This is the first end-to-end UI automation check for the AngularJS frontend.
It exercises the same flow used in the course setup instructions:

1. Open the TicketManor home page
2. Select `Concerts`
3. Search for `Berlin Philharmonic`
4. Verify that four results are shown

By default the script targets the `ticketmanor_webapp` service on port 6544.
It will reuse a running TicketManor server if one is already available at the
base URL. Otherwise it will start the app from the TicketManor project's
Python 3.13 virtual environment.
"""

from __future__ import annotations

import argparse
import contextlib
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
TICKETMANOR_ROOT = REPO_ROOT / "exercises" / "ticketmanor_webapp"
PSERVE_EXE = TICKETMANOR_ROOT / "venv" / "Scripts" / "pserve.exe"
DEFAULT_BASE_URL = "http://127.0.0.1:6544/static/#/home"
SEARCH_TERM = "Berlin Philharmonic"
EXPECTED_RESULTS_TEXT = "4 of 4"
EXPECTED_RESULT_COUNT = 4
MIN_NEWS_TITLES = 3


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a TicketManor UI smoke test.")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"URL to test (default: {DEFAULT_BASE_URL})",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Show the browser window instead of running headless.",
    )
    parser.add_argument(
        "--no-start-server",
        action="store_true",
        help="Fail instead of auto-starting the TicketManor server when it is not already running.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=45.0,
        help="Seconds to wait for the app to become ready (default: 45).",
    )
    parser.add_argument(
        "--check-all-news",
        action="store_true",
        help="Also verify the Concert News browser flow used by the later exercises.",
    )
    return parser.parse_args()


def probe_url(base_url: str, timeout: float = 2.0) -> bool:
    request_url = base_url.split("#", 1)[0]
    try:
        with urllib.request.urlopen(request_url, timeout=timeout) as response:
            return 200 <= response.status < 500
    except (urllib.error.URLError, TimeoutError, ValueError):
        return False


def start_server() -> subprocess.Popen[str]:
    if not PSERVE_EXE.exists():
        raise FileNotFoundError(f"TicketManor server executable not found: {PSERVE_EXE}")

    return subprocess.Popen(
        [str(PSERVE_EXE), "development.ini"],
        cwd=TICKETMANOR_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def wait_for_server(base_url: str, server_process: subprocess.Popen[str] | None, timeout: float) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if probe_url(base_url):
            return
        if server_process is not None and server_process.poll() is not None:
            output = ""
            if server_process.stdout is not None:
                output = server_process.stdout.read()
            raise RuntimeError(
                f"TicketManor server exited early with code {server_process.returncode}.\n{output}"
            )
        time.sleep(0.5)

    raise TimeoutError(f"Timed out waiting for TicketManor to start at {base_url}")


def run_ui_check(base_url: str, headed: bool, check_all_news: bool = False) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=not headed)
        page = browser.new_page(viewport={"width": 1440, "height": 1080})
        try:
            page.goto(base_url, wait_until="domcontentloaded")
            page.locator(".event-pill", has_text="Concerts").first.click()
            page.get_by_role("textbox", name="Which Artist do you want?").fill(SEARCH_TERM)
            page.get_by_role("button", name="Search").click()

            page.get_by_text("Search results").first.wait_for(state="visible", timeout=10_000)
            result_cards = page.locator(".scroll-container .thumbnail.pull-center")
            pages_label = page.locator(".pages").first

            result_count = result_cards.count()
            pages_text = pages_label.inner_text().strip()
            full_text = page.locator("body").inner_text()

            if result_count != EXPECTED_RESULT_COUNT:
                raise AssertionError(
                    f"Expected {EXPECTED_RESULT_COUNT} result cards, found {result_count}."
                )
            if EXPECTED_RESULTS_TEXT not in pages_text:
                raise AssertionError(
                    f"Expected paging text '{EXPECTED_RESULTS_TEXT}', got '{pages_text}'."
                )
            if SEARCH_TERM not in full_text:
                raise AssertionError(f"Expected to find '{SEARCH_TERM}' in the page results.")

            print(f"PASS: UI search for '{SEARCH_TERM}' returned {result_count} results ({pages_text}).")

            if check_all_news:
                page.get_by_role("heading", name="Concert News").wait_for(state="visible", timeout=10_000)

                news_titles = page.locator(".news-title")
                news_titles.first.wait_for(state="visible", timeout=10_000)
                title_count = news_titles.count()
                if title_count < MIN_NEWS_TITLES:
                    raise AssertionError(
                        f"Expected at least {MIN_NEWS_TITLES} news titles in the Concert News section, found {title_count}."
                    )

                print(f"PASS: Concert News section loaded with {title_count} visible news titles.")
        finally:
            browser.close()


def main() -> int:
    args = parse_args()
    server_process: subprocess.Popen[str] | None = None

    try:
        if probe_url(args.base_url):
            print(f"Using existing TicketManor server at {args.base_url}")
        elif args.no_start_server:
            print(f"ERROR: TicketManor is not running at {args.base_url}")
            return 1
        else:
            print(f"Starting TicketManor server from {TICKETMANOR_ROOT}")
            server_process = start_server()
            wait_for_server(args.base_url, server_process, args.timeout)

        run_ui_check(args.base_url, args.headed, args.check_all_news)
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
