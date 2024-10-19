import requests
import pandas as pd

# GitHub API base URL and repository details
GITHUB_BASE_URL = 'https://api.github.com'
REPO_OWNER = 'your-organization'  # Replace with your organization or username
REPO_NAME = 'your-repository'      # Replace with your repository name
TOKEN = 'your-github-token'        # Replace with your GitHub token

# Headers for authentication
headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

# Helper function to fetch and format data
def fetch_data(url, params=None):
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data from {url}. Status Code: {response.status_code}")
        print(f"Response: {response.text}")  # Print the response text for debugging
        return None

# Initialize a Pandas Excel writer
with pd.ExcelWriter('github_compliance_evidence.xlsx', engine='openpyxl') as writer:

    # 1. Commits
    commits_url = f'{GITHUB_BASE_URL}/repos/{REPO_OWNER}/{REPO_NAME}/commits'
    commits = fetch_data(commits_url)
    if commits:
        commit_data = [[commit['sha'], commit['commit']['message'], commit['commit']['author']['name'], commit['commit']['author']['date']] for commit in commits]
        commit_df = pd.DataFrame(commit_data, columns=['Commit SHA', 'Message', 'Author', 'Date'])
        commit_df.to_excel(writer, sheet_name='Commits', index=False)

    # 2. Pull Requests
    prs_url = f'{GITHUB_BASE_URL}/repos/{REPO_OWNER}/{REPO_NAME}/pulls?state=all'
    pull_requests = fetch_data(prs_url)
    if pull_requests:
        pr_data = [[pr['number'], pr['title'], pr['user']['login'], pr['state'], pr['created_at'], pr.get('merged_at')] for pr in pull_requests]
        pr_df = pd.DataFrame(pr_data, columns=['PR Number', 'Title', 'User', 'State', 'Created At', 'Merged At'])
        pr_df.to_excel(writer, sheet_name='Pull Requests', index=False)

    # 3. Issues
    issues_url = f'{GITHUB_BASE_URL}/repos/{REPO_OWNER}/{REPO_NAME}/issues'
    issues = fetch_data(issues_url)
    if issues:
        issue_data = [[issue['number'], issue['title'], issue['user']['login'], issue['state'], issue['created_at']] for issue in issues]
        issue_df = pd.DataFrame(issue_data, columns=['Issue Number', 'Title', 'User', 'State', 'Created At'])
        issue_df.to_excel(writer, sheet_name='Issues', index=False)

    # 4. Branch Protection Rules
    branch_protection_url = f'{GITHUB_BASE_URL}/repos/{REPO_OWNER}/{REPO_NAME}/branches/main/protection'
    branch_protection = fetch_data(branch_protection_url)
    if branch_protection:
        protection_data = [
            [
                branch_protection['required_pull_request_reviews']['required_approving_review_count'],
                branch_protection['enforce_admins']['enabled'],
                branch_protection['required_status_checks']['contexts'],
            ]
        ]
        branch_protection_df = pd.DataFrame(protection_data, columns=['Required Approvals', 'Enforce Admins', 'Required Status Checks'])
        branch_protection_df.to_excel(writer, sheet_name='Branch Protection', index=False)
    else:
        print('Branch protection not found.')

    # 5. Security Alerts (Dependabot)
    security_alerts_url = f'{GITHUB_BASE_URL}/repos/{REPO_OWNER}/{REPO_NAME}/vulnerability-alerts'
    security_alerts = fetch_data(security_alerts_url)
    if security_alerts:
        alert_data = [[alert['id'], alert['affected_package_name'], alert['severity'], alert['created_at']] for alert in security_alerts]
        alert_df = pd.DataFrame(alert_data, columns=['Alert ID', 'Package', 'Severity', 'Created At'])
        alert_df.to_excel(writer, sheet_name='Security Alerts', index=False)
    else:
        print('No security alerts found.')

    # 6. Code Scanning Alerts
    code_scanning_url = f'{GITHUB_BASE_URL}/repos/{REPO_OWNER}/{REPO_NAME}/code-scanning/alerts'
    code_scanning_alerts = fetch_data(code_scanning_url)
    if code_scanning_alerts:
        code_alert_data = [[alert['rule']['id'], alert['rule']['description'], alert['tool']['name'], alert['state']] for alert in code_scanning_alerts]
        code_alert_df = pd.DataFrame(code_alert_data, columns=['Rule ID', 'Description', 'Tool', 'State'])
        code_alert_df.to_excel(writer, sheet_name='Code Scanning', index=False)
    else:
        print('No code scanning alerts found.')

    # 7. Repository Access (Collaborators)
    collaborators_url = f'{GITHUB_BASE_URL}/repos/{REPO_OWNER}/{REPO_NAME}/collaborators'
    collaborators = fetch_data(collaborators_url)
    if collaborators:
        collaborator_data = [[collab['login'], collab['permissions']] for collab in collaborators]
        collaborator_df = pd.DataFrame(collaborator_data, columns=['Collaborator', 'Permissions'])
        collaborator_df.to_excel(writer, sheet_name='Collaborators', index=False)

    # 8. Repository Settings
    repo_settings_url = f'{GITHUB_BASE_URL}/repos/{REPO_OWNER}/{REPO_NAME}'
    repo_settings = fetch_data(repo_settings_url)
    if repo_settings:
        settings_data = [[repo_settings['name'], repo_settings['visibility'], repo_settings['fork'], repo_settings['archived']]]
        settings_df = pd.DataFrame(settings_data, columns=['Repo Name', 'Visibility', 'Fork Enabled', 'Archived'])
        settings_df.to_excel(writer, sheet_name='Repository Settings', index=False)

    # 9. Workflow Runs (CI/CD)
    workflow_runs_url = f'{GITHUB_BASE_URL}/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs'
    workflow_runs = fetch_data(workflow_runs_url)
    if workflow_runs:
        run_data = [[run['id'], run['name'], run['status'], run['conclusion'], run['created_at']] for run in workflow_runs['workflow_runs']]
        run_df = pd.DataFrame(run_data, columns=['Run ID', 'Workflow Name', 'Status', 'Conclusion', 'Created At'])
        run_df.to_excel(writer, sheet_name='CICD Runs', index=False)

print('GitHub compliance evidence written to github_compliance_evidence.xlsx')
