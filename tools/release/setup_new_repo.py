#!/usr/bin/env python3
"""Automate creating a new independent repository on GitHub and pushing all Vietnamese changes."""
import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REPO_NAME = "SuperRobot-Vietnamese"
REPO_DESC = "Super Robot Taisen 64 - Bản dịch tiếng Việt và hỗ trợ phát hành Windows PC"
IS_PRIVATE = False


def get_github_token() -> tuple[str, str]:
    """Get stored GitHub username and token from git credential helper."""
    p = subprocess.Popen(
        ["git", "credential", "fill"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, _ = p.communicate("protocol=https\nhost=github.com\n\n")
    username, password = "", ""
    for line in out.splitlines():
        if line.startswith("username="):
            username = line.split("=", 1)[1].strip()
        elif line.startswith("password="):
            password = line.split("=", 1)[1].strip()
    return username, password


def create_github_repo(username: str, token: str, repo_name: str, desc: str, private: bool) -> str:
    """Create a new repo on GitHub via REST API."""
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
    }
    payload = json.dumps({
        "name": repo_name,
        "description": desc,
        "private": private,
        "auto_init": False,
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            clone_url = data.get("clone_url")
            print(f"Created repository: {data.get('html_url')}")
            return clone_url
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        if e.code == 422 and "already exists" in body.lower():
            print(f"Repository {repo_name} already exists on GitHub under {username}.")
            return f"https://github.com/{username}/{repo_name}.git"
        raise RuntimeError(f"Failed to create repo ({e.code}): {body}")


def run_git(args: list[str]) -> str:
    print(f"Running: git {' '.join(args)}")
    res = subprocess.run(["git"] + args, cwd=ROOT, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.returncode != 0:
        if res.stderr:
            print(f"Error: {res.stderr.strip()}", file=sys.stderr)
        raise RuntimeError(f"git {' '.join(args)} failed with code {res.returncode}")
    return res.stdout


def main():
    username, token = get_github_token()
    if not username or not token:
        print("Error: Could not retrieve GitHub credentials from git credential helper.", file=sys.stderr)
        sys.exit(1)

    print(f"Found GitHub credentials for user: {username}")
    print(f"Creating new GitHub repository: {REPO_NAME} (private={IS_PRIVATE})...")
    clone_url = create_github_repo(username, token, REPO_NAME, REPO_DESC, IS_PRIVATE)
    print(f"Target clone URL: {clone_url}")

    # Check remotes
    remotes = run_git(["remote"]).splitlines()
    if "origin" in remotes:
        origin_url = run_git(["remote", "get-url", "origin"]).strip()
        if "dyzz/srw64-recomp" in origin_url:
            if "upstream" not in remotes:
                print("Renaming 'origin' to 'upstream'...")
                run_git(["remote", "rename", "origin", "upstream"])
            else:
                run_git(["remote", "remove", "origin"])

    # Add or update origin
    remotes = run_git(["remote"]).splitlines()
    if "origin" in remotes:
        run_git(["remote", "set-url", "origin", clone_url])
    else:
        run_git(["remote", "add", "origin", clone_url])

    print("Staging all changes...")
    run_git(["add", "-A"])

    status = run_git(["status", "--porcelain"])
    if status.strip():
        print("Committing changes...")
        commit_msg = (
            "feat: Tích hợp bản địa hóa tiếng Việt toàn diện và công cụ phát hành Windows PC\n\n"
            "- Thêm ngôn ngữ tiếng Việt (vi.json, terms/vi.json) cho toàn bộ UI và thuật ngữ game.\n"
            "- Dịch toàn bộ 45.176 câu thoại cốt truyện (131 phân cảnh) và trận chiến (259 tệp nhân vật).\n"
            "- Thêm công cụ tự động biên dịch, vá font HarmonyOS Sans và đóng gói Windows x64.\n"
            "- Cập nhật tài liệu hướng dẫn build và cài đặt Windows PC."
        )
        run_git(["commit", "-m", commit_msg])
    else:
        print("Working tree clean, no new changes to commit.")

    print("Pushing to GitHub...")
    # Inject token into push URL for authenticated push if needed, or rely on credential manager
    run_git(["push", "-u", "origin", "main"])
    print("\nSuccessfully pushed repository to:")
    print(f"https://github.com/{username}/{REPO_NAME}")


if __name__ == "__main__":
    main()

