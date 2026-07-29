import os
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

Please dont show suggestions

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
    "Aravind loves Vaishnavi"
]

query_search = []

@app.get("/search")
def search_keyword(query : str):
