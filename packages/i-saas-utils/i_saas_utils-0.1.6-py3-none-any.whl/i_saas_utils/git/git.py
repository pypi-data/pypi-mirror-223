from typing import Optional

from gitlab import Gitlab

from .git_project import GitProject


class Git:
    def __init__(
        self,
        url: Optional[str] = None,
        private_token: Optional[str] = None,
    ):
        self.gitlab = Gitlab(
            url,
            private_token,
        )
        self.gitlab.auth()

    def get_project(self, project_url: str):
        return GitProject(
            project_url, self.gitlab, self.gitlab.projects.get(project_url)
        )
