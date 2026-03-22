# LLM JSON Benchmark Tool

A Python-based system to evaluate Large Language Models (LLMs) for structured JSON output reliability, validation, and hallucination detection.

## Table of Contents
- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Demo](#demo)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## About
This project benchmarks LLMs like Ollama Mini for structured JSON output. It is designed to:
- Measure JSON validity and schema compliance
- Detect hallucinations in model responses
- Generate reliability scores for multiple runs
- Support dynamic testing for real-world scenarios

It’s a professional tool for testing LLM outputs before deployment in applications requiring structured data.

## Features
- Validate JSON output against predefined schema
- Detect hallucinations in LLM responses
- Run multiple iterations and generate reliability metrics
- Support dynamic and static input testing
- Generate detailed reports in `reports/` folder

## Installation
1. Clone the repository
```bash
git clone https://github.com/pranjalik2004/LLM_JSON_Project.git
cd LLM_JSON_Project
Create a Python virtual environment

python -m venv venv
Activate the virtual environment

Windows: venv\Scripts\activate

Linux/Mac: source venv/bin/activate

Install dependencies

pip install -r requirements.txt
Usage
Run the benchmarking script:

python benchmark.py
Check sample model output:

python -m app.main
Example JSON output:

{
  "name": "John Doe",
  "age": 21,
  "course": "Computer Science"
}
View benchmark reports:
Reports are automatically saved in the reports/ folder. Includes JSON validation results, hallucination stats, and reliability scores.

Dynamic Input Testing:
Modify benchmark_inputs.json to test custom scenarios.

Demo
Add screenshots or GIFs here (optional but recommended)

Technologies Used
Python 3.9+ – Core language

Pandas – Data handling and reporting

JSON Schema – Output validation

Ollama API – LLM server for testing

Project Structure
LLM_JSON_Project/
├─ README.md
├─ benchmark.py
├─ prompt_engine.py
├─ app/
│  ├─ __init__.py
│  └─ main.py
├─ benchmark_inputs.json
├─ reports/
├─ requirements.txt
└─ .gitignore

