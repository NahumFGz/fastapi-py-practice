from typing import Annotated

from database import SessionLocal
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from models import Users
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter(tags=["Auth"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/")
async def get_user():
    return {"user": "authenticated"}


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency):
    users = db.query(Users).all()
    return users


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    """
    Maneja la autenticación del usuario y devuelve un token de acceso.

    Parameters:
    - form_data: instancia de OAuth2PasswordRequestForm, extraída automáticamente
      por FastAPI desde un formulario `application/x-www-form-urlencoded` que contenga
      los campos `username` y `password`.

      ⚠️ Aunque Depends() está vacío, FastAPI sabe que debe usar el tipo
      OAuth2PasswordRequestForm como dependencia porque está anotado explícitamente.
      Internamente esto es equivalente a: Depends(OAuth2PasswordRequestForm)

      ✅ FastAPI permite que tanto funciones como clases sean utilizadas como dependencias.
      Si una clase como `OAuth2PasswordRequestForm` implementa un método `__call__()`
      o es compatible con el sistema de dependencias, FastAPI puede instanciarla usando
      automáticamente los datos del request (por ejemplo, `request.form()`).

    - db: instancia de SQLAlchemy Session, proporcionada automáticamente por la
      función `get_db()` a través de la inyección de dependencias.

    Returns:
    - Un token de acceso si las credenciales son válidas (aún no implementado en esta versión).
    """
    return form_data.username
