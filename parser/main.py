import importlib.util
import pathlib
import requests

DIR = "parsers"
url = "http://127.0.0.1:8000/api/v1/offers"

for file in pathlib.Path(DIR).glob("*.py"):
    spec = importlib.util.spec_from_file_location(
        f"{__name__}.imported_{file.stem}", file
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for (
        name,
        category,
        card,
        partner,
        condition,
        cashback,
        fav,
    ) in module.generate_offers():
        print(
            name,
            category,
            card,
            partner,
            condition,
            cashback,
            fav,
        )
        data = {
            "name": name,
            "category_id": category,
            "card_id": card,
            "partner": partner,
            "condition": condition,
            "cashback": cashback,
            "description": "string",
            "favorite_cashback": 0,
            "date_from": None,
            "date_to": None
        }
        res = requests.post(url, json=data)
