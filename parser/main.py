from playwright.sync_api import sync_playwright
import pymorphy3

with sync_playwright() as p:
    browser = p.chromium.launch(headless = True)
    page = browser.new_page()

    #=========== Партнеры ===================

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
            cashback = ""
            cashbacks = div.query_selector_all(".rounded-2xl.mb-1.min-h-6.py-1.px-3.inline-flex.items-center.text-white.text-tiny.mr-2")
            for c in cashbacks :
                cashback += c.text_content() + " "

            if not name:
                print("WARNING: Name of company not found in div, possible incorrect formating")

            print(name.text_content() + ": " + cashback)

    #========= Акции =========================

    page1 = browser.new_page()
    page1.goto("https://halykbank.kz/halykclub/promo")
    m = pymorphy3.MorphAnalyzer()

    load_button = page1.query_selector('.btn.btn-green-light._js_ajax_load')

    while load_button.is_visible() :
        load_button.click()
        print(str(load_button.is_visible()))
        page1.wait_for_load_state('networkidle')
        load_button = page1.query_selector('.btn.btn-green-light._js_ajax_load')
        print(str(load_button.is_visible()))

    page1.wait_for_load_state('networkidle')

    promos = page1.query_selector_all('text=бонусов в')

    for promo in promos:
        text = promo.text_content().split('бонусов в')

        company_name = ""
        data = text[1].split(" ")

        for word in data :
            correct = m.parse(word)[0]
            correct = correct.inflect({'nomn'})

            if correct :
                company_name += correct.word + " "
            else :
                company_name += word + " "

        print(text[0] + company_name)

    browser.close()
