from gettext import dpgettext
from typing import Annotated

import models
from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from routers.auth import get_current_user
from sqlalchemy.orm import Session

router = APIRouter(tags=["Todo"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get("/")
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()


@router.get("/{todo_id}")
async def read_todo(user: user_dependency, db: db_dependency, todo_id: Annotated[int, Path(gt=0)]):

    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = (
        db.query(models.Todos)
        .filter(models.Todos.id == todo_id)
        .filter(models.Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is not None:
        return todo_model

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontro la tarea")


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = models.Todos(**todo_request.model_dump(), owner_id=user.get("id"))

    db.add(todo_model)
    db.commit()

    return {"message": "Tarea creada correctamente"}


@router.put("/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: Annotated[int, Path(gt=0)],
    todo_request: TodoRequest,
):

    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = (
        db.query(models.Todos)
        .filter(models.Todos.id == todo_id)
        .filter(models.Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo no encontrado")

    todo_model.title = todo_request.title
    todo_model.description = todo_model.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    # db.add(todo_model)  # SQLalchemy detecta que es un update o create, no es necesario ponerlo
    db.commit()

    return {"message": "Actualización correcta"}


@router.delete("/{todo_id}")
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: Annotated[int, Path(gt=0)]
):
    todo_model = (
        db.query(models.Todos)
        .filter(models.Todos.id == todo_id)
        .filter(models.Todos.owner_id == user.get("id"))
        .first()
    )

    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo no encontrado")

    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()

    return {"message": "Eliminación correcta"}
