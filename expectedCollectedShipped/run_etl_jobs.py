#!/usr/bin/env python3
"""Utility entrypoint for running the expected/collected ETL scripts under SSIS.

The wrapper centralizes logging, exit code handling, and sequential execution so
SQL Agent can monitor success/failure via a single Execute Process Task.
"""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

BASE_DIR = Path(__file__).resolve().parent
SCRIPT_MAP = {
    "expected": BASE_DIR / "expectedCollected_v1.py",
    "collected": BASE_DIR / "collectedShipped_v1.py",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one or both ETL scripts")
    parser.add_argument(
        "--scripts",
        choices=["expected", "collected", "both"],
        default="both",
        help="Which script(s) to execute",
    )
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="Python interpreter to use (default: current interpreter)",
    )
    parser.add_argument(
        "--log-dir",
        default=str(BASE_DIR / "logs"),
        help="Directory for wrapper logs",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=0,
        help="Optional timeout per script in seconds (0 = no timeout)",
    )
    return parser.parse_args()


def configure_logging(log_dir: Path) -> Path:
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    log_path = log_dir / f"etl_job_{timestamp}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_path, encoding="utf-8"),
        ],
    )
    logging.info("Logging to %s", log_path)
    return log_path


def run_command(cmd: List[str], timeout: int) -> None:
    logging.info("Running command: %s", " ".join(cmd))
    try:
        completed = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            timeout=None if timeout == 0 else timeout,
        )
    except subprocess.CalledProcessError as exc:
        logging.error("Script failed with exit code %s", exc.returncode)
        if exc.stdout:
            logging.error("STDOUT:\n%s", exc.stdout)
        if exc.stderr:
            logging.error("STDERR:\n%s", exc.stderr)
        raise
    except subprocess.TimeoutExpired:
        logging.error("Timeout reached; terminating command")
        raise
    else:
        if completed.stdout:
            logging.info("STDOUT:\n%s", completed.stdout)
        if completed.stderr:
            logging.warning("STDERR:\n%s", completed.stderr)


def expand_scripts(selection: str) -> Iterable[Path]:
    if selection == "both":
        return [SCRIPT_MAP["expected"], SCRIPT_MAP["collected"]]
    return [SCRIPT_MAP[selection]]


def main() -> int:
    args = parse_args()
    log_dir = Path(args.log_dir)
    configure_logging(log_dir)

    scripts = expand_scripts(args.scripts)
    failures = []

    for script_path in scripts:
        if not script_path.exists():
            logging.error("Script not found: %s", script_path)
            failures.append(script_path.name)
            continue
        cmd = [args.python, str(script_path)]
        try:
            run_command(cmd, args.timeout)
        except Exception:
            failures.append(script_path.name)

    if failures:
        logging.error("%s script(s) failed: %s", len(failures), ", ".join(failures))
        return 1

    logging.info("All requested scripts completed successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
