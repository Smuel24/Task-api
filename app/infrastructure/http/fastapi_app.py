from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.application.services.task_service import TaskService
from app.infrastructure.persistence.memory_task_repository import MemoryTaskRepository
from app.domain.task import Task

# Inicializar
app = FastAPI(title="Task API", version="1.0.0")
repository = MemoryTaskRepository()
service = TaskService(repository)

# Modelos Pydantic para request/response
class TaskCreateRequest(BaseModel):
    title: str
    status: str = "pending"

class TaskUpdateRequest(BaseModel):
    title: str
    status: str

class TaskResponse(BaseModel):
    id: int
    title: str
    status: str
    created_at: datetime

# Endpoints
@app.get("/health")
async def health_check():
    """Verificar estado del servicio"""
    return {"status": "ok"}

@app.get("/tasks", response_model=List[TaskResponse])
async def get_tasks():
    """Obtener todas las tareas"""
    try:
        tasks = await service.get_all_tasks()
        return [TaskResponse(
            id=t.id,
            title=t.title,
            status=t.status.value,
            created_at=t.created_at
        ) for t in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tasks", response_model=TaskResponse)
async def create_task(request: TaskCreateRequest):
    """Crear nueva tarea"""
    try:
        task = await service.create_task(request.title, request.status)
        return TaskResponse(
            id=task.id,
            title=task.title,
            status=task.status.value,
            created_at=task.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    """Obtener tarea por ID"""
    try:
        task = await service.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        return TaskResponse(
            id=task.id,
            title=task.title,
            status=task.status.value,
            created_at=task.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, request: TaskUpdateRequest):
    """Actualizar tarea"""
    try:
        task = await service.update_task(task_id, request.title, request.status)
        return TaskResponse(
            id=task.id,
            title=task.title,
            status=task.status.value,
            created_at=task.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    """Eliminar tarea"""
    try:
        deleted = await service.delete_task(task_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        return {"message": "Tarea eliminada"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))