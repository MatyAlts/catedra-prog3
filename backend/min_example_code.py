# captura.py — mínimo para las Figuras 2.5 y 2.6
# uv pip install "fastapi[standard]"   ·   fastapi dev captura.py

from datetime import datetime
from decimal import Decimal
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Response
from pydantic import BaseModel, Field

app = FastAPI(
    title="Food Store — contrato de productos",
    version="1.0.0",
    description="Sólo para capturas: los datos viven en memoria.",
)


class ProductoBase(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=120)]
    precio: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]


class ProductoCreate(ProductoBase):
    categoria_id: Annotated[int, Field(gt=0)]
    descripcion: Annotated[str | None, Field(max_length=500)] = None
    disponible: bool = True


class ProductoUpdate(BaseModel):
    nombre: Annotated[str | None, Field(min_length=1, max_length=120)] = None
    precio: Annotated[Decimal | None, Field(gt=0, max_digits=10, decimal_places=2)] = None
    categoria_id: Annotated[int | None, Field(gt=0)] = None


class ProductoPublic(ProductoBase):
    id: int
    categoria_id: int
    creado_en: datetime


class PaginaDeProductos(BaseModel):
    items: list[ProductoPublic]
    total: int
    page: int
    size: int
    pages: int


_almacen: dict[int, ProductoPublic] = {}
_proximo_id = 1


@app.post("/api/v1/productos", response_model=ProductoPublic, status_code=201)
async def crear_producto(datos: ProductoCreate, response: Response):
    global _proximo_id
    producto = ProductoPublic(
        id=_proximo_id,
        creado_en=datetime.now(),
        **datos.model_dump(include={"nombre", "precio", "categoria_id"}),
    )
    _almacen[_proximo_id] = producto
    response.headers["Location"] = f"/api/v1/productos/{_proximo_id}"
    _proximo_id += 1
    return producto


@app.get("/api/v1/productos", response_model=PaginaDeProductos)
async def listar_productos(
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
    sort: Annotated[str | None, Query(pattern=r"^-?(nombre|precio|creado_en)$")] = None,
    categoria_id: Annotated[int | None, Query(gt=0)] = None,
    q: Annotated[str | None, Query(min_length=2, max_length=80)] = None,
):
    items = list(_almacen.values())
    total = len(items)
    pages = max(1, -(-total // size))
    if page > pages:
        raise HTTPException(status_code=422, detail="Página más allá del máximo")
    inicio = (page - 1) * size
    return PaginaDeProductos(
        items=items[inicio : inicio + size], total=total, page=page, size=size, pages=pages
    )


@app.get("/api/v1/productos/{producto_id}", response_model=ProductoPublic)
async def obtener_producto(producto_id: Annotated[int, Field(gt=0)]):
    producto = _almacen.get(producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@app.patch("/api/v1/productos/{producto_id}", response_model=ProductoPublic)
async def modificar_producto(producto_id: int, datos: ProductoUpdate):
    producto = _almacen.get(producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    cambios = datos.model_dump(exclude_unset=True)
    actualizado = producto.model_copy(update=cambios)
    _almacen[producto_id] = actualizado
    return actualizado


@app.delete("/api/v1/productos/{producto_id}", status_code=204)
async def borrar_producto(producto_id: int):
    if _almacen.pop(producto_id, None) is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")