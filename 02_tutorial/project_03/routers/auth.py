from datetime import datetime, timedelta, timezone
from typing import Annotated

from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from models import Users
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter(tags=["Auth"])


SECRET_KEY = "PALABRASUPERSECRETA"
ALGORITHM = "HS256"


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


##################################
def authenticate_user(username: str, password: str, db: Session) -> Users | bool:
    user: Users = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False

    if not bcrypt_context.verify(password, user.hashed_password):
        return False

    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
            )
        return {"username": username, "id": user_id}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )


##################################


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


@router.post("/token", response_model=Token)
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
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return "Failed authentification"

    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}
