# Importa la función para crear el motor de conexión a la base de datos
from sqlalchemy import create_engine

# Importa la clase base para definir los modelos de la base de datos
from sqlalchemy.ext.declarative import declarative_base

# Importa el constructor para crear sesiones que interactúan con la base de datos
from sqlalchemy.orm import sessionmaker

# Define la URL de conexión a la base de datos SQLite local (archivo todosapp.db)
SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"

# Crea el motor de conexión a la base de datos, necesario para que SQLAlchemy se conecte.
# El argumento `check_same_thread=False` es necesario en SQLite para evitar errores de concurrencia con múltiples hilos.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Crea una clase de sesión. Esta se usará para crear instancias de sesión que nos permiten hacer operaciones como consultas, inserciones o actualizaciones en la base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea una clase base que se usará como clase padre para todos los modelos de base de datos.
# Es decir, cada tabla del ORM heredará de esta clase `Base`.
Base = declarative_base()
