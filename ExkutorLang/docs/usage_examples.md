# ExkutorLang Usage Examples

## 1. Basic Directory Listing (WSL)
```exkutor
log: "Listing /tmp directory in WSL"
run_shell: "ls -la /tmp" -> target: wsl
```

## 2. Basic Directory Listing (PowerShell)
```exkutor
log: "Listing TEMP directory in PowerShell"
run_shell: "dir $env:TEMP" -> target: powershell
```

## 3. File Creation and Assertion (WSL)
```exkutor
log: "Creating a test file"
run_shell: "touch /tmp/myfile.txt" -> target: wsl
assert_exists: "/tmp/myfile.txt" -> target: wsl
```

## 4. Chained Execution (PowerShell)
```exkutor
log: "Creating directory and file in chain"
run_chain: "New-Item -ItemType Directory -Path $env:TEMP\my_dir -Force && New-Item -ItemType File -Path $env:TEMP\my_dir\file.txt" -> target: powershell
assert_exists: "$env:TEMP\my_dir\file.txt" -> target: powershell
```

## 5. Environment Variable Setup
```exkutor
set_env: "BUILD_MODE=RELEASE"
log: "Build mode set to RELEASE"
run_shell: "echo $BUILD_MODE" -> target: wsl
```

## 6. IDE Integration Scenario
```exkutor
log: "Starting build process triggered by IDE..."
set_env: "PROJECT_ROOT=/mnt/c/Users/Dev/Project"
run_shell: "cd $PROJECT_ROOT" -> target: wsl
run_chain: "cmake -B build && cmake --build build" -> target: wsl
assert_exists: "$PROJECT_ROOT/build/app.exe" -> target: wsl
log: "Build complete."
```
