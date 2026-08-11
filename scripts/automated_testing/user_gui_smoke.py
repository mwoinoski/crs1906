#!/usr/bin/env python3
"""Tk widget smoke automation for Exercise 9.1.

This drives the desktop user-management GUI programmatically through its real
widgets and verifies the add, load, update, and delete workflow against the
local REST service on port 5001.
"""

from __future__ import annotations

import argparse
import contextlib
import shutil
import sys
import time
from pathlib import Path

import requests
import tkinter as tk
from tkinter import messagebox

REPO_ROOT = Path(__file__).resolve().parents[2]
BASE_URL = "http://127.0.0.1:5001/rest/users"
CREDS = ("admin", "adminpw")
TEMP_DB_NAME = "test_db_gui.sqlite"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Tk smoke automation for Exercise 9.1.")
    parser.add_argument(
        "--ex09-root",
        default=str(REPO_ROOT / "exercises" / "solution_ex09_rest_services"),
        help="Exercise 9.1 root directory containing user_service and user_ui",
    )
    return parser.parse_args()


def wait_for(root: tk.Tk, predicate, timeout: float = 3.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        root.update()
        if predicate():
            return
        time.sleep(0.02)
    root.update()
    assert predicate()


def find_listbox_index(app, text: str) -> int | None:
    for idx in range(app.listbox.size()):
        if text in app.listbox.get(idx):
            return idx
    return None


def cleanup_root(root: tk.Tk) -> None:
    for child in list(root.winfo_children()):
        with contextlib.suppress(tk.TclError):
            child.destroy()


def prepare_test_db(source_db_path: Path, temp_db_path: Path) -> None:
    shutil.copy(source_db_path, temp_db_path)
    response = requests.patch(BASE_URL, auth=CREDS, params={"db_file": TEMP_DB_NAME}, timeout=10)
    response.raise_for_status()


def restore_db(user_service_db_path: Path, user_ui_db_path: Path, temp_db_path: Path) -> None:
    try:
        requests.patch(BASE_URL, auth=CREDS, timeout=10)
    except Exception:
        pass

    for db_path in (user_service_db_path, user_ui_db_path):
        backup_path = db_path.parent / f"{db_path.name}.backup"
        if backup_path.exists():
            shutil.copy2(backup_path, db_path)

    temp_db_path.unlink(missing_ok=True)


def main() -> int:
    args = parse_args()
    ex09_root = Path(args.ex09_root).resolve()
    user_ui_dir = ex09_root / "user_ui"
    user_service_dir = ex09_root / "user_service"
    temp_db_path = user_ui_dir / TEMP_DB_NAME
    source_db_path = user_service_dir / "test_db_with_miles.sqlite"
    user_service_db_path = user_service_dir / "users_db.sqlite"
    user_ui_db_path = user_ui_dir / "users_db.sqlite"

    root = tk.Tk()
    root.withdraw()
    errors: list[str] = []

    def fail_dialog(title: str, message: str) -> None:
        errors.append(f"{title}: {message}")

    messagebox.showerror = fail_dialog
    messagebox.askyesno = lambda *args, **kwargs: True

    try:
        prepare_test_db(source_db_path, temp_db_path)

        if str(user_ui_dir) not in sys.path:
            sys.path.insert(0, str(user_ui_dir))
        import user_gui

        cleanup_root(root)
        app = user_gui.UserApp(root)
        wait_for(root, lambda: app.listbox.size() >= 1)
        initial_count = app.listbox.size()

        email = "ada.lovelace@example.com"
        app.first_name_var.set("Ada")
        app.middles_var.set("Augusta")
        app.last_name_var.set("Lovelace")
        app.email_var.set(email)
        app.street_var.set("12 Analytical Engine Way")
        app.city_var.set("London")
        app.state_var.set("LN")
        app.post_code_var.set("A100")
        app.country_var.set("UK")
        app.save_record()

        wait_for(root, lambda: find_listbox_index(app, email) is not None)
        assert app.listbox.size() == initial_count + 1

        idx = find_listbox_index(app, email)
        assert idx is not None
        app.listbox.selection_clear(0, tk.END)
        app.listbox.selection_set(idx)
        app.load_selected_record()

        assert app.first_name_var.get() == "Ada"
        assert app.last_name_var.get() == "Lovelace"
        assert app.city_var.get() == "London"

        app.middles_var.set("Byron")
        app.city_var.set("Oxford")
        app.save_record()
        wait_for(root, lambda: app.status_var.get().startswith("Loaded"))

        idx = find_listbox_index(app, email)
        assert idx is not None
        app.listbox.selection_clear(0, tk.END)
        app.listbox.selection_set(idx)
        app.load_selected_record()

        assert app.middles_var.get() == "Byron"
        assert app.city_var.get() == "Oxford"

        app.delete_selected_record()
        wait_for(root, lambda: find_listbox_index(app, email) is None)
        assert app.listbox.size() == initial_count

        if errors:
            raise AssertionError("Unexpected GUI error dialogs: " + " | ".join(errors))

        print("PASS: Tk desktop user workflow add/load/update/delete completed successfully.")
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1
    finally:
        restore_db(user_service_db_path, user_ui_db_path, temp_db_path)
        cleanup_root(root)
        with contextlib.suppress(Exception):
            root.destroy()


if __name__ == "__main__":
    raise SystemExit(main())
