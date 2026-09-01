"""
Capítulo 5 · Figura 5.6 — Un token decodificado, con sus tres partes.

Qué muestra la captura: "un token real de desarrollo con sus tres partes
decodificadas, mostrando el contenido legible" (Cap. 5, §5.3). La advertencia
del capítulo: NO usar sitios de terceros con tokens de producción.

El capítulo muestra que un JWT tiene TRES partes separadas por puntos, cada
una codificada, y que la del medio es legible por cualquiera: está *decodificada*
(base64), NO cifrada. En el navegador se decodifica con `atob()`.

Este script imprime las tres partes decodificadas.

Uso:
    python 5_6_token_decodificado.py [TOKEN_OPCIONAL]

Vía navegador (como en §5.3):
    1. Cualquier token de sesión de desarrollo (o rompé el de abajo).
    2. Copiá la parte del medio (entre los dos puntos).
    3. En la consola del navegador: atob("...")  -> lo leés entero.
"""
from __future__ import annotations

import base64
import json
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

# Un token de desarrollo de ejemplo (las mismas 3 partes del capítulo).
TOKEN_EJEMPLO = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJzdWIiOiI0MiIsImV4cCI6MTc2NzIyNTYwMH0"
    ".dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
)


def b64url_decode(parte: str) -> bytes:
    padding = "=" * (-len(parte) % 4)
    return base64.urlsafe_b64decode(parte + padding)


def main() -> None:
    token = sys.argv[1] if len(sys.argv) > 1 else TOKEN_EJEMPLO
    encabezado, contenido, firma = token.split(".")

    print("=" * 70)
    print("Figura 5.6 · Las tres partes de un token")
    print("=" * 70)
    print(f"TOKEN: {token}\n")

    print("PARTE 1 · ENCABEZADO  (codificado)")
    print(f"  crudo : {encabezado}")
    print(f"  leído : {json.loads(b64url_decode(encabezado))}\n")

    print("PARTE 2 · CONTENIDO  (codificado, NO cifrado)")
    print(f"  crudo : {contenido}")
    print(f"  leído : {json.loads(b64url_decode(contenido))}")
    print("  >> Cualquiera con el token lo LEE. Es la advertencia del capítulo.\n")

    print("PARTE 3 · FIRMA")
    print(f"  crudo : {firma}  ({len(b64url_decode(firma))} bytes)")
    print("  >> Garantiza integridad y autenticidad; NO confidencialidad.\n")

    print("Vía navegador (como en §5.3): atob('<parte del medio>') en la consola.")
    print("ADVERTENCIA del capítulo: no uses sitios de terceros con tokens de")
    print("PRODUCCIÓN.")


if __name__ == "__main__":
    main()
