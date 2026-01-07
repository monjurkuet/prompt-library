"""Prompt management tools for agent system."""

import subprocess
from pathlib import Path


class PromptManager:
    """Wrapper around scripts/prompt_manager.py for agent operations."""

    def __init__(self, project_root: Path | None = None):
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent
        self.project_root = project_root
        self.manager_script = self.project_root / "scripts" / "prompt_manager.py"

    def _run_command(self, args: list[str]) -> str:
        """Run prompt_manager.py with given arguments."""
        cmd = ["uv", "run", "python", str(self.manager_script)] + args
        result = subprocess.run(
            cmd, cwd=self.project_root, capture_output=True, text=True
        )
        return result.stdout

    def index(self) -> str:
        """Generate prompt index."""
        return self._run_command(["index"])

    def new_prompt(self) -> str:
        """Create new prompt using scaffold."""
        return self._run_command(["new-prompt"])

    def search(self, query: str) -> str:
        """Search prompts."""
        return self._run_command(["search", query])

    def validate_all(self) -> dict[str, bool]:
        """Validate all prompts for YAML front matter."""
        results = {}
        prompt_dirs = [
            self.project_root / "analysis",
            self.project_root / "content",
            self.project_root / "development",
            self.project_root / "trading",
            self.project_root / "utilities",
        ]

        for prompt_dir in prompt_dirs:
            if not prompt_dir.exists():
                continue
            for md_file in prompt_dir.rglob("*.md"):
                results[str(md_file)] = self._validate_front_matter(md_file)

        return results

    def _validate_front_matter(self, file_path: Path) -> bool:
        """Check if file has valid YAML front matter."""
        import yaml

        try:
            with open(file_path) as f:
                content = f.read()
            if not content.startswith("---"):
                return False
            front_matter_end = content.find("---", 3)
            if front_matter_end == -1:
                return False
            front_matter = content[3:front_matter_end]
            data = yaml.safe_load(front_matter)
            required_fields = [
                "id",
                "title",
                "description",
                "category",
                "tags",
                "version",
                "status",
            ]
            return all(field in data for field in required_fields)
        except Exception:
            return False
