from git import Repo


class GitRepository:
    def __init__(self, path: str = "."):
        self.repo = Repo(path, search_parent_directories=True)

    def get_status(self) -> str:
        """Git status 반환"""
        return self.repo.git.status("--short")

    def get_diff(self) -> str:
        """git diff 반환"""
        return self.repo.git.diff()

    def get_pr_diff(self, base_branch: str = "develop") -> str:
        """PR용 git diff 반환"""
        return self.repo.git.diff(f"{base_branch}...HEAD")

    def has_changes(self) -> bool:
        """변경사항 존재 여부 반환"""
        return bool(self.get_status().strip())
