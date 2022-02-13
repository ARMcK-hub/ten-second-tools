from typing import Any, Dict

from src.READMD.config import Repository, User
from src.READMD.config_provider import JsonConfigProvider
from src.READMD.readme import GitHubReadMe


def build_repo(repo_md: Dict[Any, Any]) -> Repository:
    return Repository(
        repo_md["name"],
        repo_md["title"],
        repo_md["link"],
        repo_md["image"],
        repo_md["description"],
        repo_md["body"],
        repo_md["features"],
        repo_md["technologies"],
        repo_md["acknowledgements"],
    )


def readmd() -> None:
    config = JsonConfigProvider(
        "/workspaces/TenSecondTools/src/READMD/config/config.json"
    )
    repo_acc_md = config.get("user")
    repos_md = config.get("repositories")

    user = User(
        repo_acc_md["repoHost"],
        repo_acc_md["accountName"],
        repo_acc_md["yourName"],
        repo_acc_md["linkedInAccount"],
        repo_acc_md["email"],
        repo_acc_md["portrait"],
    )
    repos = [build_repo(md) for md in repos_md]

    rm_strategy = GitHubReadMe(user)

    for repo in repos:
        rm_strategy.to_md(repo)


if __name__ == "__main__":
    readmd()
