# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from app.main import app
from app.database import get_db, engine

# Cliente de pruebas conectado a la APP real
client = TestClient(app)

# FIXTURE: Esto se ejecuta antes de cada prueba para limpiar la tabla
# y asegurar que probamos en un entorno limpio pero REAL.
@pytest.fixture(autouse=True)
def clean_db():
    # Limpiamos las tablas antes de testear para no tener errores de duplicados
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM tasks"))
        connection.execute(text("DELETE FROM users"))
        connection.commit()

def test_api_flow_real_db():
    # A. Crear Usuario
    response = client.post(
        "/users/",
        json={"name": "Real User", "email": "real@example.com"},
    )
    assert response.status_code == 200
    data = response.json()
    user_id = data["id"]

    # B. Crear Tarea
    response = client.post(
        "/tasks/",
        json={"title": "Real DB Task", "description": "Testing MySQL", "user_id": user_id},
    )
    assert response.status_code == 200
    task_data = response.json()
    task_id = task_data["id"]

    # C. Listar Tareas
    response = client.get(f"/users/{user_id}/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Real DB Task"

    # D. Eliminar Tarea
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200