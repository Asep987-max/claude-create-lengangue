import sys
import os
import subprocess
import time
import json
import shutil

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEST_DIR = os.path.join(PROJECT_ROOT, "tests")
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
LOG_FILE = os.path.join(LOG_DIR, "exkutor_runtime.log")
SENTINEL_FILE = os.path.join(LOG_DIR, "tests_passed.sentinel")
EXKUTOR_PY = os.path.join(PROJECT_ROOT, "exkutor.py")

TESTS = [
    ("WSL Basic IO", os.path.join(TEST_DIR, "wsl", "test_basic_io.exkutor")),
    ("WSL File Ops", os.path.join(TEST_DIR, "wsl", "test_file_ops.exkutor")),
    ("WSL Chained", os.path.join(TEST_DIR, "wsl", "test_chained.exkutor")),
    ("PowerShell Basic IO", os.path.join(TEST_DIR, "powershell", "test_basic_io.exkutor")),
    ("PowerShell File Ops", os.path.join(TEST_DIR, "powershell", "test_file_ops.exkutor")),
    ("PowerShell Chained", os.path.join(TEST_DIR, "powershell", "test_chained.exkutor")),
]

def run_exkutor(script_path):
    env = os.environ.copy()
    env["PYTHONPATH"] = PROJECT_ROOT
    cmd = [sys.executable, EXKUTOR_PY, script_path]
    return subprocess.run(cmd, capture_output=True, text=True, env=env)

def get_last_error():
    if not os.path.exists(LOG_FILE): return None
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            for line in reversed(lines):
                try:
                    entry = json.loads(line)
                    if "error_type" in entry: return entry
                except: continue
    except: pass
    return None

def main():
    print("Starting ExkutorLang Test Suite execution...")
    if not os.path.exists(LOG_DIR): os.makedirs(LOG_DIR)
    if os.path.exists(SENTINEL_FILE): os.remove(SENTINEL_FILE)

    is_linux = (sys.platform != "win32")
    all_passed = True

    for name, path in TESTS:
        print(f"RUNNING: {name}")
        if not os.path.exists(path):
            print(f"FAILED: Test file not found: {path}")
            all_passed = False
            break

        result = run_exkutor(path)

        if result.returncode == 0:
            suffix = " (linux-compat-mode)" if is_linux else ""
            print(f"PASSED{suffix}: {name}")
        else:
            print(f"FAILED: {name}")
            print(f"STDOUT:\n{result.stdout}")
            print(f"STDERR:\n{result.stderr}")
            last = get_last_error()
            if last: print(f"DIAGNOSTIC: Last error: {json.dumps(last, indent=2)}")

            print("Retrying once...")
            result = run_exkutor(path)
            if result.returncode == 0:
                print(f"PASSED (on retry){suffix if is_linux else ''}: {name}")
            else:
                print(f"FAILED (retry): {name}")
                all_passed = False
                break

    if all_passed:
        print("ALL TESTS PASSED. ExkutorLang v1.0 is ready.")
        with open(SENTINEL_FILE, "w") as f: f.write("PASSED")
        sys.exit(0)
    else:
        print("Test suite failed.")
        sys.exit(1)

if __name__ == "__main__": main()
