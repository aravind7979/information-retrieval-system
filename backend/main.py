import os
import json
import string

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Please dont show suggestions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

query_search = []

def load_documents():
    docs = {}
    folder_path = "../documents"

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r") as file:
                text = file.read()

                docs[filename] = text

    return docs

# Returns:
# {
#     "doc1.txt": "Aravind is building a search engine.\nThe engine is very fast.",
#     "doc2.txt": "Founder of Abhi Technologies - Abhishekar"
# }
    
my_documents = load_documents()
print(my_documents)
print("____________________________________")
print("\n")



def clean_and_tokenize(text):
    all_clean_words = []
    text = text.lower()
    
    for p in string.punctuation:
        text = text.replace(p, "")
        
    words = text.split()
    print(words)
    
    
    stop_words = ["is", "the", "a", "an", "and", "of", "to", "in", "for", "on", "at", "by"]
    
    for word in words:
        if word not in stop_words:
            all_clean_words.append(word)
            
        
    return all_clean_words  # returns all_clean_words = ["what" "vaivi" "aravind"]
    

final_cleaned_document_data = {}
for filename, text in my_documents.items():
    final_cleaned_document_data[filename] = clean_and_tokenize(text)

print(final_cleaned_document_data)

    #{
    #"doc1.txt": ["aravind", "building", "search", "engine", "fast"],
    #"doc2.txt": ["founder", "abhi", "technologies", "abhishekar"]
    #}
    
def inverted_indexing(final_cleaned_document_data):
    inverted_index = {}
    
    for filename, words in final_cleaned_document_data.items():
        for word in words:
            
            if word not in inverted_index:
                inverted_index[word] = []
                
            if filename not in inverted_index[word]:
                inverted_index[word].append(filename)
                
    return inverted_index
    
inverted_index = inverted_indexing(final_cleaned_document_data)

@app.get("/search")
def search_docs(query: str, is_submit: bool = False):
    
    if is_submit:
        if query not in query_search:
            query_search.append(query)
            
    clean_query = []
    clean_query = clean_and_tokenize(query)
    
    matched_docs = []
    
    for word in clean_query:
        if word in inverted_index:
            
            for filename in inverted_index[word]:
                if filename not in matched_docs:
                    matched_docs.append(filename)

    for item in query_search:
        if query.lower() in item.lower():
            if item not in matched_docs:
                matched_docs.append(item)
                    
    return{
        "matches": matched_docs
    }