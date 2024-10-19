import requests
from requests.auth import HTTPBasicAuth
import pandas as pd


# Jira API endpoint and project details
JIRA_BASE_URL = 'https://your-jira-instance.atlassian.net'
PROJECT_KEY = 'ABC'  # Replace with your project key
USERNAME = 'your-email@example.com'  # Replace with your Jira email
API_TOKEN = 'your-api-token'  # Replace with your Jira API token

# Time period for fetching tickets
start_date = '2024-10-15'
end_date = '2024-10-17'

# Jira JQL query to filter tickets by project and date range
jql = f'project = {PROJECT_KEY} AND created >= "{start_date}" AND created <= "{end_date}"'

# API URL with JQL query
url = f'{JIRA_BASE_URL}/rest/api/2/search'

# Query parameters to extract additional evidence like comments, attachments, etc.
params = {
    'jql': jql,
    'maxResults': 100,
    'fields': 'key,summary,created,reporter,status,comment,changelog,attachment,worklog'
}

# Authentication
auth = HTTPBasicAuth(USERNAME, API_TOKEN)

# Send request to Jira API
response = requests.get(url, auth=auth, params=params)

# Check if successful
if response.status_code == 200:
    tickets = response.json()
    issues = tickets['issues']
    
    # Prepare data for Excel
    data = []
    for issue in issues:
        key = issue['key']
        summary = issue['fields']['summary']
        created = issue['fields']['created']
        reporter = issue['fields']['reporter']['displayName']
        status = issue['fields']['status']['name']
        
        # Handle comments (flatten the comment text)
        if 'comment' in issue['fields'] and issue['fields']['comment']['total'] > 0:
            comments = [comment['body'] for comment in issue['fields']['comment']['comments']]
            comments_text = '\n'.join(comments)  # Concatenate comments with a newline for readability
        else:
            comments_text = ''
        
        # Handle changelog (if you want to extract specific details, like status changes)
        if 'changelog' in issue and 'histories' in issue['changelog']:
            changelog_entries = [f"{history['created']} - {', '.join([item['field'] for item in history['items']])}" 
                                 for history in issue['changelog']['histories']]
            changelog_text = '\n'.join(changelog_entries)
        else:
            changelog_text = ''
        
        # Handle attachments
        if 'attachment' in issue['fields'] and len(issue['fields']['attachment']) > 0:
            attachments = [attachment['filename'] for attachment in issue['fields']['attachment']]
            attachments_text = ', '.join(attachments)
        else:
            attachments_text = ''
        
        # Handle worklogs (sum the time spent or show worklog entries)
        if 'worklog' in issue['fields'] and issue['fields']['worklog']['total'] > 0:
            worklog_entries = [f"{worklog['author']['displayName']} - {worklog['timeSpent']}" 
                               for worklog in issue['fields']['worklog']['worklogs']]
            worklog_text = '\n'.join(worklog_entries)
        else:
            worklog_text = ''

        # Add relevant fields to the data list
        data.append([
            key, summary, created, reporter, status, 
            comments_text, changelog_text, attachments_text, worklog_text
        ])
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=['Ticket Key', 'Summary', 'Created', 'Reporter', 'Status', 
                                     'Comments', 'Changelog', 'Attachments', 'Worklog'])
    
    # Write to Excel
    df.to_excel('jira_compliance_tickets.xlsx', index=False)
    
    print('Jira compliance tickets written to jira_compliance_tickets.xlsx')
else:
    print(f'Failed to fetch tickets: {response.status_code}, {response.text}')
