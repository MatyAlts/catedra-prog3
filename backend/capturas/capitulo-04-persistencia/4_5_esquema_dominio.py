"""
Capítulo 4 · Figura 4.5 — El esquema de un dominio visto desde un cliente BD.

Qué muestra la captura: "el esquema de un dominio visto desde un cliente",
las tablas del dominio de VENTAS / TRAZABILIDAD con sus claves foráneas,
índices y restricciones (Cap. 4, §4.12). La figura pide ese dominio porque es
el que tiene las redundancias (Figura 4.4).

Este script crea las tablas del dominio (para que corra sin Postgres) y las
lista con sus FKs del lado "muchos". Para la captura REAL contra PostgreSQL,
ejecutá sql/4_5_esquema_dominio.sql desde tu cliente.

Uso:
    python 4_5_esquema_dominio.py
"""
from __future__ import annotations

import sys
from decimal import Decimal

from sqlmodel import Field as SQLField
from sqlmodel import SQLModel, create_engine

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass


class Categoria(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    nombre: str


class Pedido(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    estado: str
    total: Decimal = SQLField(default=Decimal("0.00"),
                              max_digits=10, decimal_places=2)


class DireccionEntrega(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    calle: str
    ciudad: str


class DetallePedido(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    pedido_id: int = SQLField(foreign_key="pedido.id")       # lado "muchos"
    categoria_id: int | None = SQLField(default=None,
                                        foreign_key="categoria.id")
    subtotal: Decimal = SQLField(default=Decimal("0.00"),
                                 max_digits=10, decimal_places=2)


class Pago(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    pedido_id: int = SQLField(foreign_key="pedido.id")       # lado "muchos"
    monto: Decimal = SQLField(default=Decimal("0.00"),
                              max_digits=10, decimal_places=2)


class HistorialEstadoPedido(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    pedido_id: int = SQLField(foreign_key="pedido.id")       # lado "muchos"
    estado: str


def main():
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    print("=" * 70)
    print("Figura 4.5 · Tablas del dominio de ventas / trazabilidad")
    print("=" * 70)

    print("\nTABLAS DEL DOMINIO:")
    print("  - categoria                 (catálogo)")
    print("  - pedido                    (el encabezado)")
    print("  - detalle_pedido            (las líneas)          <- lado 'muchos'")
    print("  - pago                      (el cobro)            <- lado 'muchos'")
    print("  - historial_estado_pedido   (trazabilidad)        <- lado 'muchos'")
    print("  - direccion_entrega         (snapshot de envío)")

    print("\nCLAVES FORÁNEAS (la FK va del lado 'muchos' — Figura 4.1):")
    fks = [
        ("detalle_pedido.pedido_id", "pedido.id",
         "composición: se borra en cascada"),
        ("detalle_pedido.categoria_id", "categoria.id",
         "asociación: restringe/anula"),
        ("pago.pedido_id", "pedido.id", "composición"),
        ("historial_estado_pedido.pedido_id", "pedido.id", "composición"),
    ]
    for col, ref, rel in fks:
        print(f"  - {col:<36} -> {ref:<16} {rel}")

    print("\nLas REDUNDANCIAS que la Figura 4.4 anota en este dominio:")
    print("  - detalle_pedido guarda nombre/precio/subtotal snapshot (RN-04)")
    print("  - direccion_entrega guarda 6 columnas dir_snapshot_* (CHECK)")
    print("  - pedido.total = subtotal - desc + envío (CHECK)")
    print("  - pago.monto duplica pedido.total (solo prueba cruza tablas)")
    print("  - producto.url_img duplica la portada (índice único)")

    print("\nLa captura se toma con el CLIENTE (pgAdmin/DBeaver/psql) sobre la")
    print("base del TPI; ver sql/4_5_esquema_dominio.sql. Acá se ve la misma")
    print("estructura para confirmar tablas y FK.")


if __name__ == "__main__":
    main()
