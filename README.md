# Prompt Library

A curated, production-grade collection of high-quality AI prompts, architected for scalability, automation, and adaptability.

## 🎯 Purpose
This repository serves as a centralized, version-controlled library for LLM prompts. It is designed to be:
*   **Machine-Readable:** All prompts use structured YAML Front Matter for easy indexing and integration.
*   **Automated:** Includes Python tooling for validation, indexing, and documentation generation.
*   **Modular:** Organized by domain (`analysis`, `trading`, `development`, `utilities`, `content`) for intuitive navigation.

## 📁 Repository Structure
```
prompt-library/
├── analysis/           # Data analysis & extraction
├── content/            # Content creation (visual, text)
├── development/        # Coding & engineering prompts
├── trading/            # Financial & trading bot workflows
├── utilities/          # Meta-prompts & agent operations
├── metadata/           # Auto-generated indices (prompt_index.yaml)
└── scripts/            # Automation tools (prompt_manager.py)
```

## 🛠️ Tooling & Workflow

This project uses a custom CLI tool, `scripts/prompt_manager.py`, to maintain quality and consistency.

### 1. Create a New Prompt
Don't create files manually. Use the wizard to ensure metadata compliance:
```bash
uv run python scripts/prompt_manager.py new-prompt
```
*Follow the interactive prompts to define ID, category, tags, and parameters.*

### 2. Update the Index
After adding or editing a prompt, regenerate the index and update all READMEs:
```bash
uv run python scripts/prompt_manager.py index
```
*This updates `metadata/prompt_index.yaml` and injects prompt lists into category README files.*

## 📝 Prompt Standard

Every prompt file (`.md`) MUST start with a YAML Front Matter block:

```yaml
---
id: my-prompt-id
title: My Prompt Title
description: A clear description of what this prompt does.
category: utilities
sub_category: general
tags: ["tag1", "tag2"]
version: "1.0.0"
status: "active"
llm_model_compatibility: ["gpt-4o", "claude-3-opus"]
parameters:
  - name: input_text
    type: string
    description: The text to process.
---
# My Prompt Title

## ROLE
...
```

## 🚀 Quick Start

1.  **Clone the repo.**
2.  **Install dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```
3.  **Browse Prompts:**
    *   Check `metadata/prompt_index.yaml` for a machine-readable catalog.
    *   Navigate to category folders (e.g., `utilities/agent_ops/`) and check the `README.md`.

## ⭐ Featured Prompts

*   **[The Adaptive Project Architect](utilities/agent_ops/adaptive_project_architect.md):** A self-optimizing agent persona that learns your preferences.
*   **[Deep Research Agent](utilities/prompt_engineering/deep_research_agent.md):** An autonomous researcher for keeping knowledge bases up to date.
*   **[Perfect Prompt Engineer](utilities/prompt_engineering/perfect-prompt-engineer.md):** A meta-prompt to design other high-quality prompts.
*   **[Git Commit Generator](utilities/agent_ops/git_commit_generator.md):** Automate your semantic commit messages.

## 🤝 Contributing
1.  Run `new-prompt` to scaffold your file.
2.  Fill in the prompt content.
3.  Run `index` to validate and register it.
4.  Commit and push.

## 📜 License
[MIT/CC-BY-4.0]
