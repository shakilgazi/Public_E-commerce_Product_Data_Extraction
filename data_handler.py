
# File: sheets/data_handler.py
import logging
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
SHEET_ID = os.getenv('SHEET_ID')
SHEET_NAME = 'Laptop Data'

class DataHandler:
    def __init__(self, sheets_service):
        self.sheets_service = sheets_service
        self.sheet_id = SHEET_ID
        self.sheet_name = SHEET_NAME

    def append_to_sheets(self, data):
        """Append scraped data to Google Sheet."""
        try:
            sheet = self.sheets_service.spreadsheets()
            
            # Check if sheet exists, create if not
            try:
                sheet.get(spreadsheetId=self.sheet_id, ranges=[self.sheet_name]).execute()
            except:
                sheet.batchUpdate(spreadsheetId=self.sheet_id, body={
                    'requests': [{'addSheet': {'properties': {'title': self.sheet_name}}}]
                }).execute()
                logger.info(f"Created new sheet: {self.sheet_name}")
            
            # Add headers if sheet is empty
            result = sheet.values().get(spreadsheetId=self.sheet_id, range=f'{self.sheet_name}!A1:D1').execute()
            if not result.get('values'):
                headers = [
                    'Product Name', 
                    'Product Price',
                    'Brand with model', 
                    'Product Description', 
                    'Number of Review', 
                    'Number of Rating', 
                    'Product URL', 
                    'Extraction Timestamp'
                ]
                sheet.values().update(
                    spreadsheetId=self.sheet_id,
                    range=f'{self.sheet_name}!A1',
                    valueInputOption='RAW',
                    body={'values': [headers]}
                ).execute()
                logger.info("Added headers to sheet")
            
            # Append data
            sheet.values().append(
                spreadsheetId=self.sheet_id,
                range=f'{self.sheet_name}!A2',
                valueInputOption='RAW',
                body={'values': data}
            ).execute()
            logger.info(f"Appended {len(data)} rows to {self.sheet_name}")
        except Exception as e:
            logger.error(f"Error appending to Google Sheet: {e}")
            raise
