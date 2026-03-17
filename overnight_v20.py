#!/usr/bin/env python3
"""
ORCA v20 — Overnight Learning CLI Entrypoint.

Usage:
    python overnight_v20.py                   # standard nightly replay
    python overnight_v20.py --deep-review     # weekly deep review (premium models)
    python overnight_v20.py --dry-run         # no writes, no sends
    python overnight_v20.py --verbose         # debug logging

Schedule:
    Nightly: 8:00 PM CT (cron: 0 20 * * *)
    Weekly:  Sunday 6:00 PM CT (cron: 0 18 * * 0)
"""

import argparse
import logging
import os
import sys
from datetime import datetime, timezone

_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# Load .env file (Telegram, X, EIA, Google Sheets, etc.)
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(_PROJECT_ROOT, ".env"))
except ImportError:
    pass  # dotenv optional — env vars must be set externally

from orca_v20.config import FLAGS, THRESHOLDS
from orca_v20.db_bootstrap import bootstrap_db
from orca_v20.run_context import ResearchMode, RunContext, SourceMode
from orca_v20.overnight import run_overnight


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    fmt = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
    logging.basicConfig(level=level, format=fmt, datefmt="%H:%M:%S")
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


logger = logging.getLogger("orca_v20.overnight_cli")


def main() -> None:
    parser = argparse.ArgumentParser(description="ORCA v20 Overnight Learning")
    parser.add_argument("--deep-review", action="store_true",
                        help="Enable premium Layer 3 deep review")
    parser.add_argument("--dry-run", action="store_true",
                        help="Skip all writes and notifications")
    parser.add_argument("--verbose", action="store_true",
                        help="Debug-level logging")
    args = parser.parse_args()

    setup_logging(verbose=args.verbose)

    ctx = RunContext(
        research_mode=ResearchMode.STANDARD,
        source_mode=SourceMode.MINIMAL,
        dry_run=args.dry_run,
        verbose=args.verbose,
        max_api_cost_usd=THRESHOLDS.overnight_hard_budget_usd,
    )

    now = ctx.as_of_utc
    ctx.market_date = now.strftime("%Y-%m-%d")

    bootstrap_db()

    summary = run_overnight(ctx, deep_review=args.deep_review)

    logger.info(f"Overnight complete. Summary: {summary}")
    sys.exit(0)


if __name__ == "__main__":
    main()
