"""
Capítulo 7 · Figura 7.6 — Un interbloqueo en los registros del motor PostgreSQL.

Qué muestra la captura (Cap. 7, §7.11): "Los registros del motor informan los
interbloqueos con detalle: qué dos transacciones, qué recursos, y cuál fue
elegida como víctima."

Fabrica a propósito un interbloqueo siguiendo el experimento del capítulo:
    1) A bloquea el producto 3; B bloquea el producto 7.
    2) A pide el 7; B pide el 3.  -> una de las dos es elegida víctima.

Con `log_lock_waits = on` (ver sql/7_6_bloqueos.sql) el detalle completo queda
en el registro de PostgreSQL: esa es la captura 7.6.

Necesita: PostgreSQL 16+ corriendo y psycopg. Configurá las credenciales con
variables de entorno (PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE) o con la
constante DSN.

Uso:
    python 7_6_interbloqueo.py
"""
from __future__ import annotations

import os
import sys
import threading
import time

import psycopg

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

DSN = os.getenv(
    "CAPTURAS_PG_DSN",
    "host=localhost port=5432 dbname=db user=postgres password=1941",
)


def setup(conn: psycopg.Connection):
    """Crea la tabla del experimento y devuelve dos ids a disputar."""
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS captura_producto (
                id     integer PRIMARY KEY,
                nombre text NOT NULL,
                stock  integer NOT NULL DEFAULT 1
            )
            """
        )
        cur.execute(
            "INSERT INTO captura_producto (id, nombre) VALUES (3, 'a'), (7, 'b')"
            " ON CONFLICT (id) DO NOTHING"
        )
    conn.commit()
    return 3, 7


def worker_a(ids):
    a, b = ids
    conn = psycopg.connect(DSN)
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM captura_producto WHERE id = %s FOR UPDATE", (a,))
                print("[A] bloqueó producto", a, flush=True)
                time.sleep(1.0)
                print("[A] pide producto", b, "-> debe interbloquear con B", flush=True)
                cur.execute("SELECT id FROM captura_producto WHERE id = %s FOR UPDATE", (b,))
                print("[A] siguió (no debería llegar acá)", flush=True)
    except psycopg.errors.DeadlockDetected as e:
        print("\n[A] INTERBLOQUEO DETECTADO en A:", e.diag.message_primary, flush=True)
    except Exception as e:  # noqa: BLE001
        print("\n[A] error:", type(e).__name__, e, flush=True)
    finally:
        conn.close()


def worker_b(ids):
    a, b = ids
    conn = psycopg.connect(DSN)
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM captura_producto WHERE id = %s FOR UPDATE", (b,))
                print("[B] bloqueó producto", b, flush=True)
                time.sleep(1.0)
                print("[B] pide producto", a, "-> debe interbloquear con A", flush=True)
                cur.execute("SELECT id FROM captura_producto WHERE id = %s FOR UPDATE", (a,))
                print("[B] siguió (no debería llegar acá)", flush=True)
    except psycopg.errors.DeadlockDetected as e:
        print("\n[B] INTERBLOQUEO DETECTADO en B:", e.diag.message_primary, flush=True)
    except Exception as e:  # noqa: BLE001
        print("\n[B] error:", type(e).__name__, e, flush=True)
    finally:
        conn.close()


def main():
    conn = psycopg.connect(DSN)
    ids = setup(conn)
    conn.close()

    print("Vector de interbloqueo: A bloquea 3 y pide 7; B bloquea 7 y pide 3.\n")
    print("Mientras corre, ejecutá en otro terminal la vista de bloqueos:\n")
    print("    sql/7_6_bloqueos.sql  (la consulta (a))\n")

    t1 = threading.Thread(target=worker_a, args=(ids,))
    t2 = threading.Thread(target=worker_b, args=(ids,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print("\nFin. El detalle (víctima, recursos, transacciones) quedó en el log")
    print("de PostgreSQL si habilitaste log_lock_waits (sql/7_6_bloqueos.sql).")


if __name__ == "__main__":
    main()
