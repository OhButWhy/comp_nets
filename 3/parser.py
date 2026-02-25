from playwright.sync_api import sync_playwright
import csv

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    page.goto("https://quotes.toscrape.com/login")
    page.fill('input[name="username"]', "who")
    page.fill('input[name="password"]', "BOGDANELESEEV")
    page.click('input[type="submit"]')

    all_quotes = []
    while True:
        quotes = page.query_selector_all(".quote")
        for quote in quotes:
            text = quote.query_selector(".text").inner_text()
            author = quote.query_selector(".author").inner_text()
            tags = quote.query_selector(".tags").inner_text()
            author_link = quote.query_selector("span a").get_attribute("href")
            all_quotes.append({
                "text": text,
                "author": author,
                "tags": tags,
                "author_link": author_link
            })
        next_button = page.query_selector('li.next > a')
        if not next_button:
            break
        next_button.click()
        page.wait_for_load_state("load")

with open("quotes.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["text", "author", "tags", "author_link"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_quotes)
