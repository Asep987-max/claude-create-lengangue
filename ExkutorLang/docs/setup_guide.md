# ExkutorLang Setup Guide

## Prerequisites

- **Host OS**: Windows 11 (for production execution) or Linux (for logic testing/development).
- **Python**: 3.11+
- **C++ Compiler**: MSVC 2022 (Windows) or GCC/Clang (Linux). C++17 support required.
- **CMake**: 3.20+
- **WSL2**: Ubuntu/Debian distribution (Windows only).
- **PowerShell**: 7.4+ (Windows only).

## Installation

1.  **Clone the Repository**:
    ```bash
    git clone <repo_url>
    cd ExkutorLang
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Build the C++ Core**:
    ```bash
    python build.py
    ```
    This compiles the `exkutor_core` library and `exkutor_core_binding` Python extension.

4.  **Verify Build**:
    Run the test suite:
    ```bash
    python tests/run_tests.py
    ```

## Linux Compatibility Mode

ExkutorLang includes a **Linux Compatibility Mode** for development and CI environments where Windows 11 is not available.

- **Behavior**:
    - `wsl` target maps to local `bash`.
    - `powershell` target maps to local `pwsh` (if available) or stubs specific test commands.
    - `assert_exists` uses native Linux file checks.
- **Indication**:
    - `run_tests.py` output will append `(linux-compat-mode)` to passed tests.
    - Logs may contain `[linux-compat-mock]` entries.

**Note**: Production use requires a Windows 11 host to interact with actual WSL2 and PowerShell environments.

## Troubleshooting

- **ImportError: No module named exkutor_core_binding**: Ensure `build.py` succeeded and the `.so` (Linux) or `.pyd` (Windows) file is in the `ExkutorLang` root directory or `PYTHONPATH`.
- **CMake Error**: Ensure CMake 3.20+ is installed and in PATH.
- **Sanitizer Rejection**: Check `docs/syntax_reference.md` for allowed characters.
