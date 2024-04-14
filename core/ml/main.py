import spacy 
import numpy as np


nlp = spacy.load('ru_core_news_lg')
CLASS_KEYWORDS = ['Игровые сервисы',
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
                'Товары для детей'
]
CLASS_TOKENS = [nlp(keyword.lower()) for keyword in CLASS_KEYWORDS]
CLASS_TOKENS = [nlp(' '.join([str(t) for t in embedding if not t.is_stop])) for embedding in CLASS_TOKENS]

''' Version for word or sentence'''

def calculate_similarities(class_tokens, embedding):
    similarities = [class_token.similarity(embedding) for class_token in class_tokens]
    best_match_index = np.argmax(similarities)
    return best_match_index, similarities[best_match_index]


def item_to_category(item: str) -> str:
    embedding = nlp(item)
    embeddings_no_stopwrods = nlp(' '.join([str(t) for t in embedding if not t.is_stop]))

    matched_class, _ = calculate_similarities(class_tokens=CLASS_TOKENS, embedding=embeddings_no_stopwrods)
    return CLASS_KEYWORDS[matched_class]

