# Material de cátedra — Despliegue de aplicaciones web en un VPS

**Programación 3 — Tecnicatura Universitaria en Programación — UTN FRM**
Docente a cargo del módulo: Matías Santiago Torres

Este directorio contiene el **manuscrito fuente** del documento de cátedra. No es el
entregable final: el entregable son seis `.docx` armados en Word con la extensión oficial
de Claude, reproduciendo el formato de la versión final del Capítulo 1.

> **📌 DATO**
> **El material es una unidad de estudio, no un apunte de clase.** La Dirección revisó la
> Clase 1 y devolvió una versión ampliada que fijó el estándar: cada capítulo funda su
> procedimiento en el concepto que lo explica, incluye una sección de génesis histórica, la
> anatomía del protocolo o artefacto, una sección de seguridad y evolución, y cierra con
> referencias normativas y bibliográficas. El alumno tiene que poder leerlo solo, sin haber
> estado en el aula.
>
> Los nueve rasgos del patrón están enunciados en
> [`PROMPTS-WORD.md`](PROMPTS-WORD.md#el-estándar-qué-es-una-unidad-de-estudio). **Todo
> capítulo nuevo tiene que cumplirlos.**

---

## Cómo usar este manuscrito

Los archivos están numerados en el orden en que van al documento final. Cada uno es un
documento de Word separado.

| Archivo | Contenido | Clase | Palabras |
|---|---|---|---|
| `00-tarea-previa-student-pack.md` | Hoja suelta para enviar por el campus **4 semanas antes** | — | 1.150 |
| `01-dns-y-dominio.md` | Resolución de nombres, registros, TTL, wildcard, dominio propio | 1 | 10.660 |
| `02-vps-puertos-y-seguridad.md` | Aprovisionamiento, SSH, puertos, firewall, riesgos | 2 | 8.770 |
| `03-docker.md` | Imagen, capas, los dos Dockerfiles del proyecto | 3 | 7.400 |
| `04-deploy-easypanel.md` | Proyecto, servicios, Traefik, TLS, CORS en producción | 4 | 6.400 |
| `05-red-interna-y-devops.md` | Red interna, Postgres, historial, CI y buenas prácticas | 5 | 6.390 |
| `FIGURAS.md` | Catálogo de las 26 figuras, con especificación de cada una | — | — |
| `DIAGRAMAS.md` | Código Mermaid de los diagramas ya escritos | — | — |
| `PROMPTS-WORD.md` | El estándar de calidad + prompts para Claude for Word | — | — |

---

## El patrón de formato

**La versión final de la Clase 1 es `Clase_1_DNS_unidad_ampliada.docx`, y los cinco
capítulos tienen que salir idénticos a ese archivo en formato.** No se parte de
`Plantilla - TUPaD.docx`.

El procedimiento es duplicar el archivo del director, borrarle el cuerpo sin tocar el
encabezado ni el pie, y volcar el capítulo nuevo. Así el formato queda idéntico **por
construcción** y no por descripción.

| Elemento | Valor |
|---|---|
| Página | A4 vertical · 2,65 cm arriba · 2,1 abajo · 2,54 a los lados |
| Encabezado | `TECNICATURA UNIVERSITARIA EN PROGRAMACIÓN` + `UTN FRM`, y debajo el titulillo `Programación 3 · Unidad N — <título>` |
| Pie | `PROGRAMACIÓN 3` + `Página N` |
| Logos | **ninguno** |
| Cuerpo | Calibri 11 · interlineado 1,15 · 8 pt después |
| Título del capítulo | Cambria 20 negrita `#1F4E79` |
| Título 2 / Título 3 | Cambria 13 negrita `#2E74B5` / Calibri 11,5 negrita `#404040` |
| Recuadros | **tablas de 1×1 sin bordes**, celda rellena |
| Bloques de código | Consolas 9,5 · fondo `#F2F2F2` · sangría 0,42 cm · sin bordes |
| Código en línea | Consolas 10 · fondo `#EEEEEE` |
| Tablas de datos | bordes 0,5 pt `#999999` · encabezado `#D9E2F3` en negrita, repetido |
| Epígrafes | Calibri 9 · `#595959` · centrado |

La especificación completa, medida sobre el XML del archivo, está en
[`PROMPTS-WORD.md`](PROMPTS-WORD.md).

> **⚠️ OJO ACÁ**
> El documento del director **no lleva los logos institucionales** que traía
> `Plantilla - TUPaD.docx`: su encabezado y su pie son solo texto. Está verificado sobre el
> archivo. Es una diferencia deliberada de esta versión respecto de los documentos que se
> venían generando.
>
> Si en algún momento la Dirección pide los logos de vuelta, hay que reponerlos en **los
> cinco documentos**, no en uno. Conviene preguntarlo antes de armar los cinco.

> **📌 DATO**
> Dos detalles del original que se apartan de lo esperable y que se respetan igual, porque
> el criterio es "idéntico al Capítulo 1": los **recuadros son tablas** y no párrafos con
> sombreado, y los **bloques de código no llevan borde izquierdo**, solo fondo y sangría.
> Son 94 recuadros: no se maquetan a mano, se le pide al prompt que los arme.

---

## Convenciones de marcado

El manuscrito usa cuatro marcas que hay que traducir al formato del Capítulo 1.

### Marcadores de figura

```
[FIGURA 1.3: nslookup contra el DNS del ISP y contra 8.8.8.8 — ver FIGURAS.md]
```

Cada marcador está en su propia línea y arranca con `[FIGURA`. Se reemplaza por la
imagen más su epígrafe. La especificación completa de qué debe mostrar cada una está
en `FIGURAS.md`, y el código Mermaid de los diagramas en `DIAGRAMAS.md`.

> **⚠️ OJO ACÁ**
> **Nada de arte ASCII en el manuscrito.** Un esquema hecho con `┌─┐│└┘▶▼` se ve
> aceptable en el `.md` y **queda ilegible en Word**: la fuente monoespaciada rompe la
> alineación de los caracteres de recuadro, y el corrector ortográfico les mete
> subrayados rojos encima. Si un esquema necesita cajas y flechas, va como figura.
>
> Se toleran las anotaciones de una sola línea —una llave `└──┘` señalando una parte de
> una URL— porque no dependen de que dos renglones queden alineados entre sí. Todo lo
> demás, figura.

### Recuadros

El cuerpo del documento está escrito en registro académico impersonal. Los recuadros
rompen ese registro a propósito: son la voz del docente advirtiendo algo que, si no se
lee, cuesta horas. Van en segunda persona.

Cada uno va como una **tabla de 1×1 sin bordes**, con la celda rellena:

| Marca | Fondo de la celda | Color del título | Para qué |
|---|---|---|---|
| `> **⚠️ OJO ACÁ**` | `#FDECEA` | `#C00000` | Error que rompe el despliegue |
| `> **💡 PARA ENTENDER**` | `#DEEBF7` | `#2E74B5` | Concepto que aclara el porqué |
| `> **🧪 EXPERIMENTO**` | `#E2F0DC` | `#538135` | Actividad para hacer en clase |
| `> **📌 DATO**` | `#EFEFEF` | `#595959` | Información de contexto o referencia |

### Secciones de cierre obligatorias

Todo capítulo termina con la misma secuencia, en este orden: **Verificación**, **Errores
frecuentes**, **Actividades** (entre 5 y 7, las últimas de exploración), **Síntesis** y
**Referencias y lecturas complementarias**. Esa última va en prosa, no en lista: un párrafo
de fuentes normativas citadas por número y otro de bibliografía con edición, editorial y
año.

---

## Estructura del módulo

**Cinco clases de cuatro horas, más una tarea previa administrativa.**

| Clase | Título | Modalidad | Entregable del alumno |
|---|---|---|---|
| — | Tarea previa: GitHub Student Pack | — | Cuenta verificada |
| 1 | Del navegador al servidor: DNS y dominio | **Virtual** | Dominio propio con registros cargados |
| 2 | La VPS: aprovisionar, entrar y cerrar | Presencial | VPS con firewall y panel accesible por HTTPS |
| 3 | Docker: la receta reproducible | Indistinta | Los dos contenedores corriendo en local |
| 4 | El despliegue | Presencial | La calculadora publicada en internet |
| 5 | Red interna y DevOps | Presencial | Historial persistente + integración continua |

### Por qué esa modalidad

La cursada es **presencial**, pero algunas clases pueden acordarse virtuales. La
recomendación no es de comodidad: responde a qué necesita cada clase.

| Clase | Motivo |
|---|---|
| **1 — Virtual** | Es la única que **mejora** en virtual. Con cada alumno en su casa hay tantos proveedores de internet como alumnos, y el relevamiento de la sección 1.9 se vuelve un experimento colectivo real. En el aula, todos comparten resolver y el fenómeno no aparece. |
| **2 — Presencial** | Trabajo de grupo sobre una VPS compartida, con pasos irreversibles: si alguien se cierra el acceso SSH, conviene tenerlo al lado. |
| **3 — Indistinta** | Cada alumno trabaja en su propia máquina. Funciona igual de las dos formas. |
| **4 — Presencial** | Es la clase con más puntos de falla simultáneos. Diagnosticar por pantalla compartida, de a cuatro grupos a la vez, es inviable. |
| **5 — Presencial** | Ídem, y el cierre del módulo conviene hacerlo con el curso junto. |

> **⚠️ OJO ACÁ**
> La verificación del GitHub Student Pack tarda entre 3 días y 3 semanas, y a veces la
> rechazan y hay que reintentar. Mandá `00-tarea-previa-student-pack.md` por el campus
> **cuatro semanas antes** de la Clase 1. Si llegás a la primera clase y nadie está
> verificado, la clase se cae y no hay plan B.

---

## Infraestructura del práctico

- **Grupos de 3 o 4 alumnos**, una VPS por grupo.
- **Proveedor**: Hostinger, plantilla de sistema operativo con Easypanel preinstalado.
- **Dominio**: los cuatro integrantes reclaman el suyo por el Student Pack, pero el
  práctico corre sobre el de uno solo, con un registro wildcard.
- **Repositorios**: dos, separados.
  - `github.com/MatyAlts/calculadora-backend`
  - `github.com/MatyAlts/calculadora-frontend`

---

## Relación con el material existente

Este manuscrito **no reemplaza** lo que ya está en el repositorio del proyecto:

| Documento | Rol | Estado |
|---|---|---|
| `README.md` del proyecto | La aplicación en local: CORS, contrato, errores clásicos | Se mantiene |
| `DEPLOY.md` | Guía rápida de despliegue, registro informal | Se actualiza a dos repos |
| `Deploy-VPS-Easypanel.docx` | Primera versión formal del despliegue | Queda absorbido por este material |

El `README.md` del proyecto es la lectura previa obligatoria de la Clase 4: sin
entender CORS y el contrato de la API, el despliegue es una secuencia de clics sin
sentido.
