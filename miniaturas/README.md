# Miniaturas de YouTube — módulo de despliegue

15 miniaturas de **1280×720** (el tamaño que pide YouTube), una por video, generadas
desde un único script. **No se editan a mano.**

## Cómo regenerar

```
python generar.py
```

Reescribe los 15 PNG en esta carpeta. Los `.html` intermedios quedan en `_html/` y no
hacen falta para nada: se pueden borrar.

## Cómo agregar o cambiar videos

Todo está en dos tablas al principio de `generar.py`:

```python
CLASES = {
    1: {'tema': 'DNS', 'acento': '#2E9BFF', ...},
    ...
}

VIDEOS = [
    (1, 3, 'Filtrado y dominio propio'),   # clase, parte, bajada
    ...
]
```

Si la Clase 3 termina teniendo cuatro partes en vez de tres, agregás una línea a `VIDEOS`
y volvés a correr el script. Si querés cambiarle la bajada a un video, la cambiás ahí.
**El diseño no se toca nunca**, y por eso las quince siguen siendo la misma familia.

> **⚠️ OJO ACÁ**
> No edites los PNG en Photoshop ni en Canva. La próxima vez que corras el script se
> pisan. Si algo hay que cambiar visualmente, se cambia en la plantilla de `generar.py`
> y se regeneran las quince juntas — que es justamente lo que hace que sean un sistema y
> no quince imágenes sueltas.

## El sistema visual

| Elemento | Función |
|---|---|
| Fondo `#0B131D` fijo | Lo constante. Es lo que hace que se reconozcan como serie |
| **Un acento por clase** | Azul DNS · rojo VPS · verde Docker · ámbar Deploy · violeta DevOps |
| Palabra del tema, gigante | Lo único legible a 210 px de ancho. Por eso es una sola palabra |
| Número fantasma al 16 % | Se lee la parte de un vistazo sin leer el chip |
| Chips `CLASE n` / `PARTE n` | La información exacta, para cuando la miniatura se ve grande |
| Bajada | Diferencia una parte de otra cuando las tres están juntas en el feed |

El tamaño de la palabra del tema **se calcula según cuántas letras tiene**
(`tamano_tema()`), para que `DNS` y `DOCKER` ocupen el mismo ancho óptico. Si agregás un
tema de 7 letras o más, revisá esa función antes de dar por buena la salida.

## Archivos auxiliares

- `_hoja-de-contactos.png` — las quince juntas, para revisar la coherencia de la serie
- `_prueba-tamano-real.png` — cinco miniaturas a 210×118, que es como se ven en el feed
  de YouTube en celular. **Esta es la prueba que vale**: si algo no se lee acá, no se lee.

## Títulos de los videos

El nombre del archivo sigue el patrón `clase-N-parte-M-tema.png`. El título sugerido para
YouTube, en cambio, conviene que arranque por el tema, porque es lo que se busca:

```
DNS — Parte 3: filtrado y dominio propio | Programación 3
VPS — Parte 1: virtualización y acceso por SSH | Programación 3
```

> **📌 DATO — sin nombre de facultad, a propósito**
> Las miniaturas **no llevan la marca de ninguna institución**. El pie dice
> `PROGRAMACIÓN 3 • DESPLIEGUE • DEVOPS`, que describe el contenido y no dónde se dicta,
> para que el material se pueda reutilizar en varias facultades sin regenerar nada.
>
> Si alguna vez hiciera falta una tanda con marca institucional, **no se edita el PNG**: se
> agrega un campo a la plantilla de `generar.py` y se genera esa tanda aparte. Editar la
> imagen a mano rompe el sistema en la primera regeneración.
