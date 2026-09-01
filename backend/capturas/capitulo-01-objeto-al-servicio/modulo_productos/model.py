"""Capa Model. La tabla y sus relaciones."""
from decimal import Decimal
from sqlmodel import Field, SQLModel

class Producto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=80)
    precio: Decimal = Field(max_digits=10, decimal_places=2)
    categoria_id: int | None = Field(foreign_key="categoria.id")
