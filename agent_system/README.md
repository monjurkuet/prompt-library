# Agent System

Agentic system for automated prompt library management, refactoring, research integration, and self-improvement.

## Overview

The agent system automates operations in the prompt-library repository including:
- Creating and managing prompts
- Refactoring and optimizing code
- Monitoring arXiv for latest research
- Organizing directory structure
- Self-improvement through learning

## Directory Structure

```
agent_system/
├── flows/               # Langflow flows (JSON format)
├── tools/               # Custom Python tools
│   ├── __init__.py
│   ├── prompt_tools.py
│   ├── code_analyzer.py
│   ├── arxiv_integrator.py
│   ├── file_organizer.py
│   └── git_operations.py
├── GEMINI.md           # Self-improvement protocol
├── README.md           # This file
└── agent_config.yaml   # Configuration
```

## Tools

### Prompt Tools (`prompt_tools.py`)
Wrapper around `scripts/prompt_manager.py` for agent operations:
- `index()` - Generate prompt index
- `new_prompt()` - Create new prompt scaffold
- `search(query)` - Search prompts
- `validate_all()` - Validate YAML front matter

### Code Analyzer (`code_analyzer.py`)
Static analysis and refactoring capabilities:
- `analyze_file(file_path)` - Analyze Python file
- `analyze_directory(directory)` - Analyze all files
- `lint_check()` - Run ruff linting
- `format_check()` - Check formatting

### ArXiv Integrator (`arxiv_integrator.py`)
arXiv API wrapper for research monitoring:
- `search_by_keywords(keywords)` - Search by keywords
- `search_by_category(category)` - Search by category
- `get_paper_details(paper_id)` - Get paper details

### File Organizer (`file_organizer.py`)
Directory analysis and organization:
- `analyze_directory_structure()` - Analyze structure
- `find_duplicates()` - Find duplicate files
- `suggest_organization()` - Suggest improvements
- `get_directory_size()` - Calculate sizes

### Git Operations (`git_operations.py`)
Safe git operations with rollback:
- `get_status()` - Get git status
- `create_commit(message, files, dry_run)` - Create commit
- `rollback(target)` - Rollback changes
- `get_recent_commits()` - Get commit history

## Usage

### Running Tools
```python
from agent_system.tools.prompt_tools import PromptManager
from agent_system.tools.code_analyzer import CodeAnalyzer

pm = PromptManager()
pm.index()

ca = CodeAnalyzer()
ca.lint_check()
```

### Langflow Integration
Flows are stored as JSON files in `agent_system/flows/`. Import them into Langflow to build visual agent workflows.

## Configuration

See `agent_config.yaml` for:
- Agent settings
- Research parameters
- Directory paths
- Self-improvement options

## Safety Features

- Dry-run mode by default
- Git rollback capability
- User approval required for writes
- Comprehensive validation

## Development

Follow `AGENTS.md` guidelines:
- Python 3.9+
- uv for package management
- ruff for linting/formatting
- Type hints required

## Self-Improvement

The agent continuously improves through:
- User feedback integration
- Error pattern analysis
- Protocol updates (GEMINI.md)
- Research-driven enhancements
