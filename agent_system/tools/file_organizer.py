"""File organization and directory analysis tools."""

from pathlib import Path


class FileOrganizer:
    """Directory analysis and organization utilities."""

    def __init__(self, project_root: Path | None = None):
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent
        self.project_root = project_root

    def analyze_directory_structure(self) -> dict:
        """Analyze the project directory structure."""
        structure = {"directories": [], "files": [], "extensions": {}}

        for item in self.project_root.rglob("*"):
            if item.is_dir():
                if not self._should_ignore(item):
                    structure["directories"].append(
                        str(item.relative_to(self.project_root))
                    )
            elif item.is_file() and not self._should_ignore(item):
                structure["files"].append(str(item.relative_to(self.project_root)))
                ext = item.suffix
                structure["extensions"][ext] = (
                    structure["extensions"].get(ext, 0) + 1
                )

        return structure

    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored."""
        ignore_dirs = {
            ".git",
            "__pycache__",
            "node_modules",
            ".venv",
            "venv",
            ".env",
            "current",
        }
        ignore_files = {".DS_Store", "*.pyc", ".gitignore"}

        if any(parent.name in ignore_dirs for parent in path.parents):
            return True

        if path.name in ignore_dirs or path.name in ignore_files:
            return True

        return path.suffix in [".pyc", ".pyo"]

    def find_duplicates(self, directory: Path | None = None) -> dict[str, list[str]]:
        """Find files with identical names in different directories."""
        if directory is None:
            directory = self.project_root

        name_map: dict[str, list[str]] = {}
        duplicates: dict[str, list[str]] = {}

        for file_path in directory.rglob("*"):
            if file_path.is_file() and not self._should_ignore(file_path):
                name = file_path.name
                if name not in name_map:
                    name_map[name] = []
                name_map[name].append(str(file_path))

        for name, paths in name_map.items():
            if len(paths) > 1:
                duplicates[name] = paths

        return duplicates

    def suggest_organization(self) -> dict[str, list[str]]:
        """Suggest organizational improvements."""
        suggestions = {
            "move_to_utils": [],
            "consolidate_similar": [],
            "check_for_orphaned": [],
        }

        for file_path in self.project_root.rglob("*.py"):
            if self._should_ignore(file_path):
                continue

            if "util" in file_path.stem.lower() and "utilities" not in str(
                file_path.parent
            ):
                suggestions["move_to_utils"].append(str(file_path))

        return suggestions

    def get_directory_size(self, directory: Path | None = None) -> dict[str, int]:
        """Calculate directory sizes."""
        if directory is None:
            directory = self.project_root

        sizes: dict[str, int] = {}

        for item in directory.rglob("*"):
            if item.is_dir() and not self._should_ignore(item):
                try:
                    size = sum(f.stat().st_size for f in item.rglob("*") if f.is_file())
                    sizes[str(item.relative_to(self.project_root))] = size
                except (PermissionError, OSError):
                    continue

        return dict(sorted(sizes.items(), key=lambda x: x[1], reverse=True))
