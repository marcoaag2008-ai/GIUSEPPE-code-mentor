from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Dirección de la base de datos: SQLite, archivo local llamado codementor.db
DATABASE_URL = "sqlite:///./codementor.db"

# El "engine" es la conexión real hacia ese archivo
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Fábrica de sesiones: cada endpoint pedirá una sesión nueva de aquí
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de la que van a heredar todos los modelos (tablas)
Base = declarative_base()


def get_db():
    """
    Función que entrega una sesión de base de datos a un endpoint,
    y se asegura de cerrarla cuando termina, pase lo que pase.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
