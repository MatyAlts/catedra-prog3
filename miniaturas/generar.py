# -*- coding: utf-8 -*-
"""
Generador de miniaturas de YouTube para el módulo de despliegue.

Uso:
    python generar.py

Genera un PNG de 1280x720 por cada entrada de VIDEOS, en esta misma carpeta.
Para agregar una clase nueva o cambiar la cantidad de partes, se toca solo la
tabla VIDEOS de abajo y se vuelve a correr. El diseño no se toca.
"""

import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
TEMP = os.path.join(AQUI, '_html')

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

# ---------------------------------------------------------------------------
# Paleta: un acento por clase. El fondo es siempre el mismo.
# ---------------------------------------------------------------------------
CLASES = {
    1: {'tema': 'DNS',    'acento': '#2E9BFF', 'titulo': 'Del navegador al servidor'},
    2: {'tema': 'VPS',    'acento': '#FF5A47', 'titulo': 'Aprovisionar, entrar y cerrar'},
    3: {'tema': 'DOCKER', 'acento': '#25C2A0', 'titulo': 'La receta reproducible'},
    4: {'tema': 'DEPLOY', 'acento': '#FFB020', 'titulo': 'La aplicación en internet'},
    5: {'tema': 'DEVOPS', 'acento': '#A970FF', 'titulo': 'Red interna y automatización'},
}

# (clase, parte, bajada que va debajo del tema)
VIDEOS = [
    (1, 1, 'Cómo funciona la resolución de nombres'),
    (1, 2, 'Registros, delegación y caché'),
    (1, 3, 'Filtrado y dominio propio'),

    (2, 1, 'Virtualización y acceso por SSH'),
    (2, 2, 'Puertos, sockets y qué escucha el server'),
    (2, 3, 'Firewall y superficie de ataque'),

    (3, 1, 'Imágenes, capas y contenedores'),
    (3, 2, 'Escribir el Dockerfile'),
    (3, 3, 'Buenas prácticas y multi-stage'),

    (4, 1, 'Proxy inverso y Traefik'),
    (4, 2, 'HTTPS y certificados automáticos'),
    (4, 3, 'CORS en producción'),

    (5, 1, 'Red interna entre contenedores'),
    (5, 2, 'Base de datos y persistencia'),
    (5, 3, 'Integración continua'),
]


def tamano_tema(palabra):
    """El tema tiene que ocupar el ancho disponible sin desbordar."""
    return {3: 250, 4: 230, 5: 200, 6: 172}.get(len(palabra), 150)


PLANTILLA = """<!DOCTYPE html>
<html lang="es-AR"><head><meta charset="utf-8"><style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: 1280px; height: 720px; overflow: hidden; }}
  body {{
    font-family: "Segoe UI", "Arial", sans-serif;
    background: #0B131D;
    position: relative;
  }}

  /* resplandor del acento, arriba a la derecha */
  .glow {{
    position: absolute; top: -320px; right: -260px;
    width: 900px; height: 900px; border-radius: 50%;
    background: radial-gradient(circle, {acento}55 0%, {acento}00 62%);
  }}
  /* banda diagonal sutil, da profundidad sin ensuciar */
  .banda {{
    position: absolute; top: 0; right: 0; width: 560px; height: 720px;
    background: linear-gradient(200deg, {acento}18 0%, transparent 55%);
    clip-path: polygon(38% 0, 100% 0, 100% 100%, 0 100%);
  }}

  /* número gigante de fondo */
  .fantasma {{
    position: absolute; right: 34px; top: 50%; transform: translateY(-52%);
    font-family: "Segoe UI Black", "Arial Black", sans-serif;
    font-size: 560px; font-weight: 900; line-height: .78;
    color: {acento}; opacity: .16; letter-spacing: -22px;
  }}

  .marco {{ position: absolute; inset: 0; padding: 62px 68px; display: flex;
            flex-direction: column; justify-content: space-between; }}

  .arriba {{ display: flex; align-items: center; gap: 18px; }}
  .chip {{
    background: {acento}; color: #0B131D;
    font-size: 27px; font-weight: 800; letter-spacing: 3.5px;
    padding: 11px 22px 10px; border-radius: 7px;
  }}
  .chip-parte {{
    background: transparent; color: {acento};
    border: 3px solid {acento};
  }}

  .centro {{ margin-top: -14px; }}
  .tema {{
    font-family: "Segoe UI Black", "Arial Black", sans-serif;
    font-size: {tam}px; font-weight: 900; line-height: .88;
    color: #FFFFFF; letter-spacing: -5px;
    text-shadow: 0 6px 34px rgba(0,0,0,.55);
  }}
  .barra {{ width: 132px; height: 9px; background: {acento};
            border-radius: 5px; margin: 26px 0 22px; }}
  .bajada {{
    font-size: 42px; font-weight: 600; color: #C4D3E2;
    line-height: 1.18; max-width: 800px;
    text-shadow: 0 3px 18px rgba(0,0,0,.6);
  }}

  .pie {{ display: flex; align-items: center; gap: 16px;
          font-size: 25px; font-weight: 700; letter-spacing: 4.5px;
          color: #6F8296; }}
  .pie .punto {{ color: {acento}; }}
</style></head><body>
  <div class="glow"></div>
  <div class="banda"></div>
  <div class="fantasma">{parte}</div>
  <div class="marco">
    <div class="arriba">
      <div class="chip">CLASE {clase}</div>
      <div class="chip chip-parte">PARTE {parte}</div>
    </div>
    <div class="centro">
      <div class="tema">{tema}</div>
      <div class="barra"></div>
      <div class="bajada">{bajada}</div>
    </div>
    <div class="pie">
      PROGRAMACIÓN 3 <span class="punto">•</span> DESPLIEGUE <span class="punto">•</span> DEVOPS
    </div>
  </div>
</body></html>"""


def main():
    os.makedirs(TEMP, exist_ok=True)
    if not os.path.exists(CHROME):
        sys.exit(f'No encuentro Chrome en {CHROME}')

    generados = []
    for clase, parte, bajada in VIDEOS:
        c = CLASES[clase]
        html = PLANTILLA.format(
            acento=c['acento'], clase=clase, parte=parte,
            tema=c['tema'], tam=tamano_tema(c['tema']), bajada=bajada)

        base = f'clase-{clase}-parte-{parte}-{c["tema"].lower()}'
        ruta_html = os.path.join(TEMP, base + '.html')
        with open(ruta_html, 'w', encoding='utf-8') as f:
            f.write(html)

        subprocess.run([
            CHROME, '--headless', '--disable-gpu', '--hide-scrollbars',
            '--force-device-scale-factor=1',
            '--screenshot=' + os.path.join(AQUI, base + '.png'),
            '--window-size=1280,720',
            'file:///' + ruta_html.replace('\\', '/'),
        ], capture_output=True)
        generados.append(base + '.png')
        print('  ✓', base + '.png')

    print(f'\n{len(generados)} miniaturas en {AQUI}')


if __name__ == '__main__':
    main()
