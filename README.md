# Prompt Library

A curated collection of reusable AI prompts, templates and examples organized by category to help you build, test and deploy prompt-powered projects.

## Table of contents

- [About](#about)
- [Quick start](#quick-start)
- [Browse the library](#browse-the-library)
- [Repository structure](#repository-structure)
- [Contributing](#contributing)
- [License](#license)

## About

This repository groups prompts, templates and metadata into clear categories so you can find and reuse them in your projects. Each category has a short README explaining purpose and usage.

## Quick start

1. Browse the `templates/` folder for reusable prompt scaffolds.
2. Explore categories such as `trading/`, `development/`, and `content/` to find specialized prompts.
3. Use `metadata/prompt_index.yaml` to search or filter prompts by tag.

## Browse the library

- templates/: Reusable templates and project-level prompts.
- trading/: Trading-related prompts (bot development, backtesting, market analysis).
- development/: Prompts for software engineering workflows (code generation, review, debugging).
- content/: Prompts for writing, marketing and social media.
- analysis/: Data processing and visualization prompts.
- utilities/: Formatting, translation and other utility prompts.
- metadata/: Indexes, tags and changelog.

## Repository structure

<details>
<summary>Expand to view full structure</summary>

```text
prompt-library/
│
├── README.md                          # Repository overview, how to use prompts
├── LICENSE                            # License (CC BY 4.0 or MIT for prompts)
├── CONTRIBUTING.md                    # Guidelines for contributing prompts
├── .gitignore                         # Standard gitignore
│
├── templates/                         # Reusable prompt templates
│   ├── prompt_template.md
│   └── project_prompt_template.md
│
├── trading/                           # Trading-related prompts
│   ├── README.md                      # Category overview
│   │
│   ├── bot_development/               # Trading bot development
│   │   ├── README.md
│   │   ├── trading_bot_master_prompt.md
│   │   ├── trading_bot_01_video_analysis.md
│   │   ├── trading_bot_02_system_documentation.md
│   │   ├── trading_bot_03_technical_architecture.md
│   │   ├── trading_bot_04_implementation.md
│   │   ├── trading_bot_05_testing_deployment.md
│   │   └── outputs/                   # Example outputs (optional)
│   │       └── .gitkeep
│   │
│   ├── market_analysis/               # Market analysis prompts
│   │   └── README.md
│   │
│   └── backtesting/                   # Backtesting prompts
│       └── README.md
│
├── development/                       # Software development prompts
│   ├── README.md
│   ├── code_generation/
│   ├── code_review/
│   └── debugging/
│
├── content/                           # Content creation prompts
│   ├── README.md
│   ├── writing/
│   ├── marketing/
│   └── social_media/
│
├── analysis/                          # Data analysis prompts
│   ├── README.md
│   ├── data_processing/
│   └── visualization/
│
├── utilities/                         # Utility prompts
│   ├── README.md
│   ├── formatting/
│   └── translation/
│
└── metadata/                          # Prompt metadata & tracking
    ├── prompt_index.yaml              # Searchable index
    ├── tags.yaml                      # Tag definitions
    └── changelog.md                   # Version history
```

</details>

## Contributing

Contributions are welcome — please see `CONTRIBUTING.md` for guidelines. When adding prompts:

- Add a short README for the category if one does not exist.
- Include metadata (tags, description) so the prompt can be indexed.
- Add example outputs where helpful in an `outputs/` folder.

## License

The repository-level license is in the `LICENSE` file. Prompts can be licensed individually; we recommend a permissive license such as CC BY 4.0 or MIT for code-related prompt content.

---

If you'd like, I can further tweak styles (badges, images) or add a visual index page for the website. Please tell me which improvements you want next.
