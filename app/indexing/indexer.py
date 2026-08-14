import math

def build_inverted_index(cleaned_document_data):
    inverted_index = {}
    doc_lengths = {}
    
    total_docs = len(cleaned_document_data)
    if total_docs == 0:
        return {}, {}
    
    # 1. Calculate Term Frequencies (TF)
    for filename, words in cleaned_document_data.items():
        doc_lengths[filename] = len(words)
        for word in words:
            if word not in inverted_index:
                inverted_index[word] = {}

            if filename not in inverted_index[word]:
                inverted_index[word][filename] = 1
            else:
                inverted_index[word][filename] += 1

    # 2. Calculate TF-IDF
    tf_idf_index = {}
    for word, doc_counts in inverted_index.items():
        tf_idf_index[word] = {}
        
        # Document Frequency (DF): How many docs have this word?
        df = len(doc_counts) 
        
        # Inverse Document Frequency (IDF)
        idf = math.log10(total_docs / float(df))
        
        for filename, count in doc_counts.items():
            # Term Frequency = Count / Total words in document
            tf = count / float(max(doc_lengths[filename], 1))
            
            # Final Score
            tf_idf_index[word][filename] = tf * idf

    return tf_idf_index, doc_lengths
