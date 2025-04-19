from fastapi import Body, FastAPI, HTTPException, status
from pydantic import BaseModel

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


#! A. buscar por dynamic params
@app.get("/books/v1/{book_title}")
async def read_book(book_title: str):
    book_name = ""

    for book in BOOKS:
        if book.get("title", "").casefold() == book_title.casefold():
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


#! B. buscar por query params
@app.get("/books/by-author/v1")
async def read_books_by_author(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author", "").casefold() == author.casefold():
            books_to_return.append(book)

    return books_to_return


@app.get("/books/by-author/v2")
async def read_books_by_author_v2(author: str):
    books = [book for book in BOOKS if book.get("author", "").casefold() == author.casefold()]

    if len(books) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autor no encontrado")

    return books


#! C. Buscar por dynamic_param y query param
@app.get("/books/{book_author}/v1")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (
            book.get("author", "").casefold() == book_author.casefold()
            and book.get("category", "").casefold() == category.casefold()
        ):
            books_to_return.append(book)

    return books_to_return


@app.get("/books/{book_author}/v2")
async def read_author_by_query_v2(book_author: str, category: str):
    books_to_return = [
        book
        for book in BOOKS
        if book.get("author", "").casefold() == book_author.casefold()
        and book.get("category", "").casefold() == category.casefold()
    ]

    if len(books_to_return) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado")

    return books_to_return


@app.post("/books/create_book/v1")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

    return BOOKS


class Book(BaseModel):
    title: str
    author: str
    category: str


@app.post("/books/create_book/v2")
async def create_book_v2(new_book: Book):
    BOOKS.append(new_book)

    return new_book


@app.post("/books/create_book/v3")
async def create_book_v3(new_book: Book = Body(..., embed=True)):
    BOOKS.append(new_book)

    return new_book


@app.put("/books/update_book/v1")
async def update_book(update_book=Body()):

    j = 0
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title", "").casefold() == update_book.get("title", "").casefold():
            BOOKS[i] = update_book
            j = i
            break

    return BOOKS[j]


@app.put("/books/update_book/v2")
async def update_book_v2(update_book: Book):
    for index, book in enumerate(BOOKS):
        if book.get("title", "").casefold() == update_book.title.casefold():
            BOOKS[index] = update_book.model_dump()
            return {"message": "libro actualizado correctamente"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no encontrado")


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break

    return BOOKS
