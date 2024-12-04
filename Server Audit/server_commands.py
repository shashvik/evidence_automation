import paramiko
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import time
import json
import os

def ssh_and_capture_with_sudo(hostname, username, pem_file_path, json_file, output_directory):
    try:
        # Load Commands from JSON File
        with open(json_file, 'r') as f:
            commands = json.load(f)

        # Step 1: Load the PEM File
        key = paramiko.RSAKey.from_private_key_file(pem_file_path)

        # Step 2: Establish SSH Connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username, pkey=key)

        # Step 3: Elevate to Sudo
        sudo_shell = ssh.invoke_shell()
        sudo_shell.send("sudo -i\n")
        time.sleep(1)  # Wait for the privilege escalation to complete
        sudo_shell.recv(1024)  # Consume the output to clear the buffer
        
        # Step 4: Execute Commands and Capture Outputs
        for key, command in commands.items():
            print(f"Executing as sudo: {command}")
            sudo_shell.send(command + "\n")
            time.sleep(2)  # Wait for command execution
            
            # Capture Output
            output = ""
            while sudo_shell.recv_ready():
                output += sudo_shell.recv(4096).decode()

            # Add Hostname and Simulate Terminal Prompt
            simulated_prompt = f"root@{hostname}:~# {command}\n"
            full_output = simulated_prompt + output.strip()

            # Render Command Output as an Image
            terminal_image = create_image_from_text(full_output)

            # Add Timestamp with Black Background
            terminal_image_with_timestamp = add_timestamp_with_background(terminal_image)

            # Save Final Image
            output_image_path = os.path.join(output_directory, f"{key}.png")
            cv2.imwrite(output_image_path, terminal_image_with_timestamp)
            print(f"Screenshot saved to {output_image_path}")

        sudo_shell.close()
        ssh.close()
    
    except Exception as e:
        print(f"An error occurred: {e}")

def create_image_from_text(text):
    # Define Image Dimensions and Font
    width, height = 800, 600
    background_color = "black"
    text_color = "green"
    font = ImageFont.load_default()
    
    # Create a Blank Image
    image = Image.new("RGB", (width, height), color=background_color)
    draw = ImageDraw.Draw(image)
    
    # Word Wrap and Text Positioning
    lines = text.splitlines()
    y_position = 10
    line_spacing = 20
    
    for line in lines:
        draw.text((10, y_position), line, fill=text_color, font=font)
        y_position += line_spacing
        
        # Stop if text exceeds image height
        if y_position > height - line_spacing:
            draw.text((10, y_position), "[Output Truncated]", fill=text_color, font=font)
            break
    
    # Convert PIL Image to OpenCV Format
    open_cv_image = np.array(image)
    return cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

def add_timestamp_with_background(image):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.75
    font_thickness = 2
    
    # Calculate Text Size
    text_size = cv2.getTextSize(timestamp, font, font_scale, font_thickness)[0]
    text_width, text_height = text_size[0], text_size[1]
    
    # Create Black Background for Timestamp
    background = np.zeros((text_height + 10, text_width + 10, 3), dtype=np.uint8)
    cv2.putText(background, timestamp, (5, text_height + 5), font, font_scale, (255, 255, 255), font_thickness)
    
    # Overlay Timestamp on Original Image
    overlay = image.copy()
    x_offset = overlay.shape[1] - background.shape[1] - 10  # Bottom-right corner X
    y_offset = overlay.shape[0] - background.shape[0] - 10  # Bottom-right corner Y
    overlay[y_offset:y_offset+background.shape[0], x_offset:x_offset+background.shape[1]] = background
    
    return overlay


# Example Usage
if __name__ == "__main__":
    # SSH and Command Details
    hostname = "serverip"
    username = "ubuntu"
    pem_file_path = "mypem.pem"  # Path to your .pem file
    json_file = "commands.json"  # Path to the JSON file with commands
    output_directory = "screenshots"  # Directory to save screenshots

    # Ensure Output Directory Exists
    os.makedirs(output_directory, exist_ok=True)

    # Run Function
    ssh_and_capture_with_sudo(hostname, username, pem_file_path, json_file, output_directory)
