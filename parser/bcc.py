from playwright.sync_api import sync_playwright

url = 'https://club.bcc.kz/?city=21'

def generate_offers():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        #cards = page.query_selector_all('.card-select').get_attribute('href')

        #for href in cards:
        #    print(href)

        browser.close()

generate_offers()
