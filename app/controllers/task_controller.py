# app/controllers/task_controller.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import schemas
from app.services import task_service

router = APIRouter()

@router.post("/users/", tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return task_service.create_user(db, user)

@router.post("/tasks/", response_model=schemas.TaskResponse, tags=["Tasks"])
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, task)

@router.get("/users/{user_id}/tasks", response_model=list[schemas.TaskResponse], tags=["Tasks"])
def read_user_tasks(user_id: int, db: Session = Depends(get_db)):
    return task_service.get_tasks_by_user(db, user_id)

@router.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted = task_service.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}