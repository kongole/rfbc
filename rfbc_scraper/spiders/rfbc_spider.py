import scrapy
import logging
import json
from bs4 import BeautifulSoup

# Configure logging
log_file = "scrapy_errors.log"
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

class RFBCSpider(scrapy.Spider):
    name = "rfbc"

    def __init__(self, mode="live", *args, **kwargs):
        super(RFBCSpider, self).__init__(*args, **kwargs)
        self.mode = mode  # Mode: "live" or "archive"

        # Load websites dynamically
        with open("websites.json", "r", encoding="utf-8") as f:
            websites = json.load(f)["websites"]

        if mode == "archive":
            self.start_urls = [f"https://web.archive.org/web/20240101/{site}" for site in websites]
        else:
            self.start_urls = websites

        logging.info(f"Scraping in {mode.upper()} mode. URLs: {self.start_urls}")

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "LOG_LEVEL": "DEBUG",
        "DOWNLOAD_DELAY": 2,
        "ROBOTSTXT_OBEY": False,
        "HTTPERROR_ALLOW_ALL": True,
        "REDIRECT_ENABLED": True,
        "HTTPERROR_ALLOWED_CODES": [403, 404]
    }

    def clean_text(self, text):
        """Remove UI elements from scraped pages."""
        lines = text.split("\n")
        cleaned_lines = [
            line.strip() for line in lines
            if not any(
                phrase in line.lower() for phrase in [
                    "wayback machine", "please don't scroll past this",
                    "skip to content", "open menu", "close menu",
                    "privacy policy", "terms of service", "donate", "sign in",
                    "navigate", "contact us", "home", "newsletter", "about us",
                    "faq", "site map", "subscribe", "search for", "read more",
                    "write a comment", "loading comments", "submit", "powered by",
                    "copyright", "login", "sign up", "follow us", "leave a reply",
                    "back", "next", "previous", "search", "menu", "advertisement"
                ]
            )
        ]
        return " ".join(cleaned_lines)

    def remove_unwanted_sections(self, soup):
        """Remove common UI elements from pages."""
        for tag in soup(["nav", "footer", "aside", "script", "style", "header",
                         "form", "iframe", "noscript", "button", "input",
                         "select", "textarea", "svg", "img", "video", "audio",
                         "meta", "link", "object", "embed", "picture", "source",
                         "ul", "ol", "li", "noscript"]):
            tag.decompose()
        return soup

    def start_requests(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "https://www.google.com/",
            "Accept-Language": "en-US,en;q=0.9",
        }
        for url in self.start_urls:
            logging.info(f"Requesting URL: {url}")
            yield scrapy.Request(url, headers=headers, callback=self.parse, errback=self.handle_error)

    def handle_error(self, failure):
        logging.error(f"Request failed: {failure.request.url} - {failure.value}")

    def parse(self, response):
        """Extract and clean the page content."""
        try:
            soup = BeautifulSoup(response.text, "html.parser")

            # Remove UI elements
            soup = self.remove_unwanted_sections(soup)
            page_text = soup.get_text(separator=" ").strip()

            # Clean archive junk data
            if "web.archive.org" in response.url:
                page_text = self.clean_text(page_text)

            if not page_text:
                logging.warning(f"Empty content extracted from {response.url}")

            yield {
                "url": response.url,
                "content": page_text
            }

        except Exception as e:
            logging.error(f"Error processing {response.url}: {e}")
