#!/usr/bin/env python3
"""Compatibility wrapper for the slide activity runner.

The old filename is kept so existing notes and links still work.
"""

from __future__ import annotations

from run_slide_activities import main


if __name__ == "__main__":
    raise SystemExit(main())