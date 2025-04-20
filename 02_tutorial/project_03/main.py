from typing import Annotated

import models
from database import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field
from routers import auth
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(auth.router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@app.get("/")
async def read_all(db: Annotated[Session, Depends(get_db)]):
    return db.query(models.Todos).all()


@app.get("/todo/{todo_id}")
async def read_todo(db: db_dependency, todo_id: Annotated[int, Path(gt=0)]):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontro la tarea")


@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = models.Todos(**todo_request.model_dump())

    db.add(todo_model)
    db.commit()

    return {"message": "Tarea creada correctamente"}


@app.put("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(
    db: db_dependency, todo_id: Annotated[int, Path(gt=0)], todo_request: TodoRequest
):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo no encontrado")

    todo_model.title = todo_request.title
    todo_model.description = todo_model.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    # db.add(todo_model)  # SQLalchemy detecta que es un update o create, no es necesario ponerlo
    db.commit()

    return {"message": "Actualización correcta"}


@app.delete("/todo/{todo_id}")
async def delete_todo(db: db_dependency, todo_id: Annotated[int, Path(gt=0)]):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo no encontrado")

    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()

    return {"message": "Eliminación correcta"}
