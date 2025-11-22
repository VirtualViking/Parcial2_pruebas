# tests/conftest.py
import pytest
from sqlalchemy import text
from app.database import engine
from fastapi.testclient import TestClient
from app.main import app

# Este archivo configura la limpieza de la BD para TODAS las pruebas

@pytest.fixture(scope="function", autouse=True)
def clean_db():
    """Limpia las tablas antes de cada prueba para empezar de cero."""
    with engine.connect() as connection:
        # Desactivamos chequeo de llaves foráneas para borrar sin problemas
        connection.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        connection.execute(text("TRUNCATE TABLE tasks"))
        connection.execute(text("TRUNCATE TABLE users"))
        connection.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        connection.commit()

@pytest.fixture(scope="module")
def client():
    """Entrega el cliente de pruebas para hacer peticiones."""
    return TestClient(app)