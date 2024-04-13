from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless = True)
    page = browser.new_page()
    page.goto("https://halykbank.kz/halykclub")

    dropdowns = page.query_selector_all('.mb-3.cursor-pointer')
    for dropdown in dropdowns :
        dropdown.click()

    buttons = page.query_selector_all('.flex.cursor-pointer.justify-between.font-medium')

    for button in buttons :
        button.click()
        page.wait_for_load_state('networkidle')

        divs = page.query_selector_all(".rounded-lg.h-full.border.border-solid.border-gray-100.bg-gray-50.py-3.px-4")
        for div in divs :
            name = div.query_selector(".font-semibold.mb-1.text-black")
            cashback = div.query_selector(".rounded-2xl.mb-1.min-h-6.py-1.px-3.inline-flex.items-center.text-white.text-tiny.mr-2")

            if not name or not cashback :
                print("WARNING: Name of company not found in div, possible incorrect formating")

            print(name.text_content() + ": " + cashback.text_content())

    browser.close()
