categories = {'1': 10,
              '2': 5}
cards = range(1, 4)

def generate_offers():
    for card in cards:
        for c in categories.keys():
            yield (f'Jusan cashback {card}', int(c), card, None, None, categories[c], None)
