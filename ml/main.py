import spacy 
import numpy as np


nlp = spacy.load('en_core_web_md') 
CLASS_KEYWORDS = ['electronics', 'car', 'food']
CLASS_TOKENS = nlp(' '.join(CLASS_KEYWORDS))

def calculate_similarities(class_tokens, token):
    similarities = [class_token.similarity(token) for class_token in class_tokens]
    best_match_index = np.argmax(similarities)
    return best_match_index
    

print("Enter two space-separated words") 
words = input() 

tokens = nlp(words) 

for token in tokens: 
    #print(token.text, token.has_vector, token.vector_norm, token.is_oov)
    matched_class = calculate_similarities(class_tokens=CLASS_TOKENS, token=token)
    print(f"{token.text}: {CLASS_KEYWORDS[matched_class]}")
    
	

 
