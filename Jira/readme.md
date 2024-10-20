# Jira Compliance Evidence Automation
This Python script automates the extraction of compliance-related evidence from a specified Jira project. It gathers relevant information about tickets, including their details, comments, attachments, worklogs, and changelogs, and saves the data in an Excel file for reporting and compliance purposes.

## Features
Extracts and compiles:

- Ticket key
- Summary
- Created date
- Reporter
- Status
- Comments
- Changelog
- Attachments
- Worklogs

Saves all extracted data into an Excel file for easy reporting.

# Requirements
```Python 3.x
pandas library
requests library
You can install the required libraries using pip:

Copy code
pip install pandas requests
```
## Configuration

Before running the script, you need to configure the following variables in the code:
```
JIRA_BASE_URL: Your Jira instance URL.
PROJECT_KEY: The key of the project you want to extract data from.
USERNAME: Your Jira email address.
API_TOKEN: Your Jira API token.
start_date: The beginning of the date range for fetching tickets.
end_date: The end of the date range for fetching tickets.
python
Copy code
JIRA_BASE_URL = 'https://your-jira-instance.atlassian.net' # Replace with your Jira instance URL
PROJECT_KEY = 'ABC' # Replace with your project key
USERNAME = 'your-email@example.com' # Replace with your Jira email
API_TOKEN = 'your-api-token' # Replace with your Jira API token

# Time period for fetching tickets

start_date = '2024-10-15' # Replace with your desired start date
end_date = '2024-10-17' # Replace with your desired end date
```
## Usage
```
Clone or download this repository.
Update the configuration variables in the script.
Run the script using Python:
Copy code
python jira_evidence_automation.py
After execution, check the generated jira_compliance_tickets.xlsx file for the compliance evidence.
```
## Output
The script generates an Excel file named jira_compliance_tickets.xlsx containing the following columns:

- Ticket Key: The unique identifier for the ticket.
- Summary: A brief description of the ticket.
- Created: The date the ticket was created.
- Reporter: The user who reported the ticket.
- Status: The current status of the ticket.
- Comments: All comments associated with the ticket, concatenated for readability.
- Changelog: A summary of changes made to the ticket.
- Attachments: Any attachments related to the ticket.
- Worklog: Entries related to time spent on the ticket.
