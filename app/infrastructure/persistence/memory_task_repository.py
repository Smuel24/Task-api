from typing import List, Optional
from app.domain.task import Task
from app.application.ports.task_repository import TaskRepository

class MemoryTaskRepository(TaskRepository):
    def __init__(self):
        self.tasks: dict[int, Task] = {}
        self.id_counter = 1
    
    async def create(self, task: Task) -> Task:
        """Crear tarea asignando ID automático"""
        task_id = self.id_counter
        self.id_counter += 1
        
        new_task = Task(
            id=task_id,
            title=task.title,
            status=task.status,
            created_at=task.created_at
        )
        self.tasks[task_id] = new_task
        return new_task
    
    async def get_all(self) -> List[Task]:
        """Retornar todas las tareas"""
        return list(self.tasks.values())
    
    async def get_by_id(self, task_id: int) -> Optional[Task]:
        """Retornar tarea por ID o None"""
        return self.tasks.get(task_id)
    
    async def update(self, task: Task) -> Task:
        """Actualizar tarea existente"""
        if task.id not in self.tasks:
            raise ValueError(f"Tarea con ID {task.id} no existe")
        
        self.tasks[task.id] = task
        return task
    
    async def delete(self, task_id: int) -> bool:
        """Eliminar tarea y retornar True si existía"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False