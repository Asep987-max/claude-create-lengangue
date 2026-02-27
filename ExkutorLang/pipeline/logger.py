"""
Unified Logger for ExkutorLang.
Handles structured logging to file and human-readable output to stdout.
"""

import sys
import json
import os
import datetime
# Fix path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from pipeline.error_types import ExkutorError

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
LOG_FILE = os.path.join(LOG_DIR, "exkutor_runtime.log")

def _ensure_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def _get_timestamp():
    return datetime.datetime.now().isoformat()

def log_error(error: ExkutorError) -> None:
    _ensure_log_dir()
    if not error.timestamp:
        error.timestamp = _get_timestamp()
    error_dict = error.to_dict()
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(error_dict) + "\n")
    except Exception as e:
        sys.stderr.write(f"CRITICAL: Failed to write to log file: {e}\n")
    print(f"ERROR: {error}", file=sys.stdout)
    if error.raw_stderr:
        print(f"  Details: {error.raw_stderr}", file=sys.stdout)

def log_info(message: str, target: str = "") -> None:
    _ensure_log_dir()
    entry = {"level": "INFO", "message": message, "target": target, "timestamp": _get_timestamp()}
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        sys.stderr.write(f"CRITICAL: Failed to write to log file: {e}\n")
    target_str = f" [{target}]" if target else ""
    print(f"INFO{target_str}: {message}", file=sys.stdout)
