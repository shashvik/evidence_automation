import pytesseract
from PIL import Image
import re
import pandas as pd
import os

# Path to the evidence folder containing screenshots
evidence_folder = "evidence/"

# Path to Tesseract executable (adjust path if necessary)
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# Function to extract text from the image
def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

# Function to process extracted text and filter relevant user details
def process_text_to_user_details(text):
    # Updated regex pattern to capture user details more accurately
    user_pattern = re.compile(
        r"(\S+@\S+|\S+-\S+)\s+\/\s+(\d+|0)\s+(\S+)\s+(\S+)\s+(\S+)?\s*(\S+)?\s*(AKIA\w{16})?\s*(\d+)?"
    )
    users = []

    # Split text by lines and filter using regex
    lines = text.split('\n')
    for line in lines:
        match = user_pattern.search(line)  # Use search for flexibility
        if match:
            username = match.group(1)
            path = '/'
            group = match.group(2) if match.group(2) else '0'
            last_activity = match.group(3) if match.group(3) else '-'
            mfa = match.group(4) if match.group(4) else '-'
            password_age = match.group(5) if match.group(5) else '-'
            console_last_signin = match.group(6) if match.group(6) else '-'
            access_key_id = f"Active-{match.group(7)}" if match.group(7) else '-'
            active_key_age = match.group(8) if match.group(8) else '-'
            users.append({
                "User Name": username,
                "Path": path,
                "Group": group,
                "Last Activity": last_activity,
                "MFA": mfa,
                "Password Age": password_age,
                "Console Last Sign-in": console_last_signin,
                "Access Key ID": access_key_id,
                "Active Key Age": active_key_age
            })
    
    return users

# Main function to process all screenshots in the evidence folder
def process_screenshots_to_excel(evidence_folder):
    all_user_details = []

    # Iterate over each screenshot in the folder
    for filename in os.listdir(evidence_folder):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            image_path = os.path.join(evidence_folder, filename)
            print(f"Processing: {image_path}")

            # Extract text from image
            extracted_text = extract_text_from_image(image_path)
            print(f"Extracted Text: {extracted_text}")  # Debugging output

            # Extract user details from text
            user_details = process_text_to_user_details(extracted_text)

            # Check if any user details were found
            if user_details:
                print(f"Found user details: {user_details}")  # Debugging output
            else:
                print("No user details found.")  # Debugging output

            # Append details to the overall list
            all_user_details.extend(user_details)

    # Convert all user details to a DataFrame and save to Excel
    if all_user_details:  # Ensure there are details to save
        df = pd.DataFrame(all_user_details)
        output_excel = "user_access_review_filtered.xlsx"
        df.to_excel(output_excel, index=False)
        print(f"User details have been extracted and saved to {output_excel}")
    else:
        print("No user details were extracted from any images.")

# Run the process
process_screenshots_to_excel(evidence_folder)
