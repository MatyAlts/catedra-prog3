"""mismo cambio, corregido a mano.

A Alembic NO se le ocurre el renombre: comparó el esquema real con el modelo
y vio "nombre desaparece" + "nombre_completo aparece". El drop_column borra
la columna Y sus datos; la corrección usa alter_column que conserva los datos.

Revision ID: 688ea36dce96
Revises: <la migración inicial>
"""
from alembic import op


def upgrade() -> None:
    # La corrección: un renombre REAL conserva los datos.
    op.alter_column("producto", "nombre",
                    new_column_name="nombre_completo",
                    existing_type=None)


def downgrade() -> None:
    op.alter_column("producto", "nombre_completo",
                    new_column_name="nombre",
                    existing_type=None)
