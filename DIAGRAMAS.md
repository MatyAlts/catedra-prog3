# Diagramas del material — código fuente

Los diagramas del manuscrito están escritos en **Mermaid**. Se generan así:

1. Entrar a **https://mermaid.live**
2. Pegar el bloque completo en el panel izquierdo (incluida la cabecera `---`).
3. Verificar el resultado en el panel derecho.
4. **Actions → SVG** para descargar.

> **📌 DATO**
> Descargá **SVG, no PNG**. Word soporta SVG desde 2016 y el vector se ve nítido a
> cualquier tamaño, incluso al exportar el PDF o al proyectar. Un PNG se pixela apenas lo
> agrandás un poco.

> **💡 PARA ENTENDER**
> La cabecera `config: theme: neutral` de cada diagrama no es decorativa: fuerza una
> paleta gris sobria que combina con la plantilla institucional e imprime bien en blanco
> y negro. Si la sacás, salen los celestes y violetas por defecto de Mermaid y desentonan
> con el resto del documento.

---

# Clase 1

## FIGURA 1.1 — Recorrido de una petición HTTPS

```
---
config:
  theme: neutral
  sequence:
    messageFontSize: 13
    actorFontSize: 13
---
sequenceDiagram
    autonumber
    participant N as Navegador<br/>(máquina del visitante)
    participant R as Resolver DNS
    participant T as Traefik<br/>(el servidor)
    participant W as Contenedor web

    N->>R: ¿Qué IP tiene calculadora.tudominio.com?
    R-->>N: 191.101.1.42
    Note over N,R: Si esto falla, nada de lo que sigue ocurre<br/>y el servidor no registra absolutamente nada
    N->>T: Conexión TCP al puerto 443
    N->>T: Negociación TLS — el nombre viaja en SNI
    N->>T: GET / con la cabecera Host: calculadora.tudominio.com
    T->>W: Enruta según la cabecera Host
    W-->>N: Respuesta HTTP
    Note over N: El navegador renderiza la página
```

**Después de generar:** resaltar en rojo el primer intercambio (pasos 1 y 2) para que se
distinga del resto. La nota ya dice por qué.

---

## FIGURA 1.2 — Resolución recursiva

```
---
config:
  theme: neutral
---
flowchart TD
    U["Equipo del usuario"]
    R["RESOLVER RECURSIVO<br/><i>el del proveedor, o 8.8.8.8</i><br/>el único al que vos le preguntás"]
    RAIZ["Servidor raíz"]
    TLD["Servidor de .com"]
    AUT["Servidor autoritativo<br/><i>tu proveedor de DNS</i>"]
    IP["191.101.1.42"]

    U -->|"1 . ¿qué IP tiene<br/>calculadora.tudominio.com?"| R
    R -->|"2 . ¿quién administra .com?"| RAIZ
    R -->|"3 . ¿quién administra<br/>tudominio.com?"| TLD
    R -->|"4 . ¿qué IP tiene<br/>calculadora.tudominio.com?"| AUT
    AUT --> IP
    IP -->|"5 . respuesta, y queda en caché"| R
    R --> U

    style R fill:#FDECEA,stroke:#C0392B,stroke-width:3px
```

**Ya viene resaltado:** el nodo del resolver sale con el fondo rojo claro del recuadro de
advertencia, que es justo el énfasis que pide el catálogo. Agregale al costado, en Word o
en la propia imagen, la leyenda: *"puede cachear, fallar o filtrar"*.

---

# Clase 2

## FIGURA 2.4 — El recorrido de un paquete por netfilter

```
---
config:
  theme: neutral
---
flowchart TD
    RED(["Red"])
    PRE["PREROUTING<br/><i>apenas llega el paquete</i>"]
    DEC{"Decisión de<br/>enrutamiento<br/><i>¿el destino soy yo?</i>"}
    INP["INPUT"]
    FWD["FORWARD"]
    PROC(["Proceso local<br/><i>sshd, Traefik…</i>"])
    POST["POSTROUTING"]
    SALE(["Red"])
    UFW["Acá escribe <b>ufw</b>"]
    DOCK["Por acá pasa el<br/>tráfico de <b>Docker</b>"]

    RED --> PRE
    PRE --> DEC
    DEC -->|"sí, es para mí"| INP
    DEC -->|"no, es para otro"| FWD
    INP --> PROC
    FWD --> POST
    POST --> SALE

    INP -.- UFW
    FWD -.- DOCK

    style INP fill:#DEEBF7,stroke:#2E74B5,stroke-width:3px
    style FWD fill:#FDECEA,stroke:#C00000,stroke-width:3px
    style UFW fill:#DEEBF7,stroke:#2E74B5,stroke-dasharray:4
    style DOCK fill:#FDECEA,stroke:#C00000,stroke-dasharray:4
    style DEC fill:#EFEFEF,stroke:#595959,stroke-width:2px
```

**Ya viene resaltado.** Los dos nodos que importan salen con los colores de los recuadros
del material: `INPUT` en azul, como el recuadro de concepto; `FORWARD` en rojo, como el de
advertencia. Los dos globos punteados dicen quién escribe en cada uno, que es exactamente
lo que la sección 2.8 necesita que se entienda.

> **💡 PARA ENTENDER**
> Fijate por qué esta figura reemplazó al arte ASCII y no fue solo una cuestión estética.
> En el esquema de texto, `INPUT` y `FORWARD` eran dos cajitas iguales y la oposición entre
> ellas había que deducirla leyendo el párrafo de abajo. Acá la oposición **es la figura**:
> azul contra rojo, con el nombre de quién escribe en cada rama. Un diagrama que no dice
> nada que el texto no diga es decoración; este dice la conclusión antes que el texto.

---

> **⚠️ OJO ACÁ**
> Mermaid dibuja las flechas en el orden en que las escribís, no en un orden lógico
> propio. Si editás algo, revisá que la numeración 1–5 siga leyéndose de arriba hacia
> abajo. Es el error más fácil de cometer y el más difícil de ver.

> **📌 DATO**
> Los nodos `RED` y `SALE` se llaman igual a propósito: el paquete que atraviesa la máquina
> entra por la red y **vuelve a salir a la red**. Que las dos puntas del diagrama sean lo
> mismo es la forma más rápida de ver que un contenedor, para el núcleo, es *otra máquina*.

---

# Clase 3

> **📌 DATO**
> El Capítulo 3 **no tiene diagramas** en el catálogo. Su única figura, la 3.1, es una
> composición de dos capturas: `docker ps` y el navegador en `localhost:8080`. Lo que sigue
> es una figura **propuesta**, que no está en el catálogo todavía. Decidí si entra.

## FIGURA 3.2 — El orden de las capas (propuesta)

```
---
config:
  theme: neutral
---
flowchart TD
    subgraph MAL["✗ Código primero"]
        direction TB
        M1["FROM python"]
        M2["COPY . .<br/><i>todo el proyecto</i>"]
        M3["RUN pip install<br/><b>2-3 minutos</b>"]
        M1 --> M2 --> M3
    end

    subgraph BIEN["✓ Dependencias primero"]
        direction TB
        B1["FROM python"]
        B2["COPY requirements.txt"]
        B3["RUN pip install<br/><b>queda en caché</b>"]
        B4["COPY . .<br/><i>todo el proyecto</i>"]
        B1 --> B2 --> B3 --> B4
    end

    CAMBIO["Cambiás una línea de código"]
    CAMBIO -.->|"invalida desde acá<br/>hacia abajo"| M2
    CAMBIO -.->|"invalida solo esto"| B4

    style M2 fill:#FDECEA,stroke:#C0392B,stroke-width:3px
    style M3 fill:#FDECEA,stroke:#C0392B,stroke-width:3px
    style B3 fill:#F3F8EF,stroke:#538135,stroke-width:3px
    style B4 fill:#FDECEA,stroke:#C0392B,stroke-width:2px
    style CAMBIO fill:#EFEFEF,stroke:#595959,stroke-width:2px
```

**Ya viene resaltado.** En rojo, las capas que se reconstruyen; en verde, la que sobrevive.
La comparación **es** la figura: las dos columnas tienen las mismas instrucciones y solo
cambia el orden.

**Epígrafe propuesto:** Efecto del orden de las instrucciones sobre la caché de
construcción. Las mismas cuatro líneas, invertidas, convierten segundos en minutos.

---

# Clase 4

## FIGURA 4.1 — Arquitectura de Easypanel

```
---
config:
  theme: neutral
---
flowchart TD
    NET(["INTERNET"])
    T["TRAEFIK<br/><i>lee la cabecera Host</i>"]

    subgraph VPS["VPS — red interna del proyecto"]
        direction LR
        WEB["web<br/>nginx : 80"]
        API["api<br/>uvicorn : 8000"]
        DB["db<br/>postgres : 5432"]
    end

    EP["Easypanel<br/><i>construye las imágenes y<br/>administra los contenedores</i>"]
    LE["Let's Encrypt<br/><i>emite los certificados<br/>de web y api</i>"]

    NET -->|"únicos puertos abiertos:<br/><b>80 y 443</b>"| T
    T --> WEB
    T --> API
    API -->|"sin pasar por Traefik"| DB

    EP -.- VPS
    LE -.- T

    style T fill:#DEEBF7,stroke:#2E74B5,stroke-width:3px
    style DB fill:#F3F8EF,stroke:#538135,stroke-width:3px
    style NET fill:#EFEFEF,stroke:#595959,stroke-width:2px
    style EP fill:#FFFFFF,stroke:#595959,stroke-dasharray:4
    style LE fill:#FFFFFF,stroke:#595959,stroke-dasharray:4
```

**Ya viene resaltado:** Traefik en azul, como único punto de entrada, y `db` en verde
porque es el que **no tiene ninguna flecha hacia afuera**. Ese es el punto de la figura.

**Después de generar:** verificá que ninguna flecha salga de `db` hacia arriba. Si el
alumno ve una sola línea que conecte la base con internet, la figura miente.

---

## FIGURA 4.2 — Flujo de despliegue

```
---
config:
  theme: neutral
---
flowchart TD
    DEV["Equipo del alumno"]
    GH["GitHub"]
    EP["Easypanel"]
    IMG["Imagen Docker"]
    CNT["Contenedor"]
    URL(["https://api.tudominio.com"])
    NOTA["El repositorio es la única fuente de código:<br/>Easypanel <b>no</b> recibe archivos cargados a mano"]

    DEV -->|"git push"| GH
    GH -->|"clona"| EP
    EP -->|"lee el Dockerfile"| IMG
    IMG -->|"ejecuta"| CNT
    CNT -->|"enruta Traefik"| URL

    NOTA -.- GH

    style GH fill:#DEEBF7,stroke:#2E74B5,stroke-width:3px
    style URL fill:#F3F8EF,stroke:#538135,stroke-width:3px
    style NOTA fill:#FDECEA,stroke:#C0392B,stroke-dasharray:4
```

**Ya viene resaltado:** la leyenda que pedía el catálogo entra como nodo punteado en rojo,
colgada de GitHub, que es donde tiene sentido leerla.

---

## FIGURA 4.7 — Enrutamiento por cabecera Host

```
---
config:
  theme: neutral
---
flowchart TD
    H1["Host:<br/>api.tudominio.com"]
    H2["Host:<br/>calculadora.tudominio.com"]
    IP["misma IP<br/><b>191.101.1.42</b>"]
    T["TRAEFIK<br/><i>decide por la cabecera Host</i>"]
    API["contenedor api<br/>puerto 8000"]
    WEB["contenedor web<br/>puerto 80"]

    H1 --> IP
    H2 --> IP
    IP --> T
    T --> API
    T --> WEB

    style IP fill:#FDECEA,stroke:#C0392B,stroke-width:4px
    style T fill:#DEEBF7,stroke:#2E74B5,stroke-width:3px
```

**Ya viene resaltado:** el nodo "misma IP" sale en rojo y con el borde más grueso del
diagrama, porque es el punto entero de la figura. Los dos nombres entran por arriba, se
juntan en una sola dirección, y recién Traefik los vuelve a separar.

---

## FIGURA 4.8 — Secuencia del preflight

```
---
config:
  theme: neutral
  sequence:
    messageFontSize: 13
    actorFontSize: 13
---
sequenceDiagram
    autonumber
    participant N as Navegador
    participant A as API

    N->>A: OPTIONS /api/calcular<br/>Origin: https://calculadora.tudominio.com
    A-->>N: 200 — Access-Control-Allow-Origin

    alt El origen está autorizado
        N->>A: POST /api/calcular
        A-->>N: 200 — resultado 2.5
    else El origen NO está autorizado
        Note over N: El POST nunca se emite.<br/>El servidor no registra nada.
    end
```

**Después de generar:** resaltá en rojo la rama `else` completa. Es la que explica por qué
un error de CORS **no aparece en los registros del servidor**: no hay nada que registrar,
porque la petición no salió nunca del navegador.

---

# Clase 5

## FIGURA 5.1 — Qué red ve cada uno ⭐

```
---
config:
  theme: neutral
---
flowchart LR
    subgraph CASA["CASA DEL VISITANTE (Córdoba)"]
        NAV["NAVEGADOR<br/><i>acá corre el JavaScript</i>"]
    end

    subgraph VPS["VPS — red interna del proyecto"]
        direction TB
        API["api"]
        DB["db<br/><i>calculadora_db</i>"]
        API -->|"✓ resuelve por<br/>nombre interno"| DB
    end

    NAV ==>|"✓ sí puede llegar por<br/>https://api.tudominio.com"| API
    NAV -.->|"✗ no puede resolver<br/>calculadora_api"| DB

    style NAV fill:#DEEBF7,stroke:#2E74B5,stroke-width:3px
    style DB fill:#F3F8EF,stroke:#538135,stroke-width:3px
    linkStyle 2 stroke:#538135,stroke-width:4px
    linkStyle 3 stroke:#C0392B,stroke-width:3px
```

**Ya viene resaltado:** la flecha gruesa verde es el camino que sí existe; la punteada roja,
el que no. Las dos salen del mismo navegador, y esa es toda la lección.

**Después de generar:** agregale al costado la leyenda del catálogo —*"el navegador del
visitante no está en la red del servidor, y no hay forma de que lo esté"*— cerca de la
flecha punteada.

> **⚠️ OJO ACÁ**
> Los índices de `linkStyle` cuentan **todas** las flechas del diagrama en el orden en que
> están escritas, incluidas las de adentro de los `subgraph`. Acá la flecha `api → db` es la
> número 2 y la punteada es la 3. Si agregás o movés una sola línea, los colores se corren
> de lugar y no salta ningún error: simplemente se pinta la flecha equivocada.
