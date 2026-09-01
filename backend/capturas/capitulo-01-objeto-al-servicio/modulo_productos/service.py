"""Capa Service. La lógica de negocio, sin estado; recibe UoW por parámetro."""
from core.uow import UnitOfWork
from .repository import ProductoRepository
from .schemas import ProductoPublic

class ProductoService:
    @staticmethod
    def obtener(uow: UnitOfWork, producto_id: int) -> ProductoPublic:
        repo = uow.productos  # composición: el UoW trae los repositorios
        producto = repo.get_by_id(producto_id)
        return ProductoPublic.from_model(producto)
