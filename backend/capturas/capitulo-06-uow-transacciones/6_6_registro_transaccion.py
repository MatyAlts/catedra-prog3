"""
Capítulo 6 · Figura 6.6 — El registro de una transacción completa.

Qué muestra la captura (Cap. 6, §6.10): "El registro de sentencias ... sirve
para ver dónde empieza y dónde termina cada transacción. Con el registro
activado se ven las marcas de inicio y de confirmación, y eso responde la
pregunta de si dos escrituras fueron juntas o separadas."

Se consigue con `engine.echo = True`, que imprime cada sentencia SQL. Este
script ejecuta DOS escrituras (Usuario + Rol) en la MISMA transacción y muestra
el `BEGIN` que las envuelve y el `COMMIT` final del log.

En PostgreSQL el log muestra las marcas explícitas que la figura enseña a
buscar: un `BEGIN`, los dos `INSERT` adentro y un único `COMMIT` que los cierra.
Si fueran dos transacciones (dos UOW), verías dos `COMMIT` —esa es la pista.

CONEXIÓN (sin credenciales en el código):
    Antes de correr, seteá la variable de entorno CAPTURAS_PG_DSN con el DSN
    de tu base. Ejemplo (PowerShell):
        $env:CAPTURAS_PG_DSN = "postgresql://postgres:TU_CLAVE@localhost:5432/db"
    y luego:
        python 6_6_registro_transaccion.py
"""
from __future__ import annotations

import os
import sys

from sqlmodel import Field as SQLField
from sqlmodel import Session, SQLModel, create_engine

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

_DSN = os.environ.get("CAPTURAS_PG_DSN")
if not _DSN:
    sys.exit(
        "Falta la variable CAPTURAS_PG_DSN. Seteala primero, por ejemplo:\n"
        '  $env:CAPTURAS_PG_DSN = "postgresql://postgres:TU_CLAVE@localhost:5432/db"\n'
        "y volvé a correr este script."
    )

# echo=True es el que imprime las sentencias -> el registro que se captura.
engine = create_engine(_DSN, echo=True)


class Usuario(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    nombre: str
    rol_id: int | None = SQLField(default=None, foreign_key="rol.id")


class Rol(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    nombre: str


def main():
    SQLModel.metadata.create_all(engine)

    print("\nEjecutando DOS escrituras (Usuario + Rol) en la MISMA transacción...\n")
    print("-" * 70)
    print("A partir de acá, el log del motor (esto es lo que se captura):")
    print("-" * 70)

    with Session(engine) as s:
        # Las DOS escrituras van en la misma transacción: entre el BEGIN y el
        # COMMIT del log van las dos sentencias INSERT juntas.
        rol = Rol(nombre="cliente")
        s.add(rol)
        s.flush()
        s.add(Usuario(nombre="ana", rol_id=rol.id))
        s.commit()  # aquí aparece el COMMIT

    print("-" * 70)
    print("Cómo leerlo: el BEGIN abre la transacción, los 2 INSERT (usuario y")
    print("rol) van adentro, y el COMMIT la cierra. Si fueran UOWs aparte,")
    print("verías 2 COMMITs —esa es la pista que la figura enseña a buscar.")


if __name__ == "__main__":
    main()
