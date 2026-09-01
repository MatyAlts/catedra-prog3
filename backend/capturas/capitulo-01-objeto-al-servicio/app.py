"""
Capítulo 1 · Figura 1.5 — La documentación automática.

Mini-app para tomar la captura de la documentación interactiva con un endpoint
desplegado y ejecutado desde el navegador, y el 422 de validación al lado.

Qué muestra la captura:
  · La interfaz Swagger (http://127.0.0.1:8000/docs).
  · El endpoint GET /productos/{producto_id} desplegado y EJECUTADO.
  · Al mandar `abc` donde va el entero: el 422 con el detalle de validación.

Uso (en ESTA carpeta capitulo-01):
    python -m uvicorn app:app --reload

Luego:
    1. Abrí http://127.0.0.1:8000/docs
    2. Desplegá GET /productos/{producto_id} → Try it out → producto_id = 1 → Execute.
       La respuesta exitosa muestra el ProductoPublic serializado (Decimal como
       cadena, Figura 2.4).
    3. En el mismo endpoint probá producto_id = abc → Execute → verás el 422
       con el detalle: "input is not a valid integer". Eso es la Figura 1.5.

La base es SQLite en el archivo capturas1.db (se crea sola al arrancar).
"""

from __future__ import annotations

import os
import sys
from decimal import Decimal

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import Field as SQLField
from sqlmodel import SQLModel, Session, create_engine

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

DATABASE_URL = os.getenv("CAPTURAS_DB", "sqlite:///./capturas1.db")
engine = create_engine(DATABASE_URL, echo=True)


class Producto(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    nombre: str
    precio: Decimal = SQLField(default=Decimal("0.00"),
                               max_digits=10, decimal_places=2)
    categoria_id: int | None = None


class ProductoPublic(BaseModel):
    id: int
    nombre: str
    precio: str  # viaja como cadena, nunca como float


app = FastAPI(title="Captura 1.5 · Documentación automática")


@app.on_event("startup")
def arrancar():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        if not s.query(Producto).first():
            s.add_all([
                Producto(nombre="Hamburguesa", precio=Decimal("8500.00"),
                         categoria_id=1),
                Producto(nombre="Papas fritas", precio=Decimal("2900.50"),
                         categoria_id=1),
            ])
            s.commit()


def get_session():
    with Session(engine) as s:
        yield s


@app.get("/productos/{producto_id}", response_model=ProductoPublic)
def obtener_producto(producto_id: int, session: Session = Depends(get_session)):
    p = session.get(Producto, producto_id)
    if p is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return ProductoPublic(id=p.id, nombre=p.nombre, precio=f"{p.precio:.2f}")
