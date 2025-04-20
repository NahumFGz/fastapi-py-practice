from typing import Annotated

import models
from database import engine
from fastapi import FastAPI
from routers import auth, todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix="/auth")
app.include_router(todos.router, prefix="/todo")
