# Basic Synonym Dictionary for Semantic Expansion
SYNONYM_DICT = {
    "car": ["automobile", "vehicle", "truck"],
    "engine": ["motor", "machine"],
    "building": ["constructing", "creating", "making"],
    "fast": ["quick", "rapid", "speedy"],
    "founder": ["creator", "owner", "inventor"],
    "search": ["find", "discover", "seek"]
}

def expand_query_with_synonyms(query_words):
    """
    Takes a list of clean query words and returns an expanded list
    including known synonyms to simulate basic semantic matching.
    """
    expanded_words = set(query_words)
    
    for word in query_words:
        if word in SYNONYM_DICT:
            for synonym in SYNONYM_DICT[word]:
                expanded_words.add(synonym)
                
    return list(expanded_words)
