import re

def generate_snippet(query_words, original_text, snippet_length=150):
    text_lower = original_text.lower()
    
    best_index = -1
    # Find the first occurrence of any search word
    for word in query_words:
        idx = text_lower.find(word)
        if idx != -1:
            best_index = idx
            break
            
    if best_index == -1:
        # If no exact word found, just return the beginning
        snippet = original_text[:snippet_length]
        return snippet.replace('\n', ' ') + "..."
        
    start = max(0, best_index - 40)
    end = min(len(original_text), best_index + snippet_length)
    
    snippet = original_text[start:end].replace('\n', ' ')
    
    if start > 0:
        snippet = "..." + snippet
    if end < len(original_text):
        snippet = snippet + "..."
        
    return snippet
