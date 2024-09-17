from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import sqlite3
from typing import List, Optional
from datetime import date
import db


app = FastAPI()

db.init_db()


def get_db():
    connection = sqlite3.connect("library.db")
    try:
        yield connection
    finally:
        connection.close()


class Author(BaseModel):
    name: str


class Book(BaseModel):
    title: str
    author_id: int
    published_date: Optional[date] = None


# Create author
@app.post("/authors/", response_model=Author)
def create_author(author: Author, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("INSERT INTO authors (name) VALUES (?)", (author.name,))
    db.commit()
    author_id = cursor.lastrowid
    return {**author.model_dump(), "id": author_id}


# Read author
@app.get("/authors/{author_id}", response_model=Author)
def read_author(author_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM authors WHERE id = ?", (author_id,))
    author = cursor.fetchone()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return {"id": author[0], "name": author[1]}


# Update author
@app.put("/authors/{author_id}", response_model=Author)
def update_author(author_id: int, updated_author: Author, 
                  db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM authors WHERE id = ?", (author_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Author not found")
    cursor.execute(
        "UPDATE authors SET name = ? WHERE id = ?",
        (updated_author.name, author_id),
    )
    db.commit()
    return {**updated_author.model_dump(), "id": author_id}


# Create book
@app.post("/books/", response_model=Book)
def create_book(book: Book, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO books (title, author_id, published_date) VALUES (?, ?, ?)",
        (book.title, book.author_id, book.published_date),
    )
    db.commit()
    book_id = cursor.lastrowid
    return {**book.model_dump(), "id": book_id}


# Read book
@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {
        "id": book_id,
        "title": book[1],
        "author_id": book[2],
        "published_date": book[3],
    }


# Update book
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book,
                db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Book not found")
    cursor.execute(
        "UPDATE books SET title = ?, author_id = ?, published_date = ? WHERE id = ?",
        (updated_book.title, updated_book.author_id,
         updated_book.published_date, book_id),
    )
    db.commit()
    return {**updated_book.model_dump(), "id": book_id}


# Partial update book
@app.patch("/books/{book_id}")
def partial_update_book(book_id: int, updates: dict,
                        db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Book not found")

    set_clause = ', '.join([f"{key} = ?" for key in updates.keys()])
    values = list(updates.values()) + [book_id]

    cursor.execute(f"UPDATE books SET {set_clause} WHERE id = ?", values)
    db.commit()
    return {"book_id": book_id, "updated_fields": updates}


# List all books
@app.get("/books/", response_model=List[Book])
def list_books(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return [
        {"id": book[0], "title": book[1], "author_id": book[2], "published_date": book[3]}
        for book in books
    ]


# Task 1: Delete a book
@app.delete("/books/delete")
def delete_book(book_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="Book not found")
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    db.commit()
    return {"response": f"Book with ID {book_id} has been deleted."}


# Task 2: Search books by title
@app.get("/books/search/", response_model=List[Book])
def search_books(title: str, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE ?", (f"%{title}%",))
    books = cursor.fetchall()
    return [
            {
                "id": book[0], "title": book[1],
                "author_id": book[2],
                "published_date": book[3]
            }
            for book in books
            ]
