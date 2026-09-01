"""
Capítulo 1 · Figura 1.6 — La estructura de un módulo.

Qué muestra la captura: los CINCO archivos de un módulo del TPI
(router.py, service.py, repository.py, model.py, tasks.py) y qué capa es cada
uno. La figura puede ser el árbol real del proyecto o un diagrama; acá se
genera el esqueleto mínimo de los cinco archivos para capturar el árbol.

Cada archivo se crea dentro de la carpeta `modulo_productos/`, y después se
lista el árbol con capas anotadas — eso es lo que se captura.

Uso (en esta carpeta capitulo-01):
    python 1_6_estructura_modulo.py
"""
from __future__ import annotations

import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

BASE = os.path.join(os.path.dirname(__file__), "modulo_productos")

ARCHIVOS = {
    "router.py": '''\
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
''',
    "service.py": '''\
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
''',
    "repository.py": '''\
"""Capa Repository. Acceso a datos, todo con await."""
from core.repositories import BaseRepository
from .model import Producto

class ProductoRepository(BaseRepository[Producto]):
    pass  # hereda get_by_id, list, count, create, ...
''',
    "model.py": '''\
"""Capa Model. La tabla y sus relaciones."""
from decimal import Decimal
from sqlmodel import Field, SQLModel

class Producto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=80)
    precio: Decimal = Field(max_digits=10, decimal_places=2)
    categoria_id: int | None = Field(foreign_key="categoria.id")
''',
    "tasks.py": '''\
"""Tareas diferidas del módulo (segundo cliente de Service, NO una capa nueva)."""
import taskiq
from core.uow import UnitOfWork
from .service import ProductoService

@taskiq.task
async def recalcular_ventas(producto_id: int) -> None:
    # TB-04: sesión y UoW propios, y llama al MISMO ProductoService.
    async with UnitOfWork() as uow:
        ProductoService.actualizar_ventas(uow, producto_id)
''',
}


def main():
    print("=" * 70)
    print("Figura 1.6 · La estructura de un módulo (5 capas)")
    print("=" * 70)

    for nombre, contenido in ARCHIVOS.items():
        ruta = os.path.join(BASE, nombre)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)

    print("\nArchivos generados en: modulo_productos/\n")
    print("  modulo_productos/")
    capa = {
        "router.py": "Router    - HTTP puro",
        "service.py": "Service   - lógica de negocio (sin estado)",
        "repository.py": "Repository - acceso a datos (con await)",
        "model.py": "Model     - la tabla y sus relaciones",
        "tasks.py": "Task      - segundo cliente de Service",
    }
    for nombre in ["router.py", "service.py", "repository.py", "model.py", "tasks.py"]:
        print(f"    ├── {nombre:<14} {capa[nombre]}")

    print("\nEn el TPI real estos archivos viven dentro de su dominio; el árbol")
    print("que se captura es el del proyecto. Esta plantilla vale como ejemplo")
    print("para la figura 1.6.")


if __name__ == "__main__":
    main()
