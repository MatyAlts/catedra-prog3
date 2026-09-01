"""
Capítulo 3 · Figura 3.6 — Traza de `MissingGreenlet`.

Qué muestra la captura: "una traza de la excepción y dónde está su causa real".
La clave pedagógica (Cap. 3, §3.8): el mensaje `MissingGreenlet` **no señala la
causa**; la causa está en el acceso a la relación NO precargada, en una línea
común (sin await).

Reproduce el error clásico del ORM async: SQLAlchemy ejecuta el ORM síncrono
dentro de un greenlet y salta al bucle SÓLO cuando la I/O ocurre dentro de un
`await`. Acceder a `usuario.rol` (no precargada) desde código común intenta
emitir una consulta desde fuera del greenlet → MissingGreenlet.

Uso:
    python 3_6_missing_greenlet.py

Necesita: aiosqlite + sqlmodel + sqlalchemy (motor async mínimo). En el TPI la
causa es la misma con psycopg async: el repositorio no declaró selectinload()
para la relación que la respuesta va a leer (EA-05).
"""
import asyncio
import sys
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import Field as SQLField
from sqlmodel import Relationship, SQLModel, select

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

# Motor ASYNC a SQLite en memoria. Cualquier driver async de SQLAlchemy
# (aiosqlite, asyncpg, psycopg async...) reproduce este mismo comportamiento.
engine = create_async_engine("sqlite+aiosqlite:///:memory:")


class Rol(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    nombre: str


class Usuario(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    nombre: str
    rol_id: int | None = SQLField(default=None, foreign_key="rol.id")
    # Relationship declarada pero que NO se precarga: la consulta del
    # "repositorio" trae el Usuario sin selectinload(), así que `usuario.rol`
    # queda sin cargar. Acceder a ella dispara la carga perezosa.
    rol: Optional[Rol] = Relationship()


async def reproducir():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        rol = Rol(nombre="cliente")
        session.add(rol)
        await session.flush()
        session.add(Usuario(nombre="ana", rol_id=rol.id))
        await session.commit()

    async with AsyncSession(engine) as session:
        usuario = await session.scalar(select(Usuario))
        print("Usuario obtenido. La línea de abajo dispara la carga perezosa\n"
              "desde código común (sin await) y debe lanzar MissingGreenlet:\n")
        print("    rol = usuario.rol.nombre  # <-- CAUSA REAL, línea sin await\n")
        # El acceso a la relación NO precargada. SQLAlchemy intenta emitir una
        # consulta, no encuentra greenlet al que volver, y lanza la excepción.
        rol = usuario.rol.nombre
        print(f"Rol: {rol}")


if __name__ == "__main__":
    try:
        asyncio.run(reproducir())
    except Exception as exc:  # noqa: BLE001 - mostramos la traza completa
        print("=" * 70)
        print(f"Excepción lanzada: {type(exc).__name__}: {exc}")
        print("=" * 70)
        import traceback

        print("\n=== TRACEBACK COMPLETO (lo que va en la captura) ===\n")
        traceback.print_exc()
        print("\n" + "=" * 70)
        print("CLAVE PEDAGÓGICA (Figura 3.6):")
        print("  - DONDE SALTA:   `await_only` / MissingGreenlet, generado")
        print("                   por SQLAlchemy al intentar I/O fuera del")
        print("                   greenlet.")
        print("  - CAUSA REAL:    `usuario.rol.nombre`, acceso a una relación")
        print("                   NO precargada, en una línea sin await.")
        print("  - SOLUCIÓN:      precargar con selectinload() en la consulta")
        print("                   del repositorio (EA-05 del TPI).")
