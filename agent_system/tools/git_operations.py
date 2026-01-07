"""Safe git operations with rollback support."""

import subprocess
from pathlib import Path


class GitOperations:
    """Safe git operations with rollback capability."""

    def __init__(self, project_root: Path | None = None):
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent
        self.project_root = project_root

    def _run_git(
        self, args: list[str], check: bool = True
    ) -> subprocess.CompletedProcess:
        """Run git command."""
        return subprocess.run(
            ["git"] + args,
            cwd=self.project_root,
            capture_output=True,
            text=True,
            check=check,
        )

    def get_status(self) -> dict:
        """Get current git status."""
        result = self._run_git(["status", "--porcelain"], check=False)
        files = {"modified": [], "added": [], "deleted": [], "untracked": []}

        for line in result.stdout.splitlines():
            if not line:
                continue
            status_code, file_path = line[:2], line[3:]
            if status_code == "M":
                files["modified"].append(file_path)
            elif status_code == "A":
                files["added"].append(file_path)
            elif status_code == "D":
                files["deleted"].append(file_path)
            elif status_code == "??":
                files["untracked"].append(file_path)

        return files

    def create_commit(
        self, message: str, files: list[str] | None = None, dry_run: bool = False
    ) -> dict:
        """Create a commit with optional dry-run."""
        commit_data = {"message": message, "files": files or [], "dry_run": dry_run}

        if dry_run:
            return {**commit_data, "status": "dry_run", "commit_hash": None}

        if files:
            self._run_git(["add"] + files)
        else:
            self._run_git(["add", "."])

        result = self._run_git(["commit", "-m", message])
        commit_hash = result.stdout.split()[1] if result.returncode == 0 else None

        return {**commit_data, "status": "committed", "commit_hash": commit_hash}

    def rollback(self, target: str | None = None) -> dict:
        """Rollback to previous state."""
        result = self._run_git(["reset", "--hard", target]) if target else self._run_git(["reset", "--hard", "HEAD~1"])

        return {
            "status": "rolled_back",
            "target": target or "HEAD~1",
            "success": result.returncode == 0,
        }

    def get_recent_commits(self, count: int = 5) -> list[dict]:
        """Get recent commit history."""
        result = self._run_git(["log", f"-{count}", "--oneline"])
        commits = []

        for line in result.stdout.splitlines():
            if line:
                parts = line.split(maxsplit=1)
                commits.append(
                    {"hash": parts[0], "message": parts[1] if len(parts) > 1 else ""}
                )

        return commits

    def create_branch(self, branch_name: str, dry_run: bool = False) -> dict:
        """Create a new branch."""
        if dry_run:
            return {"status": "dry_run", "branch": branch_name}

        result = self._run_git(["checkout", "-b", branch_name])
        return {
            "status": "created" if result.returncode == 0 else "failed",
            "branch": branch_name,
        }

    def merge_branch(self, branch_name: str, dry_run: bool = False) -> dict:
        """Merge a branch into current."""
        if dry_run:
            return {"status": "dry_run", "branch": branch_name}

        result = self._run_git(["merge", branch_name])
        return {
            "status": "merged" if result.returncode == 0 else "failed",
            "branch": branch_name,
        }
