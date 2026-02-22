# Container Health Monitor

A Python-based project for monitoring container health, featuring a self-hosted GitHub Actions CI/CD pipeline and an RPE-based powerlifting tracker.

## Features

- Automated code quality checks with Pylint via GitHub Actions
- Self-hosted runner on Ubuntu VM
- RPE Calculator with Streamlit frontend
- OOP-based lift tracking with e1RM calculations

## Setup

### Prerequisites
- Python 3.8+
- pip

### Installation
```bash
pip install -r requirements.txt
```

### Run RPE Calculator
```bash
streamlit run rpecalculator.py
```

## CI/CD

This project uses GitHub Actions with a self-hosted runner for automated Pylint checks on every push to main.

## Tech Stack

- Python
- Streamlit
- GitHub Actions
- Ubuntu (self-hosted runner)
