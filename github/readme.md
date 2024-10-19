# GitHub Compliance Evidence Automation
This Python script automates the extraction of compliance-related evidence from a specified GitHub repository. The script gathers various data points, including commit history, pull requests, issues, branch protection rules, security alerts, and workflow runs, and saves the information in an Excel file for easy reporting and compliance purposes.

## Features
Extracts and compiles:

## Commit history
Pull requests and issues (combined)
Branch protection rules
Security alerts (Dependabot)
Code scanning alerts
CI/CD workflow runs
Repository collaborators
Repository settings
Saves all extracted data into an Excel file with multiple sheets.

## Requirements
Python 3.x
pandas library
openpyxl library
requests library
You can install the required libraries using pip:


```Copy code
pip install pandas openpyxl requests
Configuration
Before running the script, you need to configure the following variables in the code:


REPO_OWNER: Your GitHub username or organization name.
REPO_NAME: The name of the repository you want to extract data from.
TOKEN: Your GitHub personal access token with appropriate permissions (at least repo scope for private repositories).
python
Copy code
REPO_OWNER = 'your-organization'  # Replace with your organization or username
REPO_NAME = 'your-repository'      # Replace with your repository name
TOKEN = 'your-github-token'        # Replace with your GitHub token
```

## Usage
```Clone or download this repository.
Update the configuration variables in the script.
Run the script using Python:
bash
Copy code
python github_evidence_automation.py

After execution, check the generated github_compliance_evidence.xlsx file for the compliance evidence.
```
## Output
The script generates an Excel file named github_compliance_evidence.xlsx containing multiple sheets with the following data:

- Commits: Detailed commit history.
- Pull Requests: Information about all pull requests (including closed).
- Issues: List of issues, including whether they are pull requests.
- Branch Protection: Details about branch protection rules.
- Security Alerts: Any security alerts from Dependabot.
- Code Scanning: Results of code scanning alerts.
- Collaborators: List of repository collaborators and their permissions.
- Repository Settings: Basic settings of the repository.
- CICD Runs: Information about CI/CD workflow runs.
