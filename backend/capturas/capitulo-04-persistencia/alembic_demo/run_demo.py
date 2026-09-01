"""
Capítulo 4 · Figura 4.6 — Proyecto Alembic REAL: el renombre mal detectado.

Monto un mini-proyecto Alembic que se ejecuta de verdad y reproduce en vivo
lo que el capítulo explica (§4.11): cuando renombrás una columna, Alembic con
`--autogenerate` NO detecta el renombre. Genera un `drop_column` + `add_column`
que PIERDE los datos; hay que corregirlo a mano por `alter_column`.

PREPARACIÓN (una vez):
    python -m alembic -c alembic.ini revision --autogenerate -m "inicial"
    python -m alembic -c alembic.ini upgrade head

FLUJO DE LA FIGURA (lo reproduce este script):
    1. `models.py` tiene `Producto.nombre`        (estado A, ya migrado)
    2. Insertamos 3 filas en la tabla `producto`.
    3. Renombramos en el MODELO: `nombre` -> `nombre_completo`   (estado B)
    4. `alembic revision --autogenerate`: genera la migración BAD
       -> la copiamos a capturas/4_6_mal_drop_add.py  (PIERDE datos)
    5. Escribimos la versión corregida por `alter_column`
       -> capturas/4_6_bien_alter_column.py          (conserva datos)
    6. Retiramos la mala de versions/ (para no romper la cadena) y
       mostramos el estado final.

Las dos migraciones quedan en `alembic_demo/capturas/`, listas para abrir
en el editor y capturar sin interferir con el ciclo real de Alembic.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "demo.db")
MODELS = os.path.join(HERE, "models.py")
VERSIONS = os.path.join(HERE, "versions")
CAPTURAS = os.path.join(HERE, "capturas")

ESTADO_A = "id = Column(String(36), primary_key=True)\n    nombre = Column(String(80), nullable=False)\n"
ESTADO_B = "id = Column(String(36), primary_key=True)\n    nombre_completo = Column(String(80), nullable=False)\n"


def nb(texto: str) -> str:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    return texto


def run(args: list[str], label: str) -> subprocess.CompletedProcess:
    print(nb(f"\n$ {label}"))
    r = subprocess.run(args, cwd=HERE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    out = (r.stderr or r.stdout or "").strip()
    if out:
        print(out)
    return r


def set_modelo(fragmento: str) -> None:
    with open(MODELS, "r", encoding="utf-8") as f:
        contenido = f.read()
    contenido = re.sub(
        r'id = Column\(String\(36\), primary_key=True\)\n    nombre[^\n]*',
        fragmento.rstrip(),
        contenido,
    )
    with open(MODELS, "w", encoding="utf-8") as f:
        f.write(contenido)


def main() -> None:
    banner = "=" * 70
    print(nb(banner))
    print(nb("Figura 4.6 · Proyecto Alembic REAL — el renombre mal detectado"))
    print(nb(banner))
    print(nb("Las capturas quedan en: alembic_demo/capturas/"))

    if not os.path.exists(DB):
        # Estado A + migración inicial
        print(nb("\n[1] Estado A: modelo con `nombre`. Migración inicial."))
        set_modelo(ESTADO_A)
        run(["python", "-m", "alembic", "-c", "alembic.ini", "revision",
             "--autogenerate", "-m", "inicial"], "alembic revision --autogenerate -m inicial")
        run(["python", "-m", "alembic", "-c", "alembic.ini", "upgrade", "head"],
            "alembic upgrade head")
    else:
        print(nb("\n[1] demo.db ya existe — se reutiliza la migración inicial."))

    # Estado A asegurado en el modelo
    set_modelo(ESTADO_A)

    # Sembrar 3 filas
    print(nb("\n[2] Insertamos 3 productos."))
    seed = '"import sqlite3\\nc=sqlite3.connect(\\"demo.db\\")\\nc.executemany(\\"INSERT INTO producto (id, nombre) VALUES (?, ?)\\" , [(\\"p1\\",\\"Hamburguesa\\"),(\\"p2\\",\\"Empanada\\"),(\\"p3\\",\\"Milanesa\\")])\\nc.commit()\\nprint(\\"OK filas\\", c.total_changes)\\nc.close()\\n"'
    with open("_seed.py", "w", encoding="utf-8") as f:
        f.write("import sqlite3\nc=sqlite3.connect('demo.db')\nc.executemany('INSERT INTO producto (id, nombre) VALUES (?, ?)' , [('p1','Hamburguesa'),('p2','Empanada'),('p3','Milanesa')])\nc.commit()\nprint('Filas insertadas:', c.total_changes)\nc.close()\n")
    r = subprocess.run(["python", "_seed.py"], cwd=HERE, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    print((r.stdout or r.stderr or "").strip())
    os.remove(os.path.join(HERE, "_seed.py"))

    # Estado B: renombrar en el modelo
    print(nb("\n[3] Renombramos en el MODELO: `nombre` -> `nombre_completo`."))
    set_modelo(ESTADO_B)

    # Autogenerate
    print(nb("\n[4] alembic revision --autogenerate  -> genera la migración (drop + add)."))
    r = run(["python", "-m", "alembic", "-c", "alembic.ini", "revision",
             "--autogenerate", "-m", "renombre"], "alembic revision --autogenerate -m renombre")

    generada = None
    for fn in sorted(os.listdir(VERSIONS)):
        if "renombre" in fn.lower():
            generada = os.path.join(VERSIONS, fn)
    if not generada:
        print(nb("!!! no se encontró la migración generada. Revisar alembic."))
        return

    with open(generada, "r", encoding="utf-8") as f:
        contenido = f.read()

    os.makedirs(CAPTURAS, exist_ok=True)
    bad_dest = os.path.join(CAPTURAS, "4_6_mal_drop_add.py")
    good_dest = os.path.join(CAPTURAS, "4_6_bien_alter_column.py")
    shutil.copy(generada, bad_dest)

    rev_id = re.search(r'revision = (["\'])([^"\']+)\1', contenido).group(2)

    print(nb("\n--- migración GENERADA por Alembic (drop + add) ---"))
    print(nb(contenido))
    print(nb("--- fin fragmento generado ---"))

    corregida = f'''\
"""mismo cambio, corregido a mano.

A Alembic NO se le ocurre el renombre: comparó el esquema real con el modelo
y vio "nombre desaparece" + "nombre_completo aparece". El drop_column borra
la columna Y sus datos; la corrección usa alter_column que conserva los datos.

Revision ID: {rev_id}
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
'''
    with open(good_dest, "w", encoding="utf-8") as f:
        f.write(corregida)

    # Retirar la migración mala de versions/ para no romper la cadena
    os.remove(generada)

    print(nb("\n[5] Versión CORREGIDA (alter_column · conserva datos):"))
    print(nb(corregida))
    print(nb("\n[6] Escribimos en capturas/ y retiramos la mala de versions/."))
    print(nb("\nCómo se verifica que el renombre REAL conserva datos (Cap. 4, §4.11):"))
    print(nb("  SELECT nombre_completo FROM producto;  -> 3 filas, no NULLs."))


if __name__ == "__main__":
    main()
