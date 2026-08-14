import string

def clean_and_tokenize(text):
    all_clean_words = []
    text = text.lower()
    
    for p in string.punctuation:
        text = text.replace(p, "")
        
    words = text.split()
    
    # Expanded stopwords list
    stop_words = ["is", "the", "a", "an", "and", "of", "to", "in", "for", "on", "at", "by", "this", "that", "it"]
    
    for word in words:
        if word not in stop_words:
            all_clean_words.append(word)
            
    return all_clean_words
