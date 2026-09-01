"""
Capítulo 8 · Figura 8.7 — El buzón drenando después de una caída.

Qué muestra la captura (Cap. 8, §8.12): la tabla de eventos de salida con
filas acumuladas SIN publicar (la "caída") y, al lado, la misma tabla después
de reanudar el publicador: "las marcas de publicación apareciendo son el
contenido."

Reproduce las tres partes del experimento del capítulo:
    Parte 1 · confirmás un pedido -> la fila del evento está, SIN marcar.
    Parte 2 · "la caída"          -> más eventos se acumulan sin publicar.
    Parte 3 · "revivís"           -> el publicador drena marcando publicados.

La tabla `eventos_salida` es la del TPI (§8.5): cada fila tiene identificador,
tipo, canal, contenido, creado_en, publicado_en (NULO mientras espera) e
intentos. Al publicar se MARCA la fila; no se borra.

Acá el "publicador" es un bucle en memoria para no necesitar Redis. En el TPI
real es la tarea taskiq `publicar_outbox`: toma el lote con FOR UPDATE SKIP
LOCKED, publica en Redis y marca en la MISMA transacción (Figura 8.2).

Corre en SQLite. La consola imprime la tabla ANTES (acumulada) y DESPUÉS
(drenada).

Uso:
    python 8_7_buzon_drenando.py
"""
from __future__ import annotations

import sqlite3
import sys
from datetime import datetime, timezone

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

DB = "buzon_demo.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS eventos_salida (
    identificador   INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo            TEXT NOT NULL,
    canal           TEXT NOT NULL,
    contenido       TEXT NOT NULL,
    creado_en       TEXT NOT NULL,
    publicado_en    TEXT,             -- NULO mientras espera
    intentos        INTEGER NOT NULL DEFAULT 0
);
"""

SELECT_TODOS = """
SELECT identificador, tipo, canal, contenido,
       creado_en, publicado_en, intentos
FROM   eventos_salida
ORDER  BY identificador;
"""


def tabular(rows, titulo):
    print("\n" + "=" * 72)
    print(titulo)
    print("=" * 72)
    print(f"{'id':<3} {'tipo':<18} {'canal':<14} {'pub':<22} intentos")
    print("-" * 72)
    for r in rows:
        pub = r[5] if r[5] else "NULL (sin publicar)"
        print(f"{r[0]:<3} {r[1]:<18} {r[2]:<14} {pub:<22} {r[6]}")
    print()


def ahora():
    return datetime.now(timezone.utc).strftime("%H:%M:%S")


def main():
    conn = sqlite3.connect(DB)
    conn.execute(SCHEMA)
    conn.execute("DELETE FROM eventos_salida")  # limpia entre corridas
    conn.commit()

    print("\n- PARTE 1 · confirmás un pedido (el publicador aún no corrió) -\n")
    conn.execute(
        "INSERT INTO eventos_salida (tipo, canal, contenido, creado_en)"
        " VALUES ('pedido.confirmado', 'pedidos', 'pedido:42', ?)",
        (ahora(),),
    )
    conn.commit()
    tabular(conn.execute(SELECT_TODOS).fetchall(),
            "Buzón tras confirmar pedido 42: la fila existe, SIN marcar.")

    print("- PARTE 2 · 'la caída', confirmás 2 pedidos más (siguen sin publicar) -\n")
    for pedido in (43, 44):
        conn.execute(
            "INSERT INTO eventos_salida (tipo, canal, contenido, creado_en)"
            " VALUES ('pedido.confirmado', 'pedidos', ?, ?)",
            (f"pedido:{pedido}", ahora()),
        )
    conn.commit()
    tabular(conn.execute(SELECT_TODOS).fetchall(),
            "Buzón acumulado: 3 filas sin publicar (profundidad = 3).")

    print("- PARTE 3 · 'revivís'; el publicador drena marcando publicados -\n")
    # En el TPI real: publicar_outbox toma el lote con FOR UPDATE SKIP LOCKED,
    # publica en Redis y marca en la MISMA transacción (Figura 8.2).
    pendientes = conn.execute(
        "SELECT identificador FROM eventos_salida WHERE publicado_en IS NULL"
    ).fetchall()
    for (eid,) in pendientes:
        conn.execute(
            "UPDATE eventos_salida SET publicado_en = ?, intentos = intentos + 1"
            " WHERE identificador = ?",
            (ahora(), eid),
        )
        print(f"   + publicado evento {eid}")
    conn.commit()

    tabular(conn.execute(SELECT_TODOS).fetchall(),
            "Buzón drenado: TODO marcado como publicado (nada se borró).")

    print("Diagnóstico del TPI que esto ilustra (§8.12):")
    print("  - profundidad   = filas sin publicar  (acá 3, luego 0).")
    print("  - antigüedad    = el más viejo sin publicar.")
    print("  - intentos      = 0: atrasado; cerca del máximo: fallando.")

    conn.close()


if __name__ == "__main__":
    main()
