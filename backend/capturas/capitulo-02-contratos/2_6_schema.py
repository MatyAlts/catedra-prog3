"""
Capítulo 2 · Figura 2.6 — El schema en la especificación.

Qué muestra la captura: "el fragmento de la especificación correspondiente a
un modelo, mostrando cómo cada restricción declarada aparece traducida. Es la
evidencia de que el contrato se deriva del código." (Cap. 2, §2.12).

El capítulo indica usar `model_json_schema()`, que devuelve "el esquema del
modelo, que es literalmente lo que aparece en la especificación".

Este script imprime:
  1. El fragmento del /openapi.json correspondiente a ProductoCreate (vía
     httpx contra la app levantada), o si no está levantada, el mismo JSON
     con model_json_schema().

Uso:
    (opción A) con la app levantada (python -m uvicorn app:app --reload):
        python 2_6_schema.py
        -> imprime la parte del openapi.json de ProductoCreate.

    (opción B) sin levantar nada, lo mismo desde pydantic:
        python 2_6_schema.py --local
"""
from __future__ import annotations

import json
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

from app import ProductoCreate  # noqa: E402


def imprimir(nombre, esquema) -> None:
    print("=" * 70)
    print(f"Figura 2.6 · El schema en la especificación: {nombre}")
    print("=" * 70)
    print(json.dumps(esquema, indent=2, ensure_ascii=False))
    print("\nCómo leerlo (Cap. 2, §2.12): cada restricción declarada en el")
    print("código (min_length=1, ge=0) aparece traducida acá. El contrato se")
    print("deriva del código y no se desactualiza.")


def main() -> None:
    # El fragmento exacto del /openapi.json del modelo.
    if "--local" in sys.argv:
        imprimir("ProductoCreate (model_json_schema)", ProductoCreate.model_json_schema())
        return

    try:
        import httpx

        spec = httpx.get("http://127.0.0.1:8000/openapi.json").json()
        esquema = spec["components"]["schemas"]["ProductoCreate"]
        imprimir("ProductoCreate (desde /openapi.json)", esquema)
    except Exception as e:  # noqa: BLE001
        print("No pude leer /openapi.json (¿está la app levantada?).", e)
        print("Uso la misma generación local para que igualmente veas el schema:\n")
        imprimir("ProductoCreate (model_json_schema)", ProductoCreate.model_json_schema())


if __name__ == "__main__":
    main()
