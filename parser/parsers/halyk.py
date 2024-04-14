from playwright.sync_api import sync_playwright
import pymorphy3

import spacy
import numpy as np


nlp = spacy.load("ru_core_news_lg")
CLASS_KEYWORDS = [
    "Игровые сервисы",
    "Салоны красоты и косметики",
    "Одежда и обувь",
    "Мебель",
    "Медицинские услуги",
    "Кафе и рестораны",
    "Такси",
    "Онлайн кино и музыка",
    "Путешествия",
    "Фитнес и SPA",
    "Супермаркеты",
    "Образование",
    "Доставка еды",
    "Питомцы",
    "Товары для детей",
]
CLASS_TOKENS = [nlp(keyword.lower()) for keyword in CLASS_KEYWORDS]
CLASS_TOKENS = [
    nlp(" ".join([str(t) for t in embedding if not t.is_stop]))
    for embedding in CLASS_TOKENS
]

""" Version for word or sentence"""


def calculate_similarities(class_tokens, embedding):
    similarities = [class_token.similarity(embedding) for class_token in class_tokens]
    best_match_index = np.argmax(similarities)
    return best_match_index, similarities[best_match_index]


def item_to_category(item: str) -> str:
    embedding = nlp(item.lower())
    embeddings_no_stopwrods = nlp(
        " ".join([str(t) for t in embedding if not t.is_stop])
    )
    matched_class, _ = calculate_similarities(
        class_tokens=CLASS_TOKENS, embedding=embeddings_no_stopwrods
    )
    return CLASS_KEYWORDS[matched_class]


def generate_offers():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # =========== Партнеры ===================

        page.goto("https://halykbank.kz/halykclub")

        dropdowns = page.query_selector_all(".mb-3.cursor-pointer")
        for dropdown in dropdowns:
            dropdown.click()

        buttons = page.query_selector_all(
            ".flex.cursor-pointer.justify-between.font-medium"
        )

        for button in buttons:
            button.click()
            page.wait_for_load_state("networkidle")

            divs = page.query_selector_all(
                ".rounded-lg.h-full.border.border-solid.border-gray-100.bg-gray-50.py-3.px-4"
            )
            for div in divs:
                name = div.query_selector(".font-semibold.mb-1.text-black")
                cashback = div.query_selector(
                    "[style*='background: rgb(252, 176, 22)'].rounded-2xl.mb-1.min-h-6.py-1.px-3.inline-flex.items-center.text-white.text-tiny.mr-2"
                )
                condition = div.query_selector(
                    "[style*='background: rgb(6, 140, 110)'].rounded-2xl.mb-1.min-h-6.py-1.px-3.inline-flex.items-center.text-white.text-tiny.mr-2"
                )

                if not name:
                    print(
                        "WARNING: Name of company not found in div, possible incorrect formating"
                    )

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
                print(item_to_category(name.text_content().lower()))
                yield (
                    name.text_content(),
                    CLASS_KEYWORDS.index(item_to_category(name.text_content().lower())),
                    4,
                    name.text_content(),
                    condition,
                    float(cashback),
                    None,
                )

        # ========= Акции =========================

        page1 = browser.new_page()
        page1.goto("https://halykbank.kz/halykclub/promo")
        m = pymorphy3.MorphAnalyzer()

        load_button = page1.query_selector(".btn.btn-green-light._js_ajax_load")

        while load_button.is_visible():
            load_button.click()
            page1.wait_for_load_state("networkidle")
            load_button = page1.query_selector(".btn.btn-green-light._js_ajax_load")

        page1.wait_for_load_state("networkidle")

        promos = page1.query_selector_all("text=бонусов в")

        for promo in promos:
            text = promo.text_content().split("бонусов в")

            company_name = ""
            data = text[1].split(" ")

            for word in data:
                correct = m.parse(word)[0]
                correct = correct.inflect({"nomn"})

                if correct:
                    company_name += correct.word + " "
                else:
                    company_name += word + " "

            #            print(text[0] + company_name)

            yield (
                company_name,
                None,
                4,
                company_name,
                None,
                float(text[0].split("%")[0]),
                None,
            )

        browser.close()
