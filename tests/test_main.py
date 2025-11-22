# tests/test_main.py
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# 1. Configuración de BD temporal para pruebas (SQLite en memoria)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea las tablas en la BD temporal
Base.metadata.create_all(bind=engine)

# 2. Override (Sobreescribir) la dependencia de BD
# Esto hace que la API use la BD temporal en vez de la real durante el test
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# 3. Prueba del Flujo Completo
def test_api_flow():
    # A. Crear Usuario
    response = client.post(
        "/users/",
        json={"name": "Test User", "email": "test@example.com"},
    )
    assert response.status_code == 200
    data = response.json()
    user_id = data["id"]
    assert data["email"] == "test@example.com"

    # B. Crear Tarea para ese usuario
    response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Testing API", "user_id": user_id},
    )
    assert response.status_code == 200
    task_data = response.json()
    task_id = task_data["id"]
    assert task_data["title"] == "Test Task"

    # C. Listar Tareas del usuario
    response = client.get(f"/users/{user_id}/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) > 0
    assert tasks[0]["title"] == "Test Task"

    # D. Eliminar Tarea
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Task deleted"}