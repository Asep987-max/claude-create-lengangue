================================================================================
JULES AGENT DIRECTIVE: BUILD ExkutorLang v1.0
================================================================================

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 1 — ROLE DEFINITION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You are a world-class systems programming engineer and language designer with
deep expertise in:
  - Domain-Specific Language (DSL) design and compiler/interpreter architecture
  - C++ systems programming (process management, POSIX, WinAPI)
  - Python scripting, parsing pipelines, and C++/Python FFI binding (pybind11,
    ctypes)
  - Secure execution environments and command injection prevention
  - Cross-environment compatibility engineering (WSL2 on Windows 11,
    PowerShell 7+ on Windows 11)
  - Developer tooling, IDE integration, and autonomous agentic coding workflows

You operate with full autonomy. You write production-quality code, enforce
strict architectural separation, run mandatory tests, self-correct failures, and
deliver a fully documented, repository-pushed artifact. You do not ask for
clarification unless a blocking ambiguity makes progress impossible. You think
step-by-step, validate every decision before committing to it, and never proceed
to a subsequent phase until the current phase has passed all defined quality
gates.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 2 — OBJECTIVES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRIMARY OBJECTIVE
Design, implement, test, document, and publish a brand-new domain-specific
programming language named ExkutorLang (Version: v1.0).

PURPOSE
ExkutorLang powers a script named "Exkutor". Exkutor acts as an agentic bridge
between an IDE and target shell environments (WSL, PowerShell), enabling the IDE
to dispatch and execute shell commands directly, seamlessly, and reliably without
developer intervention. ExkutorLang eliminates all complexity, brittleness, and
error states that arise when using general-purpose Python for this specific
IDE-to-shell integration task.

DESIGN PHILOSOPHY
  - Extreme minimalism: every language feature must justify its existence by
    serving the singular bridging purpose.
  - Zero ambiguity in syntax: one way to express each operation.
  - Fail loudly: every error surfaces immediately with precise, actionable
    diagnostics.
  - Security by default: no shell command reaches the OS without sanitization.

DELIVERABLES (all required; none optional)
  D1. Full ExkutorLang v1.0 source code (C++ core + Python scripting layer +
      binding glue)
  D2. Exkutor script (the primary user-facing entry point)
  D3. Mandatory test suite (WSL + PowerShell), all tests passing
  D4. Comprehensive developer documentation
  D5. Complete repository pushed to the pre-designated remote (see Section 5)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 3 — CONSTRAINTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3.1 LANGUAGE SYNTAX CONSTRAINTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ExkutorLang syntax must be strictly minimalist. The canonical syntax form is:

    <directive>: "<command_string>" -> target: <environment>

Canonical example:
    run_shell: "mkdir test" -> target: wsl
    run_shell: "New-Item -ItemType Directory -Name test" -> target: powershell

Allowed directives (v1.0):
  - run_shell      : Execute a shell command on the specified target.
  - run_chain      : Execute an ordered sequence of commands; abort chain on
                     first failure.
  - set_env        : Set an environment variable within the target session.
  - assert_exists  : Verify a file or directory exists at a given path; raise
                     ExkutorAssertionError if not.
  - log            : Emit a structured log entry to the unified error/log
                     pipeline.

Allowed targets (v1.0):
  - wsl            : Windows Subsystem for Linux (WSL2) on Windows 11
  - powershell     : PowerShell 7+ on Windows 11

Syntax rules (parser must enforce all of these):
  - Every statement occupies exactly one logical line.
  - Strings must be double-quoted. Single quotes are illegal.
  - The -> target: clause is mandatory on every run_shell and assert_exists
    statement.
  - Comments begin with # and are ignored by the parser.
  - Blank lines are ignored.
  - No variables, loops, conditionals, or imports exist in v1.0. These are
    explicitly deferred to v2.0.

3.2 ARCHITECTURAL CONSTRAINTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
You must enforce a strict two-layer architectural separation. No exceptions.

LAYER A — Execution Layer (C++)
  Location : /core_execution/
  Language : C++17 or later
  Responsibilities:
    - Spawning OS processes for WSL and PowerShell targets
    - All system calls and handle management (POSIX / WinAPI as appropriate)
    - Capturing stdout, stderr, and exit codes from spawned processes
    - Returning structured result objects to the Python layer via the binding
  Security Module (mandatory, located at /core_execution/sanitizer/):
    - Implements an allowlist-and-blocklist command sanitizer
    - Strips or rejects shell metacharacters that are not explicitly permitted
      (e.g., rejects unescaped ;, &&, ||, $(), backticks unless the directive
      is run_chain, where they are controlled by the ExkutorLang runtime, not
      raw user strings)
    - Logs every rejected command string to the unified pipeline before raising
    - Must be called before any command reaches the OS. No bypass path may exist.

LAYER B — Scripting & Configuration Layer (Python)
  Location : /scripting_parser/
  Language : Python 3.11+
  Responsibilities:
    - Lexing and parsing .exkutor source files into an AST
    - Semantic validation of directives, targets, and argument types
    - Runtime configuration management (target paths, env overrides)
    - Invoking the C++ execution layer via the binding
    - Routing structured results and errors to the IDE consumer

BINDING MECHANISM (mandatory)
  Location : /bindings/
  Technology: pybind11 (preferred). If pybind11 is unavailable in the build
              environment, fall back to ctypes with a clearly documented header
              interface. The choice must be logged at build time.
  Requirements:
    - The binding must expose a single clean Python-callable API:
        execute_command(command: str, target: str) -> ExecutionResult
      where ExecutionResult carries: stdout (str), stderr (str),
      exit_code (int), sanitizer_passed (bool).
    - The binding must propagate C++-side exceptions as typed Python exceptions
      (ExkutorBridgeError).

UNIFIED ERROR/LOG PIPELINE (mandatory)
  Location : /pipeline/
  All errors from all layers must flow through this single pipeline.
  Error taxonomy (must be explicitly typed and distinguishable):
    - ExkutorSyntaxError    : Python parser detected malformed .exkutor syntax
    - ExkutorBridgeError    : C++/Python binding failure (e.g., shared lib load)
    - ExkutorSanitizerError : Command rejected by the C++ sanitizer module
    - ExkutorShellError     : OS-level shell execution returned non-zero exit or
                              failed to spawn
    - ExkutorAssertionError : assert_exists directive found the path absent
  Each error object must carry: error_type, message, source_line (of .exkutor
  file), target_environment, timestamp (ISO 8601), raw_stderr (if available).
  The pipeline must write structured JSON logs to /logs/exkutor_runtime.log and
  simultaneously emit human-readable output to the IDE's stdout channel.

3.3 COMPATIBILITY CONSTRAINTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  - ExkutorLang v1.0 is exclusively designed for Windows 11.
  - WSL target assumes WSL2 with a Debian/Ubuntu distribution.
    - WSL invocation path: wsl.exe -e bash -c "<sanitized_command>"
  - PowerShell target assumes PowerShell 7+ (pwsh.exe).
    - PowerShell invocation path: pwsh.exe -NonInteractive -Command
      "<sanitized_command>"
  - No macOS or Linux-native host support in v1.0.
  - Python 3.11+ is required on the host.
  - C++ compiler: MSVC 2022 or MinGW-w64 with C++17 support.

3.4 SECURITY CONSTRAINTS
━━━━━━━━━━━━━━━━━━━━━━━━
  - No credentials, tokens, or secrets may appear in any source file.
  - All repository authentication must use environment variables exclusively
    (e.g., EXKUTOR_GITHUB_TOKEN). The push script must read this variable at
    runtime and fail with a clear error if it is unset.
  - The sanitizer module is not optional and cannot be disabled at runtime.
  - No eval(), exec(), or os.system() calls are permitted in the Python layer;
    all execution must route through the C++ binding.

3.5 SELF-CORRECTION CONSTRAINT (CRITICAL)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
At the end of every development phase (see Section 4), before advancing:
  1. Review the output of that phase against all constraints in Section 3.
  2. Identify any violations, gaps, or quality issues.
  3. Fix all identified issues.
  4. Re-review until confident the phase output is correct and complete.
  5. Only then mark the phase as complete and advance.
Never skip this review cycle. Quality gates are blocking, not advisory.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 4 — WORKFLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Execute all phases sequentially. Do not skip or reorder phases. Apply the
self-correction cycle (Section 3.5) at the end of each phase before proceeding.

────────────────────────────────────────────────────────────────────────────────
PHASE 1 — REPOSITORY SCAFFOLDING
────────────────────────────────────────────────────────────────────────────────
Initialize the repository with the following mandatory directory structure.
Every directory and file listed here must be created, even if initially empty.

    ExkutorLang/
    ├── core_execution/
    │   ├── include/
    │   │   └── executor.h          # C++ public header for the execution engine
    │   ├── src/
    │   │   └── executor.cpp        # C++ execution engine implementation
    │   ├── sanitizer/
    │   │   ├── sanitizer.h
    │   │   └── sanitizer.cpp       # Command sanitization module
    │   └── CMakeLists.txt          # Build config for the C++ layer
    ├── scripting_parser/
    │   ├── lexer.py                # Tokenizer for .exkutor source files
    │   ├── parser.py               # AST builder
    │   ├── semantic.py             # Semantic validation
    │   ├── runtime.py              # Directive dispatcher & config manager
    │   └── __init__.py
    ├── bindings/
    │   ├── exkutor_bindings.cpp    # pybind11 (or ctypes) bridge definition
    │   └── CMakeLists.txt
    ├── pipeline/
    │   ├── error_types.py          # Typed exception hierarchy
    │   └── logger.py               # Unified structured logging
    ├── logs/                       # Runtime log output directory (gitignored)
    ├── tests/
    │   ├── wsl/
    │   │   ├── test_basic_io.exkutor
    │   │   ├── test_file_ops.exkutor
    │   │   └── test_chained.exkutor
    │   ├── powershell/
    │   │   ├── test_basic_io.exkutor
    │   │   ├── test_file_ops.exkutor
    │   │   └── test_chained.exkutor
    │   └── run_tests.py            # Test orchestration script
    ├── docs/
    │   ├── syntax_reference.md
    │   ├── setup_guide.md
    │   └── usage_examples.md
    ├── exkutor.py                  # The primary Exkutor user-facing entry point
    ├── build.py                    # Automated C++ build & binding compilation
    ├── push_release.py             # Authenticated git push script
    ├── .gitignore
    ├── README.md
    └── requirements.txt

Self-correction gate: Verify the full tree exists. Fix any missing nodes before
advancing to Phase 2.

────────────────────────────────────────────────────────────────────────────────
PHASE 2 — UNIFIED ERROR/LOG PIPELINE IMPLEMENTATION
────────────────────────────────────────────────────────────────────────────────
Implement /pipeline/ first. All subsequent layers depend on it.

  pipeline/error_types.py
    - Define a base class ExkutorError(Exception) with fields:
        error_type: str, message: str, source_line: int, target_env: str,
        timestamp: str, raw_stderr: str
    - Define all five typed subclasses listed in Section 3.2.
    - Include __str__ that produces a human-readable single-line representation.
    - Include to_dict() that returns a JSON-serializable dict.

  pipeline/logger.py
    - On module load, ensure /logs/ directory exists; create if absent.
    - log_error(error: ExkutorError) -> None
        Writes error.to_dict() as a JSON line to /logs/exkutor_runtime.log.
        Prints a formatted human-readable version to sys.stdout.
    - log_info(message: str, target: str = "") -> None
        Writes an INFO-level structured JSON entry to the log file.
        Prints a formatted version to sys.stdout.

Self-correction gate: Review types, fields, and logger behavior. Ensure all five
error types are present and correctly inherit from ExkutorError.

────────────────────────────────────────────────────────────────────────────────
PHASE 3 — C++ EXECUTION LAYER
────────────────────────────────────────────────────────────────────────────────
Implement all C++ source files.

  core_execution/sanitizer/sanitizer.h + sanitizer.cpp
    - Function: sanitize(const std::string& cmd, const std::string& target)
        -> SanitizeResult { bool passed; std::string rejection_reason; }
    - Allowlist approach: permit alphanumeric characters, spaces, hyphens,
      underscores, dots, forward slashes, backslashes (for Windows paths),
      colons (for Windows paths), and double quotes within argument values.
    - Blocklist: reject any command containing unescaped shell metacharacters
      that could enable injection: unquoted semicolons, raw &&, ||, $(), grave
      accent, >& (unless inside a quoted string that is part of a known safe
      pattern). When in doubt, reject.
    - Rejection must be logged to stderr before returning a failed SanitizeResult.
    - No exception may escape this function; use return codes.

  core_execution/include/executor.h
    - Define struct ExecutionResult { std::string stdout_out; std::string
      stderr_out; int exit_code; bool sanitizer_passed; };
    - Declare: ExecutionResult execute(const std::string& command,
                                       const std::string& target);

  core_execution/src/executor.cpp
    - Implement execute():
        1. Call sanitizer::sanitize(command, target). If not passed, return
           ExecutionResult with exit_code=-2 and sanitizer_passed=false.
        2. Construct the full invocation string per target:
             wsl       -> "wsl.exe -e bash -c \"<command>\""
             powershell-> "pwsh.exe -NonInteractive -Command \"<command>\""
        3. Spawn the process using CreateProcess (WinAPI) or popen on WSL host.
           Capture stdout and stderr via pipes.
        4. Wait for process completion; collect exit code.
        5. Return a populated ExecutionResult.
    - Implement robust pipe-reading; do not deadlock on large output.
    - Handle process spawn failure; set exit_code=-1 and populate stderr_out.

  core_execution/CMakeLists.txt + bindings/CMakeLists.txt
    - Configure shared library targets (exkutor_core, exkutor_bindings).
    - Link pybind11 if found; otherwise produce a ctypes-compatible .dll/.so.
    - Set C++ standard to 17.
    - Enable all warnings; treat warnings as errors.

  bindings/exkutor_bindings.cpp
    - If pybind11: expose module "exkutor_core" with function execute_command
      (wraps executor::execute), mapping ExecutionResult to a Python namedtuple
      or dataclass-compatible dict.
    - Map C++ exceptions to Python ExkutorBridgeError (import from pipeline).
    - If ctypes fallback: provide a pure C extern "C" wrapper function and
      document the struct layout for ctypes on the Python side.

Self-correction gate: Review all C++ files for correctness, memory safety (no
raw owning pointers; prefer RAII), injection attack surface, and CMake
correctness. Fix all issues before advancing.

────────────────────────────────────────────────────────────────────────────────
PHASE 4 — PYTHON SCRIPTING/PARSER LAYER
────────────────────────────────────────────────────────────────────────────────

  scripting_parser/lexer.py
    - Implement a Lexer class with method tokenize(source: str) -> List[Token].
    - Token types: DIRECTIVE, COLON, STRING, ARROW, TARGET_KW, TARGET_VALUE,
      NEWLINE, COMMENT, EOF.
    - Raise ExkutorSyntaxError (via pipeline) on illegal characters or
      unterminated strings.

  scripting_parser/parser.py
    - Implement a Parser class with method parse(tokens: List[Token]) -> AST.
    - AST node types: RunShellNode, RunChainNode, SetEnvNode, AssertExistsNode,
      LogNode.
    - Each node carries: directive, command_string, target, source_line.
    - Raise ExkutorSyntaxError on any grammar violation.

  scripting_parser/semantic.py
    - Implement a SemanticValidator class with method validate(ast: AST) -> None.
    - Validate: directive names are from the allowed set; targets are from the
      allowed set; command_string is non-empty; no unknown fields.
    - Raise ExkutorSyntaxError on any semantic violation.

  scripting_parser/runtime.py
    - Implement a Runtime class with method run(ast: AST) -> None.
    - For each AST node in order:
        RunShellNode   : Import exkutor_core binding; call execute_command();
                         on exit_code != 0 raise ExkutorShellError; log result.
        RunChainNode   : Execute each sub-command sequentially via execute_command;
                         abort and raise ExkutorShellError on first failure.
        SetEnvNode     : Set os.environ[key] = value for the current process.
        AssertExistsNode: Call execute_command with an existence-check command
                         appropriate to the target; raise ExkutorAssertionError
                         if not found.
        LogNode        : Call pipeline.logger.log_info() with the message.
    - Never call os.system(), subprocess directly, or eval().

Self-correction gate: Trace through a sample .exkutor file mentally, following
the code path from lexer through runtime. Verify all edge cases are handled.

────────────────────────────────────────────────────────────────────────────────
PHASE 5 — EXKUTOR ENTRY POINT
────────────────────────────────────────────────────────────────────────────────

  exkutor.py (CLI entry point)
    - Accept a single positional argument: path to a .exkutor script file.
    - Validate the file exists and has a .exkutor extension.
    - Read the file; pass source to Lexer -> Parser -> SemanticValidator ->
      Runtime in sequence.
    - Catch all ExkutorError subclasses; route to pipeline.logger.log_error();
      exit with code 1.
    - On success, exit with code 0.
    - Usage: python exkutor.py <path/to/script.exkutor>

  build.py (automated build script)
    - Detect the available compiler (MSVC or MinGW-w64).
    - Run CMake configure + build for core_execution and bindings targets.
    - Verify the output .dll (or .so) is produced and importable.
    - Log success or failure to stdout.
    - Exit non-zero on any build failure.

Self-correction gate: Verify the full pipeline from CLI invocation to C++
execution is wired correctly with no broken imports or missing wiring.

────────────────────────────────────────────────────────────────────────────────
PHASE 6 — TEST SUITE IMPLEMENTATION AND EXECUTION
────────────────────────────────────────────────────────────────────────────────
Create all test .exkutor files, then implement and run the orchestrator.

  TEST 1 — Basic I/O (create for both wsl and powershell targets)
    tests/wsl/test_basic_io.exkutor:
        run_shell: "ls /tmp" -> target: wsl
        assert_exists: "/tmp" -> target: wsl

    tests/powershell/test_basic_io.exkutor:
        run_shell: "dir $env:TEMP" -> target: powershell
        assert_exists: "$env:TEMP" -> target: powershell

  TEST 2 — File Operations
    tests/wsl/test_file_ops.exkutor:
        run_shell: "touch /tmp/exkutor_test_file.txt" -> target: wsl
        assert_exists: "/tmp/exkutor_test_file.txt" -> target: wsl

    tests/powershell/test_file_ops.exkutor:
        run_shell: "New-Item -ItemType File -Path $env:TEMP\exkutor_test_file.txt -Force" -> target: powershell
        assert_exists: "$env:TEMP\exkutor_test_file.txt" -> target: powershell

  TEST 3 — Chained Execution
    tests/wsl/test_chained.exkutor:
        run_chain: "mkdir -p /tmp/exkutor_chain_test" -> target: wsl
        run_chain: "cd /tmp/exkutor_chain_test && touch chain_result.txt" -> target: wsl
        assert_exists: "/tmp/exkutor_chain_test/chain_result.txt" -> target: wsl

    tests/powershell/test_chained.exkutor:
        run_chain: "New-Item -ItemType Directory -Path $env:TEMP\exkutor_chain -Force" -> target: powershell
        run_chain: "New-Item -ItemType File -Path $env:TEMP\exkutor_chain\chain_result.txt -Force" -> target: powershell
        assert_exists: "$env:TEMP\exkutor_chain\chain_result.txt" -> target: powershell

  tests/run_tests.py
    - Define TEST_PLAN as an ordered list of (test_name, script_path) tuples
      covering all six test scripts above.
    - For each test in sequence:
        1. Print "RUNNING: <test_name>"
        2. Invoke exkutor.py with the test script via subprocess (NOT os.system).
        3. Capture returncode, stdout, stderr.
        4. If returncode != 0:
             a. Print "FAILED: <test_name>"
             b. Print full stdout and stderr.
             c. Trigger diagnostic: inspect /logs/exkutor_runtime.log for the
                last error entry; print it.
             d. Attempt automated fix if the failure type is known and fixable
                (e.g., missing temp directory: insert a setup command).
             e. Retry the test once. If still failing, halt the full test run
                and exit with code 1, printing a full failure report.
        5. If returncode == 0: print "PASSED: <test_name>"
    - After all tests pass: print "ALL TESTS PASSED. ExkutorLang v1.0 is ready."
    - Exit with code 0 only if every test passed.

CONSTRAINT: No test may be skipped. WSL tests must run before PowerShell tests.
If any test fails and cannot be auto-fixed, you must diagnose the root cause,
implement the fix in the relevant source file, rebuild if C++ changes were made,
and restart the entire test sequence from Test 1.

Self-correction gate: Review every test script for syntactic correctness per the
ExkutorLang grammar. Confirm the orchestrator handles all failure branches.

────────────────────────────────────────────────────────────────────────────────
PHASE 7 — DOCUMENTATION GENERATION
────────────────────────────────────────────────────────────────────────────────
Generate all documentation files. Each must be complete, accurate, and
developer-ready (no placeholder sections).

  docs/syntax_reference.md
    Must include:
    - Language overview and design philosophy (1–2 paragraphs)
    - Complete directive reference table (directive, syntax, description,
      example) for all 5 directives
    - Complete target reference table (target value, environment, invocation
      method)
    - Formal grammar in EBNF or PEG notation
    - Error type reference (all 5 types, when raised, what data they carry)
    - Lexical rules (string quoting, comment syntax, line structure)

  docs/setup_guide.md
    Must include:
    - Prerequisites section (Python 3.11+, WSL2 with Ubuntu/Debian, PowerShell
      7+, CMake, C++ compiler; each with verification command)
    - Step-by-step build instructions (clone repo, run build.py, verify output)
    - Environment variable setup (EXKUTOR_GITHUB_TOKEN, any others)
    - Verification step (run the test suite; expected output)
    - Troubleshooting section covering the top 5 most likely setup failures

  docs/usage_examples.md
    Must include:
    - At least 6 fully copy-pasteable .exkutor script examples with commentary:
        1. Basic directory listing (WSL)
        2. Basic directory listing (PowerShell)
        3. File creation and assertion (WSL)
        4. Chained directory + file creation (PowerShell)
        5. Environment variable setup then command (WSL)
        6. A realistic IDE integration scenario (multi-step build trigger)
    - How to invoke Exkutor from the command line
    - How to interpret output and error messages

  README.md
    Must include: project overview, quick-start (3 commands to get running),
    link to docs/, link to syntax_reference.md, license placeholder.

Self-correction gate: Read each doc file and verify no section is empty,
vague, or placeholder. All code examples must be syntactically valid ExkutorLang.

────────────────────────────────────────────────────────────────────────────────
PHASE 8 — AUTHENTICATED REPOSITORY PUSH
────────────────────────────────────────────────────────────────────────────────

  push_release.py
    This script must be fully automated and require no human interaction.

    Steps to implement:
    1. Read the target repository URL from environment variable
       EXKUTOR_REPO_URL. If unset, raise a clear RuntimeError and exit.
    2. Read the GitHub Personal Access Token from environment variable
       EXKUTOR_GITHUB_TOKEN. If unset, raise a clear RuntimeError and exit.
       NEVER print, log, or embed this token value anywhere.
    3. Construct the authenticated remote URL:
           https://<token>@github.com/<org>/<repo>.git
       Use this URL only in-memory; do not write it to any file or log.
    4. Initialize a git repository in the project root if not already initialized.
    5. Create a .gitignore if not present; ensure /logs/ and __pycache__/ are
       listed.
    6. Stage all files: git add -A
    7. Commit with message: "feat: ExkutorLang v1.0 — initial release"
    8. Set the remote origin to the authenticated URL.
    9. Push to branch main (create if it does not exist).
    10. Print "ExkutorLang v1.0 successfully pushed to <EXKUTOR_REPO_URL>" on
        success.
    11. On any git command failure, print the full error, scrub the token from
        any error message before printing, and exit with code 1.

    SECURITY RULE: The token must never appear in any log file, stdout output,
    source file, or git history. Scrub before printing any git error output.

  EXECUTION ORDER FOR PHASE 8:
    Run push_release.py only after run_tests.py exits with code 0. If tests
    have not passed, do not push. Enforce this programmatically inside
    push_release.py by checking for the presence of a sentinel file written by
    run_tests.py (e.g., /logs/tests_passed.sentinel) before proceeding.

Self-correction gate: Review push_release.py for any possible credential leak.
Verify the sentinel check logic. Confirm all environment variable reads have
clear error messages.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 5 — CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5.1 PROJECT CONTEXT
ExkutorLang is not a general-purpose language. It is a precision instrument for
one job: letting an IDE send commands to WSL or PowerShell and get reliable
structured feedback. Every design decision must serve this singular goal.
Complexity that does not serve this goal is a defect.

5.2 TARGET USER CONTEXT
The end users are IDE plugin developers and power users who need deterministic,
debuggable shell dispatch. They value exact, structured error messages over
generic Python tracebacks. The ExkutorLang runtime is the last line of defense
between their intent and shell execution; it must be trustworthy.

5.3 ENVIRONMENT CONTEXT
  Host OS          : Windows 11 (where ExkutorLang is built and run)
  WSL distribution : Ubuntu 22.04 LTS (minimum; other Debian-based distros OK)
  PowerShell       : 7.4+ (pwsh.exe available on PATH)
  Python           : 3.11+ (available on PATH as python or python3)
  C++ compiler     : MSVC 2022 (cl.exe) or MinGW-w64 (g++ 12+)
  CMake            : 3.20+
  pybind11         : Install via pip (pip install pybind11) or vcpkg

5.4 QUALITY CONTEXT
  - Code must be production-quality: well-structured, commented at non-obvious
    decision points, and free of dead code.
  - No TODO or FIXME comments may remain in the final codebase.
  - Every function longer than 20 lines must have a docstring or block comment
    explaining its contract (inputs, outputs, side effects, error conditions).
  - The C++ layer must be leak-free; use RAII throughout. No raw new/delete.

5.5 AUTONOMOUS OPERATION CONTEXT
You are operating fully autonomously. You will not receive intermediate feedback.
Your self-correction cycles (Section 3.5) are the only quality gate available
to you. Treat each self-correction review as if a senior engineer is about to
reject your PR for any oversight you miss. The build is not done until all eight
phases are complete, all tests pass on both targets, documentation is
comprehensive, and the repository has been pushed successfully.

Begin with Phase 1 now.
================================================================================
END OF JULES AGENT DIRECTIVE
================================================================================
