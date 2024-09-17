This project is a simple student exercise that simulates library operations. It demonstrates basic functionality for managing library data using Python, FastAPI, and SQLite, and uses `uvicorn` as the server.

## Features

- **Book Management**: Add, update, delete, and retrieve information about books.
- **Author Management**: Add, update, and retrieve information about authors.
- **Book Search**: Search for books by title.

## Project Structure

- `main.py`: Contains the main logic for running the FastAPI application, including the API endpoints for managing the library system.
- `db.py`: Responsible for database operations such as setting up tables and handling database queries.

## Endpoints

### Author Endpoints:
- **POST /authors/**: Add a new author (requires `name`).
- **GET /authors/{author_id}**: Retrieve information about a specific author by ID.
- **PUT /authors/{author_id}**: Update an author’s information by ID.

### Book Endpoints:
- **POST /books/**: Add a new book (requires `title`, `author_id`, and optionally `published_date`).
- **GET /books/**: Retrieve a list of all books.
- **GET /books/{book_id}**: Retrieve a specific book by ID.
- **PATCH /books/{book_id}**: Partially update a book's details.
- **DELETE /books/{book_id}**: Delete a specific book by ID.
- **GET /books/search/**: Search books by title (requires query parameter `title`).

## Requirements

To run the project, you need:

1. **Python 3.x**: Make sure you have Python installed. You can download it from [here](https://www.python.org/downloads/).
2. **SQLite**: This project uses SQLite for the database.
3. **FastAPI and Uvicorn**: Install the necessary libraries with:
    ```bash
    pip install fastapi uvicorn sqlite3
    ```

## How to Run

1. **Clone the repository** to your local machine:
    ```bash
    git clone https://github.com/aiatasan/library_exercise.git
    ```

2. **Navigate to the project directory**:
    ```bash
    cd library_exercise
    ```

3. **Run the application using Uvicorn**:
    ```bash
    uvicorn main:app --reload
    ```

   This will start the FastAPI server, and you can access the application at `http://127.0.0.1:8000`.

4. **View API Documentation**:

   You can see all available API endpoints by visiting `http://127.0.0.1:8000/docs`.
   FastAPI automatically generates this interactive documentation for you.
