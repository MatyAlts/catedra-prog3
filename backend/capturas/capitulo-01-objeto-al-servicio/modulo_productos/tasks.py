"""Tareas diferidas del módulo (segundo cliente de Service, NO una capa nueva)."""
import taskiq
from core.uow import UnitOfWork
from .service import ProductoService

@taskiq.task
async def recalcular_ventas(producto_id: int) -> None:
    # TB-04: sesión y UoW propios, y llama al MISMO ProductoService.
    async with UnitOfWork() as uow:
        ProductoService.actualizar_ventas(uow, producto_id)
