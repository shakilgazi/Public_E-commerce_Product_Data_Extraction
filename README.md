# Public_E-commerce_Product_Data_Extraction

## Overview

This project scrapes data for laptops (product name, price, extraction timestamp, and product URL) from [Webscraper.io's test e-commerce site](https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops) and saves the data to a Google Sheet in the "Laptop Data" tab.

## Prerequisites

- Python 3.8+
- Google Cloud Project with Sheets API enabled
- A Google account with access to the Sheet

## Setup Instructions

1.  **Clone the Repository**:

    ```bash
    git clone https://github.com/shakilgazi/Public_E-commerce_Product_Data_Extraction.git
    cd Public_E-commerce_Product_Data_Extraction
    ```

2.  **Set Up a Virtual Environment** (recommended):

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On WSL2/Linux
    # Or: .venv\Scripts\activate  # On Windows
    ```

3.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables**:

    - Copy `.env.example` to `.env`:
      ```bash
      cp .env.example .env
      ```
    - Edit `.env` with your Google Sheet ID and Drive folder ID:

      ```plaintext
      SHEET_ID = <your_sheet_id>

      like
      https://docs.google.com/spreadsheets/d/<your_sheet_id>/edit?
      ```

5.  **Add Google API Credentials**:

    - Download `credentials.json` from Google Cloud Console (with Sheets API enabled).
    - Place `credentials.json` in the project directory (`Public_E-commerce_Product_Data_Extraction/`).

6.  **Run the Script**:

    ```bash
    python test_auth.py
    python scrape_laptop.py
    ```

    - On first run, a browser window will open for OAuth authentication. Sign in with your Google account.
    - The script will:
      - Scrape laptops from the test site.
      - Save data to the "Laptop Data" tab in the specified Google Sheet.
      - Log progress to the terminal.

## Files

- `scrape_laptop.py`: Main script for scraping and saving data.
- `requirements.txt`: Python dependencies.
- `.env.example`: Template for environment variables.
- `test_auth.py`: this script will complete the OAuth and create 'token.json' file.
- `.gitignore`: Excludes sensitive files (e.g., `.env`, `credentials.json`, `token.json`).

## Notes

- The Google Sheet must have view access for verification (Share > Anyone with the link > Viewer).
- The script creates the "Laptop Data" tab with headers: Product Name, Price, Extraction Timestamp, Product URL.

## Dependencies

See `requirements.txt` for a full list. Key libraries:

- `selenium`: For web scraping.
- `google-api-python-client`, `google-auth-oauthlib`: For Google Sheets API.
- `python-dotenv`: For environment variables.
- `webdriver-manager`: For ChromeDriver management.
