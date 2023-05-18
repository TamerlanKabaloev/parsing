import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image
import pytesseract
import hashlib
import os
import requests
import json

pytesseract.pytesseract.tesseract_cmd = r'C:\\\Program Files\\\Tesseract-OCR\\\tesseract.exe'
# Set the path to the downloaded ChromeDriver executable
driver_path = 'chromedriver2.exe' 

# Set up the Chrome driver
service = Service(driver_path)
options = Options()

# Adjust the zoom level by 10%
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--force-device-scale-factor=0.9")
options.add_argument("--disable-blink-features=AutomationControlled")

# Set the website URL
url = 'YOUR TARGET WEBSITE'

# Set the directory to save text results
results_dir = 'text_results'

# Create the results directory if it doesn't exist
os.makedirs(results_dir, exist_ok=True)

# Telegram bot settings
telegram_token = 'YOUR TOKEN'
chat_id = 'YOUR CHAT_ID'

# Function to send a Telegram message to the group chat
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
    params = {'chat_id': chat_id, 'text': message}
    response = requests.get(url, params)
    if response.status_code == 200:
        print('Telegram message sent successfully.')
    else:
        print('Failed to send Telegram message.')

# Function to extract text from the screenshot using OCR
def extract_text_from_screenshot(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='rus')
    return text

# Function to save text results to a file
def save_text_results(text):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f'{results_dir}/{timestamp}.txt'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f'Text results saved to: {filename}')

# Function to check if the text has changed
def has_text_changed(text):
    yesterday = datetime.now() - timedelta(minutes=1)
    yesterday_file = f'{results_dir}/{yesterday.strftime("%Y-%m-%d_%H-%M-%S")}.txt'
    if not os.path.isfile(yesterday_file):
        return True
    with open(yesterday_file, 'r', encoding='utf-8') as file:
        old_text = file.read()
    return hashlib.md5(text.encode('utf-8')).hexdigest() != hashlib.md5(old_text.encode('utf-8')).hexdigest()


# Open the website in the browser
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)
time.sleep(10)
# Save a screenshot of the webpage
screenshot_path = 'screenshot.png'
driver.save_screenshot(screenshot_path)

# Close the browser
driver.quit()

# Extract text from the screenshot
text = extract_text_from_screenshot(screenshot_path)

rows = text.split('\n')[6:9]
extracted_text = '\n'.join(rows)

# Save the text results
save_text_results(extracted_text)

# Save the text results
#     save_text_results(text)

# Check if the text has changed

message = 'Последняя новость:\n' + extracted_text
send_telegram_message(message)
