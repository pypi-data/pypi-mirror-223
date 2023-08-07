from typing import Any

import git
from gitlab import Gitlab
from gitlab.v4.objects import Project

from .git_repo import GitRepo


class GitProject:
    def __init__(
        self,
        url: str,
        gitlab: Gitlab,
        project: Project,
    ):
        self.url = url
        self.gitlab = gitlab
        self.project = project

    def clone(self, path: str):
        repo = git.Repo.clone_from(
            f"https://oauth2:{self.gitlab.private_token}@{self.gitlab.url.lstrip('https://')}/{self.url}",
            to_path=path,
        )
        return GitRepo(self.project, repo)

    def get_file_tree(self, *args, **kwargs):
        return self.project.repository_tree(*args, **kwargs)

    def get_namespaces(self):
        projects = self.get_file_tree(
            "projects",
            all=True,
        )

        namespaces: list[dict[str, Any]] = []
        for project in projects:
            namespaces.extend(
                self.get_file_tree(
                    project["path"],
                    all=True,
                )
            )
        return list(filter(lambda x: x["name"] != "_common_services", namespaces))

    def find_namespace(self, namespace: str):
        for ns in self.get_namespaces():
            if ns["name"] == namespace:
                return ns
        return False
