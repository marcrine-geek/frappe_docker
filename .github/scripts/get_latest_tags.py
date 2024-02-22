from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from typing import Literal
import os


token = os.getenv("GITHUB_TOKEN")
print(token)
Repo = Literal["frontend"]
MajorVersion = Literal["master"]

username="marcrine-geek"

def get_latest_tag(repo: Repo, version: MajorVersion) -> str:
    regex = rf"{version}.*"
    git_url = f"https://{username}:{token}@github.com/marcrine-geek/{repo}.git"

    print(git_url)
    refs = subprocess.check_output(
        (
            "git",
            "ls-remote",
            git_url,
            # str(regex),
        ),
        encoding="UTF-8",
        env={
                "GITHUB_TOKEN": token,
            },
    ).split()[1::2]

    print("0000000")

    if not refs:
        raise RuntimeError(f'No tags found for version "{regex}"')
    ref = refs[-1]
    matches: list[str] = re.findall(regex, ref)
    if not matches:
        raise RuntimeError(f'Can\'t parse tag from ref "{ref}"')
    return matches[0]

def update_env(file_name: str, frappe_tag: str, erpnext_tag: str | None = None):
    text = f"\nFRAPPE_VERSION={frappe_tag}"
    if erpnext_tag:
        text += f"\nERPNEXT_VERSION={erpnext_tag}"

    with open(file_name, "a") as f:
        f.write(text)


def _print_resp(frappe_tag: str, erpnext_tag: str | None = None):
    print(json.dumps({"frappe": frappe_tag, "erpnext": erpnext_tag}))


def main(_args: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", choices=["frontend"], required=True)
    parser.add_argument("--version", choices=["master"], required=True)
    args = parser.parse_args(_args)

    frappe_tag = get_latest_tag(args.repo, args.version)
    
    print("--------", frappe_tag)
    # file_name = os.getenv("GITHUB_ENV")
    # if file_name:
    #     update_env(file_name, frappe_tag)
    _print_resp(frappe_tag)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
