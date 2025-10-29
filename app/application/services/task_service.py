from typing import List, Optional
from datetime import datetime
from app.domain.task import Task, TaskStatus
from app.application.ports.task_repository import TaskRepository

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository
    
    async def create_task(self, title: str, status: str = "pending") -> Task:
        """Crear nueva tarea con validaciones"""
        if not title or len(title.strip()) == 0:
            raise ValueError("El título no puede estar vacío")
        
        if status not in ["pending", "done"]:
            raise ValueError("El estado debe ser 'pending' o 'done'")
        
        task = Task(
            id=0,
            title=title,
            status=TaskStatus(status),
            created_at=datetime.now()
        )
        return await self.repository.create(task)
    
    async def get_all_tasks(self) -> List[Task]:
        """Obtener todas las tareas"""
        return await self.repository.get_all()
    
    async def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Obtener tarea por ID"""
        if task_id <= 0:
            raise ValueError("El ID debe ser mayor a 0")
        return await self.repository.get_by_id(task_id)
    
    async def update_task(self, task_id: int, title: str, status: str) -> Task:
        """Actualizar tarea"""
        if not title or len(title.strip()) == 0:
            raise ValueError("El título no puede estar vacío")
        
        if status not in ["pending", "done"]:
            raise ValueError("El estado debe ser 'pending' o 'done'")
        
        existing_task = await self.repository.get_by_id(task_id)
        if not existing_task:
            raise ValueError(f"Tarea con ID {task_id} no encontrada")
        
        updated_task = Task(
            id=task_id,
            title=title,
            status=TaskStatus(status),
            created_at=existing_task.created_at
        )
        return await self.repository.update(updated_task)
    
    async def delete_task(self, task_id: int) -> bool:
        """Eliminar tarea"""
        if task_id <= 0:
            raise ValueError("El ID debe ser mayor a 0")
        return await self.repository.delete(task_id)