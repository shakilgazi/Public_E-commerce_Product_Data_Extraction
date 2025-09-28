# File: auth/token_manager.py
import os
import logging
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TokenManager:
    def __init__(self, scopes, credentials_file='credentials.json', token_file='token.json'):
        self.scopes = scopes
        self.credentials_file = credentials_file
        self.token_file = token_file

    def get_credentials(self):
        """Generate or refresh credentials and store them in token.json."""
        try:
            creds = None
            # Load existing token if it exists
            if os.path.exists(self.token_file):
                creds = Credentials.from_authorized_user_file(self.token_file, self.scopes)
                logger.info(f"Loaded credentials from {self.token_file}")

            # If no valid credentials, refresh or generate new ones
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    try:
                        creds.refresh(Request())
                        logger.info("Refreshed expired token")
                    except Exception as e:
                        logger.warning(f"Failed to refresh token: {e}. Generating new token.")
                        creds = None

                if not creds:
                    if not os.path.exists(self.credentials_file):
                        raise FileNotFoundError(f"{self.credentials_file} not found. Please provide valid Google API credentials.")
                    flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.scopes)
                    creds = flow.run_local_server(port=0)
                    logger.info("Generated new credentials via OAuth flow")

                # Save the credentials to token.json
                with open(self.token_file, 'w') as token:
                    token.write(creds.to_json())
                    logger.info(f"Saved credentials to {self.token_file}")

            return creds
        except Exception as e:
            logger.error(f"Error generating or refreshing credentials: {e}")
            raise