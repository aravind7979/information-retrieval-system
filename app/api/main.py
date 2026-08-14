import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.ingestion.reader import load_documents
from app.preprocessing.cleaner import clean_and_tokenize
from app.indexing.indexer import build_inverted_index
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

# Global State (In-Memory Index for now)
my_documents = {}
final_cleaned_document_data = {}
inverted_index = {}
query_search = []

def initialize_search_engine():
    global my_documents, final_cleaned_document_data, inverted_index
    
    # Resolving path to the documents folder at the root
    # Since main.py is in app/api/, we go up two directories
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    docs_path = os.path.join(base_dir, "documents")
    
    my_documents = load_documents(docs_path)
    
    for filename, text in my_documents.items():
        final_cleaned_document_data[filename] = clean_and_tokenize(text)
        
    inverted_index = build_inverted_index(final_cleaned_document_data)
    
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

# Dependency to get DB session
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
    
    for word in clean_query:
        if word in inverted_index:
            for filename, score in inverted_index[word].items():
                if filename not in document_scores:
                    document_scores[filename] = score
                else:
                    document_scores[filename] += score
                    
    sorted_docs = sorted(document_scores, key=document_scores.get, reverse=True)
    
    # Add history matches (simplified for now)
    for item in query_search:
        if query.lower() in item.lower():
            if item not in sorted_docs:
                sorted_docs.append(item)
                    
    return {
        "matches": sorted_docs
    }
