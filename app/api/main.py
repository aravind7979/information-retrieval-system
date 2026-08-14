import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.ingestion.reader import load_documents
from app.preprocessing.cleaner import clean_and_tokenize
from app.indexing.indexer import build_inverted_index
from app.retrieval.snippets import generate_snippet
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
query_search = []

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
        if query not in query_search:
            query_search.append(query)
            
    clean_query = clean_and_tokenize(query)
    document_scores = {}
    
    # Calculate TF-IDF Score
    for word in clean_query:
        if word in inverted_index:
            for filename, tf_idf_score in inverted_index[word].items():
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
        snippet = generate_snippet(clean_query, original_text)
        
        formatted_results.append({
            "title": filename,
            "score": round(score, 4),
            "snippet": snippet,
            "type": "document"
        })
    
    # Add history matches (simplified for now)
    for item in query_search:
        if query.lower() in item.lower():
            # Check if history item is already added to results
            if not any(r["title"] == item for r in formatted_results):
                formatted_results.append({
                    "title": item,
                    "score": 0,
                    "snippet": "Previous Search",
                    "type": "history"
                })
                    
    return {
        "matches": formatted_results
    }
