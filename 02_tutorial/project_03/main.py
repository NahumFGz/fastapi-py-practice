from typing import Annotated

import models
from database import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException, Path, status
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
async def read_all(db: Annotated[Session, Depends(get_db)]):
    return db.query(models.Todos).all()


@app.get("/todo/{todo_id}")
async def read_todo(db: db_dependency, todo_id: Annotated[int, Path(gt=0)]):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontro la tarea")
