# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Conexión a MySQL (phpMyAdmin).
# Formato: mysql+pymysql://usuario:contraseña@host:puerto/nombre_bd
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3307/parcial_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Función para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()