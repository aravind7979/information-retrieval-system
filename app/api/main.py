import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.ingestion.reader import load_documents
from app.preprocessing.cleaner import clean_and_tokenize
from app.indexing.indexer import build_inverted_index
from app.retrieval.snippets import generate_snippet
from app.query.parser import parse_boolean_query
from app.storage import models, database
from app.storage.database import engine, SessionLocal

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Global State
my_documents = {}
final_cleaned_document_data = {}
inverted_index = {}
doc_lengths = {}

def initialize_search_engine():
    global my_documents, final_cleaned_document_data, inverted_index, doc_lengths
    
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    docs_path = os.path.join(base_dir, "documents")
    
    my_documents = load_documents(docs_path)
    
    for filename, text in my_documents.items():
        final_cleaned_document_data[filename] = clean_and_tokenize(text)
        
    inverted_index, doc_lengths = build_inverted_index(final_cleaned_document_data)
    
    # Populate SQLite with Document Metadata
    db = SessionLocal()
    for filename, text in my_documents.items():
        existing = db.query(models.DocumentMetadata).filter(models.DocumentMetadata.filename == filename).first()
        if not existing:
            filepath = os.path.join(docs_path, filename)
            size = os.path.getsize(filepath) if os.path.exists(filepath) else 0
            ext = os.path.splitext(filename)[1]
            doc_meta = models.DocumentMetadata(
                filename=filename,
                filepath=filepath,
                extension=ext,
                size_bytes=size
            )
            db.add(doc_meta)
    db.commit()
    db.close()

# Initialize on startup
initialize_search_engine()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/search")
def search_docs(query: str, is_submit: bool = False, db: Session = Depends(get_db)):
    
    if is_submit:
        existing_history = db.query(models.SearchHistory).filter(models.SearchHistory.query_text == query).first()
        if not existing_history:
            new_history = models.SearchHistory(query_text=query)
            db.add(new_history)
            db.commit()
            
    # Phase 5 Logic: Phrase Search Parsing
    operator, parts, is_phrase, stripped_query = parse_boolean_query(query)
    
    part_doc_sets = []
    all_clean_words = [] 
    
    # Get documents for each part of the boolean query
    for part in parts:
        clean_part = clean_and_tokenize(part)
        all_clean_words.extend(clean_part)
        
        part_docs = set()
        for word in clean_part:
            if word in inverted_index:
                for filename in inverted_index[word].keys():
                    part_docs.add(filename)
        part_doc_sets.append(part_docs)
        
    # Apply Boolean Logic (AND / OR / NOT) using Python Sets
    final_docs = set()
    if operator == "OR":
        for doc_set in part_doc_sets:
            final_docs = final_docs.union(doc_set)
    elif operator == "AND":
        if len(part_doc_sets) > 0:
            final_docs = part_doc_sets[0]
            for doc_set in part_doc_sets[1:]:
                final_docs = final_docs.intersection(doc_set)
    elif operator == "NOT":
        if len(part_doc_sets) > 0:
            final_docs = part_doc_sets[0]
            if len(part_doc_sets) > 1:
                final_docs = final_docs.difference(part_doc_sets[1])

    # Phase 5: Filter exact phrases
    if is_phrase:
        phrase_filtered_docs = set()
        search_target = stripped_query.lower()
        for doc in final_docs:
            original_text = my_documents.get(doc, "").lower()
            # Direct string substring check for exact phrasing
            if search_target in original_text:
                phrase_filtered_docs.add(doc)
        final_docs = phrase_filtered_docs

    # Calculate TF-IDF Score only for documents that passed the filters
    document_scores = {}
    for word in all_clean_words:
        if word in inverted_index:
            for filename, tf_idf_score in inverted_index[word].items():
                if filename in final_docs:
                    if filename not in document_scores:
                        document_scores[filename] = tf_idf_score
                    else:
                        document_scores[filename] += tf_idf_score
                    
    # Sort documents by TF-IDF score
    sorted_filenames = sorted(document_scores, key=document_scores.get, reverse=True)
    
    # Format the results
    formatted_results = []
    for filename in sorted_filenames:
        score = document_scores[filename]
        original_text = my_documents.get(filename, "")
        snippet = generate_snippet(all_clean_words, original_text)
        
        formatted_results.append({
            "title": filename,
            "score": round(score, 4),
            "snippet": snippet,
            "type": "document"
        })
    
    # Fetch History Matches from SQLite
    all_history_records = db.query(models.SearchHistory).all()
    for record in all_history_records:
        if query.lower() in record.query_text.lower():
            if not any(r["title"] == record.query_text for r in formatted_results):
                formatted_results.append({
                    "title": record.query_text,
                    "score": 0,
                    "snippet": "Previous Search",
                    "type": "history"
                })
                    
    return {
        "matches": formatted_results
    }
