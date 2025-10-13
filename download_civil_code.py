import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin

BASE_URL = "https://www.legisquebec.gouv.qc.ca/fr/document/lc/CCQ-1991"
OUTPUT_FOLDER = "data/Civil_Code"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def save_article(article_number, article_text):
    filename = f"article_{article_number}.txt"
    path = os.path.join(OUTPUT_FOLDER, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(article_text)

def scrape_page(url):
    print(f"📖 Scraping {url}")
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    articles = soup.find_all("p", class_="article")
    for art in articles:
        number_tag = art.find("span", class_="artnum")
        number = number_tag.text.strip() if number_tag else "Unknown"
        text = clean_text(art.get_text(" "))
        save_article(number, text)
        print(f"✅ Saved Article {number}")

def scrape_civil_code():
    print("🔍 Finding sub-pages for each Book of the Civil Code...")
    res = requests.get(BASE_URL)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    # Find all links to sub-pages (Books / Titles)
    links = [a["href"] for a in soup.select("a[href*='/fr/document/lc/CCQ-1991/']")]
    links = list(dict.fromkeys(links))  # remove duplicates

    if not links:
        print("⚠️ No sub-pages found — structure may have changed.")
        return

    for link in links:
        full_url = urljoin(BASE_URL, link)
        scrape_page(full_url)

    print("✅ All articles saved to data/Civil_Code")

if __name__ == "__main__":
    scrape_civil_code()
