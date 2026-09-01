# Capturas — Backend desde POO

Carpeta con los **códigos mínimos** para tomar las **capturas de pantalla** de
las figuras cuyo origen es `captura` en [`FIGURAS.md`](../FIGURAS.md). Las de
origen `diagrama` ya están en [`DIAGRAMAS.md`](../DIAGRAMAS.md) (Mermaid) y sus
PNG en [`Imagenes/`](../Imagenes).

Hay **una subcarpeta por capítulo**. Cada una contiene los scripts que generan
la pantalla que se captura, con las instrucciones en el `docstring` de cada
archivo.

## Mapa figura-carpeta

| Figura | Título | Carpeta / archivo |
| --- | --- | --- |
| 1.5 | Documentación automática (endpoint + 422) | `capitulo-01-objeto-al-servicio/app.py` |
| 1.6 | Estructura de un módulo | `capitulo-01-objeto-al-servicio/1_6_estructura_modulo.py` |
| 2.5 | Un `422` con dos errores en la doc | `capitulo-02-contratos/app.py` |
| 2.6 | El schema en la especificación | `capitulo-02-contratos/2_6_schema.py` |
| 3.6 | Una traza de `MissingGreenlet` | `capitulo-03-bucle-eventos/3_6_missing_greenlet.py` |
| 4.5 | El esquema de un dominio en un cliente BD | `capitulo-04-persistencia/4_5_esquema_dominio.py` + `sql/4_5_esquema_dominio.sql` |
| 4.6 | Una migración generada (renombre) | `capitulo-04-persistencia/alembic_demo/` (proyecto Alembic real, `run_demo.py`) |
| 5.6 | Un token decodificado | `capitulo-05-autenticacion/5_6_token_decodificado.py` |
| 6.6 | El registro de una transacción completa | `capitulo-06-uow-transacciones/6_6_registro_transaccion.py` |
| 7.6 | Un interbloqueo en los registros del motor | `capitulo-07-corazon-transaccional/7_6_interbloqueo.py` + `sql/7_6_bloqueos.sql` |
| 8.7 | El buzón drenando después de una caída | `capitulo-08-robustez/8_7_buzon_drenando.py` |

## Dependencias

```bash
pip install -r requirements.txt
```

Las dependencias por figura:
- **1.5 / 2.5 / 2.6** — fastapi, uvicorn, sqlmodel, sqlalchemy, pydantic.
- **3.6** — sqlmodel, sqlalchemy, aiosqlite (motor async mínimo).
- **4.5** — sqlmodel (el `sql` corre contra PostgreSQL del TPI).
- **4.6** — alembic + sqlalchemy (proyecto Alembic real). La migración
  generada y la corregida quedan en `alembic_demo/capturas/`.
- **5.6** — ninguno (decodifica base64).
- **6.6** — sqlmodel, sqlalchemy, **psycopg2-binary** + PostgreSQL corriendo.
- **7.6** — psycopg + PostgreSQL corriendo.
- **8.7** — sqlite3 (de la biblioteca estándar).

### Figuras que necesitan PostgreSQL (6.6 y 7.6)

Ambas leen la conexión de la variable de entorno `CAPTURAS_PG_DSN` (nada de
credenciales en el código). Configurala una vez por sesión y corré el script:

```powershell
$env:CAPTURAS_PG_DSN = "postgresql://postgres:TU_CLAVE@localhost:5432/db"
python capitulo-06-uow-transacciones/6_6_registro_transaccion.py
```

La figura 6.6 imprime el log del motor (`BEGIN … INSERT … COMMIT`) y la 7.6
provoca un interbloqueo entre dos conexiones con `FOR UPDATE`.

## Orden sugerido de toma

Cada script imprime/formatea la pantalla exacta que pide la figura. Para las
que requieren la app (`app.py`), levantala con:

```bash
python -m uvicorn app:app --reload
```

y seguí los pasos del `docstring` (abrir `/docs`, ejecutar el endpoint, mandar
datos inválidos…). El resto son scripts autónomos:

```bash
python nombre_del_script.py
```

## Notas sobre la consola

Todos los scripts fuerzan UTF-8 en su salida (`sys.stdout.reconfigure`) para que
los acentos y caracteres españoles se vean correctos en Windows. Si tu terminal
aun así no muestra bien los acentos al capturar, tomá la captura desde una
ventana con `chcp 65001` o pegá la salida en el documento (el archivo de texto
está en UTF-8).

## Coherencia con FIGURAS.md

Las capturas de este módulo reproducen **literalmente** lo que `FIGURAS.md`
declara que muestra cada figura (el detalle del `422` con `loc/type/msg/input`,
la traza de `MissingGreenlet` con su causa real, los límites `BEGIN…COMMIT`,
etc.). Cualquier cambio en el catálogo debe reflejarse acá.
