from typing import Annotated

import models
from database import SessionLocal, engine
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#! db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
async def read_all(db: Annotated[Session, Depends(get_db)]):
    return db.query(models.Todos).all()
