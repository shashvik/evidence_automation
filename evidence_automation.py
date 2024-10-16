import time
import json
import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set Chrome options to connect to an existing Chrome session
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Set up Selenium webdriver with Chrome options
driver = webdriver.Chrome(options=chrome_options)

# Read URLs from JSON file
with open("urls.json", "r") as file:
    urls = json.load(file)

# Define function to add timestamp with black background
def add_timestamp_with_background(image):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.75
    font_thickness = 2
    text_size = cv2.getTextSize(timestamp, font, font_scale, font_thickness)[0]
    text_width, text_height = text_size[0], text_size[1]
    background = np.zeros((text_height + 10, text_width + 10, 3), dtype=np.uint8)
    cv2.putText(background, timestamp, (5, text_height+5), font, font_scale, (255, 255, 255), font_thickness)
    overlay = image.copy()
    x_offset = overlay.shape[1] - background.shape[1] - 10  # Adjusted for bottom right position
    y_offset = overlay.shape[0] - background.shape[0] - 10  # Adjusted for bottom right position
    overlay[y_offset:y_offset+background.shape[0], x_offset:x_offset+background.shape[1]] = background
    alpha = 1
    cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

# Iterate over each URL and take a screenshot
for screenshot_name, url in urls.items():
    # Navigate to the specified URL
    driver.get(url)

    # Wait for the page to load (you can adjust the sleep time based on the loading time of the website)
    time.sleep(5)

    # Take a screenshot
    screenshot_path = f"{screenshot_name}_screenshot.png"
    screenshot_path = "evidence/"+screenshot_path
    print(screenshot_path)
    driver.save_screenshot(screenshot_path)

    # Open the screenshot using OpenCV
    img = cv2.imread(screenshot_path)

    # Add timestamp with black background to the screenshot
    add_timestamp_with_background(img)

    # Save the modified screenshot
    cv2.imwrite(screenshot_path, img)

# Close the browser
driver.quit()
