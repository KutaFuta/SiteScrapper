import requests
from bs4 import BeautifulSoup
import time
import random

class BaseScraper:
    def __init__(self, domain, start_page, num_pages):
        self.domain = self.purify_domain(domain)
        self.start_page = start_page
        self.num_pages = num_pages

    def purify_domain(self, domain):
        if domain.endswith('/'):
            domain = domain[:-1]
        return domain

    def fetch_html(self, url, retries=3):
        for _ in range(retries):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    return response.text
            except requests.exceptions.RequestException as e:
                print(f"Error fetching {url}: {e}")
                time.sleep(2)  # Wait before retrying
        return None

    def generate_unique_id(self):
        current_time_ms = int(time.time() * 1000)
        random_number = random.randint(1000, 9999)
        return f"{current_time_ms}{random_number}"

    def scrape(self):
        raise NotImplementedError("Scrape method must be implemented by subclasses")
