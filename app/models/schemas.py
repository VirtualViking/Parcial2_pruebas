# app/models/schemas.py
from pydantic import BaseModel
from typing import List, Optional

# Esquema para crear Usuario
class UserCreate(BaseModel):
    name: str
    email: str

# Esquema para crear Tarea
class TaskCreate(BaseModel):
    title: str
    description: str
    user_id: int

# Esquema para devolver Tarea (Response)
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool
    user_id: int

    class Config:
        from_attributes = True