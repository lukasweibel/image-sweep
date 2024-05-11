import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import csv
import uuid
import sys
from pathlib import Path
import os
import glob

def start_scraping():
    timeout = 3000
    
    download_path = 'data/screenshots'
    
    mobile_device = 'iPhone X'

    def run(playwright):
        failures = 0
        browser = playwright.chromium.launch(headless=True)
        device = playwright.devices[mobile_device]
        #context = browser.new_context(**device)
        context = browser.new_context(
            **device,
            accept_downloads=True
        )
        
        try:
            page = context.new_page()
            page.goto("https://prankshit.com/fake-whatsapp-chat-generator.php", timeout=timeout)
            
            page.wait_for_load_state('load')
            
            try:
                button = page.locator('text="Download image "')
                if button.is_visible():
                    with page.expect_download() as download_info:
                        button.click()
                    download = download_info.value

                    original_path = download.path()
                    
                    unique_id = uuid.uuid4()  # Generate a unique identifier
                    file_name = f"{unique_id}.png"  # Use UUID to form a new file name
                    
                    new_path = os.path.join(download_path, file_name)
                    os.rename(original_path, new_path)
                    print(f"Downloaded file saved to: {new_path}")
            except Exception as e:
                print(f"Failed to interact, error: {e}")
        except PlaywrightTimeoutError as e:
                print(f"Encountered a timeout: {e}")

        context.close()
        browser.close()
        
    with sync_playwright() as playwright:
        run(playwright)
        
def run_generator():
    delete_png_files('data/screenshots')
    for _ in range(15):
        start_scraping()
    
    
def delete_png_files(folder_path):
    file_pattern = os.path.join(folder_path, '*.png')
    
    png_files = glob.glob(file_pattern)
    
    for file_path in png_files:
        os.remove(file_path)

if __name__ == "__main__":
    run_generator()
