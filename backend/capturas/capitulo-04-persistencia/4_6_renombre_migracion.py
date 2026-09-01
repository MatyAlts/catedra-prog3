"""
Capítulo 4 · Figura 4.6 — Una migración generada, con el renombre mal detectado.

Qué muestra la captura (Cap. 4, §4.11): el archivo de migración que Alembic
genera cuando renombrás un campo. Alembic NO detecta el renombre: lo ve como
`drop_column('nombre')` + `add_column('nombre_completo')`, lo que PIERDE los
datos. La versión corregida a mano usa `alter_column(..., new_column_name=...)`.

Este script imprime los DOS fragmentos que van en la captura: el generado
(que pierde datos) y el corregido (que conserva datos).

Experimento completo del capítulo con un proyecto Alembic real:
    1. Modelo con campo `nombre` -> alembic revision --autogenerate; upgrade.
    2. Insertá 3 filas.
    3. Renombrá a `nombre_completo` en el modelo.
    4. alembic revision --autogenerate   -> ve drop+add.
    5. Corregí a mano por alter_column; upgrade; verificá que los datos quedan.

Uso:
    python 4_6_renombre_migracion.py
"""
from __future__ import annotations

import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

MALA = '''\
"""generado automáticamente: 'renombrar nombre -> nombre_completo'

Revision ID: abc123
Revises: xyz789
"""
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    # Lo que ALEMBIC genera solo: NO es un renombre, es
    # borrar la columna (y sus datos) y crear otra vacía.
    op.drop_column("producto", "nombre")
    op.add_column("producto", sa.Column("nombre_completo", sa.String(80), nullable=False))

def downgrade() -> None:
    op.drop_column("producto", "nombre_completo")
    op.add_column("producto", sa.Column("nombre", sa.String(80), nullable=False))
'''

CORREGIDA = '''\
"""mismo cambio, corregido a mano

Revision ID: abc123
Revises: xyz789
"""
from alembic import op

def upgrade() -> None:
    # La corrección: un VERDADERO renombre conserva los datos.
    op.alter_column("producto", "nombre",
                    new_column_name="nombre_completo",
                    existing_type=None)

def downgrade() -> None:
    op.alter_column("producto", "nombre_completo",
                    new_column_name="nombre",
                    existing_type=None)
'''


def main():
    print("=" * 70)
    print("Figura 4.6 · Lo que Alembic genera para un renombre (PIERDE datos)")
    print("=" * 70)
    print(MALA)
    print("=" * 70)
    print("La versión corregida a mano (conserva datos) · alter_column")
    print("=" * 70)
    print(CORREGIDA)
    print("=" * 70)
    print("Qué revisar en la captura / por qué (Cap. 4, §4.11):")
    print("  - 'La herramienta no se equivocó: comparó dos esquemas y no")
    print("    puede adivinar tu intención.'")
    print("  - drop_column + add_column  =>  se pierden los datos.")
    print("  - alter_column + new_column_name  =>  renombre real, datos vivos.")


if __name__ == "__main__":
    main()
