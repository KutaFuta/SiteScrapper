import json
import os
from scrapers.panu_scraper import PanuScraper

def save_to_json(data, filename):
    # Create ScrapedData folder if it doesn't exist
    if not os.path.exists('__ScrapedData__'):
        os.makedirs('__ScrapedData__')
    filepath = os.path.join('__ScrapedData__', filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    available_domains = {
        "panu": {
            "domain": "https://panu.live/",
            "scraper_class": PanuScraper
        },
        # Add more domains and their corresponding scraper classes here
    }

    print("Select a domain:")
    for i, domain_name in enumerate(available_domains.keys(), 1):
        print(f"{i}. {domain_name}")

    selected_option = int(input("Enter the number of the selected domain: "))
    selected_domain_name = list(available_domains.keys())[selected_option - 1]
    selected_domain_info = available_domains[selected_domain_name]

    domain = selected_domain_info["domain"]
    ScraperClass = selected_domain_info["scraper_class"]

    start_page = int(input("Enter the start page number: "))
    num_pages = int(input("Enter the number of pages to check: "))

    scraper = ScraperClass(domain, start_page, num_pages)
    scraping_pages = scraper.scrape()

    filename = f"{domain.replace('https://', '').replace('http://', '').replace('/', '_')}_page_{start_page}_to_{start_page + num_pages - 1}.json"
    save_to_json(scraping_pages, filename)
    print(f"Scraping pages saved to __ScrapedData__/{filename}")
