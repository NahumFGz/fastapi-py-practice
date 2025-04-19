from fastapi import FastAPI, HTTPException

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"},
]

app = FastAPI()


@app.get("/books")
async def read_all_books():
    return {"data": BOOKS}


@app.get("/books/v1/{book_title}")
async def read_book(book_title: str):
    book_name = ""

    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            book_name = book
            break
    if book_name != "":
        return book_name
    else:
        return {"message": "No encontrado"}


@app.get("/books/v2/{book_title}")
async def read_book_v2(book_title: str):
    # Buscamos el primer libro cuyo título coincida con el parámetro 'book_title', ignorando mayúsculas/minúsculas
    book = next(
        (b for b in BOOKS if b["title"].casefold() == book_title.casefold()),
        None,  # Valor por defecto si no se encuentra ningún libro
    )

    # Si encontramos el libro, lo devolvemos
    if book:
        return book

    # Si no se encontró el libro, lanzamos una excepción HTTP 404 con un mensaje personalizado
    raise HTTPException(status_code=404, detail="Libro no encontrado")
