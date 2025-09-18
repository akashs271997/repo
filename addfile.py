#!/usr/bin/env python3
"""
Generate 100 Python test files inside docs/tests of the given GitHub repo,
commit and push the changes.

Run:
    python create_and_push_tests.py
"""

import os
import subprocess
import sys
from pathlib import Path

# === User-editable variables ===
repo_clone_url_ssh = "git@github.com:akashs271997/repo.git"   # SSH clone url
repo_clone_url_https = "https://github.com/akashs271997/repo.git"  # HTTPS clone url
local_base = r"C:\Users\AkashSivaraman\Downloads\github_files\repo"  # your actual repo path
target_subpath = "docs/tests"  # path inside the repo where tests will be created
branch = "main"
num_files = 100
commit_message = f"Add {num_files} test files to {target_subpath}"

# === End of user-editable vars ===

def run(cmd, cwd=None, check=True):
    print("> " + " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=check)

def choose_clone_url():
    # prefer SSH if agent works, fallback to HTTPS (optionally with token)
    try:
        subprocess.run(
            ["git", "ls-remote", repo_clone_url_ssh],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return repo_clone_url_ssh
    except Exception:
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            https_with_token = repo_clone_url_https.replace("https://", f"https://{token}@")
            return https_with_token
        return repo_clone_url_https

def ensure_repo_exists(local_dir: Path, clone_url: str):
    if local_dir.exists() and (local_dir / ".git").exists():
        print(f"Repo already present at {local_dir}. Fetching latest {branch}...")
        run(["git", "fetch", "origin", branch], cwd=str(local_dir))
        run(["git", "checkout", branch], cwd=str(local_dir))
        run(["git", "pull", "origin", branch], cwd=str(local_dir))
    else:
        print(f"Cloning {clone_url} into {local_dir} ...")
        run(["git", "clone", clone_url, str(local_dir)])
        run(["git", "checkout", branch], cwd=str(local_dir))

def create_tests(repo_dir: Path, subpath: str, n: int):
    target_dir = repo_dir / subpath
    target_dir.mkdir(parents=True, exist_ok=True)
    for i in range(1, n + 1):
        filename = target_dir / f"test_{i:03}.py"
        content = f"""import unittest

class TestCase{i:03}(unittest.TestCase):
    def test_sample(self):
        # placeholder test
        self.assertEqual(1 + 1, 2)

if __name__ == "__main__":
    unittest.main()
"""
        filename.write_text(content, encoding="utf-8")
        print("Created/Updated", filename)

def git_commit_and_push(repo_dir: Path, msg: str):
    run(["git", "add", "."], cwd=str(repo_dir))
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=str(repo_dir),
        capture_output=True,
        text=True
    )
    if result.stdout.strip() == "":
        print("No changes to commit.")
        return
    run(["git", "commit", "-m", msg], cwd=str(repo_dir))
    run(["git", "push", "origin", branch], cwd=str(repo_dir))
    print("✅ Pushed to origin/" + branch)

def main():
    repo_dir = Path(local_base)
    clone_url = choose_clone_url()
    try:
        ensure_repo_exists(repo_dir, clone_url)
    except Exception as e:
        print("Error cloning or preparing repo:", e)
        sys.exit(1)

    create_tests(repo_dir, target_subpath, num_files)

    try:
        git_commit_and_push(repo_dir, commit_message)
    except Exception as e:
        print("Error during git commit/push:", e)
        print("Make sure you have push permissions and authentication configured.")
        sys.exit(1)

if __name__ == "__main__":
    main()
