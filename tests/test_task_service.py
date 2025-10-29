import pytest
from datetime import datetime
from app.domain.task import Task, TaskStatus
from app.application.services.task_service import TaskService
from app.infrastructure.persistence.memory_task_repository import MemoryTaskRepository

@pytest.fixture
async def service():
    """Fixture para crear un servicio con repositorio en memoria"""
    repo = MemoryTaskRepository()
    return TaskService(repo)

@pytest.mark.asyncio
async def test_create_task(service):
    """Test: Crear una tarea válida"""
    task = await service.create_task("Estudiar SOLID", "pending")
    assert task.id == 1
    assert task.title == "Estudiar SOLID"
    assert task.status == TaskStatus.PENDING

@pytest.mark.asyncio
async def test_create_task_empty_title(service):
    """Test: No permitir título vacío"""
    with pytest.raises(ValueError):
        await service.create_task("", "pending")

@pytest.mark.asyncio
async def test_get_all_tasks(service):
    """Test: Obtener todas las tareas"""
    await service.create_task("Tarea 1", "pending")
    await service.create_task("Tarea 2", "done")
    
    tasks = await service.get_all_tasks()
    assert len(tasks) == 2

@pytest.mark.asyncio
async def test_get_task_by_id(service):
    """Test: Obtener tarea por ID"""
    await service.create_task("Tarea test", "pending")
    task = await service.get_task_by_id(1)
    assert task.title == "Tarea test"

@pytest.mark.asyncio
async def test_update_task(service):
    """Test: Actualizar tarea"""
    await service.create_task("Tarea original", "pending")
    updated = await service.update_task(1, "Tarea actualizada", "done")
    assert updated.title == "Tarea actualizada"
    assert updated.status == TaskStatus.DONE

@pytest.mark.asyncio
async def test_delete_task(service):
    """Test: Eliminar tarea"""
    await service.create_task("Tarea a eliminar", "pending")
    deleted = await service.delete_task(1)
    assert deleted is True
    
    task = await service.get_task_by_id(1)
    assert task is None