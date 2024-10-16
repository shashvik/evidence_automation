
# evidence_automation

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
