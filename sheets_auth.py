
# File: auth/sheets_auth.py
import logging
from googleapiclient.discovery import build
from token_manager import TokenManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class SheetsAuth:
    def __init__(self):
        self.scopes = SCOPES
        self.token_manager = TokenManager(self.scopes)

    def get_sheets_service(self):
        """Authenticate and return Google Sheets API service."""
        try:
            creds = self.token_manager.get_credentials()
            service = build('sheets', 'v4', credentials=creds)
            logger.info("Successfully authenticated with Google Sheets API")
            return service
        except Exception as e:
            logger.error(f"Error setting up Google Sheets API: {e}")
            raise
