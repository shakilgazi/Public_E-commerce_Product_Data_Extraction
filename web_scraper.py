
# File: scraper/web_scraper.py
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self):
        self.url = 'https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops'

    def scrape_laptops(self):
        """Scrape first 100 laptops' name, price, brand, description, ratings, reviews, and URL."""
        try:
            # Setup Selenium
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            
            driver.get(self.url)
            logger.info(f"Navigated to {self.url}")
            time.sleep(5)
            
            products = driver.find_elements(By.XPATH, '//div[@class="card thumbnail"]')[:100]
            data = []
            for product in products:
                try:
                    product_data = {}
                    
                    # Product name
                    name_elements = product.find_elements(By.XPATH, './/h4/a[@class="title"]')
                    product_data['Product Name'] = (
                        driver.execute_script("return arguments[0].getAttribute('title');", name_elements[0]).strip()
                        if name_elements else "N/A path not found"
                    )

                    # Brand with model
                    product_data['Brand with model'] = (
                        driver.execute_script("return arguments[0].textContent;", name_elements[0]).strip()
                        if name_elements else "N/A path not found"
                    )
                    
                    # Product price
                    price_elements = product.find_elements(By.XPATH, './/h4[@class="price float-end card-title pull-right"]/span')
                    product_data['Product Price'] = (
                        driver.execute_script("return arguments[0].textContent;", price_elements[0]).strip()
                        if price_elements else "N/A path not found"
                    )

                    # Product Description
                    description_elements = product.find_elements(By.XPATH, './/p[@class="description card-text"]')
                    product_data['Product Description'] = (
                        driver.execute_script("return arguments[0].textContent;", description_elements[0]).strip()
                        if description_elements else "N/A path not found"
                    )
                    
                    # Product URL (Fixed to avoid f-string backslash issue)
                    url_elements = product.find_elements(By.XPATH, './/h4/a[@class="title"]')
                    product_data['Product URL'] = (
                        "https://webscraper.io" + driver.execute_script("return arguments[0].getAttribute('href');", url_elements[0]).strip()
                        if url_elements else "N/A path not found"
                    )

                    # Product Review
                    review_elements = product.find_elements(By.XPATH, './/p[@class="review-count float-end"]/span')
                    product_data['Number of Review'] = (
                        driver.execute_script("return arguments[0].textContent;", review_elements[0]).strip()
                        if review_elements else "N/A path not found"
                    )

                    # Product Rating
                    rating_elements = product.find_elements(By.XPATH, './/p[@data-rating]')
                    product_data['Number of Rating'] = (
                        driver.execute_script("return arguments[0].getAttribute('data-rating');", rating_elements[0]).strip()
                        if rating_elements else "N/A path not found"
                    )
                    
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
                    logger.info(f"Scraped: {product_data['Product Name']}")
                except Exception as e:
                    logger.warning(f"Error scraping a product: {e}")
                    continue
            
            driver.quit()
            return data
        except Exception as e:
            logger.error(f"Error during web scraping: {e}")
            raise
