# AWS IAM Table Scraper

A Python script that scrapes IAM service tables from AWS documentation and converts them to markdown format.

I really don't know what I'm doing in Python.

## Setup

### Prerequisites
- Python 3.x

### Running

1. Clone this repository

2. Create a virtual environment:
```bash
python3 -m venv .venv
```

3. Activate the virtual environment:
```bash
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script:
```bash
python main.py
```

The script will:
1. Fetch the AWS IAM documentation page
2. Extract the specified table
3. Convert it to markdown format
4. Save the result to `aws_iam_table.md`

## Updating Dependencies

To update the locked dependency versions:

1. Ensure your virtual environment is activated
2. Update all packages to their latest versions:
```bash
pip install --upgrade requests beautifulsoup4
```

3. Generate a new requirements.txt with the updated versions:
```bash
pip freeze > requirements.txt
```

4. Review the changes to requirements.txt and commit them if everything works as expected:
```bash
git diff requirements.txt  # Review changes
git add requirements.txt
git commit -m "chore: update dependencies"
```