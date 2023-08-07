import git
from gitlab.v4.objects import Project


class GitRepo:
    def __init__(self, gitlab_project: Project, repo: git.Repo):
        self.project = gitlab_project
        self.repo = repo
        self.default_branch = repo.active_branch.name

    def change_branch(self, branch_name: str):
        if branch_name not in self.repo.branches:
            self.repo.create_head(branch_name)
        self.repo.git.checkout(branch_name)

    def add_files(self, files: list[str]):
        self.repo.index.add(files)

    def commit(self, message: str, add_all: bool = False):
        if add_all:
            self.repo.git.add(all=True)
        self.repo.index.commit(message)

    def push(
        self,
    ):
        self.repo.git.push("--set-upstream", "origin", self.repo.active_branch)

    def create_mr(
        self,
        title: str,
        source_branch: str | None = None,
        description: str = "",
        target_branch: str | None = None,
    ):
        if source_branch is None:
            source_branch = self.repo.active_branch.name
        if target_branch is None:
            target_branch = self.default_branch

        return self.project.mergerequests.create(
            {
                "source_branch": source_branch,
                "target_branch": target_branch,
                "title": title,
                "description": description,
            }
        )
