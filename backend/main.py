import os
import json

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

database = [
    "Vaivi Search Engine",
    "Founder of Vaivi - Aravind Babu",
    "How to build search engine",
    "Aravind Vaishnavi",
    "Vaishnavi"
]

query_search = []

@app.get("/search")
def search_keyword(query : str, is_submit: bool = False):
    if is_submit == True:
        if query not in query_search:
            query_search.append(query)

    result = []

    for item in database:
        if query.lower() in item.lower():
            result.append(item)


    for item in query_search:
        if query.lower() in item.lower():
            result.append(item)


    return {
        "matches" : result
    }
