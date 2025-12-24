# Repository Structure

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
