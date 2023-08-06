import datetime
import os
from typing import Optional, TypedDict
from git.repo import Repo
import giturlparse
from urllib.parse import urljoin


class GitInfo(TypedDict):
    gitHash: str
    gitRepo: str
    gitSSHRepo: str
    gitUser: str
    localRepoRootDir: str
    mergedAt: datetime.datetime


def get_git_repo_info() -> GitInfo:
    repo = Repo(".", search_parent_directories=True)
    parsed_repo = giturlparse.parse(repo.remotes.origin.url)
    return {
        "gitHash": repo.head.commit.hexsha,
        "gitRepo": repo.remotes.origin.url,
        "gitSSHRepo": parsed_repo.url2ssh.rstrip(".git"),
        "gitUser": repo.head.commit.author.name or "unknown-git-user",
        "localRepoRootDir": os.path.dirname(repo.git_dir),
        "mergedAt": repo.head.commit.committed_datetime,
    }


def get_git_ssh_file_path(git_info: GitInfo, local_file_path):
    absolute_file_path = os.path.abspath(local_file_path)
    relative_path = os.path.relpath(absolute_file_path, git_info["localRepoRootDir"])
    return urljoin(git_info["gitSSHRepo"], relative_path)
