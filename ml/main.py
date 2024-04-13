import spacy 
import numpy as np


nlp = spacy.load('en_core_web_md') 
CLASS_KEYWORDS = ['electronics', 'car', 'food']
CLASS_TOKENS = nlp(' '.join(CLASS_KEYWORDS))


''' Version for word or sentence'''

def calculate_similarities(class_tokens, embedding):
    similarities = [class_token.similarity(embedding) for class_token in class_tokens]
    best_match_index = np.argmax(similarities)
    return best_match_index, similarities[best_match_index]

print("Enter space-separated words or commas") 
inputs = input() 
inputs = inputs.split(',')

embeddings = [nlp(inp) for inp in inputs]
embeddings_no_stopwrods = [nlp(' '.join([str(t) for t in embedding if not t.is_stop])) for embedding in embeddings]

#print(search_doc_no_stop_words.similarity(main_doc_no_stop_words))

for embedding in embeddings_no_stopwrods:
    matched_class, similarity_value = calculate_similarities(class_tokens=CLASS_TOKENS, embedding=embedding)
    print(f"Input: {embedding.text}, Class: {CLASS_KEYWORDS[matched_class]}\nSim_value:{similarity_value}\n")



''' Version for only one word'''

'''
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

'''
    
	

 
