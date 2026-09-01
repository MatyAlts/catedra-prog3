"""Capa Repository. Acceso a datos, todo con await."""
from core.repositories import BaseRepository
from .model import Producto

class ProductoRepository(BaseRepository[Producto]):
    pass  # hereda get_by_id, list, count, create, ...
