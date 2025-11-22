# tests/test_integration.py

def test_full_crud_flow(client):
    """Prueba de Integración: Ciclo completo Usuario -> Tarea -> Listar -> Borrar"""
    
    # 1. Crear Usuario
    print("Paso 1: Creando usuario...")
    req_user = client.post("/users/", json={"name": "Integration User", "email": "flow@test.com"})
    assert req_user.status_code == 200
    user_id = req_user.json()["id"]

    # 2. Crear Tarea
    print("Paso 2: Creando tarea...")
    req_task = client.post("/tasks/", json={
        "title": "Integration Task", 
        "description": "Testing full flow", 
        "user_id": user_id
    })
    assert req_task.status_code == 200
    task_id = req_task.json()["id"]

    # 3. Listar Tareas del Usuario
    print("Paso 3: Verificando lista...")
    req_list = client.get(f"/users/{user_id}/tasks")
    assert req_list.status_code == 200
    tasks = req_list.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Integration Task"

    # 4. Eliminar Tarea
    print("Paso 4: Eliminando tarea...")
    req_del = client.delete(f"/tasks/{task_id}")
    assert req_del.status_code == 200
    
    # 5. Verificar que ya no existe
    req_list_again = client.get(f"/users/{user_id}/tasks")
    assert len(req_list_again.json()) == 0