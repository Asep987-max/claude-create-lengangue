"""
Authenticated Repository Push Script.
"""
import os
import sys
import subprocess

SENTINEL_FILE = os.path.join(os.path.dirname(__file__), "logs", "tests_passed.sentinel")

def main():
    # 1. Check Sentinel
    if not os.path.exists(SENTINEL_FILE):
        print("Error: Tests must pass before release. Run tests/run_tests.py first.", file=sys.stderr)
        sys.exit(1)

    # 2. Read Env Vars
    repo_url = os.environ.get("EXKUTOR_REPO_URL")
    if not repo_url:
        print("Error: EXKUTOR_REPO_URL environment variable not set.", file=sys.stderr)
        sys.exit(1)

    token = os.environ.get("EXKUTOR_GITHUB_TOKEN")
    if not token:
        print("Error: EXKUTOR_GITHUB_TOKEN environment variable not set.", file=sys.stderr)
        sys.exit(1)

    # 3. Construct Auth URL (In-Memory Only)
    # repo_url format: https://github.com/org/repo.git or similar
    # auth_url format: https://<token>@github.com/org/repo.git
    # Handle if URL already has protocol
    if "https://" in repo_url:
        host_path = repo_url.split("https://")[1]
        auth_url = f"https://{token}@{host_path}"
    else:
        # Assuming github.com path
        auth_url = f"https://{token}@github.com/{repo_url}"

    print(f"Preparing to push to {repo_url}...")

    # 4. Initialize Git
    # Assuming we are in the project root or running from it
    # We are in ExkutorLang/ usually? No, script is in ExkutorLang/.
    # Project root is `.`.

    try:
        if not os.path.exists(".git"):
            subprocess.check_call(["git", "init"], stdout=subprocess.DEVNULL)

        # 5. Add files
        subprocess.check_call(["git", "add", "-A"])

        # 6. Commit
        # Check if anything to commit
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if status.stdout.strip():
            subprocess.check_call(["git", "commit", "-m", "feat: ExkutorLang v1.0 — initial release"])

        # 7. Set Remote
        # We don't want to leak token in `git remote -v` output if written to disk config?
        # `git remote add origin <url>` writes to .git/config.
        # Ideally we push to URL directly without adding remote, OR we assume this env is ephemeral.
        # Spec says: "Set the remote origin to the authenticated URL."

        # Check if origin exists
        remotes = subprocess.run(["git", "remote"], capture_output=True, text=True).stdout
        if "origin" in remotes:
            subprocess.check_call(["git", "remote", "set-url", "origin", auth_url])
        else:
            subprocess.check_call(["git", "remote", "add", "origin", auth_url])

        # 8. Push
        print("Pushing to main...")
        # Capture stderr to scrub token if failure
        proc = subprocess.run(["git", "push", "-u", "origin", "main"], capture_output=True, text=True)

        if proc.returncode != 0:
            # Scrub token
            sanitized_err = proc.stderr.replace(token, "[REDACTED_TOKEN]")
            print(f"Error pushing to remote: {sanitized_err}", file=sys.stderr)
            sys.exit(1)

        print(f"ExkutorLang v1.0 successfully pushed to {repo_url}")

    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
