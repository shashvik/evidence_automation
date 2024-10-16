
# evidence_automation
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Instructions:
This automation system is used to help take screenshots for evidence collection, and add a system timestamp to it, this will reduce efforts while executing evidence collection for aws and other resources.

Steps:

Step 1: Make sure you have python3 and pip3 installed on your machine.
step2:  Copy the contents of this folder to a location of your choice and run the below from this path in your terminal:

        pip3 install -r requirements.txt
Step3: Close all instances of google chrome and run the below from your terminal:

        /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

Step 4: Make sure you have logged into whatever application you want to retrieve evidence from( say you want aws, then make sure you are the aws session on the browser that comes up from the previous command is valid( you can use myaccess to start it))

Step 5: Run Evidence_automation.py

Step 6: Al evidence you be placed in the evidence folder with appropriate names.

Note: If you want to modify or add some more evidence then simply add them to the "urls.json" file with the "evidence_name:actual_url" structure.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Now that you have the Evidence screenshots in the /Evidence folder use an LLM with OCR capabilities to extract the relavent information to conduct user access reviews as well.

Here is a sample prompt that can be used to do this:
Start Prompt:

"I'm conducting a user access review and need to extract information from a screenshot of our system's administrator panel. Please analyze the image and provide the following:

Extract all user data visible in the screenshot, including usernames, roles, permissions, and any other relevant information.
Present this data in a clear, tabular format. The table should have columns for each piece of information (e.g., User Name, Administrator type, Account type, Role, Permission, etc.).
If any fields are empty or not visible in the image, please indicate this in the table.
After presenting the table, briefly summarize any notable patterns or potential security concerns you observe in the user access setup (e.g., number of users with full control, distribution of roles, etc.).

This information will be used for a comprehensive review of our system's access controls and permissions. Please ensure all visible data is accurately transcribed."

End Prompt

Use this promt in conjunction with a script to send the screenshots to the LLM witht hsi prompt and download the results into named csv files.
