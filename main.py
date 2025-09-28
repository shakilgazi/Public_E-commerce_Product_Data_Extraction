
# File: main.py
import logging
from sheets_auth import SheetsAuth
from web_scraper import WebScraper
from data_handler import DataHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main function to execute the sheet service, scraping, and data storage."""
    try:
        # Initialize modules
        sheets_auth = SheetsAuth()
        sheets_service = sheets_auth.get_sheets_service()
        web_scraper = WebScraper()
        data_handler = DataHandler(sheets_service)
        
        # Scrape laptop data
        laptop_data = web_scraper.scrape_laptops()
        
        if not laptop_data:
            logger.warning("No data scraped, exiting")
            return
        
        # Append to Google Sheet
        data_handler.append_to_sheets(laptop_data)
        logger.info("Script completed successfully")
    except Exception as e:
        logger.error(f"Script failed: {e}")
        raise

if __name__ == '__main__':
    main()



# import os
# from dotenv import load_dotenv

# load_dotenv()
# print(f"Sheet ID: {os.getenv('SHEET_ID')}")
# print("Setup complete!")



# print("Setup Done")



# python main.py


