from playwright.sync_api import sync_playwright


def let_par(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Если url — это страница логина, логинимся
        if "login" in url:
            page.goto(url)
            page.fill('input[name="username"]', "who")
            page.fill('input[name="password"]', "BOGDANELESEEV")
            page.click('input[type="submit"]')
        else:
            page.goto(url)

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
    return all_quotes
