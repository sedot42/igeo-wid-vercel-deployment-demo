import os
from typing import Annotated
from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [os.getenv("FRONTEND_ORIGIN") or "", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET"],
    # allow_headers=["*"],
)

books = [
    {"name": "Iliad", "author": "Homer", "year": 800, "genre": "Epic"},
    {"name": "Othello", "author": "Shakespeare", "year": 1603, "genre": "Tragedy"},
    {"name": "Emma", "author": "Austen", "year": 1815, "genre": "Romance"},
    {"name": "Moby", "author": "Melville", "year": 1851, "genre": "Adventure"},
    {"name": "Siddhartha", "author": "Hesse", "year": 1922, "genre": "Philosophical"},
]


@app.get("/books/{name}")
def get_book_by_name(
    name: Annotated[str, Path(title="Name des Buchs", min_length=4)],
):
    """Gibt Buch nach Namen zurück."""
    book = [b for b in books if b["name"] == name]
    if len(book) > 0:
        return book[0]
    else:
        raise HTTPException(status_code=404, detail="Buch wurde nicht gefunden.")


@app.get("/books")
def get_books(
    author: Annotated[str | None, Query(title="Author des Buchs")] = None,
    year: Annotated[
        int | None, Query(title="Erscheinungsjahr des Buchs", gt=0, lt=2026)
    ] = None,
):
    """Gibt gefilterte Bücherliste zurück."""
    results = books
    if year:
        results = [b for b in results if b["year"] == year]
    if author:
        results = [b for b in results if b["author"] == author]
    return results
