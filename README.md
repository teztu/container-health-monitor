# RPE Lift Tracker

A Python-OOP powerlifting tracker with RPE-based e1RM calculations and a Streamlit frontend, with automated CI/CD via GitHub Actions.

## Features

- Log lifts with weight, reps and RPE (6 to 10)
- Automatic e1RM calculation based on RPE chart
- Personal bests per exercise (Squat, Bench, Deadlift)
- Target weight calculator
- Delete incorrect lifts
- Automated code quality checks with Pylint on every push

## Setup

### Prerequisites
- Python 3.8+
- pip

### Installation
```bash
pip install streamlit
```

### Run
```bash
streamlit run rpecalculator.py
```

## CI/CD

Automated Pylint checks run on every push to main via GitHub Actions with a self-hosted runner configured on a local Ubuntu VM (VirtualBox). The pipeline enforces a minimum code quality score to maintain code standards.

## Tech Stack

- Python
- Streamlit
- GitHub Actions
- Ubuntu VM (VirtualBox) - self-hosted runner
