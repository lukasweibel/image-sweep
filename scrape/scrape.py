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
    
    #delete_png_files('data/screenshots')
    
    mobile_device = 'iPhone X'
    
    devices = ['iPhone X', 'iPhone 13 mini', 'Samsung Galaxy S21']
    
    with open('scrape/websites.txt', 'r') as file:
        websites = [line.strip() for line in file.readlines()]

    def run(playwright):
        failures = 0
        browser = playwright.chromium.launch(headless=True)
        device = playwright.devices[mobile_device]
        context = browser.new_context(**device)
        
        for website in websites:
            try:
                page = context.new_page()
                page.goto(website, timeout=timeout)
                
                page.wait_for_load_state('load')
                
                try:
                    button = page.locator('text="Akzeptieren"')
                    if button.is_visible():
                        button.click()
                        print(f"Akzeptieren {website}")
                    else:
                        print(f"'Akzeptieren button not visible on {website}")

                    page.screenshot(path=f'data/screenshots/{uuid.uuid1()}.png')
                
                except Exception as e:
                    print(f"Failed to interact with {website}, error: {e}")
                page.close()
            except PlaywrightTimeoutError as e:
                    print(f"Encountered a timeout: {e}")
            except Exception as e:
                print(f"General error on {website}: {e}")

        context.close()
        browser.close()
        print("fauilures: " + str(failures))
        
    with sync_playwright() as playwright:
        run(playwright)
    
def delete_png_files(folder_path):
    file_pattern = os.path.join(folder_path, '*.png')
    
    png_files = glob.glob(file_pattern)
    
    for file_path in png_files:
        os.remove(file_path)

if __name__ == "__main__":
    start_scraping()
