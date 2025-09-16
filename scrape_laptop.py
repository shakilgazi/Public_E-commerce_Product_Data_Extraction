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
SHEET_NAME = 'Laptop Data'

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
        time.sleep(5)  # Adjusted to 5 seconds as per previous setup
        
        # Find product elements using XPath
        products = driver.find_elements(By.XPATH, '//div[@class="card thumbnail"]')[:100]  # Limit to first 10
        data = []
        for product in products:
            try:
                product_data = {}
                
                # Product name
                name_elements = product.find_elements(By.XPATH, './/h4/a[@class="title"]')
                if name_elements:
                    product_text_name = driver.execute_script(
                        "return arguments[0].getAttribute('title');", name_elements[0]
                    ).strip()
                    if product_text_name:
                        product_data['Product Name'] = product_text_name
                    else:
                        product_data['Product Name'] = "N/A text not found"
                else:
                    product_data['Product Name'] = "N/A path not found"

                # Brand with model
                Brand_with_model_elements = product.find_elements(By.XPATH, './/h4/a[@class="title"]')
                if Brand_with_model_elements:
                    product_text_Brand_with_model = driver.execute_script(
                        "return arguments[0].textContent;", name_elements[0]
                    ).strip()
                    if product_text_Brand_with_model:
                        product_data['Brand with model'] = product_text_Brand_with_model
                    else:
                        product_data['Brand with model'] = "N/A text not found"
                else:
                    product_data['Brand with model'] = "N/A path not found"
                
                # Product price
                price_elements = product.find_elements(By.XPATH, './/h4[@class="price float-end card-title pull-right"]/span')
                if price_elements:
                    product_text_price = driver.execute_script(
                        "return arguments[0].textContent;", price_elements[0]
                    ).strip()
                    if product_text_price:
                        product_data['Product Price'] = product_text_price
                    else:
                        product_data['Product Price'] = "N/A text not found"
                else:
                    product_data['Product Price'] = "N/A path not found"

                # Product Description
                description_elements = product.find_elements(By.XPATH, './/p[@class="description card-text"]')
                if description_elements:
                    product_text_description = driver.execute_script(
                        "return arguments[0].textContent;", description_elements[0]
                    ).strip()
                    if product_text_description:
                        product_data['Product Description'] = product_text_description
                    else:
                        product_data['Product Description'] = "N/A text not found"
                else:
                    product_data['Product Description'] = "N/A path not found"
                
                # Product URL
                url_elements = product.find_elements(By.XPATH, './/h4/a[@class="title"]')
                if url_elements:
                    product_url = driver.execute_script(
                        "return arguments[0].getAttribute('href');", url_elements[0]
                    )
                    if product_url:
                        product_data['Product URL'] = f"https://webscraper.io{product_url}"
                    else:
                        product_data['Product URL'] = "N/A href not found"
                else:
                    product_data['Product URL'] = "N/A path not found"

                # Product Review
                Review_elements = product.find_elements(By.XPATH, './/p[@class="review-count float-end"]/span')
                if Review_elements:
                    product_text_Review = driver.execute_script(
                        "return arguments[0].textContent;", Review_elements[0]
                    ).strip()
                    if product_text_Review:
                        product_data['Number of Review'] = product_text_Review
                    else:
                        product_data['Number of Review'] = "N/A text not found"
                else:
                    product_data['Number of Review'] = "N/A path not found"

                # Product Rating
                Rating_elements = product.find_elements(By.XPATH, './/p[@data-rating]')
                if Rating_elements:
                    product_text_Rating = driver.execute_script(
                        "return arguments[0].getAttribute('data-rating');", Rating_elements[0]
                    ).strip()
                    if product_text_Rating:
                        product_data['Number of Rating'] = product_text_Rating
                    else:
                        product_data['Number of Rating'] = "N/A text not found"
                else:
                    product_data['Number of Rating'] = "N/A path not found"
                
                # Timestamp
                product_data['Extraction Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                data.append([
                    product_data['Product Name'],
                    product_data['Product Price'],
                    product_data['Brand with model'],
                    product_data['Product Description'],
                    product_data['Number of Review'],
                    product_data['Number of Rating'],
                    product_data['Product URL'],
                    product_data['Extraction Timestamp']
                ])
                logger.info(f"Scraped:{product_data['Product Name']}, {product_data['Product Price']}, {product_data['Brand with model']},, {product_data['Product Description']}, {product_data['Number of Review']}, {product_data['Number of Rating']}, {product_data['Product URL']}, {product_data['Extraction Timestamp']}")
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
            headers = [
                'Product Name', 
                'Product Price',
                'Brand with model', 
                'Product Description', 
                'Number of Review', 
                'Number of Rating', 
                'Product URL', 
                'Extraction Timestamp']
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


#python scrape_laptop.py




