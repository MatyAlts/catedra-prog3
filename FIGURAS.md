# Catálogo de figuras

Especificación de las 26 figuras referenciadas en el manuscrito. Cada entrada indica
**qué debe mostrar**, **qué resaltar** y el **epígrafe sugerido**.

## Resumen

| Tipo | Cantidad | Quién las produce |
|---|---|---|
| Diagramas | 8 | Se dibujan a partir del esquema provisto acá |
| Capturas de pantalla | 18 | Se toman del VPS y las cuentas reales |

### Dónde va cada figura

| Figura | Sección | Figura | Sección | Figura | Sección |
|---|---|---|---|---|---|
| 1.1 | 1.3 | 2.5 | 2.8.2 | 4.5 | 4.7.2 |
| 1.2 | 1.4.3 | 2.6 | 2.10 | 4.6 | 4.7.4 |
| 1.3 | 1.9.2 | 3.1 | 3.8.2 | 4.7 | 4.8.2 |
| 1.4 | 1.10 | 4.1 | 4.3 | 4.8 | 4.10.3 |
| 1.5 | 1.13 | 4.2 | 4.3.1 | 4.9 | 4.11.1 |
| 1.6 | 1.14 | 4.3 | 4.5 | 5.1 | 5.3 |
| 2.1 | 2.4 | 4.4 | 4.7.1 | 5.2 | 5.5 |
| 2.2 | 2.5.3 | | | 5.3 | 5.7.2 |
| 2.3 | 2.6.3 | | | 5.4 | 5.9 |
| 2.4 | 2.7.1 | | | | |

> **📌 DATO**
> Esta tabla importa sobre todo si vas a **parchear** un documento ya armado en lugar de
> regenerarlo. Con la renumeración, una sección que antes se llamaba 1.7.2 ahora es 1.9.2,
> y un parche que compare por número de sección se desalinea entero. Ver la advertencia del
> PROMPT 5 en `PROMPTS-WORD.md`.

> **⚠️ OJO ACÁ**
> **El Capítulo 2 pasó de 5 figuras a 6.** La 2.4 es nueva —el diagrama de netfilter que
> reemplazó al arte ASCII— y las que eran 2.4 y 2.5 corrieron a **2.5 y 2.6**. Si ya
> tenías capturadas la de `nmap` y la del panel de Easypanel, hay que **renombrar los
> archivos** antes de insertarlas: el PROMPT 4 se guía por el nombre.

### Reutilización del documento anterior

`Deploy-VPS-Easypanel.docx` ya contiene cinco figuras aprovechables:

| Figura del `.docx` | Reemplaza o alimenta a |
|---|---|
| Fig. 1 — Arquitectura de destino | **4.1** y **4.7** |
| Fig. 2 — Comportamiento erróneo con `127.0.0.1` | **5.1** (ampliada) |
| Fig. 3 — Flujo de construcción y publicación | **4.2** |
| Fig. 4 — Resolución de nombres y enrutamiento | **1.2** (parcial) |
| Fig. 5 — Secuencia de preflight | **4.8** |

---

## Criterios generales para las capturas

| Criterio | Detalle |
|---|---|
| Resolución | Ventana a 1440 px de ancho como mínimo |
| Tema | Claro, para que imprima legible |
| Recorte | Solo la sección relevante, no la pantalla completa |
| Resaltado | Recuadro rojo de 2 px sobre el elemento clave |
| Datos sensibles | Difuminar IP real, contraseñas y tokens |
| Dominio | Usar el dominio real del docente; es más creíble que `tudominio.com` |

> **⚠️ OJO ACÁ**
> Antes de capturar cualquier pantalla del panel, revisá dos veces que no haya
> contraseñas, cadenas de conexión completas ni tokens a la vista. La captura de la
> sección Environment es la más peligrosa: ahí conviven variables inocentes con la
> contraseña de Postgres. Difuminá antes de pegar, no después.

---

# Capítulo 1 — DNS y dominio

## FIGURA 1.1 — Recorrido de una petición HTTPS
**Tipo:** diagrama

Cinco pasos en secuencia horizontal, de izquierda a derecha, con el navegador a la
izquierda y el servidor a la derecha.

```
[Navegador]
    │
    │ 1. ¿Qué IP tiene calculadora.tudominio.com?
    ▼
[Resolver DNS] ──────► 191.101.1.42
    │
    │ 2. Conexión TCP al puerto 443 de 191.101.1.42
    ▼
[Servidor: Traefik]
    │
    │ 3. Negociación TLS  (el nombre viaja en SNI)
    │ 4. GET /  con  Host: calculadora.tudominio.com
    ▼
[Contenedor web]
    │
    │ 5. Respuesta
    ▼
[Navegador renderiza]
```

**Resaltar:** el paso 1 en un color distinto, con una nota al margen: *"si esto falla,
los pasos 2 a 5 no se ejecutan y el servidor no registra nada"*.

**Epígrafe:** Recorrido de una petición HTTPS. La resolución de nombres es previa e
independiente de la conexión con el servidor.

---

## FIGURA 1.2 — Resolución recursiva
**Tipo:** diagrama

```
[Equipo del usuario]
        │
        ▼
  [Resolver recursivo]  ◄── el del proveedor, o 8.8.8.8
        │
        ├──► [Servidor raíz]        ¿quién administra .com?
        │
        ├──► [Servidor de .com]     ¿quién administra tudominio.com?
        │
        └──► [Servidor autoritativo] ¿qué IP tiene calculadora.tudominio.com?
                    │
                    ▼
              191.101.1.42
```

**Resaltar:** el resolver recursivo, con la leyenda *"el único al que vos le preguntás.
Puede cachear, fallar o filtrar"*.

**Epígrafe:** Resolución recursiva. El usuario nunca consulta la jerarquía
directamente: siempre lo hace a través de un resolver.

---

## FIGURA 1.3 — Filtrado del resolver ⭐
**Tipo:** captura de terminal — **la figura más importante del capítulo**

Una única terminal con las cuatro consultas ejecutadas una debajo de la otra. Las dos
primeras son la prueba de control y son imprescindibles: sin ellas la figura no
demuestra filtrado, solo un fallo genérico de DNS.

```
nslookup google.com
nslookup easypanel.host
nslookup app.mi-proyecto.3xzl86.easypanel.host
nslookup app.mi-proyecto.3xzl86.easypanel.host 8.8.8.8
```

**Condición:** debe tomarse desde una conexión que reproduzca el filtrado. El resultado
válido es: `google.com` resuelve, `easypanel.host` NO resuelve, y con `8.8.8.8` sí
resuelve. Cualquier otra combinación no demuestra filtrado.

**Resaltar:** recuadro verde sobre `google.com` resolviendo (la prueba de control),
recuadro rojo sobre el fallo, recuadro verde sobre la resolución con `8.8.8.8`.

**Epígrafe:** El mismo nombre, consultado a dos resolvers distintos, produce resultados
incompatibles, mientras un dominio de control resuelve con normalidad en ambos. El
filtrado ocurre en el resolver, no en el dominio.

> **⚠️ OJO ACÁ**
> Sacala desde la conexión **hogareña de Claro**, que es donde el fallo se reproduce.
> **No sirve desde datos móviles**: la red móvil de Claro resuelve `easypanel.host` sin
> problema, verificado el 27/07/2026. Son infraestructuras distintas con resolvers
> distintos.
>
> Es la única de las 26 que depende de una condición que no controlás, y es el respaldo
> para cuando el relevamiento en vivo no salga como esperabas. **Sacala primera, antes
> que ninguna otra.**

> **📌 DATO**
> Si la Clase 1 se da virtual, el relevamiento colectivo del curso te va a dar material
> mucho mejor que esta figura: una tabla real con los proveedores de tus propios
> alumnos. Considerá reemplazar o complementar esta captura con esa tabla en la edición
> del año siguiente.

---

## FIGURA 1.4 — Verificación global de la resolución
**Tipo:** composición de dos capturas de navegador

`dnschecker.org` consultando **un subdominio inventado** del dominio del docente
—`ejemplo.tudominio.com`—, que resuelve igual gracias al registro comodín. Eso demuestra
dos cosas a la vez: que el comodín funciona y que resuelve desde todo el mundo.

**Composición:** dos recortes lado a lado.
- **Izquierda:** el panel de resolvers desde el campo de búsqueda —donde se lee el
  nombre consultado— hasta unos doce resultados.
- **Derecha:** el mapa, desde su título *DNS Propagation Map*.

**Resaltar:** el campo de búsqueda con el subdominio inventado, y cualquier fila que
haya devuelto un resultado distinto al resto.

**Epígrafe:** Verificación de la resolución desde múltiples ubicaciones geográficas. Un
subdominio que nunca fue cargado individualmente resuelve por efecto del registro
comodín.

> **⚠️ OJO ACÁ**
> **Sacale la publicidad.** `dnschecker.org` intercala banners entre el texto y el mapa,
> y en un documento de cátedra con el escudo institucional en el encabezado no puede
> aparecer publicidad de una empresa. Peor todavía si el aviso es de un registrador de
> dominios, que es competencia del que el capítulo recomienda dos páginas antes.
>
> Recortando el panel izquierdo y el mapa por separado, la publicidad y el texto en
> inglés se van solos.

> **📌 DATO**
> Si en la captura aparece **algún resolver que no devuelve la dirección** mientras el
> resto sí, resaltalo: ilustra en vivo lo que explica la sección 1.9. Pero el epígrafe no
> debe atribuirle una causa: puede ser filtrado, una caché negativa previa a la creación
> del registro, o ese resolver caído en ese momento. La herramienta no permite
> distinguirlo, y el material no debe afirmar lo que no se puede demostrar.

---

## FIGURA 1.5 — Ofertas de dominio del Student Pack
**Tipo:** captura de navegador

`education.github.com/pack` con las tarjetas de Namecheap, name.com y .TECH visibles.

**Resaltar:** recuadro sobre la oferta de Namecheap.

**Epígrafe:** Ofertas de registro de dominio incluidas en el GitHub Student Developer
Pack.

---

## FIGURA 1.6 — Registros DNS cargados
**Tipo:** captura del panel de Namecheap

Pestaña *Advanced DNS* con los dos registros A visibles: **Host `*`** y **Host `@`**,
ambos hacia la misma dirección IP, con TTL en *5 min*.

**Encuadre:** desde el nombre del dominio hasta debajo de *ADD NEW RECORD*, sin la barra
de navegación superior ni la columna lateral izquierda. Las dos filas de registros deben
ocupar buena parte de la figura, no un rincón.

**Resaltar:** recuadro sobre el `*` de la columna *Host*, con la nota
*"solo el asterisco, no `*.tudominio.com`"*.

**No difuminar la IP.** Es pública de todos modos —el dominio resuelve a ella— y una
dirección real hace la figura mucho más convincente que un recuadro borroneado.

**Epígrafe:** Registro comodín y registro del vértice apuntando a la dirección del VPS.

> **📌 DATO**
> Conservá visible la pestaña *Advanced DNS* activa y el nombre del dominio. Son lo que
> le dice al alumno **dónde** está parado. Sin eso, la tabla de registros podría ser de
> cualquier proveedor y el alumno no sabe adónde ir a buscarla.

---

# Capítulo 2 — VPS, puertos y seguridad

## FIGURA 2.1 — Plantilla de sistema operativo
**Tipo:** captura de hPanel

Sección de cambio de sistema operativo con la plantilla Easypanel seleccionada.

**Resaltar:** la plantilla elegida y, si está visible, la advertencia de borrado.

**Epígrafe:** Selección de la plantilla con Easypanel preinstalado en hPanel.

---

## FIGURA 2.2 — Claves SSH del grupo
**Tipo:** captura de hPanel

Sección *SSH Keys* con cuatro claves cargadas, una por integrante, con nombres
identificables.

**Resaltar:** que son cuatro entradas independientes.

**Difuminar:** el contenido de las claves.

**Epígrafe:** Cuatro claves públicas independientes: un acceso por integrante,
revocable por separado.

---

## FIGURA 2.3 — Puertos en escucha
**Tipo:** captura de terminal

Salida de `sudo ss -tlnp` en el VPS recién instalado.

**Resaltar:** las cuatro líneas de 22, 80, 443 y 3000, con el nombre del proceso a la
derecha.

**Epígrafe:** Puertos en escucha y proceso responsable de cada uno.

---

## FIGURA 2.4 — El recorrido de un paquete por netfilter ⭐
**Tipo:** diagrama — **figura clave del capítulo**

Reemplaza al esquema en arte ASCII que traía la sección 2.7.1, que en Word resultaba
ilegible. El código fuente en Mermaid está en `DIAGRAMAS.md`.

Debe mostrar el flujo desde la red hasta su destino, con la **decisión de enrutamiento**
como bifurcación central y las dos ramas excluyentes:

```
red → PREROUTING → decisión de enrutamiento →  ¿es para mí?   → INPUT   → proceso local
                                            →  ¿es para otro? → FORWARD → POSTROUTING → red
```

**Resaltar:** las dos ramas con colores distintos. `INPUT` es donde escribe `ufw`;
`FORWARD` es por donde pasa el tráfico de Docker. Esa oposición visual es todo el valor
de la figura, y es lo que hace comprensible la sección 2.8.

**Epígrafe:** Recorrido de un paquete por los puntos de enganche de netfilter. La decisión
de enrutamiento separa dos caminos excluyentes: `ufw` escribe en uno y Docker pasa por el
otro.

---

## FIGURA 2.5 — Verificación externa ⭐
**Tipo:** captura de terminal — **figura clave del capítulo**

Salida de `nmap -Pn tudominio.com` ejecutado **desde el equipo del docente**, no desde
el servidor.

**Resaltar:** que aparecen únicamente 22, 80 y 443.

**Ideal:** capturar la salida de `sudo ufw status verbose` al lado, para poder contrastar
lo declarado con lo real.

**Epígrafe:** La única verificación válida del estado de los puertos se realiza desde
fuera del servidor.

---

## FIGURA 2.6 — Dominio del panel
**Tipo:** captura de Easypanel

*Settings → Domain* con `easypanel.tudominio.com` configurado, y la barra del navegador
mostrando el candado.

**Resaltar:** el candado de la barra de direcciones.

**Epígrafe:** El panel de administración publicado bajo el dominio propio, con
certificado válido.

---

# Capítulo 3 — Docker

## FIGURA 3.1 — Ambos contenedores en local
**Tipo:** composición de dos capturas

A la izquierda, una terminal con `docker ps` mostrando los dos contenedores. A la
derecha, el navegador en `http://localhost:8080` con una operación resuelta.

**Resaltar:** la columna PORTS de `docker ps`, donde se ve `8000->8000` y `8080->80`.

**Epígrafe:** Los dos servicios del proyecto ejecutándose en el equipo del alumno.

---

# Capítulo 4 — El despliegue

## FIGURA 4.1 — Arquitectura de Easypanel
**Tipo:** diagrama

```
                    INTERNET
                       │
              puertos 80 y 443
                       │
              ┌────────▼────────┐
              │     TRAEFIK     │  ← lee la cabecera Host
              └────────┬────────┘
                       │  red interna del proyecto
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
  ┌──────────┐   ┌──────────┐   ┌──────────┐
  │   web    │   │   api    │   │    db    │
  │ nginx:80 │   │ uvicorn  │   │ postgres │
  │          │   │  :8000   │   │  :5432   │
  └──────────┘   └──────────┘   └──────────┘
                       └──────────────┘
                    sin pasar por Traefik

  Easypanel: construye las imágenes y administra los tres contenedores
  Let's Encrypt: emite los certificados de web y api
```

**Resaltar:** que solo 80 y 443 cruzan la frontera de internet, y que `db` no tiene
ninguna flecha hacia afuera.

**Epígrafe:** Arquitectura interna. Traefik es el único punto de entrada; los servicios
se comunican entre sí por la red interna del proyecto.

---

## FIGURA 4.2 — Flujo de despliegue
**Tipo:** diagrama

```
[Equipo del alumno]  ──git push──►  [GitHub]
                                       │
                                    clona
                                       ▼
                                  [Easypanel]
                                       │
                              lee el Dockerfile
                                       ▼
                                 [Imagen Docker]
                                       │
                                    ejecuta
                                       ▼
                                  [Contenedor]
                                       │
                                 enruta Traefik
                                       ▼
                            https://api.tudominio.com
```

**Resaltar:** la leyenda *"el repositorio es la única fuente de código: Easypanel no
recibe archivos cargados a mano"*.

**Epígrafe:** Flujo de construcción y publicación.

---

## FIGURA 4.3 — Proyecto creado
**Tipo:** captura de Easypanel

Vista del proyecto `calculadora` con los servicios `api`, `web` y `db` listados y en
verde.

**Nota:** conviene tomarla al final de la Clase 5, cuando existan los tres servicios, y
usarla en ambos capítulos.

**Epígrafe:** El proyecto con sus tres servicios en ejecución.

---

## FIGURA 4.4 — Configuración del origen
**Tipo:** captura de Easypanel

Sección *Source* del servicio `api`, con el repositorio, la rama y el Build path
visibles.

**Resaltar:** recuadro rojo sobre el campo **Build path**, con el valor `/`, y una nota:
*"la barra sola, porque el repositorio contiene la aplicación en su raíz"*.

**Epígrafe:** Configuración del origen del servicio `api`.

---

## FIGURA 4.5 — Variables de entorno
**Tipo:** captura de Easypanel

Sección *Environment* del servicio `api` con `ORIGENES_PERMITIDOS` cargada.

**Difuminar:** cualquier otra variable con credenciales, en particular `DATABASE_URL`.

**Epígrafe:** El origen autorizado se declara como variable de entorno, no en el código.

---

## FIGURA 4.6 — La API publicada
**Tipo:** captura de navegador

`https://api.tudominio.com/docs` con la interfaz de FastAPI cargada.

**Resaltar:** el candado y el dominio completo en la barra de direcciones.

**Epígrafe:** Documentación interactiva de la API, publicada con certificado válido.

---

## FIGURA 4.7 — Enrutamiento por cabecera Host
**Tipo:** diagrama

```
  Host: api.tudominio.com          Host: calculadora.tudominio.com
            │                                    │
            │        misma IP: 191.101.1.42      │
            └──────────────┬─────────────────────┘
                           ▼
                     ┌──────────┐
                     │ TRAEFIK  │
                     └────┬─────┘
              ┌───────────┴───────────┐
              ▼                       ▼
      contenedor api            contenedor web
       puerto 8000                puerto 80
```

**Resaltar:** el texto "misma IP", que es el punto de toda la figura.

**Epígrafe:** Alojamiento virtual. Un único servidor y una única dirección IP atienden
dos dominios distintos; la cabecera `Host` determina el destino.

---

## FIGURA 4.8 — Secuencia del preflight
**Tipo:** diagrama de secuencia

```
Navegador                                    API
    │                                         │
    │  OPTIONS /api/calcular                  │
    │  Origin: https://calculadora.tudominio  │
    ├────────────────────────────────────────►│
    │                                         │
    │  200  Access-Control-Allow-Origin: ...  │
    │◄────────────────────────────────────────┤
    │                                         │
    │  ¿el origen está autorizado?            │
    │  SÍ ──► continúa      NO ──► se detiene │
    │                                         │
    │  POST /api/calcular                     │
    ├────────────────────────────────────────►│
    │  200  { "resultado": 2.5 }              │
    │◄────────────────────────────────────────┤
```

**Resaltar:** la rama "NO", con la nota: *"el POST nunca se emite. El servidor no
registra nada"*.

**Epígrafe:** Verificación previa y petición efectiva. Si el preflight no autoriza el
origen, la petición real no llega a emitirse.

---

## FIGURA 4.9 — Las dos peticiones
**Tipo:** captura del navegador

Pestaña Red con `OPTIONS` y `POST` hacia `/api/calcular`, ambas en 200.

**Resaltar:** las dos filas, con una nota: *"dos peticiones, no una"*.

**Epígrafe:** El preflight y la petición efectiva, ambas correctas.

---

# Capítulo 5 — Red interna y DevOps

## FIGURA 5.1 — Qué red ve cada uno ⭐
**Tipo:** diagrama — **la figura conceptual central del módulo**

```
   CASA DEL VISITANTE (Córdoba)          VPS (red interna del proyecto)
  ┌──────────────────────────┐        ┌──────────────────────────────┐
  │                          │        │                              │
  │   ┌──────────────────┐   │        │   ┌──────┐      ┌────────┐   │
  │   │    NAVEGADOR     │   │        │   │ api  │─────►│   db   │   │
  │   │                  │   │        │   └──────┘      └────────┘   │
  │   │ acá corre el JS  │   │        │       ▲     calculadora_db   │
  │   └────────┬─────────┘   │        │       │                      │
  │            │             │        │       │  ✓ resuelve por      │
  └────────────┼─────────────┘        │       │    nombre interno    │
               │                      └───────┼──────────────────────┘
               │   ✗ no puede resolver        │
               │     calculadora_api          │
               │                              │
               └──────────────────────────────┘
                  ✓ sí puede llegar por
                    https://api.tudominio.com
```

**Resaltar:** la cruz sobre el intento de resolución interna desde el navegador, con la
leyenda: *"el navegador del visitante no está en la red del servidor, y no hay forma de
que lo esté"*.

**Epígrafe:** Ámbito de ejecución y visibilidad de red. El frontend se ejecuta fuera del
servidor; por eso la API requiere un dominio público y la base de datos no.

---

## FIGURA 5.2 — Base de datos sin exposición
**Tipo:** captura de Easypanel

Servicio `db` con la pestaña *Domains & Proxy* **vacía**, sin ningún dominio ni puerto
publicado.

**Resaltar:** recuadro sobre la sección vacía, con la nota: *"deliberadamente vacío"*.

**Difuminar:** la contraseña generada.

**Epígrafe:** El servicio de base de datos no declara dominio ni publica puertos.

---

## FIGURA 5.3 — Aislamiento demostrado ⭐
**Tipo:** composición de dos capturas — **la figura más importante del capítulo**

Lado a lado, con el mismo ancho:

- **Izquierda:** navegador en `https://api.tudominio.com/api/historial` mostrando tres
  operaciones en JSON.
- **Derecha:** terminal con `nmap -Pn -p 5432 tudominio.com` informando el puerto
  cerrado o filtrado.

**Resaltar:** un recuadro verde sobre el JSON y uno rojo sobre el estado del puerto.

**Epígrafe:** La base de datos atiende consultas de la API y resulta simultáneamente
inalcanzable desde internet. Ambas afirmaciones son ciertas al mismo tiempo.

---

## FIGURA 5.4 — Verificación en la integración
**Tipo:** captura de GitHub

Un pull request con la verificación de pruebas resuelta.

**Ideal:** capturar **dos estados** y presentarlos juntos: uno en rojo con la prueba
fallando y el botón de integración bloqueado, y otro en verde tras la corrección.

**Resaltar:** el mensaje de bloqueo de la integración en la captura en rojo.

**Epígrafe:** La verificación automática impide integrar código con pruebas fallidas.

---

## Lista de control

### Diagramas (7)

- [ ] 1.1 Recorrido de una petición HTTPS
- [ ] 1.2 Resolución recursiva
- [ ] 4.1 Arquitectura de Easypanel
- [ ] 4.2 Flujo de despliegue
- [ ] 4.7 Enrutamiento por cabecera Host
- [ ] 4.8 Secuencia del preflight
- [ ] 5.1 Qué red ve cada uno ⭐

### Capturas (18)

- [ ] 1.3 Filtrado del resolver ⭐ *(requiere conexión de Claro)*
- [ ] 1.4 dnschecker.org
- [ ] 1.5 Ofertas del Student Pack
- [ ] 1.6 Registros DNS cargados
- [ ] 2.1 Plantilla de sistema operativo
- [ ] 2.2 Claves SSH del grupo
- [ ] 2.3 Puertos en escucha
- [ ] 2.4 Verificación externa con nmap ⭐
- [ ] 2.5 Dominio del panel
- [ ] 3.1 Ambos contenedores en local
- [ ] 4.3 Proyecto con sus servicios
- [ ] 4.4 Configuración del origen
- [ ] 4.5 Variables de entorno
- [ ] 4.6 La API publicada
- [ ] 4.9 Las dos peticiones
- [ ] 5.2 Base de datos sin exposición
- [ ] 5.3 Aislamiento demostrado ⭐
- [ ] 5.4 Verificación en la integración

### Orden sugerido de captura

| Momento | Figuras |
|---|---|
| Antes de empezar, desde una conexión de Claro | 1.3 |
| Al reclamar el dominio | 1.5, 1.6, 1.4 |
| Al aprovisionar el VPS | 2.1, 2.2, 2.3, 2.4, 2.5 |
| Con Docker en local | 3.1 |
| Durante el despliegue | 4.4, 4.5, 4.6, 4.9 |
| Con los tres servicios arriba | 4.3, 5.2, 5.3 |
| Al configurar la integración continua | 5.4 |

> **⚠️ OJO ACÁ**
> La **1.3** es la única que depende de una condición externa que no controlás: necesita
> una conexión donde el filtrado se reproduzca. Sacala primero, apenas tengas un
> servicio levantado con dominio autogenerado. Si dejás esa captura para el final y ese
> día el filtrado no se reproduce, te quedaste sin la figura que sostiene el argumento
> más importante del Capítulo 1.
