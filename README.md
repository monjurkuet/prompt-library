# Prompt Library

A curated collection of high-quality, production-ready prompts for various AI applications.

## 🎯 Purpose
This repository contains professionally crafted prompts designed to minimize hallucination and maximize output quality across different use cases.

## 📁 Repository Structure
```
prompt-library/
├── trading/          # Trading & finance prompts
├── development/      # Software development prompts
├── content/          # Content creation prompts
├── analysis/         # Data analysis prompts
└── utilities/        # General utility prompts
```

## 📁 Prompt Repository Structure
```
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

## 📁 Prompt File Structure Standard

### Each prompt file should follow this template:
```
# [Prompt Title]

## Metadata
- **Category:** Trading > Bot Development
- **AI Model:** Gemini 1.5 Pro (or applicable models)
- **Complexity:** Advanced
- **Estimated Time:** 15-30 minutes
- **Dependencies:** [Previous prompts required]
- **Version:** 1.0
- **Last Updated:** 2024-12-24
- **Tags:** #trading #video-analysis #multimodal #bitcoin

## Purpose
[Clear description of what this prompt achieves]

## Prerequisites
- [ ] Previous prompts completed (if applicable)
- [ ] Required access/tools
- [ ] Input data/files needed

## Input Requirements
[What the user needs to provide]

## Prompt
[THE ACTUAL PROMPT GOES HERE]

## Expected Output
[Description of what the AI should produce]

## Example Output
[Optional: Sample output for reference]

## Tips for Best Results
- Tip 1
- Tip 2
- Tip 3

## Common Issues & Solutions
| Issue | Solution |
|-------|----------|
| Hallucination about X | Add constraint Y |

## Validation Checklist
- [ ] Output contains required elements
- [ ] No hallucinations detected
- [ ] Format matches specification

## Related Prompts
- [Link to related prompts]

## Changelog
- v1.0 (2024-12-24): Initial version
```

## 🚀 Quick Start

### Finding Prompts
1. Browse by category in the folder structure
2. Use the [Prompt Index](metadata/prompt_index.yaml) for searching
3. Filter by tags in individual prompt files

### Using a Prompt
1. Navigate to the relevant category
2. Read the prompt file completely
3. Check prerequisites and dependencies
4. Copy the prompt from the designated section
5. Provide required inputs as specified
6. Validate output using the checklist

## 📋 Prompt Categories

### Trading
- **Bot Development**: Complete trading bot creation workflow
- **Market Analysis**: Market condition analysis prompts
- **Backtesting**: Strategy validation prompts

[Add other categories...]

## 🏷️ Tagging System
Prompts are tagged for easy discovery:
- `#complexity-beginner` `#complexity-intermediate` `#complexity-advanced`
- `#model-gemini` `#model-claude` `#model-gpt4`
- `#multimodal` `#text-only` `#code-generation`

## 🤝 Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📜 License
[Choose appropriate license - CC BY 4.0 is common for prompts]

## 🔍 Search Tips
Use GitHub search with tags: `#trading filename:*.md`

## ⭐ Featured Prompts
- [Trading Bot Development Master Prompt](trading/bot_development/trading_bot_master_prompt.md)
- [Add other featured prompts]

## 📊 Prompt Quality Standards
All prompts in this repository:
- ✅ Include metadata and version tracking
- ✅ Specify expected outputs
- ✅ Provide validation checklists
- ✅ Include examples where applicable
- ✅ Are tested for hallucination reduction