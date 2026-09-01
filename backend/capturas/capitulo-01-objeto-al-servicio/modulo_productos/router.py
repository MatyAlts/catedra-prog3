"""Capa Router (HTTP). Traduce la petición y nada más."""
from fastapi import APIRouter, Depends
from core.uow import UnitOfWork
from .service import ProductoService
from .schemas import ProductoPublic

router = APIRouter(prefix="/productos", tags=["productos"])

@router.get("/{producto_id}", response_model=ProductoPublic)
def obtener(  # noqa: E501  <- NO construye el UoW; lo recibe por Depends
    producto_id: int,
    uow: UnitOfWork = Depends(get_uow),   # el Router NO construye
):
    return ProductoService.obtener(uow, producto_id)
