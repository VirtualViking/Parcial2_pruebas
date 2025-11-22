# tests/test_unit.py

def test_create_user_unit(client):
    """Prueba Unitaria: Verifica que se pueda crear un usuario individualmente"""
    response = client.post("/users/", json={"name": "Unit User", "email": "unit@test.com"})
    assert response.status_code == 200
    assert response.json()["email"] == "unit@test.com"
    assert "id" in response.json()

def test_task_default_status(client):
    """Prueba Unitaria: Verifica que una tarea nazca con is_completed = False"""
    # 1. Necesitamos un usuario primero (setup)
    user_resp = client.post("/users/", json={"name": "Task Owner", "email": "task@test.com"})
    user_id = user_resp.json()["id"]

    # 2. Creamos la tarea
    response = client.post("/tasks/", json={
        "title": "Default Check", 
        "description": "Checking default", 
        "user_id": user_id
    })
    
    # 3. Verificamos que is_completed sea False por defecto
    assert response.status_code == 200
    assert response.json()["is_completed"] is False