from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import uuid
from pathlib import Path
import os
import glob

def start_scraping_screenshots(device):
    timeout = 4000
    
    mobile_device = device
    
    with open('scrape/websites.txt', 'r') as file:
        websites = [line.strip() for line in file.readlines()]

    def run(playwright):
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
        
    with sync_playwright() as playwright:
        run(playwright)
        
def start_scraping_whatsapp():
    timeout = 3000
    
    download_path = 'data/screenshots'
    
    mobile_device = 'iPhone X'

    def run(playwright):
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
                    
                    unique_id = uuid.uuid4()
                    file_name = f"{unique_id}.png"
                    
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
        
def run_scraping():
    delete_png_files('data/screenshots')
    start_scraping_screenshots('Desktop Chrome')
    start_scraping_screenshots('iPhone X')
    for _ in range(15):
        start_scraping_whatsapp()
    
def delete_png_files(folder_path):
    file_pattern = os.path.join(folder_path, '*.png')
    
    png_files = glob.glob(file_pattern)
    
    for file_path in png_files:
        os.remove(file_path)

if __name__ == "__main__":
    run_scraping()