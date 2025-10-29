from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.task import Task

class TaskRepository(ABC):
    @abstractmethod
    async def create(self, task: Task) -> Task:
        """Crear una nueva tarea"""
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Task]:
        """Obtener todas las tareas"""
        pass
    
    @abstractmethod
    async def get_by_id(self, task_id: int) -> Optional[Task]:
        """Obtener tarea por ID"""
        pass
    
    @abstractmethod
    async def update(self, task: Task) -> Task:
        """Actualizar una tarea"""
        pass
    
    @abstractmethod
    async def delete(self, task_id: int) -> bool:
        """Eliminar una tarea"""
        pass