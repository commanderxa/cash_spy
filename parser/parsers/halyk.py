from playwright.sync_api import sync_playwright
import pymorphy3

def generate_offers():
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
                cashback = div.query_selector("[style*='background: rgb(252, 176, 22)'].rounded-2xl.mb-1.min-h-6.py-1.px-3.inline-flex.items-center.text-white.text-tiny.mr-2")
                condition = div.query_selector("[style*='background: rgb(6, 140, 110)'].rounded-2xl.mb-1.min-h-6.py-1.px-3.inline-flex.items-center.text-white.text-tiny.mr-2")

                if not name:
                    print("WARNING: Name of company not found in div, possible incorrect formating")
                
                if cashback:
                    cashback = cashback.text_content()
                else:
                    cashback = ""

                if condition:
                    condition = condition.text_content()
                else:
                    condition = ""

#                print(name.text_content() + ": " + cashback)

                try:
                    cashback = float(cashback.split("%")[0])
                except:
                    cashback = 0
                yield (name.text_content(), None, None, name.text_content(), condition, float(cashback), None)

        #========= Акции =========================

        page1 = browser.new_page()
        page1.goto("https://halykbank.kz/halykclub/promo")
        m = pymorphy3.MorphAnalyzer()

        load_button = page1.query_selector('.btn.btn-green-light._js_ajax_load')

        while load_button.is_visible() :
            load_button.click()
            page1.wait_for_load_state('networkidle')
            load_button = page1.query_selector('.btn.btn-green-light._js_ajax_load')

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

#            print(text[0] + company_name)

            yield (company_name, None, None, company_name, None, float(text[0].split("%")[0]), None)

        browser.close()
