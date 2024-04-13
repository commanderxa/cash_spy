import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define class keywords
class_keywords = {
    'Electronics': ['battery', 'charger', 'device'],
    'Car Items': ['tire', 'oil', 'spark plug'],
    'Food': ['chocolate', 'snack', 'beverage']
}

class_vectors = [np.mean([nlp(keyword).vector_norm for keyword in keywords])
                 for keywords in class_keywords.values()]
class_vectors = [np.array([[np.mean(class_vector)]]) for class_vector in class_vectors]
print(class_vectors)
class_labels = list(class_keywords.keys())

# Function to extract keywords from item
def extract_keywords(item):
    return [token.text.lower() for token in nlp(item) if not token.is_stop and token.text.isalpha()]

# Function to extract description from item (mock function)
def extract_description(item):
    return item  # For demonstration purposes, returning the item itself

# Function to match items to classes using cosine similarity
def cosine_similarity_matching(item_vector, class_vectors, class_labels):
    #A = np.array([[5, 3, 4]])
    #B = np.array([[4, 2, 4]])

    print("hello")
    #print([item_vector,item_vector,item_vector])
    print(np.array(class_vectors).reshape(3, -1))
    print(cosine_similarity(np.array([item_vector,item_vector,item_vector]).reshape(3, -1), np.array(class_vectors).reshape(3, -1)))
    similarities = [cosine_similarity(item_vector, class_vector) for class_vector in class_vectors]
    print(similarities)
    best_match_index = np.argmax(similarities)
    return class_labels[best_match_index]

# Function for keyword matching with word embeddings
def keyword_matching_with_embeddings(item):
    item_keywords = extract_keywords(item)
    #print(item_keywords)
    #np.mean(nlp(item_keywords[0]).vector)
    item_vector = [nlp(keyword).vector_norm for keyword in item_keywords ]
    item_vector = np.array([[np.mean(item_vector)]])
    #item_vector = np.array([item_vector])
    print(item_vector)
    matched_class = cosine_similarity_matching(item_vector, class_vectors, class_labels)
    return matched_class

# Function for description analysis with word embeddings
def description_analysis_matching_with_embeddings(item):
    description = extract_description(item)
    description_vector = np.mean([nlp(token.text).vector for token in nlp(description)], axis=0)
    
    matched_class = cosine_similarity_matching(description_vector, class_vectors, class_labels)
    return matched_class

# Main function
def main():
    items = ['Smartphone', 'Engine Oil', 'Chocolate Bar']

    print("Matching items to classes using Keyword Matching with Word Embeddings:")
    for item in items:
        matched_class = keyword_matching_with_embeddings(item)
        print(f"{item}: {matched_class}")

    # print("\nMatching items to classes using Description Analysis with Word Embeddings:")
    # for item in items:
    #     matched_class = description_analysis_matching_with_embeddings(item)
    #     print(f"{item}: {matched_class}")

if __name__ == "__main__":
    main()