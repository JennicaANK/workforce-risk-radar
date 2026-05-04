# workforce-risk-radar
Multimodal early warning system for workforce layoff trends using WARN, FRED, and GDELT data.

## Overview
This project builds a multimodal early warning system for workforce layoff trends in California using:

- California WARN Act layoff records
- FRED macroeconomic indicators
- Indeed job postings data
- GDELT news sentiment data

The objective is to identify leading indicators that precede increases in mass layoffs.

## Team Members
- Athish Kumar
- Aye Nyein Kyaw
- Lila Nguyen

# Workforce Risk Radar

## 1. Project Summary

Workforce Risk Radar is a data science dashboard that identifies early warning signals for workforce layoff risk in California. The project integrates multiple data sources—including WARN layoff notices, macroeconomic indicators, job posting trends, and news sentiment—to estimate monthly layoff risk.

The system processes raw data into structured features, applies predictive modeling, and presents results through an interactive Dash web application. The dashboard enables users to explore trends, understand modeling decisions, and interpret predicted risk levels.

---

## 2. Setup Instructions

### Requirements

- Python 3.9+
- pip

### Install Dependencies

```bash
git clone https://github.com/JennicaANK/workforce-risk-radar.git
cd workforce-risk-radar

python -m venv venv
source venv/bin/activate   # Mac/Linux
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

## 3. End-to-End Pipeline

Data Sources
   |
   |-- WARN Act Layoff Data (California)
   |-- FRED Macroeconomic Indicators
   |-- Indeed Job Postings Data
   |-- GDELT News Sentiment Data
   |
Data Processing (notebooks/)
   |
   |-- Cleaning WARN data
   |-- Building monthly dataset
   |-- Generating news sentiment features
   |-- Integrating external datasets
   |-- Feature engineering (lags)
   |
Modeling
   |
   |-- Train/test split (time-based)
   |-- Model experimentation
   |-- Final model selection
   |
Outputs (data/processed/)
   |
   |-- master_monthly.csv
   |-- final_predictions.csv
   |-- final_risk_scores.csv
   |-- metrics & coefficients
   |
Dashboard (app/)
   |
   |-- Loads processed data
   |-- Displays EDA, methods, and results

## 4. Repository Structure & Key Code Locations

workforce-risk-radar/
│
├── app/
│   ├── app.py                # Main Dash application
│   ├── pages/                # Dashboard pages
│   ├── utils/
│   │   └── data_loader.py    # Loads processed data
│   └── assets/               # CSS styling
│
├── data/
│   ├── raw/                  # Original datasets
│   ├── interim/              # Intermediate data
│   └── processed/            # Final model outputs
│
├── notebooks/                # Data pipeline & modeling
│   ├── 01_build_master_monthly.ipynb     # Constructs main dataset
│   ├── 02_gdelt_news_signal.ipynb        # Builds news sentiment features
│   ├── 03_warn_processing.ipynb          # Cleans WARN layoff data
│   ├── 04_kaggle_tech_layoffs.ipynb      # External layoffs dataset integration
│   ├── 05_WARN.ipynb                     # Additional WARN analysis
│   ├── 06_preliminary_results.ipynb      # Early modeling + insights
│   ├── 07_final_modeling.ipynb           # Final model training
│   └── 07_final_modeling-Copy1.ipynb     # Alternate/backup modeling version
│
├── requirements.txt
├── README.md
└── LICENSE
