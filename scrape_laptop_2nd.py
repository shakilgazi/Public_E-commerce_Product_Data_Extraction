import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SHEET_ID = os.getenv('SHEET_ID')  # From .env
SHEET_NAME = 'Laptop Data 2'

def get_sheets_service():
    """Authenticate and return Google Sheets API service."""
    try:
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        service = build('sheets', 'v4', credentials=creds)
        logger.info("Successfully authenticated with Google Sheets API")
        return service
    except Exception as e:
        logger.error(f"Error setting up Google Sheets API: {e}")
        raise

def scrape_laptops():
    """Scrape first 10 laptops' name, price, and URL from the e-commerce site."""
    try:
        # Setup Selenium
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        url = 'https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops'
        driver.get(url)
        logger.info(f"Navigated to {url}")
        
        # Wait for page to load
        time.sleep(2)
        
        # Find product elements
        products = driver.find_elements(By.CLASS_NAME, 'thumbnail')[:100]  # Limit to first 10
        data = []
        for product in products:
            try:
                name = product.find_element(By.CLASS_NAME, 'title').text.strip()
                price = product.find_element(By.CLASS_NAME, 'price').text.strip()
                product_url = product.find_element(By.CLASS_NAME, 'title').get_attribute('href')
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data.append([name, price, timestamp, product_url])
                logger.info(f"Scraped: {name}, {price}, {product_url}")
            except Exception as e:
                logger.warning(f"Error scraping a product: {e}")
                continue
        
        driver.quit()
        return data
    except Exception as e:
        logger.error(f"Error during web scraping: {e}")
        raise

def append_to_sheets(service, data):
    """Append scraped data to Google Sheet."""
    try:
        sheet = service.spreadsheets()
        
        # Check if sheet exists, create if not
        try:
            sheet.get(spreadsheetId=SHEET_ID, ranges=[SHEET_NAME]).execute()
        except:
            sheet.batchUpdate(spreadsheetId=SHEET_ID, body={
                'requests': [{'addSheet': {'properties': {'title': SHEET_NAME}}}]
            }).execute()
            logger.info(f"Created new sheet: {SHEET_NAME}")
        
        # Add headers if sheet is empty
        result = sheet.values().get(spreadsheetId=SHEET_ID, range=f'{SHEET_NAME}!A1:D1').execute()
        if not result.get('values'):
            headers = ['Product Name', 'Price', 'Extraction Timestamp', 'Product URL']
            sheet.values().update(
                spreadsheetId=SHEET_ID,
                range=f'{SHEET_NAME}!A1',
                valueInputOption='RAW',
                body={'values': [headers]}
            ).execute()
            logger.info("Added headers to sheet")
        
        # Append data
        sheet.values().append(
            spreadsheetId=SHEET_ID,
            range=f'{SHEET_NAME}!A2',
            valueInputOption='RAW',
            body={'values': data}
        ).execute()
        logger.info(f"Appended {len(data)} rows to {SHEET_NAME}")
    except Exception as e:
        logger.error(f"Error appending to Google Sheet: {e}")
        raise

def main():
    """Main function to execute the scraping and data storage."""
    try:
        # Get Google Sheets service
        sheets_service = get_sheets_service()
        
        # Scrape laptop data
        laptop_data = scrape_laptops()
        
        if not laptop_data:
            logger.warning("No data scraped, exiting")
            return
        
        # Append to Google Sheet
        append_to_sheets(sheets_service, laptop_data)
        logger.info("Script completed successfully")
    except Exception as e:
        logger.error(f"Script failed: {e}")
        raise

if __name__ == '__main__':
    main()


#python scrape_laptop_2nd.py

