# app/main.py
from fastapi import FastAPI
from app.database import engine
from app.models import models
from app.controllers import task_controller

# Esta línea crea las tablas automáticamente en phpMyAdmin si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Incluimos las rutas que definimos en el controlador
app.include_router(task_controller.router)

@app.get("/")
def read_root():
    return {"message": "API de Tareas funcionando correctamente"}