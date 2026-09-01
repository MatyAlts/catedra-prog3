"""
Capítulo 2 · Mini-app para las figuras 2.5 y 2.6.

  2.5 · Un 422 en la documentación interactiva: enviar un ProductoCreate
        inválido y mostrar el detalle desplegado (loc, type, msg, input),
        idealmente con DOS errores a la vez (nombre vacío + precio negativo)
        para que se vea que es una LISTA.
  2.6 · El schema en la especificación: el fragmento de OpenAPI/JSON Schema
        de ProductoCreate que aparece en /docs (la evidencia de que el
        contrato se deriva del código).

Uso (en esta carpeta capitulo-02):
    python -m uvicorn app:app --reload

Luego:
    2.5: abrí http://127.0.0.1:8000/docs → POST /productos → Try it out →
         body: {"nombre": "", "precio": -1} → Execute → 422 desplegado con
         DOS errores en la lista.
    2.6: en la misma página, el modelo ProductoCreate aparece con sus
         restricciones (min_length=1, ge=0) traducidas; o pedí el JSON en
         bruto con:  curl http://127.0.0.1:8000/openapi.json
         El script 2_6_schema.py imprime ese fragmento para capturar.
"""

from __future__ import annotations

import os
import sys
from decimal import Decimal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlmodel import Field as SQLField
from sqlmodel import SQLModel, Session, create_engine

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

DATABASE_URL = os.getenv("CAPTURAS_DB", "sqlite:///./capturas2.db")
engine = create_engine(DATABASE_URL)


class Producto(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    nombre: str
    precio: Decimal = SQLField(default=Decimal("0.00"),
                               max_digits=10, decimal_places=2)


class ProductoCreate(BaseModel):
    """El schema de entrada (Figura 2.6: lo que aparece en la especificación)."""
    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: str = Field(min_length=1, max_length=80,
                        description="No puede quedar vacío")
    precio: Decimal = Field(ge=Decimal("0"),
                            description="No puede ser negativo")


class ProductoPublic(BaseModel):
    id: int
    nombre: str
    precio: str


app = FastAPI(title="Captura 2.5 · Un 422 con dos errores")


@app.on_event("startup")
def arrancar():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as s:
        yield s


@app.post("/productos", response_model=ProductoPublic, status_code=201)
def crear_producto(datos: ProductoCreate):
    # Con nombre vacío y precio negativo, Pydantic eleva el 422 ANTES de
    # entrar acá, y reporta los DOS errores a la vez (Figura 2.2/diagnóstico).
    if datos.nombre.strip() == "":
        raise HTTPException(status_code=422, detail="nombre vacío")
    return ProductoPublic(id=1, nombre=datos.nombre, precio=f"{datos.precio:.2f}")
