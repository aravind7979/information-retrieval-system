# Custom Information Retrieval System (IRS)

**Live Demo:** [https://information-retrieval-system.vercel.app/](https://information-retrieval-system.vercel.app/)

## 🚀 About This Project

I built this project to deeply understand the core mechanics of how modern search engines work under the hood. Instead of relying on pre-built libraries like Elasticsearch or heavy machine learning models right out of the gate, I wanted to build the mathematical algorithms and data structures from scratch in pure Python.

This project represents my learning journey through Information Retrieval, from basic text parsing to TF-IDF mathematical ranking, Boolean logic filtering, and eventually Semantic Search expansion.

## 🧠 Features & Learning Milestones

Throughout the development of this engine, I focused on implementing the following core computer science and NLP concepts:

- **Inverted Indexing**: Engineered a custom inverted index (mapping Words -> Documents) to replace slow linear scanning.
- **TF-IDF Mathematical Ranking**: Built the Term Frequency-Inverse Document Frequency algorithm from scratch to mathematically score and rank the relevance of documents.
- **Boolean Logic & Set Theory**: Implemented `AND`, `OR`, and `NOT` query operators utilizing highly optimized Python `set` intersections and unions.
- **Exact Phrase Searching**: Built a secondary pipeline to filter documents using exact string matching when queries are wrapped in quotes.
- **Semantic Synonym Expansion**: Bridged the vocabulary gap by creating a synonym dictionary that silently expands user queries (e.g., searching "car" automatically searches for "automobile" and "vehicle").
- **Persistent Storage**: Integrated SQLite via SQLAlchemy to persist document metadata and user search history across server restarts.
- **Contextual Snippets**: Wrote an algorithm to extract and highlight the surrounding text context of a matched keyword for the frontend UI.

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, PyPDF2
- **Database**: SQLite
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Deployment**: AWS EC2 (Backend), Vercel (Frontend)

## 💻 How to Run Locally

If you want to clone this repo and run the search engine on your own machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/information-retrieval-system.git
   cd information-retrieval-system
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the FastAPI backend:**
   ```bash
   uvicorn app.api.main:app --reload
   ```

4. **Launch the Frontend:**
   Just double-click `frontend/index.html` to open it in your browser!
