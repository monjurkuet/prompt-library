"""Code analysis tools for refactoring."""

import ast
import subprocess
from pathlib import Path


class CodeAnalyzer:
    """Static analysis and refactoring capabilities."""

    def __init__(self, project_root: Path | None = None):
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent
        self.project_root = project_root

    def analyze_file(self, file_path: Path) -> dict:
        """Analyze a Python file."""
        with open(file_path) as f:
            content = f.read()

        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            return {"error": str(e)}

        classes = []
        functions = []
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom) and node.module:
                for alias in node.names:
                    imports.append(f"{node.module}.{alias.name}")

        return {
            "file": str(file_path),
            "classes": classes,
            "functions": functions,
            "imports": imports,
            "line_count": len(content.splitlines()),
        }

    def analyze_directory(self, directory: Path) -> list[dict]:
        """Analyze all Python files in a directory."""
        results = []
        for py_file in directory.rglob("*.py"):
            results.append(self.analyze_file(py_file))
        return results

    def lint_check(self, file_paths: list[Path] | None = None) -> dict[str, str]:
        """Run ruff linting."""
        files = [str(self.project_root)] if file_paths is None else [str(f) for f in file_paths]

        cmd = [
            "uv",
            "run",
            "ruff",
            "check",
            "--select",
            "E,F,I,UP,B,SIM",
            "--ignore",
            "E501",
            "--line-length",
            "120",
        ] + files

        result = subprocess.run(
            cmd, cwd=self.project_root, capture_output=True, text=True
        )

        if result.returncode == 0:
            return {"status": "clean"}
        else:
            return {"status": "issues_found", "output": result.stdout}

    def format_check(self, file_paths: list[Path] | None = None) -> dict[str, str]:
        """Check code formatting with ruff."""
        files = [str(self.project_root)] if file_paths is None else [str(f) for f in file_paths]

        cmd = ["uv", "run", "ruff", "format", "--check"] + files

        result = subprocess.run(
            cmd, cwd=self.project_root, capture_output=True, text=True
        )

        if result.returncode == 0:
            return {"status": "clean"}
        else:
            return {"status": "needs_formatting", "output": result.stdout}
