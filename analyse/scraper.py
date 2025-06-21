from facebook_page_scraper import Facebook_scraper
import json
import os

page = 'jiramaofisialy'
posts_count = 100
browser = "chrome"
timeout = 600
headless = True  # Mode sans fenêtre

scraper = Facebook_scraper(page, posts_count, browser, timeout=timeout, headless=headless)

data = scraper.scrap_to_json()
print(json.dumps(data, indent=4, ensure_ascii=False))
