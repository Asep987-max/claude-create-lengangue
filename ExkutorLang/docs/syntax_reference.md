# ExkutorLang v1.0 Syntax Reference

## Overview
ExkutorLang is a minimalist domain-specific language designed exclusively for executing shell commands on Windows 11 via WSL2 and PowerShell 7+. It eliminates ambiguity and enforces security by default.

## Directives

| Directive | Syntax | Description | Example |
| :--- | :--- | :--- | :--- |
| `run_shell` | `run_shell: "<cmd>" -> target: <env>` | Executes a single command in the target environment. | `run_shell: "ls -la" -> target: wsl` |
| `run_chain` | `run_chain: "<cmd>" -> target: <env>` | Executes a chain of commands (allowing `&&`). | `run_chain: "cd /tmp && ls" -> target: wsl` |
| `set_env` | `set_env: "VAR=VALUE"` | Sets an environment variable for the session. | `set_env: "BUILD_DIR=/tmp/build"` |
| `assert_exists` | `assert_exists: "<path>" -> target: <env>` | Verifies a file or directory exists. Raises error if not. | `assert_exists: "/tmp/file" -> target: wsl` |
| `log` | `log: "<message>"` | Emits a structured log message. | `log: "Starting build..."` |

## Targets

| Target Value | Environment | Description |
| :--- | :--- | :--- |
| `wsl` | WSL2 (Debian/Ubuntu) | Executes via `wsl.exe -e bash -c "..."` |
| `powershell` | PowerShell 7+ | Executes via `pwsh.exe -NonInteractive -Command "..."` |

## Grammar (EBNF-ish)

```ebnf
script        = { statement } ;
statement     = directive_stmt | comment | newline ;
directive_stmt= directive ":" string [ arrow_clause ] newline ;
arrow_clause  = "->" "target" ":" target_value ;
directive     = "run_shell" | "run_chain" | "set_env" | "assert_exists" | "log" ;
target_value  = "wsl" | "powershell" ;
string        = '"' { character } '"' ;
comment       = "#" { character } newline ;
```

## Error Types

- **ExkutorSyntaxError**: Malformed syntax.
- **ExkutorBridgeError**: C++/Python binding failure.
- **ExkutorSanitizerError**: Command rejected by security sanitizer.
- **ExkutorShellError**: Shell command failed (non-zero exit code).
- **ExkutorAssertionError**: Assertion failed.

## Lexical Rules
- Strings must be double-quoted.
- Statements must be on a single line.
- Comments start with `#`.
