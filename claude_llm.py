import os
import requests
import pandas as pd

# Path to the evidence folder containing screenshots
evidence_folder = "evidence/"

# API endpoint and your API key (replace with actual values)
api_url = "https://api.claude.ai/v1/chat"  # Replace with actual Claude API URL
api_key = "YOUR_API_KEY"  # Replace with your API key

# Define the prompt
prompt = (
    "I am conducting a thorough user access review and need your assistance in analyzing a screenshot from our system's administrator panel. "
    "Please perform the following tasks:\n\n"
    "1. Data Extraction: Carefully analyze the image and extract all relevant user data visible in the screenshot. This should include:\n"
    "- Usernames\n"
    "- Roles\n"
    "- Permissions\n"
    "- Any additional information relevant to user access (e.g., account types, last activity, MFA status).\n\n"
    "2. Tabular Presentation: Present the extracted data in a clear, organized table format. The table should contain the following columns:\n"
    "- User Name\n"
    "- Administrator Type\n"
    "- Account Type\n"
    "- Role\n"
    "- Permission\n"
    "- Last Activity (if visible)\n"
    "- MFA Status (if visible)\n\n"
    "If any fields are empty or not visible in the image, please indicate this explicitly in the table with a placeholder (e.g., 'N/A' or 'Not Visible').\n\n"
    "3. Summary of Observations: After presenting the table, provide a brief summary of any notable patterns, trends, or potential security concerns identified in the user access setup. "
    "Consider aspects such as:\n"
    "- The number of users with elevated privileges or full control.\n"
    "- The distribution of roles across users.\n"
    "- Any instances of redundant or unnecessary permissions that could pose security risks.\n\n"
    "This information will contribute to a comprehensive review of our system's access controls and permissions. "
    "Please ensure that all visible data is accurately transcribed and presented in a clear and concise manner."
)

# Function to send a request to Claude
def call_claude(image_path, prompt):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Prepare the payload
    files = {
        "file": open(image_path, "rb")
    }
    
    data = {
        "prompt": prompt,
        "model": "claude-2",  # or any specific model you need
        "max_tokens": 1500  # Adjust based on expected output
    }

    response = requests.post(api_url, headers=headers, data=data, files=files)
    return response.json()

# Main function to process all screenshots in the evidence folder
def process_screenshots_to_csv(evidence_folder):
    # Iterate over each screenshot in the folder
    for filename in os.listdir(evidence_folder):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            image_path = os.path.join(evidence_folder, filename)
            print(f"Processing: {image_path}")

            # Call Claude with the image and prompt
            result = call_claude(image_path, prompt)

            # Extract results and save to a CSV file
            # Assuming the result has a 'table' field in the expected format
            if 'table' in result:
                df = pd.DataFrame(result['table'])  # Convert the result to a DataFrame
                output_csv = os.path.splitext(filename)[0] + "_user_access_review.csv"  # Create CSV file name
                df.to_csv(output_csv, index=False)  # Save to CSV
                print(f"Results saved to {output_csv}")
            else:
                print("No table found in the response.")

# Run the process
process_screenshots_to_csv(evidence_folder)
