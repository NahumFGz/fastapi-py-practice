from typing import Annotated, Optional

from fastapi import Body, FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

app = FastAPI()


# Clase base que define un libro (sin Pydantic, se usa solo como estructura interna)
class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


# Base de datos simulada en memoria
BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book!", 5, 2030),
    Book(2, "Be Fast with FastAPI", "codingwithroby", "A great book!", 5, 2030),
    Book(3, "Master Endpoints", "codingwithroby", "A awesome book!", 5, 2029),
    Book(4, "HP1", "Author 1", "Book Description", 2, 2028),
    Book(5, "HP2", "Author 2", "Book Description", 3, 2027),
    Book(6, "HP3", "Author 3", "Book Description", 1, 2026),
]


# Modelo de entrada con validaciones automáticas usando Pydantic
class BookRequest(BaseModel):
    id: Optional[int] = Field(description="No se necesita el id para crear", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2029,
            }
        }
    }


# =================== VERSIONAMIENTO EN ENDPOINTS ===================


# Leer todos los libros
@app.get("/books/v1", status_code=status.HTTP_200_OK)
# V1: implementación básica sin uso de Annotated
async def read_all_books_v1():
    return BOOKS


@app.get("/books/v2", status_code=status.HTTP_200_OK)
# V2: igual funcionalidad que V1, pero aquí podríamos ir introduciendo Annotated aunque no se aplica aún
async def read_all_books_v2():
    return BOOKS


@app.get("/books/v3", status_code=status.HTTP_200_OK)
# V3: sin cambios adicionales aquí, útil si luego se agregan validaciones o documentación adicional
async def read_all_books_v3():
    return BOOKS


# Buscar por rating
@app.get("/books-rating/v1")
# V1: usamos Query con validaciones, pero sin Annotated
async def read_book_by_rating_v1(book_rating: int = Query(gt=0, lt=6)):
    return [book for book in BOOKS if book.rating == book_rating]


@app.get("/books-rating/v2")
# V2: usamos Annotated para separar el tipo y la metadata (más legible y compatible con herramientas externas)
async def read_book_by_rating_v2(book_rating: Annotated[int, Query(gt=0, lt=6)]):
    return [book for book in BOOKS if book.rating == book_rating]


@app.get("/books-rating/v3")
# V3: misma validación pero ahora agregamos descripción para mejorar la documentación Swagger
async def read_book_by_rating_v3(book_rating: Annotated[int, Query(gt=0, lt=6, description="Debe estar entre 1 y 5")]):
    return [book for book in BOOKS if book.rating == book_rating]


# Buscar por fecha de publicación
@app.get("/books/publish/v1")
async def read_books_by_publish_date_v1(published_date: int = Query(gt=1999, lt=2031)):
    return [book for book in BOOKS if book.published_date == published_date]


@app.get("/books/publish/v2")
async def read_books_by_publish_date_v2(published_date: Annotated[int, Query(gt=1999, lt=2031)]):
    return [book for book in BOOKS if book.published_date == published_date]


@app.get("/books/publish/v3")
async def read_books_by_publish_date_v3(
    published_date: Annotated[int, Query(gt=1999, lt=2031, description="Año entre 2000 y 2030")],
):
    return [book for book in BOOKS if book.published_date == published_date]


# Crear nuevo libro
@app.post("/create-book/v1")
# V1: el modelo BookRequest es interpretado como Body por defecto, sin ser explícito
async def create_book_v1(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return {"message": "Libro creado correctamente"}


@app.post("/create-book/v2")
# V2: usamos Annotated con Body() para hacer explícito que el dato viene del cuerpo del request
async def create_book_v2(book_request: Annotated[BookRequest, Body()]):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return {"message": "Libro creado correctamente"}


@app.post("/create-book/v3")
# V3: usamos embed=True para anidar el JSON y añadimos descripción en Swagger
async def create_book_v3(book_request: Annotated[BookRequest, Body(embed=True, description="Datos del nuevo libro")]):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return {"message": "Libro creado correctamente"}


# Actualizar libro (todo el objeto)
@app.put("/books/update_book/v1")
# V1: Body no está explícito
async def update_book_v1(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            return {"message": "Libro actualizado"}
    raise HTTPException(status_code=404, detail="Item not found")


@app.put("/books/update_book/v2")
# V2: especificamos que book viene del cuerpo con Annotated y Body()
async def update_book_v2(book: Annotated[BookRequest, Body()]):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            return {"message": "Libro actualizado"}
    raise HTTPException(status_code=404, detail="Item not found")


@app.put("/books/update_book/v3")
# V3: anidamos el JSON (embed=True)
async def update_book_v3(book: Annotated[BookRequest, Body(embed=True)]):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            return {"message": "Libro actualizado"}
    raise HTTPException(status_code=404, detail="Item not found")


# Actualizar libro por ID
@app.put("/books/v1/{book_id}")
# V1: ID sin validación, body no explícito
async def update_book_by_id_v1(book_id: int, book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            updated_book = Book(**book.model_dump())
            updated_book.id = book_id
            BOOKS[i] = updated_book
            return {"message": "Libro actualizado"}
    raise HTTPException(status_code=404, detail="Item not found")


@app.put("/books/v2/{book_id}")
# V2: validamos que ID sea positivo con Annotated y Body explícito
async def update_book_by_id_v2(book_id: Annotated[int, Path(gt=0)], book: Annotated[BookRequest, Body()]):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            updated_book = Book(**book.model_dump())
            updated_book.id = book_id
            BOOKS[i] = updated_book
            return {"message": "Libro actualizado"}
    raise HTTPException(status_code=404, detail="Item not found")


@app.put("/books/v3/{book_id}")
# V3: además se agrega descripción al parámetro ID y se anida el body
async def update_book_by_id_v3(
    book_id: Annotated[int, Path(gt=0, description="ID positivo del libro")],
    book: Annotated[BookRequest, Body(embed=True)],
):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            updated_book = Book(**book.model_dump())
            updated_book.id = book_id
            BOOKS[i] = updated_book
            return {"message": "Libro actualizado"}
    raise HTTPException(status_code=404, detail="Item not found")


# Eliminar libro
@app.delete("/books/v1/{book_id}")
# V1: validamos que ID sea positivo, sin más metadatos
async def delete_book_v1(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return {"message": "Eliminado correctamente"}
    raise HTTPException(status_code=404, detail="no encontrado")


@app.delete("/books/v2/{book_id}")
# V2: usamos Annotated con Path (más limpio y legible)
async def delete_book_v2(book_id: Annotated[int, Path(gt=0)]):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return {"message": "Eliminado correctamente"}
    raise HTTPException(status_code=404, detail="no encontrado")


@app.delete("/books/v3/{book_id}")
# V3: añadimos descripción en Swagger para documentar mejor el parámetro
async def delete_book_v3(book_id: Annotated[int, Path(gt=0, description="ID del libro a eliminar")]):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return {"message": "Eliminado correctamente"}
    raise HTTPException(status_code=404, detail="no encontrado")


# =================== FUNCIONES AUXILIARES ===================


# Genera un nuevo ID secuencial para libros nuevos
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
