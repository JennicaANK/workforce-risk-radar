# Workforce Risk Radar

Multimodal early warning dashboard for California workforce layoff trends using WARN, FRED, GDELT, and layoff dataset features.

## Overview

Workforce Risk Radar is a data science project that estimates monthly layoff risk in California. It combines public layoff notices, macroeconomic indicators, and news signals into a modeling pipeline, then presents the results in an interactive Dash dashboard.

The dashboard lets users review the project objective, explore EDA, inspect analysis methods, view major findings, and compare actual WARN layoffs against model predictions.

## Team Members

- Athish Kumar
- Aye Nyein Kyaw
- Lila Nguyen

## Data Sources

- California WARN Act layoff records
- FRED macroeconomic indicators
- GDELT news volume and tone signals
- Kaggle tech layoffs dataset

## Repository Structure

```text
workforce-risk-radar/
├── app/
│   ├── app.py                    # Dash application entry point
│   ├── app.yaml                  # Deployment configuration
│   ├── requirements.txt          # Python dependencies for the app
│   ├── assets/
│   │   └── style.css             # Dashboard styling
│   ├── pages/                    # Dash pages
│   │   ├── home.py
│   │   ├── objective.py
│   │   ├── eda.py
│   │   ├── analysis_methods.py
│   │   ├── major_findings.py
│   │   └── live_demo.py
│   ├── utils/
│   │   └── data_loader.py        # Helpers for loading processed CSV outputs
│   └── data/
│       ├── raw/                  # Source data snapshots
│       ├── interim/              # Extracted/intermediate WARN tables
│       └── processed/            # Final modeling outputs used by the dashboard
├── notebooks/
│   ├── 01_build_master_monthly.ipynb
│   ├── 02_gdelt_news_signal.ipynb
│   ├── 03_warn_processing.ipynb
│   ├── 04_kaggle_tech_layoffs.ipynb
│   ├── 05_WARN.ipynb
│   ├── 06_preliminary_results.ipynb
│   ├── 07_final_modeling.ipynb
│   └── data/processed/           # Notebook-side processed exports
├── data/                         # Root-level data folder
├── LICENSE
└── README.md
```

## Setup

### Requirements

- Python 3.9+
- pip

### Install Dependencies

```bash
git clone https://github.com/JennicaANK/workforce-risk-radar.git
cd workforce-risk-radar

python -m venv venv
source venv/bin/activate

pip install -r app/requirements.txt
```

On Windows, activate the virtual environment with:

```bash
venv\Scripts\activate
```

## Run the Dashboard

```bash
cd app
python app.py
```

The app runs locally in debug mode. Open the local URL printed in the terminal, typically `http://127.0.0.1:8050/`.

## Pipeline

```text
Data Sources
   |
   |-- California WARN layoff records
   |-- FRED macroeconomic indicators
   |-- GDELT news tone and volume features
   |-- Kaggle tech layoffs dataset
   |
Data Processing and Feature Engineering
   |
   |-- Clean WARN records
   |-- Build monthly layoff dataset
   |-- Create GDELT news features
   |-- Add macroeconomic indicators
   |-- Generate lagged model features
   |
Modeling
   |
   |-- Time-based train/test split
   |-- Model comparison
   |-- Final model selection
   |-- Risk level assignment
   |
Dashboard Outputs
   |
   |-- master_monthly.csv
   |-- final_predictions.csv
   |-- final_risk_scores.csv
   |-- model metrics
   |-- coefficients and feature importance
```

## Key App Files

- `app/app.py`: creates the Dash app, registers pages, and builds the navigation.
- `app/pages/home.py`: landing dashboard with latest risk level and actual-vs-predicted layoffs.
- `app/pages/eda.py`: exploratory visualizations.
- `app/pages/analysis_methods.py`: modeling and methodology page.
- `app/pages/major_findings.py`: final results and interpretation.
- `app/pages/live_demo.py`: interactive demo view.
- `app/utils/data_loader.py`: loads processed CSV files from `app/data/processed/`.

## Key Processed Outputs

- `app/data/processed/master_monthly.csv`: final monthly modeling dataset.
- `app/data/processed/final_predictions.csv`: actual and predicted WARN layoff values.
- `app/data/processed/final_risk_scores.csv`: predicted layoffs with assigned risk levels.
- `app/data/processed/regression_metrics.csv`: regression model performance.
- `app/data/processed/classification_metrics.csv`: risk-level classification metrics.
- `app/data/processed/final_model_coefficients.csv`: final model coefficients.
- `app/data/processed/feature_importance.csv`: feature importance output.
