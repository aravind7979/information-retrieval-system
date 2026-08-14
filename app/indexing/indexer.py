def build_inverted_index(cleaned_document_data):
    inverted_index = {}
    
    for filename, words in cleaned_document_data.items():
        for word in words:
            if word not in inverted_index:
                inverted_index[word] = {}

            if filename not in inverted_index[word]:
                inverted_index[word][filename] = 1
            else:
                inverted_index[word][filename] += 1

    return inverted_index
