from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
import os

class PanuScraper(BaseScraper):
    def scrape(self):
        scraping_pages = []
        for page_num in range(self.start_page, self.start_page + self.num_pages):
            url = f"{self.domain}/page/{page_num}/"
            print(f"Checking URL: {url}")  # Debug statement
            html = self.fetch_html(url)
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                for post_item in soup.find_all('div', class_='post-item-wrap'):
                    post_data = {}
                    title_tag = post_item.find('a', class_='blog-img')
                    if title_tag:
                        post_data['unique_id'] = self.generate_unique_id()
                        post_data['url'] = title_tag['href']
                        post_data['title'] = title_tag['title']
                        # Fetch the post page to get the video URL
                        post_html = self.fetch_html(post_data['url'])
                        if post_html:
                            post_soup = BeautifulSoup(post_html, 'html.parser')
                            meta_tag = post_soup.find('meta', property='og:video:url')
                            if meta_tag:
                                post_data['Video_URL'] = meta_tag['content']
                    img_tag = post_item.find('img', class_='blog-picture')
                    if img_tag:
                        post_data['image'] = img_tag['src']
                    if post_data:
                        scraping_pages.append(post_data)
        return scraping_pages
