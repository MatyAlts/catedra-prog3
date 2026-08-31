# Diagramas — Frontend desde cero

Código Mermaid de las figuras declaradas como `diagrama` en
[`FIGURAS.md`](FIGURAS.md). Un bloque por figura, encabezado por su número.

Se rinden a imagen antes de insertarlos en el `.docx`: el manuscrito Word no
lleva Mermaid.

---

## Figura 1.1 — El recorrido de una petición

Los pasos 1 a 4 son red; los 5 a 8 son navegador. La separación tiene que verse:
es la que explica por qué un fallo de resolución no deja rastro en el servidor.

```mermaid
flowchart TD
    A["1 · Resolución del nombre<br/>foodstore.example → 203.0.113.10"] --> B["2 · Conexión<br/>TCP puerto 443 + TLS"]
    B --> C["3 · Petición HTTP<br/>método · ruta · encabezados · cuerpo"]
    C --> D["4 · Respuesta HTTP<br/>código · encabezados · cuerpo"]
    D --> E["5 · Parseo<br/>el texto se convierte en DOM"]
    E --> F["6 · Recursos subordinados<br/>estilos, imágenes, scripts"]
    F --> G["7 · Estilo, disposición y pintado"]
    G --> H["8 · Ejecución de scripts<br/>que pueden modificar el DOM"]
    H -.->|"vuelve a 7"| G

    classDef red fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    classDef nav fill:#E2F0DC,stroke:#538135,color:#375623
    class A,B,C,D red
    class E,F,G,H nav
```

## Figura 1.2 — Anatomía de una petición HTTP

La línea en blanco va destacada: es el delimitador que separa metadatos de datos
y el que nadie ve hasta que se lo señalan.

```mermaid
flowchart TB
    subgraph P["Petición HTTP"]
        direction TB
        L["<b>Línea de petición</b><br/>POST /api/v1/pedidos HTTP/1.1"]
        E["<b>Encabezados</b><br/>Host · Authorization · Content-Type<br/>Idempotency-Key · Accept · Content-Length"]
        V["<b>Línea en blanco</b><br/>delimita metadatos de datos"]
        C["<b>Cuerpo</b><br/>{ direccion_id, items }"]
        L --- E --- V --- C
    end

    classDef linea fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    classDef enc fill:#EFEFEF,stroke:#595959,color:#333333
    classDef vacia fill:#FDECEA,stroke:#C00000,color:#C00000
    classDef cuerpo fill:#E2F0DC,stroke:#538135,color:#375623
    class L linea
    class E enc
    class V vacia
    class C cuerpo
```

## Figura 1.3 — Anatomía de una URL

El fragmento se marca aparte: es el único componente que **no viaja al
servidor**, y esa propiedad tiene consecuencias prácticas.

```mermaid
flowchart LR
    U["https://foodstore.example:443/api/v1/productos?categoria=3&pagina=2#resultados"]
    U --> E["<b>Esquema</b><br/>https"]
    U --> A["<b>Autoridad</b><br/>foodstore.example"]
    U --> P["<b>Puerto</b><br/>443"]
    U --> R["<b>Ruta</b><br/>/api/v1/productos"]
    U --> Q["<b>Consulta</b><br/>categoria=3&pagina=2"]
    U --> F["<b>Fragmento</b><br/>resultados<br/><i>no viaja al servidor</i>"]

    classDef viaja fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    classDef noviaja fill:#FDECEA,stroke:#C00000,color:#C00000
    class E,A,P,R,Q viaja
    class F noviaja
```

## Figura 1.4 — Del byte al píxel

El árbol de render tiene que verse **más chico** que el DOM: es la forma visual
de explicar que un nodo con `display: none` existe y no se dibuja.

```mermaid
flowchart TD
    B["Bytes recibidos por la red"] --> T["Texto decodificado<br/>según charset"]
    T --> D["<b>DOM</b><br/>árbol completo del documento"]
    S["Hojas de estilo"] --> C["<b>CSSOM</b><br/>árbol de reglas"]
    D --> R["<b>Árbol de render</b><br/>sólo lo que se dibuja<br/><i>display:none queda afuera</i>"]
    C --> R
    R --> L["<b>Disposición</b><br/>posición y tamaño de cada caja"]
    L --> P["<b>Pintado</b><br/>píxeles en pantalla"]

    classDef entrada fill:#EFEFEF,stroke:#595959,color:#333333
    classDef arbol fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    classDef render fill:#E2F0DC,stroke:#538135,color:#375623
    class B,T,S entrada
    class D,C arbol
    class R,L,P render
```

## Figura 2.1 — Las cuatro áreas del modelo de caja

El margen va con relleno transparente y borde punteado: es la única de las cuatro
áreas donde el fondo del elemento **no** se ve. Esa es la diferencia práctica
entre relleno y margen.

```mermaid
flowchart TB
    subgraph M["MARGEN · transparente, no muestra el fondo"]
        subgraph B["BORDE · border"]
            subgraph P["RELLENO · padding · muestra el fondo"]
                C["CONTENIDO<br/>width × height<br/>el texto o los hijos"]
            end
        end
    end

    classDef margen fill:#FFFFFF,stroke:#C00000,stroke-dasharray:5 5,color:#C00000
    classDef borde fill:#EFEFEF,stroke:#595959,stroke-width:3px,color:#333333
    classDef relleno fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    classDef contenido fill:#E2F0DC,stroke:#538135,color:#375623
    class M margen
    class B borde
    class P relleno
    class C contenido
```

## Figura 2.2 — `content-box` frente a `border-box`

Misma declaración, dos anchos reales. El número final de cada columna es el punto
de la figura.

```mermaid
flowchart TB
    D["<b>Declarado en ambos casos</b><br/>width: 300px · padding: 20px · border: 2px"]
    D --> CB["<b>box-sizing: content-box</b><br/><i>valor por defecto</i>"]
    D --> BB["<b>box-sizing: border-box</b><br/><i>lo que casi siempre se quiere</i>"]
    CB --> CB2["contenido 300<br/>+ relleno 20 + 20<br/>+ borde 2 + 2"]
    BB --> BB2["borde 2 + 2<br/>+ relleno 20 + 20<br/>+ contenido 256"]
    CB2 --> CB3["<b>Ocupa 344 px</b>"]
    BB2 --> BB3["<b>Ocupa 300 px</b>"]

    classDef decl fill:#EFEFEF,stroke:#595959,color:#333333
    classDef malo fill:#FDECEA,stroke:#C00000,color:#C00000
    classDef bueno fill:#E2F0DC,stroke:#538135,color:#375623
    class D decl
    class CB,CB2,CB3 malo
    class BB,BB2,BB3 bueno
```

## Figura 2.3 — El orden de la cascada

Lo importante de esta figura es que se vea que **en cuanto un criterio decide, los
siguientes no se consultan**. La especificidad es el tercero, no el primero.

```mermaid
flowchart TD
    I["Varias declaraciones compiten<br/>por la misma propiedad"] --> C1{"1 · ¿Distinto origen<br/>o importancia?"}
    C1 -->|sí| G["<b>Gana</b>"]
    C1 -->|no| C2{"2 · ¿Distinta capa<br/>en cascada?"}
    C2 -->|sí| G
    C2 -->|no| C3{"3 · ¿Distinta<br/>especificidad?"}
    C3 -->|sí| G
    C3 -->|no| C4["4 · Gana la última<br/>que aparece"]
    C4 --> G

    classDef inicio fill:#EFEFEF,stroke:#595959,color:#333333
    classDef criterio fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    classDef gana fill:#E2F0DC,stroke:#538135,color:#375623
    class I inicio
    class C1,C2,C3,C4 criterio
    class G gana
```

## Figura 2.4 — Los ejes de Flexbox

Dos contenedores idénticos con distinto `flex-direction`. Las etiquetas de los
ejes son el contenido de la figura: muestran por qué `justify-content` cambia de
efecto visual sin cambiar de definición.

```mermaid
flowchart LR
    subgraph R["flex-direction: row"]
        direction LR
        R1["principal →<br/><b>justify-content</b>"]
        R2["cruzado ↓<br/><b>align-items</b>"]
    end
    subgraph C["flex-direction: column"]
        direction LR
        C1["principal ↓<br/><b>justify-content</b>"]
        C2["cruzado →<br/><b>align-items</b>"]
    end

    classDef principal fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    classDef cruzado fill:#E2F0DC,stroke:#538135,color:#375623
    class R1,C1 principal
    class R2,C2 cruzado
```

## Figura 2.5 — Grid adaptable con `auto-fill` y `minmax`

Tres anchos de contenedor, una sola declaración de CSS y ninguna consulta de
medios. La declaración va al pie, visible en los tres casos.

```mermaid
flowchart TB
    D["grid-template-columns: repeat(auto-fill, minmax(220px, 1fr))"]
    D --> A["<b>Contenedor 300 px</b><br/>1 columna"]
    D --> B["<b>Contenedor 700 px</b><br/>2 columnas"]
    D --> C["<b>Contenedor 1200 px</b><br/>4 columnas"]

    classDef decl fill:#EFEFEF,stroke:#595959,color:#333333
    classDef col fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    class D decl
    class A,B,C col
```

## Figura 3.1 — De Mocha al ciclo anual

El nodo de ES4 abandonado va en rojo y con su consecuencia anotada: de esa crisis
sale la decisión de avanzar en incrementos chicos y publicar una vez por año.

```mermaid
flowchart LR
    A["<b>1995</b><br/>Mocha → LiveScript<br/>→ JavaScript<br/><i>10 días</i>"] --> B["<b>1996</b><br/>JScript<br/><i>ingeniería inversa</i>"]
    B --> C["<b>1997</b><br/>ECMA-262 ed. 1"]
    C --> D["<b>1999</b><br/>ES3"]
    D --> E["<b>2008</b><br/>ES4 ABANDONADO<br/><i>el comité se divide</i>"]
    E --> F["<b>2009</b><br/>ES5"]
    F --> G["<b>2015</b><br/>ES2015"]
    G --> H["<b>2015 → hoy</b><br/>una edición por año<br/><i>TC39, 4 etapas</i>"]

    classDef hito fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    classDef crisis fill:#FDECEA,stroke:#C00000,stroke-width:3px,color:#C00000
    classDef hoy fill:#E2F0DC,stroke:#538135,color:#375623
    class A,B,C,D,F,G hito
    class E crisis
    class H hoy
```

## Figura 3.2 — Valor y referencia en memoria

Lo que la figura tiene que hacer evidente: en la columna izquierda hay dos cajas;
en la derecha hay dos flechas a **una sola** caja.

```mermaid
flowchart TB
    subgraph V["Primitivos · copia por VALOR"]
        VA["let a = 5"] --> VC1["caja propia<br/><b>5</b>"]
        VB["let b = a<br/>b = 10"] --> VC2["caja propia<br/><b>10</b>"]
    end
    subgraph R["Objetos · copia por REFERENCIA"]
        RA["let p1"] --> RC["<b>un solo objeto</b><br/>{ precio: 5000 }"]
        RB["let p2 = p1<br/>p2.precio = 5000"] --> RC
    end

    classDef valor fill:#E2F0DC,stroke:#538135,color:#375623
    classDef refer fill:#FDECEA,stroke:#C00000,color:#C00000
    class VA,VB,VC1,VC2 valor
    class RA,RB,RC refer
```

## Figura 3.3 — Pila, colas y bucle de eventos

Las dos colas van separadas y con su regla de vaciado escrita al lado: es la
diferencia que explica todo el orden de ejecución.

```mermaid
flowchart TB
    P["<b>PILA DE LLAMADAS</b><br/>lo que se ejecuta ahora<br/><i>un solo hilo</i>"]
    MT["<b>COLA DE MICROTAREAS</b><br/>promesas · queueMicrotask<br/><i>se vacía ENTERA</i>"]
    T["<b>COLA DE TAREAS</b><br/>setTimeout · eventos · red<br/><i>se toma UNA por vuelta</i>"]
    R["<b>RENDERIZADO</b><br/>disposición y pintado<br/><i>mismo hilo</i>"]
    B(["BUCLE DE EVENTOS"])

    B --> P
    P -->|"pila vacía"| MT
    MT -->|"cola vacía"| R
    R --> T
    T -->|"una tarea"| B

    classDef pila fill:#FDECEA,stroke:#C00000,color:#C00000
    classDef micro fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    classDef tarea fill:#EFEFEF,stroke:#595959,color:#333333
    classDef render fill:#E2F0DC,stroke:#538135,color:#375623
    class P pila
    class MT micro
    class T tarea
    class R render
```

## Figura 3.4 — El orden de vaciado

La figura debe hacer visible la asimetría: **todas** las microtareas contra **una
sola** tarea. Ese contraste es el contenido.

```mermaid
flowchart TD
    S1["<b>1 · Vaciar la pila</b><br/>ejecutar todo el código síncrono"]
    S2["<b>2 · Vaciar TODAS las microtareas</b><br/>si una encola otra, también va ahora"]
    S3["<b>3 · Renderizar</b><br/>recién acá se dibuja"]
    S4["<b>4 · Tomar UNA sola tarea</b><br/>el resto espera la próxima vuelta"]
    S1 --> S2 --> S3 --> S4
    S4 -->|"vuelve al paso 1"| S1

    classDef paso fill:#EFEFEF,stroke:#595959,color:#333333
    classDef todas fill:#DEEBF7,stroke:#2E74B5,stroke-width:3px,color:#1F4E79
    classDef una fill:#FDECEA,stroke:#C00000,stroke-width:3px,color:#C00000
    classDef render fill:#E2F0DC,stroke:#538135,color:#375623
    class S1 paso
    class S2 todas
    class S3 render
    class S4 una
```

## Figura 3.5 — La cadena de prototipos

La flecha punteada de la búsqueda es lo importante: recorre la cadena **en tiempo
de ejecución**, cada vez, hasta encontrar la propiedad o llegar a `null`.

```mermaid
flowchart TB
    I["<b>milanesa</b><br/>instancia<br/>nombre · precio"]
    PP["<b>Producto.prototype</b><br/>descripcion()"]
    OP["<b>Object.prototype</b><br/>toString() · hasOwnProperty()"]
    N["<b>null</b><br/><i>fin de la cadena</i>"]

    I -->|"[[Prototype]]"| PP
    PP -->|"[[Prototype]]"| OP
    OP -->|"[[Prototype]]"| N
    I -.->|"milanesa.toString()<br/>no está acá..."| PP
    PP -.->|"...ni acá..."| OP
    OP -.->|"<b>encontrada</b>"| OP

    classDef inst fill:#E2F0DC,stroke:#538135,color:#375623
    classDef proto fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    classDef fin fill:#EFEFEF,stroke:#595959,color:#333333
    class I inst
    class PP,OP proto
    class N fin
```

## Figura 4.1 — El árbol de nodos

Los nodos de texto van en otro color: son el punto de la figura. El `<ul>` tiene
cinco hijos, no dos, y eso explica por qué `childNodes` y `children` no coinciden.

```mermaid
flowchart TB
    UL["<b>ul</b><br/><i>elemento</i>"]
    T1["texto<br/><i>salto + indentación</i>"]
    L1["<b>li</b><br/><i>elemento</i>"]
    T2["texto<br/><i>salto + indentación</i>"]
    L2["<b>li</b><br/><i>elemento</i>"]
    T3["texto<br/><i>salto</i>"]
    TX1["texto<br/><i>Milanesa</i>"]
    TX2["texto<br/><i>Empanadas</i>"]

    UL --> T1
    UL --> L1
    UL --> T2
    UL --> L2
    UL --> T3
    L1 --> TX1
    L2 --> TX2

    classDef elem fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    classDef txt fill:#EFEFEF,stroke:#999999,stroke-dasharray:4 3,color:#595959
    class UL,L1,L2 elem
    class T1,T2,T3,TX1,TX2 txt
```

## Figura 4.2 — Las tres fases de propagación

Un solo clic recorre el árbol **dos veces**. Ese es el compromiso entre Netscape y
Microsoft que el W3C adoptó entero.

```mermaid
flowchart TB
    D1["document"] -->|"1 · captura"| C1["ul.lista"]
    C1 -->|"2 · captura"| B["<b>button</b><br/>FASE OBJETIVO"]
    B -->|"3 · burbujeo"| C2["ul.lista"]
    C2 -->|"4 · burbujeo"| D2["document"]

    classDef captura fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    classDef objetivo fill:#FDECEA,stroke:#C00000,stroke-width:3px,color:#C00000
    classDef burbujeo fill:#E2F0DC,stroke:#538135,color:#375623
    class D1,C1 captura
    class B objetivo
    class C2,D2 burbujeo
```

## Figura 4.3 — Delegación frente a un manejador por elemento

Las anotaciones sobre qué pasa al agregar un botón nuevo son tan importantes como
los números.

```mermaid
flowchart TB
    subgraph SIN["Sin delegación · 100 manejadores"]
        S1["ul.lista<br/><i>sin manejador</i>"]
        S1 --> S2["button ×100<br/><b>100 manejadores</b>"]
        S2 --> S3["Botón nuevo<br/><b>NO funciona</b><br/><i>hay que registrarlo aparte</i>"]
    end
    subgraph CON["Con delegación · 1 manejador"]
        C1["ul.lista<br/><b>1 manejador</b>"]
        C1 --> C2["button ×100<br/><i>sin manejador propio</i>"]
        C2 --> C3["Botón nuevo<br/><b>funciona solo</b><br/><i>el evento burbujea igual</i>"]
    end

    classDef malo fill:#FDECEA,stroke:#C00000,color:#C00000
    classDef bueno fill:#E2F0DC,stroke:#538135,color:#375623
    class S1,S2,S3 malo
    class C1,C2,C3 bueno
```

## Figura 4.4 — Cómo una clausura mantiene vivo un nodo removido

La zona del documento y la zona de memoria van separadas: el nodo salió de la
primera y sigue en la segunda. Esa es toda la figura.

```mermaid
flowchart TB
    subgraph DOC["Documento · lo que se ve en pantalla"]
        BODY["body"]
        CONT["div.contenedor<br/><i>vacío</i>"]
        BODY --> CONT
    end
    subgraph MEM["Memoria · lo que sigue vivo"]
        H["manejador<br/><i>clausura</i>"]
        P["div.panel<br/><b>NODO SEPARADO</b><br/><i>removido del documento</i>"]
        A["pedidos[]<br/><i>y sigue creciendo</i>"]
        H -->|"referencia"| P
        H -->|"referencia"| A
    end
    CANAL["canalDeEventos<br/><i>suscripción nunca dada de baja</i>"] -->|"mantiene vivo"| H

    classDef doc fill:#E2F0DC,stroke:#538135,color:#375623
    classDef fuga fill:#FDECEA,stroke:#C00000,color:#C00000
    classDef canal fill:#EFEFEF,stroke:#595959,color:#333333
    class BODY,CONT doc
    class H,P,A fuga
    class CANAL canal
```

## Figura 5.1 — Estados de una promesa

Las flechas van en un solo sentido y no hay vuelta atrás: una promesa resuelta es
un valor, no una operación en curso.

```mermaid
flowchart LR
    P["<b>PENDIENTE</b><br/>la operación no terminó"]
    C["<b>CUMPLIDA</b><br/>tiene un valor<br/><i>.then()</i>"]
    R["<b>RECHAZADA</b><br/>tiene un motivo<br/><i>.catch()</i>"]
    P -->|"resolve(valor)"| C
    P -->|"reject(motivo)"| R
    C -.->|"<b>no hay vuelta atrás</b>"| C
    R -.->|"<b>no hay vuelta atrás</b>"| R

    classDef pend fill:#EFEFEF,stroke:#595959,color:#333333
    classDef cump fill:#E2F0DC,stroke:#538135,color:#375623
    classDef rech fill:#FDECEA,stroke:#C00000,color:#C00000
    class P pend
    class C cump
    class R rech
```

## Figura 5.2 — Cuándo `fetch` rechaza y cuándo cumple

Esta es la figura que previene el error más frecuente del capítulo. La columna de
la derecha tiene que sorprender: **404 y 500 cumplen la promesa.**

```mermaid
flowchart TB
    F["fetch(url)"]
    F --> RECH["<b>RECHAZA</b><br/><i>el catch se ejecuta</i>"]
    F --> CUMP["<b>CUMPLE</b><br/><i>el catch NO se ejecuta</i>"]
    RECH --> R1["Fallo de red<br/><i>no hubo respuesta</i>"]
    RECH --> R2["Bloqueo por origen<br/><i>CORS</i>"]
    RECH --> R3["Cancelación<br/><i>AbortError</i>"]
    CUMP --> C1["200 OK"]
    CUMP --> C2["404 Not Found"]
    CUMP --> C3["422 Unprocessable"]
    CUMP --> C4["500 Server Error"]
    C2 --> V["hay que mirar<br/><b>respuesta.ok</b>"]
    C3 --> V
    C4 --> V

    classDef rechaza fill:#FDECEA,stroke:#C00000,color:#C00000
    classDef cumple fill:#E2F0DC,stroke:#538135,color:#375623
    classDef aviso fill:#DEEBF7,stroke:#2E74B5,stroke-width:3px,color:#1F4E79
    class RECH,R1,R2,R3 rechaza
    class CUMP,C1,C2,C3,C4 cumple
    class V aviso
```

## Figura 5.3 — La verificación previa de CORS

Dos peticiones donde el código escribió una. Y si la primera falla, la segunda no
existe: el servidor nunca se entera.

```mermaid
sequenceDiagram
    participant C as Código
    participant N as Navegador
    participant S as Servidor
    C->>N: fetch(url, {method:"POST", headers:{Authorization}})
    Note over N: JSON + encabezado propio<br/>→ requiere verificación
    N->>S: OPTIONS /api/v1/pedidos
    Note right of N: Access-Control-Request-Method: POST<br/>Access-Control-Request-Headers: authorization
    S-->>N: 204 + Access-Control-Allow-*
    Note over N: sólo si autoriza,<br/>se emite la real
    N->>S: POST /api/v1/pedidos
    S-->>N: 201 Created
    N-->>C: respuesta
```

## Figura 5.4 — El hueco de la reconexión

El tramo perdido va marcado en rojo. Lo que la figura tiene que dejar claro es que
la recuperación la resuelve **el servidor**, no el navegador.

```mermaid
sequenceDiagram
    participant F as Frontend
    participant S as Servidor
    F->>S: GET /eventos (sin Last-Event-ID)
    S-->>F: evento de sincronización inicial
    S-->>F: id:1041 pedido_actualizado
    Note over F,S: ✂ se cae la conexión
    Note right of S: id:1042 · id:1043 · id:1044<br/>publicados y NO recibidos
    F->>S: reconecta con Last-Event-ID: 1041
    Note over S: busca los eventos<br/>posteriores a 1041
    S-->>F: id:1042 · id:1043 · id:1044
    Note over F,S: si el hueco es muy grande,<br/>el servidor manda "resync"<br/>y el cliente recarga todo
```


## Figura 6.1 — Del `.ts` al `.js`: el borrado

La flecha de abajo es la que importa: **el JavaScript se emite igual aunque la
verificación haya encontrado errores.** Verificación y emisión son independientes.

```mermaid
flowchart TB
    TS["<b>archivo.ts</b><br/>function subtotal(<br/>&nbsp;&nbsp;precio: number,<br/>&nbsp;&nbsp;cantidad: number<br/>): number"]
    TS --> V["<b>1 · Verificación</b><br/>analiza las anotaciones<br/><i>emite un informe</i>"]
    TS --> E["<b>2 · Emisión</b><br/>quita las anotaciones"]
    V --> INF["errores de tipo<br/><i>en la consola</i>"]
    E --> JS["<b>archivo.js</b><br/>function subtotal(<br/>&nbsp;&nbsp;precio,<br/>&nbsp;&nbsp;cantidad<br/>)"]
    INF -.->|"<b>NO detiene la emisión</b>"| JS

    classDef fuente fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    classDef paso fill:#EFEFEF,stroke:#595959,color:#333333
    classDef aviso fill:#FDECEA,stroke:#C00000,color:#C00000
    classDef salida fill:#E2F0DC,stroke:#538135,color:#375623
    class TS fuente
    class V,E paso
    class INF aviso
    class JS salida
```

## Figura 6.2 — Tipado estructural frente a nominal

Misma forma, distinto nombre. Lo que en TypeScript compila, en un lenguaje nominal
es un error — y esa diferencia sale del modelo de objetos del Capítulo 3.

```mermaid
flowchart TB
    subgraph TSC["TypeScript · ESTRUCTURAL"]
        A1["interface Punto<br/>{ x: number; y: number }"]
        A2["interface Coordenada<br/>{ x: number; y: number }"]
        A1 -->|"const c: Coordenada = p<br/><b>compila</b>"| A2
    end
    subgraph NOM["Java / C# · NOMINAL"]
        B1["class Punto<br/>{ int x; int y; }"]
        B2["class Coordenada<br/>{ int x; int y; }"]
        B1 -->|"Coordenada c = p<br/><b>error de compilación</b>"| B2
    end

    classDef ok fill:#E2F0DC,stroke:#538135,color:#375623
    classDef no fill:#FDECEA,stroke:#C00000,color:#C00000
    class A1,A2 ok
    class B1,B2 no
```

## Figura 6.3 — El estrechamiento de una unión discriminada

Dentro de cada rama el compilador sabe exactamente qué propiedades existen. El
`default` con `never` va destacado: es la red que avisa cuando se agrega un estado.

```mermaid
flowchart TB
    U["<b>type Resultado</b><br/>tres formas con la misma<br/>propiedad discriminante"]
    U --> S{"switch (r.estado)"}
    S -->|"&quot;cargando&quot;"| C["sólo existe<br/><b>r.estado</b>"]
    S -->|"&quot;exito&quot;"| E["existe además<br/><b>r.pedidos</b>"]
    S -->|"&quot;error&quot;"| R["existe además<br/><b>r.mensaje</b>"]
    S -->|"default"| N["<b>const x: never = r</b><br/><i>falla al compilar si se<br/>agregó un caso sin contemplar</i>"]

    classDef tipo fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    classDef rama fill:#E2F0DC,stroke:#538135,color:#375623
    classDef red fill:#FDECEA,stroke:#C00000,stroke-width:3px,color:#C00000
    class U,S tipo
    class C,E,R rama
    class N red
```

## Figura 6.4 — Dónde mienten los tipos

La línea vertical es el contenido de la figura: a la izquierda el compilador
verifica, a la derecha el programador afirma. Todo lo que entra cruza esa línea.

```mermaid
flowchart LR
    subgraph EXT["Afuera · sin verificar"]
        J["respuesta.json()<br/><i>devuelve any</i>"]
        P["JSON.parse()<br/><i>del almacenamiento</i>"]
        A["as / any<br/><i>afirmación del programador</i>"]
    end
    F["<b>EL BORDE</b><br/>acá se valida<br/>una sola vez"]
    subgraph INT["Adentro · verificado"]
        T["tipos del dominio<br/>Pedido · Producto · EstadoPedido"]
        V["vistas y lógica<br/><i>el compilador ayuda de verdad</i>"]
        T --> V
    end
    J --> F
    P --> F
    A --> F
    F --> T

    classDef fuera fill:#FDECEA,stroke:#C00000,color:#C00000
    classDef borde fill:#DEEBF7,stroke:#2E74B5,stroke-width:3px,color:#1F4E79
    classDef dentro fill:#E2F0DC,stroke:#538135,color:#375623
    class J,P,A fuera
    class F borde
    class T,V dentro
```


## Figura 7.1 — Del script suelto al empaquetado

Cada nodo lleva el problema que resolvía, no sólo su nombre. El último salto es el
importante: Vite no resolvió un problema nuevo, **notó que uno viejo había
desaparecido**.

```mermaid
flowchart LR
    A["<b>2005 · etiquetas en orden</b><br/>sin módulos, todo global<br/><i>el orden ES la dependencia</i>"]
    B["<b>2009 · CommonJS</b><br/>módulos reales<br/><i>síncrono: no sirve en el navegador</i>"]
    C["<b>AMD</b><br/>asincrónico para el navegador<br/><i>la comunidad partida en dos</i>"]
    D["<b>2011 · Browserify</b><br/>resolver antes de servir"]
    E["<b>2012 · Webpack</b><br/>todo es un nodo del grafo"]
    F["<b>2015 · Rollup</b><br/>eliminar lo que no se usa<br/><i>gracias a los import estáticos</i>"]
    G["<b>2020 · esbuild + Vite</b><br/>el navegador YA entiende import<br/><i>¿por qué empaquetar en desarrollo?</i>"]
    A --> B --> C --> D --> E --> F --> G

    classDef viejo fill:#EFEFEF,stroke:#595959,color:#333333
    classDef medio fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    classDef hoy fill:#E2F0DC,stroke:#538135,stroke-width:3px,color:#375623
    class A,B,C viejo
    class D,E,F medio
    class G hoy
```

## Figura 7.2 — Vite: desarrollo frente a producción

Dos estrategias para dos problemas distintos. Las dependencias pre-procesadas
aparecen en ambos lados: se hacen una sola vez.

```mermaid
flowchart TB
    subgraph DEV["DESARROLLO · importa la velocidad de recarga"]
        D1["dependencias<br/>pre-procesadas con esbuild<br/><i>una sola vez, cacheadas</i>"]
        D2["código propio<br/><b>SIN empaquetar</b>"]
        D3["el navegador pide<br/>módulo por módulo"]
        D4["el servidor transforma<br/><b>sólo lo pedido</b>"]
        D2 --> D3 --> D4
    end
    subgraph PROD["PRODUCCIÓN · importa el tamaño y las peticiones"]
        P1["dependencias<br/>pre-procesadas"]
        P2["Rollup empaqueta todo"]
        P3["elimina lo que no se usa<br/>divide por import dinámico<br/>agrega huella al nombre"]
        P4["<b>unos pocos archivos</b>"]
        P2 --> P3 --> P4
    end

    classDef dev fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    classDef prod fill:#E2F0DC,stroke:#538135,color:#375623
    class D1,D2,D3,D4 dev
    class P1,P2,P3,P4 prod
```

## Figura 7.3 — El ciclo de vida de un elemento personalizado

La flecha de retorno es el contenido de la figura: **mover el elemento vuelve a
disparar el ciclo**, y por eso las suscripciones se duplican si nadie las da de baja.

```mermaid
flowchart TB
    C["<b>constructor</b><br/><i>NO tocar el DOM<br/>NO leer atributos</i>"]
    CC["<b>connectedCallback</b><br/>se insertó en el documento<br/><i>acá va el trabajo real</i>"]
    AC["<b>attributeChangedCallback</b><br/>cambió un atributo observado"]
    DC["<b>disconnectedCallback</b><br/>se quitó del documento<br/><i>acá van TODAS las bajas</i>"]
    C --> CC
    CC <--> AC
    CC --> DC
    DC -->|"<b>si se mueve de lugar,<br/>vuelve a montarse</b>"| CC

    classDef ctor fill:#FDECEA,stroke:#C00000,color:#C00000
    classDef vida fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    classDef baja fill:#E2F0DC,stroke:#538135,stroke-width:3px,color:#375623
    class C ctor
    class CC,AC vida
    class DC baja
```

## Figura 7.4 — Qué aísla el DOM en la sombra

La fila de Tailwind es la que decide la arquitectura del proyecto: **los estilos
globales no cruzan**, y las utilidades de Tailwind son estilos globales.

```mermaid
flowchart LR
    subgraph DOC["Documento principal"]
        G1["estilos globales<br/><b>Tailwind</b>"]
        G2["querySelector<br/>desde el documento"]
        G3["propiedades heredables<br/>tipografía · color"]
        G4["propiedades personalizadas<br/>--color-marca"]
        G5["contenido en ranuras"]
    end
    F{{"FRONTERA<br/>de la sombra"}}
    S["<b>Árbol en la sombra</b><br/>estilos propios aislados"]
    G1 -->|"<b>NO cruza</b>"| F
    G2 -->|"<b>NO cruza</b>"| F
    G3 -->|"sí cruza"| F
    G4 -->|"sí cruza"| F
    G5 -->|"se proyecta"| F
    F --> S

    classDef no fill:#FDECEA,stroke:#C00000,color:#C00000
    classDef si fill:#E2F0DC,stroke:#538135,color:#375623
    classDef borde fill:#DEEBF7,stroke:#2E74B5,stroke-width:3px,color:#1F4E79
    class G1,G2 no
    class G3,G4,G5 si
    class F,S borde
```


## Figura 8.1 — Por tipo frente a por funcionalidad

Lo que la figura tiene que hacer evidente: a la izquierda, para tocar el carrito hay
que abrir cinco carpetas; a la derecha, una. Y borrarlo es borrar esa una.

```mermaid
flowchart TB
    subgraph T["Por TIPO de archivo"]
        direction TB
        T1["components/"]
        T2["services/"]
        T3["store/"]
        T4["types/"]
        T5["utils/"]
        TC["<b>tocar el carrito</b><br/><i>= abrir las cinco</i>"]
        T1 -.-> TC
        T2 -.-> TC
        T3 -.-> TC
        T4 -.-> TC
        T5 -.-> TC
    end
    subgraph F["Por FUNCIONALIDAD"]
        direction TB
        F1["features/carrito/<br/>ui/ · service.ts"]
        F2["features/catalogo/"]
        F3["features/pedidos/"]
        FC["<b>tocar el carrito</b><br/><i>= abrir una</i><br/><b>borrarlo</b> = borrar una"]
        F1 --> FC
    end

    classDef malo fill:#FDECEA,stroke:#C00000,color:#C00000
    classDef bueno fill:#E2F0DC,stroke:#538135,color:#375623
    class T1,T2,T3,T4,T5,TC malo
    class F1,F2,F3,FC bueno
```

## Figura 8.2 — Las capas y la dirección de las dependencias

Las flechas van en un solo sentido. Las dos prohibiciones —hacia arriba y en
horizontal entre features— van tachadas en rojo: son el contenido de la figura.

```mermaid
flowchart TB
    A["<b>Arranque</b> · app/main.ts"]
    R["<b>Router</b> · app/router.ts"]
    V["<b>Vistas</b> · pages/&lt;n&gt;/index.ts"]
    FA["<b>Feature A</b><br/>ui/ · service.ts"]
    FB["<b>Feature B</b><br/>ui/ · service.ts"]
    S["<b>Stores</b> · <b>Cliente API</b> · <b>Cliente de eventos</b>"]
    TY["<b>Types</b> · sin lógica, sin imports"]
    E["<b>api/eventos.ts</b><br/><i>TRANSVERSAL</i><br/>recibe datos sin pedirlos<br/>traduce evento → invalidación"]

    A --> R --> V
    V --> FA
    V --> FB
    FA --> S
    FB --> S
    S --> TY
    FA -.->|"<b>PROHIBIDO</b><br/>horizontal"| FB
    S -.->|"<b>PROHIBIDO</b><br/>hacia arriba"| V
    E -.->|"invalida claves"| S

    classDef capa fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    classDef base fill:#E2F0DC,stroke:#538135,color:#375623
    classDef trans fill:#EFEFEF,stroke:#595959,stroke-dasharray:5 5,color:#333333
    class A,R,V,FA,FB capa
    class S,TY base
    class E trans
```

## Figura 8.3 — Estado del cliente frente a estado del servidor

La pregunta del medio es la figura. `CartItem` va sobre la línea: es la única
excepción declarada a RN-F03.

```mermaid
flowchart TB
    Q{{"¿Quién es el dueño<br/>de este dato?"}}
    Q -->|"el servidor<br/><i>yo tengo una copia</i>"| SRV["<b>QueryClient</b><br/>productos · pedidos · stock<br/><i>puede quedar vieja</i><br/><i>se invalida y recarga</i>"]
    Q -->|"sólo existe acá"| CLI["<b>Stores</b><br/>authStore · cartStore · uiStore<br/>filterStore · checkoutStore · eventosStore<br/><i>nadie más lo cambia</i>"]
    CI["<b>CartItem</b><br/>nombre y precio_ref<br/><i>copia de exhibición</i><br/><b>excepción declarada a RN-F03</b><br/>se revalida al montar el carrito"]
    SRV -.-> CI
    CLI -.-> CI

    classDef pregunta fill:#DEEBF7,stroke:#2E74B5,stroke-width:3px,color:#1F4E79
    classDef srv fill:#EFEFEF,stroke:#595959,color:#333333
    classDef cli fill:#E2F0DC,stroke:#538135,color:#375623
    classDef exc fill:#FDECEA,stroke:#C00000,color:#C00000
    class Q pregunta
    class SRV srv
    class CLI cli
    class CI exc
```

## Figura 8.4 — Los siete pasos del arranque

El paso 2 va destacado: mostrar carga **y nunca login** es lo que evita el parpadeo
en cada recarga. El canal se abre último, recién en el paso 7.

```mermaid
flowchart TD
    P1["<b>1</b> · Lee el estado persistido"]
    P1 -->|"sin token"| SIN["rehidratación terminada<br/>sesión anónima<br/><b>sin abrir canal</b>"]
    P1 -->|"con token"| P2["<b>2</b> · Muestra ESTADO DE CARGA<br/><b>nunca la vista de login</b> · RN-F06<br/>y pide GET /auth/me"]
    P2 -->|"200"| P3["<b>3</b> · Completa usuario<br/>termina la rehidratación"]
    P2 -->|"401"| P4["<b>4</b> · Limpia authStore<br/>termina como anónima<br/><b>no abre el canal</b>"]
    P3 --> P5["<b>5</b> · Recién ahora el Router<br/>resuelve la ruta y monta la vista"]
    SIN --> P5
    P4 --> P5
    P5 --> P6["<b>6</b> · Precarga en paralelo<br/>catálogo y árbol de categorías"]
    P6 --> P7["<b>7</b> · Si hay sesión, abre el<br/><b>ÚNICO</b> EventSource · RN-F10<br/>con el último id persistido"]

    classDef paso fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    classDef clave fill:#FDECEA,stroke:#C00000,stroke-width:3px,color:#C00000
    classDef fin fill:#E2F0DC,stroke:#538135,color:#375623
    class P1,P3,P5,P6,SIN,P4 paso
    class P2 clave
    class P7 fin
```

## Figura 8.5 — El ciclo de vida de la clave de idempotencia

Los tres momentos marcados en rojo son tres bugs distintos, y los tres terminan en
un pedido duplicado y un doble cargo.

```mermaid
flowchart TD
    A["Usuario entra al<br/><b>último paso del checkout</b>"]
    B["<b>crypto.randomUUID()</b><br/>se genera acá<br/><i>NO al confirmar</i>"]
    C["se persiste en checkoutStore<br/><i>sobrevive a una recarga</i>"]
    D["viaja en el encabezado<br/><b>Idempotency-Key</b>"]
    E{"¿llegó la respuesta?"}
    F["reintento con<br/><b>la misma clave</b><br/><i>el servidor reconoce el reenvío</i>"]
    G["<b>onSuccess</b><br/>recién acá se descarta"]
    A --> B --> C --> D --> E
    E -->|"no · corte de red"| F --> D
    E -->|"sí · 201"| G

    classDef normal fill:#DEEBF7,stroke:#2E74B5,color:#1F4E79
    classDef critico fill:#FDECEA,stroke:#C00000,stroke-width:3px,color:#C00000
    classDef fin fill:#E2F0DC,stroke:#538135,color:#375623
    class A,D,E normal
    class B,C,F critico
    class G fin
```
