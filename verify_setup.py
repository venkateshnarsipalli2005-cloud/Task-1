#!/usr/bin/env python3
"""
Project Initialization & Verification Script
Validates all project files are in place
"""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

REQUIRED_FILES = {
    "Documentation": [
        "README.md",
        "GETTING_STARTED.md",
        "POWERBI_GUIDE.md",
        "PROJECT_DOCUMENTATION.md",
    ],
    "Configuration": [
        "config.py",
        "requirements.txt",
        ".gitignore",
    ],
    "Notebooks": [
        "notebooks/01_data_exploration.ipynb",
        "notebooks/02_feature_engineering.ipynb",
        "notebooks/03_model_training.ipynb",
        "notebooks/04_forecasting_analysis.ipynb",
    ],
    "Scripts": [
        "scripts/data_loader.py",
        "scripts/feature_engineer.py",
        "scripts/forecast_pipeline.py",
    ],
    "Directory Structure": [
        "data/raw/README.md",
        "data/processed/README.md",
        "outputs/README.md",
        "dashboards/README.md",
    ]
}

EXPECTED_DIRECTORIES = [
    "notebooks",
    "scripts",
    "data",
    "data/raw",
    "data/processed",
    "outputs",
    "dashboards",
]


def check_files():
    """Verify all required files exist"""
    print("\n" + "="*60)
    print("PROJECT STRUCTURE VERIFICATION")
    print("="*60)
    
    all_present = True
    
    for category, files in REQUIRED_FILES.items():
        print(f"\n📁 {category}")
        print("-" * 60)
        
        for file_path in files:
            full_path = PROJECT_ROOT / file_path
            exists = full_path.exists()
            status = "✅" if exists else "❌"
            print(f"  {status} {file_path}")
            
            if not exists:
                all_present = False
    
    return all_present


def check_directories():
    """Verify all required directories exist"""
    print("\n📂 Directory Structure")
    print("-" * 60)
    
    all_present = True
    
    for dir_path in EXPECTED_DIRECTORIES:
        full_path = PROJECT_ROOT / dir_path
        exists = full_path.exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {dir_path}/")
        
        if not exists:
            all_present = False
    
    return all_present


def print_next_steps():
    """Print next steps for user"""
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    
    steps = [
        ("1️⃣", "Read GETTING_STARTED.md for setup instructions"),
        ("2️⃣", "Create virtual environment: python -m venv venv"),
        ("3️⃣", "Activate environment: source venv/bin/activate"),
        ("4️⃣", "Install dependencies: pip install -r requirements.txt"),
        ("5️⃣", "Prepare data in data/raw/ folder"),
        ("6️⃣", "Open Jupyter: jupyter notebook"),
        ("7️⃣", "Run notebooks in order (01 → 02 → 03 → 04)"),
        ("8️⃣", "Import outputs/powerbi_data.csv to Power BI"),
        ("9️⃣", "Follow POWERBI_GUIDE.md for dashboard creation"),
        ("🔟", "Share results with stakeholders"),
    ]
    
    for emoji, step in steps:
        print(f"  {emoji} {step}")


def print_project_structure():
    """Print complete project structure"""
    print("\n" + "="*60)
    print("PROJECT STRUCTURE")
    print("="*60)
    
    structure = """
task-1/
├── 📄 README.md                          # Main documentation
├── 📄 GETTING_STARTED.md                 # Setup guide
├── 📄 POWERBI_GUIDE.md                   # Dashboard instructions
├── 📄 PROJECT_DOCUMENTATION.md           # Complete documentation
├── 🔧 config.py                          # Configuration file
├── 📋 requirements.txt                   # Python dependencies
├── 🚫 .gitignore                         # Git ignore rules
│
├── 📚 notebooks/                         # Jupyter Notebooks
│   ├── 01_data_exploration.ipynb         # EDA & data validation
│   ├── 02_feature_engineering.ipynb      # Create 50+ features
│   ├── 03_model_training.ipynb           # Train 3 forecasting models
│   └── 04_forecasting_analysis.ipynb     # Generate forecasts & insights
│
├── 🐍 scripts/                           # Python modules
│   ├── data_loader.py                    # Data loading utilities
│   ├── feature_engineer.py               # Feature engineering
│   └── forecast_pipeline.py              # Complete pipeline
│
├── 💾 data/                              # Data directory
│   ├── raw/                              # Raw CSV files
│   │   └── README.md                     # Data instructions
│   └── processed/                        # Engineered features
│       └── README.md
│
├── 📊 outputs/                           # Results & exports
│   ├── *.png                             # Visualizations
│   ├── *.csv                             # Data exports
│   ├── *.json                            # Analysis results
│   └── README.md
│
└── 📈 dashboards/                        # Power BI files
    └── README.md
    """
    
    print(structure)


def main():
    """Main verification routine"""
    print("\n🚀 Retail Sales Forecasting Project - Initialization")
    
    # Check files
    files_ok = check_files()
    
    # Check directories
    dirs_ok = check_directories()
    
    # Print structure
    print_project_structure()
    
    # Print status
    print("\n" + "="*60)
    if files_ok and dirs_ok:
        print("✅ PROJECT SETUP COMPLETE")
        print("="*60)
    else:
        print("⚠️  SETUP INCOMPLETE")
        print("="*60)
        print("\nPlease ensure all files and directories are in place.")
    
    # Print next steps
    print_next_steps()
    
    # Print features
    print("\n" + "="*60)
    print("KEY FEATURES")
    print("="*60)
    features = [
        "✨ 4 comprehensive Jupyter notebooks",
        "📊 3 advanced forecasting models (Prophet, ARIMA, XGBoost)",
        "🔧 Reusable Python modules for data & forecasting",
        "📈 50+ engineered time series features",
        "💼 Power BI integration ready",
        "📋 Complete documentation & guides",
        "🎯 Business insights & recommendations",
        "🚀 Production-ready code",
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    print("\n" + "="*60)
    print("Happy Forecasting! 📊🚀")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
