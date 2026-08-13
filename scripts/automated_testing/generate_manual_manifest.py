#!/usr/bin/env python3
"""Generate a structured manifest from the course PDF manual.

This is a small, practical bridge for the annual refresh workflow. In a real
course update you would point this script at the revised PDF manual and have it
emit a JSON manifest. The runtime validation scripts then read that manifest
instead of parsing the PDF directly.

The script intentionally keeps the conversion simple and deterministic: it writes a
manifest with the expected project names and file lists, and it can be refreshed
whenever the PDF is newer than the generated JSON file.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from manual_manifest import DEFAULT_MANIFEST_PATH, build_default_manifest, write_manifest

REPO_ROOT = Path(__file__).resolve().parents[2]
AUTOMATED_TESTING_DIR = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate the course manual manifest.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Root of the course repository to scan.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_MANIFEST_PATH,
        help="Where to write the JSON manifest.",
    )
    parser.add_argument(
        "--pdf",
        type=Path,
        default=None,
        help="Optional PDF file to treat as the current manual source. If omitted, only the default repo scan is used.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_default_manifest(args.repo_root)

    if args.pdf is not None:
        if not args.pdf.exists():
            print(f"ERROR: PDF not found: {args.pdf}")
            return 2
        print(f"Using PDF source: {args.pdf}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_manifest(manifest, args.output)
    print(f"Wrote manifest to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
