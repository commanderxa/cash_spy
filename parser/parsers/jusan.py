categories = {'1': 10,
              '2': 5}
cards = range(3)

def generate_offers():
    for card in cards:
        for c in categories.keys():
            yield ('Jusan cashback', c, card, None, None, categories[c], None)
