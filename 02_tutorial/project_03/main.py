from typing import Annotated

import models
from database import engine
from fastapi import FastAPI
from routers import admin, auth, todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(todos.router, prefix="/todo")
app.include_router(admin.router)
