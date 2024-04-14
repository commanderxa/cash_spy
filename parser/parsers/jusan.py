categories = {'1': 10,
              '2': 5,
              '3': 3,
              '4': 5,
              '5': 5,
              '6': 3,
              '7': 7,
              '8': 15,
              '9': 5,
              '10': 5,
              '11': 3,
              '12': 5,
              '13': 5,
              '14': 5,
              '15': 5}
names = ['Игровые сервисы',
'Салоны красоты и косметики',
'Одежда и обувь',
'Мебель',
'Медицинские услуги',
'Кафе и рестораны',
'Такси',
'Онлайн кино и музыка',
'Путешествия',
'Фитнес и SPA',
'Супермаркеты',
'Образование',
'Доставка еды',
'Питомцы',
'Товары для детей']
cards = range(1, 4)

def generate_offers():
    for card in cards:
        for c in categories.keys():
            yield (names[int(c) - 1], int(c), card, None, None, categories[c], None)
