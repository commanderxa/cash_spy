import importlib.util
import pathlib

DIR = "parsers"

for file in pathlib.Path(DIR).glob('*.py'):
    spec = importlib.util.spec_from_file_location(f"{__name__}.imported_{file.stem}", file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for name, category, card, partner, condition, cashback, fav in module.generate_offers():
        print(partner + ' ' + cashback)
