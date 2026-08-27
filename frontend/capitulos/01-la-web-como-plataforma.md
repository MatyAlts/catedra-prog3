# Capítulo 1 — La web como plataforma: HTTP, el navegador y el documento

*Unidad de estudio · Edición ampliada con fundamentos teóricos*

## 1.1. Alcance de la clase

Este capítulo abre el módulo de frontend por el único lugar posible: no por el
código que se escribe, sino por la plataforma sobre la que ese código se ejecuta.
Antes de la primera línea de HTML conviene responder una pregunta que casi nunca
se formula y que gobierna todo lo que viene después: **¿qué es exactamente lo que
ocurre cuando alguien escribe una dirección y aparece una página?**

La respuesta no es un detalle de cultura general. Quien no sabe que el protocolo
de la web **no recuerda nada entre una petición y la siguiente** no puede entender
por qué el Trabajo Práctico Integrador manda un token en cada llamada. Quien no
sabe que **el navegador jamás rechaza un documento mal formado** no puede entender
por qué toda la validación vive en el servidor. Y quien no sabe que **el método
POST no es idempotente según la norma** va a leer la regla RN-F07 del TPI —la
clave de idempotencia del checkout— como un capricho del enunciado, cuando es la
consecuencia directa de una decisión tomada en 1996.

El alumno que llega a este módulo sabe programar. Conoce variables, funciones,
condicionales y estructuras de datos, porque los trabajó en Programación 1 y 2.
Lo que no conoce es el entorno donde ese conocimiento va a ejecutarse, y ese
entorno tiene reglas propias que no se deducen de saber programar. Este capítulo
las establece.

A diferencia de un lenguaje, la web no se diseñó de una vez. Se acumuló durante
más de treinta años sobre un puñado de decisiones tomadas al principio, cuando
nadie imaginaba para qué se iba a usar. Casi todas las rarezas que el alumno va a
encontrar en los capítulos siguientes —incluidas las de JavaScript— se explican
por compatibilidad hacia atrás con esas decisiones. Por eso el capítulo empieza
por el origen: no como anécdota histórica, sino porque **conocer el problema que
una tecnología vino a resolver es la única forma de juzgar si una solución
propuesta lo resuelve**.

Al finalizar la clase, el alumno debe poder leer la sección 6 del TPI —la
especificación de la API REST— y entender qué describe cada columna de esas
tablas, sin haber escrito todavía una línea de código de cliente.

**Contenidos**

1. Origen y objetivos de diseño de la web.
2. El recorrido completo de una petición, de la barra de direcciones a la
   pantalla.
3. Arquitectura del protocolo HTTP: modelo petición-respuesta y ausencia de
   estado.
4. Semántica de los métodos: seguridad e idempotencia.
5. Códigos de estado y qué informa cada familia.
6. Anatomía de una petición y de una respuesta, campo por campo.
7. Anatomía del identificador uniforme de recurso.
8. El navegador por dentro: del byte al píxel.
9. Anatomía del documento HTML.
10. HTML semántico y el árbol de accesibilidad.
11. Estudio de caso: leer la especificación de la API del TPI.
12. Herramientas de diagnóstico.
13. Seguridad y evolución: HTTPS, encabezados y las versiones del protocolo.

---

## 1.2. Por qué existe la web: origen y objetivos de diseño

A fines de la década de 1980 el problema no era la falta de información en red,
sino lo contrario. El CERN, el laboratorio europeo de física de partículas, era en
ese momento el nodo de internet más grande de Europa, con miles de
investigadores, decenas de sistemas incompatibles entre sí y una rotación
permanente de personal. La documentación de cada experimento vivía en el sistema
que su autor hubiera elegido, en el formato que ese sistema impusiera, accesible
sólo para quien conociera el procedimiento exacto de acceso. Cuando un
investigador se iba, su documentación quedaba huérfana. El problema estaba
formulado con precisión en la propuesta que Tim Berners-Lee presentó en marzo de
1989, titulada *Information Management: A Proposal*: **la información existía, pero
recuperarla exigía conocer de antemano dónde estaba y cómo se accedía a ese lugar
en particular.**

Las herramientas disponibles no lo resolvían, y conviene entender por qué, porque
cada una falló por una razón distinta y de esas tres razones salieron las tres
decisiones de diseño de la web.

**FTP**, el protocolo de transferencia de archivos, permitía traer un documento de
una máquina remota, pero exigía saber el nombre de la máquina, la ruta exacta del
archivo y con frecuencia unas credenciales. Un documento traído por FTP era un
archivo suelto: no había forma de que ese documento señalara a otro documento en
otra máquina. **El problema no era transferir: era relacionar.**

**Gopher**, desarrollado en 1991 en la Universidad de Minnesota, sí organizaba la
información, y lo hacía bien: presentaba cada servidor como un árbol de menús
navegable, y por un tiempo creció más rápido que la web. Su modelo era
jerárquico y cerrado —cada servidor era un árbol propio—, de modo que un elemento
de un menú no podía apuntar al interior de otro servidor como si fuera parte del
mismo tejido. Y en 1993 la universidad anunció que cobraría licencias por la
implementación del servidor. Ese anuncio, en un momento en que la alternativa
acababa de liberarse al dominio público, fue determinante: **la adopción de una
tecnología de red depende tanto de su licencia como de su diseño.**

Los sistemas de **hipertexto** existían desde mucho antes y eran técnicamente
superiores. El Memex de Vannevar Bush (1945), el proyecto Xanadu de Ted Nelson
(1960) y HyperCard de Apple (1987) proponían documentos vinculados con
capacidades que la web todavía hoy no tiene: enlaces bidireccionales, control de
versiones, integridad referencial garantizada. Ninguno escaló a una red mundial, y
la razón es la misma en los tres casos: **garantizar la integridad de los enlaces
exige coordinación central, y la coordinación central no escala.** Si el sistema
promete que ningún enlace se rompe, alguien tiene que saber qué apunta a qué, y
ese alguien se convierte en el cuello de botella de toda la red.

De ese diagnóstico salieron las cuatro decisiones de diseño que explican
absolutamente todo lo observable en este módulo. Vale la pena enunciarlas juntas,
porque el resto del capítulo —y buena parte del resto del módulo— consiste en
descubrir sus consecuencias.

**Primera: identificadores universales.** Cualquier recurso, en cualquier
servidor, se nombra con una cadena única y global que no requiere catálogo central
ni registro previo. Es el URI, y su consecuencia es que un documento puede señalar
a otro sin pedirle permiso a nadie.

**Segunda: un protocolo sin estado.** El servidor no recuerda nada entre una
petición y la siguiente. Cada petición llega sola, sin historia, y debe bastarse a
sí misma. La consecuencia inmediata es que el servidor puede atender millones de
peticiones sin guardar contexto de ninguna, y por lo tanto puede replicarse en
tantas máquinas como haga falta. La consecuencia molesta es que **la sesión hay
que reconstruirla en cada petición**, y de ahí sale el encabezado `Authorization`
con el token que el TPI exige en casi todos sus endpoints.

**Tercera: tolerancia al error en el formato.** El navegador nunca rechaza un
documento por estar mal formado; hace el mejor esfuerzo por mostrarlo igual. Esta
decisión fue deliberada y es la razón por la que la web pudo crecer con millones
de autores sin formación técnica. Su consecuencia es severa: **el HTML no valida
nada**, y por lo tanto ninguna comprobación hecha en el cliente puede considerarse
una garantía. Toda la validación real vive del lado del servidor, que en el TPI son
los esquemas de la sección 7.

**Cuarta: enlaces unidireccionales sin integridad referencial.** Un documento
apunta a otro sin que el apuntado lo sepa y sin que nadie verifique que el destino
existe. Es exactamente lo que Xanadu se negaba a aceptar, y es la razón por la que
la web escaló y Xanadu no. El precio son los enlaces rotos, y se pagó a
conciencia.

El resto es cronología. En 1990 Berners-Lee implementó en una estación NeXT el
primer servidor y el primer navegador —que además era editor, un detalle que se
perdió en el camino—, y el 25 de diciembre de ese año se produjo la primera
comunicación exitosa entre cliente y servidor. El 6 de agosto de 1991 el proyecto
se anunció públicamente en el grupo de noticias `alt.hypertext`. El 30 de abril de
1993 el CERN liberó el software al dominio público, sin regalías: la decisión que
Minnesota no tomó.

> **💡 PARA ENTENDER**
> Fijate en algo que va a volver una y otra vez en este módulo: **las tres
> tecnologías que fracasaron eran mejores que la que ganó.** FTP transfería bien.
> Gopher organizaba bien. Xanadu vinculaba muchísimo mejor.
>
> La web ganó porque resignó garantías a cambio de no necesitar coordinación. Y esa
> es la forma de pensar que te va a servir cuando le pidas algo a un agente de IA:
> no preguntes solamente si una solución funciona, preguntá **qué resignó para
> funcionar**. Siempre resignó algo. Si no lo ves, es que todavía no lo entendiste.

---

## 1.3. Qué ocurre entre la barra de direcciones y la pantalla

Antes de formalizar el protocolo conviene tener el recorrido completo a la vista,
aunque sea de manera aproximada. La secuencia que sigue describe lo que pasa
cuando alguien escribe `https://foodstore.example/productos` y presiona Enter.
Cada paso se desarrolla más adelante en este capítulo o en capítulos posteriores;
la numeración de la referencia acompaña a cada uno.

1. **Resolución del nombre.** El nombre `foodstore.example` no sirve para
   establecer una conexión: hace falta una dirección de red. El sistema operativo
   consulta al resolver configurado, que devuelve una dirección IP. Este tramo es
   previo e independiente de todo lo demás, y cuando falla, el servidor no registra
   absolutamente nada, porque la petición nunca llegó a emitirse.

2. **Conexión.** Con la dirección en mano se abre una conexión TCP contra el
   puerto correspondiente —443 para HTTPS— y sobre ella se negocia el cifrado TLS
   (sección 1.12).

3. **Petición.** El navegador emite una petición HTTP: una línea con el método y la
   ruta, un conjunto de encabezados y, si corresponde, un cuerpo (sección 1.6).

4. **Respuesta.** El servidor devuelve un código de estado, sus propios
   encabezados y el cuerpo de la respuesta (secciones 1.5 y 1.6).

5. **Parseo.** El navegador lee el HTML recibido y construye el **DOM**, que es la
   representación en memoria del documento (sección 1.8). Este es el objeto que
   todo el resto del módulo va a manipular.

6. **Recursos subordinados.** Durante el parseo el navegador descubre referencias a
   hojas de estilo, imágenes y scripts, y emite una petición nueva por cada una.
   Una página no es una descarga: son decenas.

7. **Estilo, disposición y pintado.** El navegador combina el DOM con las reglas de
   estilo, calcula la geometría de cada elemento y finalmente dibuja los píxeles
   (sección 1.7).

8. **Ejecución de scripts.** El código JavaScript se ejecuta y puede modificar el
   DOM, lo que obliga a rehacer parte del trabajo anterior. Este es el tema del
   Capítulo 4.

*(Ver Figura 1.1: el recorrido completo de una petición.)*

Dos observaciones sobre esta lista, ambas importantes.

La primera es que **los pasos 1 a 4 no son responsabilidad del frontend**, y sin
embargo son donde se originan la mayoría de los errores que el frontend tiene que
manejar. Un desarrollador de cliente que no distingue un fallo de resolución de un
fallo de conexión, ni un error de red de un error de aplicación, va a escribir
manejo de errores inútil. El Capítulo 5 vuelve sobre esto con la sección 14.1 del
TPI en la mano.

La segunda es que **el paso 5 produce el objeto sobre el que trabaja todo este
módulo**. El HTML que viaja por la red es texto; el DOM es una estructura de datos
en memoria. Confundirlos es el error conceptual más común de quien empieza, y el
Capítulo 4 está dedicado íntegramente a esa distinción.

---

## 1.4. Arquitectura del protocolo HTTP

### 1.4.1. El modelo petición-respuesta y la ausencia de estado

HTTP es un protocolo de **petición y respuesta**: el cliente emite una petición, el
servidor devuelve exactamente una respuesta, y el intercambio termina. El servidor
nunca inicia la conversación. Esta asimetría es constitutiva y tiene una
consecuencia práctica enorme, que el TPI enfrenta de lleno en su sección 11: si el
servidor necesita avisarle algo al cliente —que un pedido cambió de estado, por
ejemplo—, **no puede simplemente mandárselo**. Hace falta un mecanismo adicional, y
el Capítulo 5 estudia el que el TPI eligió.

La segunda característica es la que más consecuencias tiene: HTTP **no tiene
estado**. El servidor no guarda información sobre peticiones anteriores. Cada
petición llega como si fuera la primera, sin conocimiento de las que la
precedieron.

Conviene ser preciso con el vocabulario, porque acá se confunden dos cosas
distintas. Que el protocolo no tenga estado **no significa que la aplicación no lo
tenga**: significa que el estado no vive en el protocolo. La aplicación guarda
usuarios, pedidos y stock en una base de datos, y eso es estado. Lo que el
protocolo no hace es asociar automáticamente una petición con la anterior.

Esa asociación hay que construirla, y siempre se construye igual: **la petición
lleva consigo lo que hace falta para reconstruir el contexto**. En el TPI eso es un
token firmado que viaja en el encabezado `Authorization` con el esquema `Bearer`,
y que el servidor verifica en cada petición sin consultar ninguna tabla de
sesiones. La sección 5.1 del TPI lo dice explícitamente: el backend no almacena
sesiones ni listas de tokens.

> **💡 PARA ENTENDER**
> Esto explica una cosa que a veces molesta y parece redundante: **por qué tenés que
> mandar el token en cada llamada.** ¿No sería más cómodo mandarlo una vez y que el
> servidor se acuerde?
>
> Sería más cómodo para vos y catastrófico para el sistema. Si el servidor se
> acordara, tendría que guardar tu sesión en algún lado, y entonces todas tus
> peticiones tendrían que ir a la misma máquina que la guardó. Con un servidor
> solo no se nota. Con veinte servidores atrás de un balanceador, se cae todo.
>
> La incomodidad de repetir el token es el precio de que el sistema pueda crecer
> agregando máquinas. Es un intercambio, no un descuido.

### 1.4.2. Semántica de los métodos: seguridad e idempotencia

El método de una petición declara **qué se pretende hacer** con el recurso. La
norma vigente, la RFC 9110, define un conjunto acotado y —esto es lo importante—
clasifica cada método según dos propiedades que no son sinónimas y que se
confunden todo el tiempo.

Un método es **seguro** cuando no está destinado a modificar el estado del
servidor. `GET`, `HEAD` y `OPTIONS` lo son. La palabra "destinado" no está de
adorno: la norma no puede impedir que un servidor mal escrito borre algo al recibir
un `GET`, lo que la norma establece es que quien emite un `GET` tiene derecho a
suponer que no está modificando nada. De ahí se desprende una consecuencia
concreta: **los intermediarios pueden repetir y cachear libremente un método
seguro**, y por eso una acción destructiva jamás debe exponerse detrás de un `GET`.

Un método es **idempotente** cuando ejecutarlo varias veces produce el mismo efecto
que ejecutarlo una sola vez. `GET`, `HEAD`, `OPTIONS`, `PUT` y `DELETE` lo son.
Nótese que idempotente no quiere decir que la respuesta sea igual: un `DELETE`
repetido puede devolver 204 la primera vez y 404 la segunda. Lo que se mantiene
igual es **el estado resultante del servidor**: el recurso está borrado en ambos
casos.

Y acá aparece el que importa. **`POST` no es seguro ni idempotente.** Ninguna de
las dos. Repetir un `POST` puede crear dos recursos donde debía haber uno.

Esa propiedad —o mejor dicho, esa carencia— es la que funda una de las once reglas
obligatorias del frontend del TPI. Cuando un cliente emite un `POST` para crear un
pedido y la respuesta no llega, el cliente queda en la peor situación posible: **no
sabe si el pedido se creó o no.** Si reintenta, puede duplicarlo. Si no reintenta,
puede perderlo.

La norma no resuelve ese problema, porque no puede: es inherente a una red poco
confiable. Lo resuelve la aplicación, y siempre de la misma manera: el cliente
genera un identificador único antes de emitir la petición, lo manda como
encabezado, y el servidor lo usa para reconocer un reenvío. Eso es exactamente la
regla **RN-F07** del TPI, que exige generar la clave con `crypto.randomUUID()` al
entrar al último paso del checkout y enviarla en el encabezado `Idempotency-Key`.

> **📌 NOTA**
> Guardá esta conexión, porque es el modelo de todo el módulo: **RN-F07 no es una
> ocurrencia del enunciado. Es la respuesta de la aplicación a una propiedad que la
> norma le atribuye a POST desde 1996.**
>
> Cuando llegues al Capítulo 8 y la implementes, no la vas a estar copiando de la
> consigna: vas a saber qué problema resuelve. Y si un agente de IA te propone un
> checkout sin clave de idempotencia, vas a poder decirle exactamente qué le falta y
> por qué.

### 1.4.3. Códigos de estado

Toda respuesta empieza por un número de tres dígitos. El primer dígito define la
familia, y cada familia responde una pregunta distinta. Interpretar bien esa
primera cifra es lo que separa un manejo de errores útil de uno decorativo.

| Familia | Significado | Qué informa realmente |
| --- | --- | --- |
| `1xx` | Informativa | La petición se recibió y el proceso continúa |
| `2xx` | Éxito | La petición se recibió, se entendió y se procesó |
| `3xx` | Redirección | Hace falta una acción adicional para completarla |
| `4xx` | Error del cliente | **La petición está mal. Repetirla igual no sirve** |
| `5xx` | Error del servidor | La petición podía estar bien; el servidor falló |

La distinción entre `4xx` y `5xx` es la que gobierna la lógica de reintento del
cliente, y es también la que más se maltrata. Un `4xx` dice que **la petición
estaba mal**: reintentarla sin cambios va a producir el mismo resultado y sólo
consume recursos. Un `5xx` dice que el servidor no pudo, y ahí un reintento sí
puede tener sentido, porque la causa puede ser transitoria.

Dentro de `4xx` hay tres pares que conviene no confundir, porque el TPI los usa con
precisión en su catálogo de la sección 14.1:

- **401 frente a 403.** El 401 dice "no sé quién sos": falta la credencial o no es
  válida. El 403 dice "sé quién sos y no te alcanza": la credencial es válida pero
  el rol no autoriza esa operación. Un cliente que los trata igual va a mandar al
  usuario a la pantalla de login cuando el problema era de permisos.
- **400 frente a 422.** El 400 indica una petición malformada. El 422 indica que la
  petición estaba bien formada pero su contenido no pasó la validación semántica.
- **404 frente a 410.** El 404 dice que no se encontró. El 410 dice que existió y
  ya no está, de forma permanente.

Merece mención aparte el **429**, que indica que el cliente superó un límite de
peticiones. El TPI lo usa en su límite de intentos de autenticación —sección 4.4—
y lo acompaña del encabezado `Retry-After`, que dice cuánto esperar. Un cliente
que ignora ese encabezado y reintenta de inmediato empeora exactamente el problema
que el límite intenta contener.

> **⚠️ OJO ACÁ**
> **Un código de estado es información de diagnóstico, no un cartel de error.**
>
> Cuando algo falla y ves un 401, no anotes "falló la petición": anotá "el servidor
> me dijo que no sabe quién soy". Son cosas distintas y llevan a arreglos
> distintos.
>
> Y prestá atención a la diferencia entre **recibir un 500 y no recibir nada**. Un
> 500 significa que la petición llegó, el servidor la procesó y explotó adentro: hay
> log del lado del servidor y lo podés buscar. No recibir nada significa que la
> petición **nunca llegó**, y ahí no hay log de nada: el problema está en la red, en
> la resolución del nombre o en la conexión. Confundir esos dos casos te puede
> costar una tarde entera buscando en el lugar equivocado.

---

## 1.5. Anatomía de una petición y de una respuesta

Una petición HTTP es texto con una estructura fija. Conviene verla entera una vez,
campo por campo, porque todo lo que el TPI especifica en su sección 6 es
exactamente esto.

```
POST /api/v1/pedidos HTTP/1.1
Host: foodstore.example
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
Idempotency-Key: 6f4a2b18-9c3d-4e5a-8f01-2d7b6c9e4a13
Accept: application/json
Content-Length: 87

{"direccion_id": 42, "items": [{"producto_id": 7, "cantidad": 2}]}
```

La primera línea es la **línea de petición** y tiene tres partes separadas por
espacios: el **método** (`POST`), que declara la intención según la semántica de la
sección 1.4.2; el **destino** (`/api/v1/pedidos`), que es la ruta dentro del
servidor; y la **versión** del protocolo (`HTTP/1.1`).

Después vienen los **encabezados**, uno por línea, con la forma `Nombre: valor`.
Los de este ejemplo cubren los casos más frecuentes:

- **`Host`** indica a qué nombre de dominio va dirigida la petición. Es obligatorio
  desde HTTP/1.1 y su ausencia fue el motivo de esa versión: sin él, un servidor
  con muchos sitios en la misma dirección IP no puede saber cuál se le pide.
- **`Authorization`** transporta la credencial. El esquema `Bearer` significa
  literalmente "al portador": quien tenga el token puede usarlo. Esto tiene una
  consecuencia de seguridad que el Capítulo 5 desarrolla.
- **`Content-Type`** declara el formato del cuerpo. El servidor no lo adivina: lo
  lee de acá.
- **`Idempotency-Key`** es el encabezado de la sección 1.4.2, el que la regla
  RN-F07 del TPI exige en el checkout.
- **`Accept`** declara qué formatos entiende el cliente.
- **`Content-Length`** indica el tamaño del cuerpo en bytes.

Una línea en blanco separa los encabezados del **cuerpo**. Esa línea vacía no es
formateo: es el delimitador que le dice al receptor dónde terminan los metadatos y
dónde empiezan los datos. Los métodos sin cuerpo, como `GET`, terminan ahí.

La respuesta tiene la misma estructura, con una diferencia en la primera línea:

```
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/v1/pedidos/1043
Content-Length: 214

{"id": 1043, "estado": "pendiente", "total": "4750.00", ...}
```

La **línea de estado** lleva la versión, el código numérico y una frase
descriptiva. Esa frase es para las personas: **ningún programa debe tomar
decisiones leyéndola**, porque no está garantizada. El número sí lo está.

De los encabezados de respuesta conviene señalar dos. **`Location`** acompaña a un
201 e indica dónde quedó el recurso recién creado. Y en el cuerpo hay un detalle
que va a reaparecer con fuerza en el Capítulo 6: **el total viaja como cadena de
texto**, `"4750.00"`, no como número. No es un descuido del ejemplo. Es la regla
**RN-F08** del TPI, y el motivo se estudia cuando corresponda: el tipo numérico de
JavaScript no puede representar exactamente ciertos valores decimales, y el dinero
no admite ese error.

*(Ver Figura 1.2: anatomía de una petición HTTP campo por campo.)*

> **🧪 EXPERIMENTO**
> Abrí cualquier sitio en el navegador y presioná F12 para abrir las herramientas de
> desarrollo. Andá a la pestaña **Network** o **Red** y recargá la página con la
> pestaña abierta.
>
> 1. Contá cuántas peticiones se emitieron. ¿Cuántas esperabas?
> 2. Hacé clic en la primera de todas, la del documento, y buscá los encabezados de
>    petición y de respuesta. Encontrá los que se describieron arriba.
> 3. Buscá una petición que haya devuelto un código que **no** sea 200 y anotá cuál
>    es y de qué recurso se trata.
> 4. Ordená la lista por tamaño y fijate qué recurso pesa más.
>
> Lo que estás mirando es exactamente el texto de esta sección, capturado en vivo.
> **Esta pestaña va a ser tu herramienta principal durante los ocho capítulos**, así
> que conviene que te acostumbres desde hoy.

---

## 1.6. Anatomía del identificador uniforme de recurso

El URI es la primera de las cuatro decisiones de diseño de la sección 1.2, y la
que sostiene a las otras tres. Su sintaxis está normada por la RFC 3986 y tiene
cinco componentes:

```
https://foodstore.example:443/api/v1/productos?categoria=3&pagina=2#resultados
```

| Componente | Valor en el ejemplo | Delimitador | Qué identifica |
| --- | --- | --- | --- |
| Esquema | `https` | termina en `://` | El protocolo, y con él cómo interpretar el resto |
| Autoridad | `foodstore.example` | hasta `:`, `/`, `?` o `#` | El servidor que aloja el recurso |
| Puerto | `443` | empieza en `:` | El punto de conexión; se omite si es el del esquema |
| Ruta | `/api/v1/productos` | empieza en `/` | El recurso dentro del servidor |
| Consulta | `categoria=3&pagina=2` | empieza en `?` | Parámetros como pares `clave=valor` |
| Fragmento | `resultados` | empieza en `#` | Un punto dentro del recurso ya recibido |

El **esquema** (`https`) indica el protocolo, y por lo tanto cómo interpretar todo
lo que sigue. La **autoridad** (`foodstore.example`) nombra al servidor. El
**puerto** casi siempre se omite porque cada esquema tiene el suyo por defecto: 443
para `https`, 80 para `http`. La **ruta** identifica el recurso dentro del
servidor. La **cadena de consulta**, que empieza en `?`, transporta parámetros como
pares `clave=valor` separados por `&`; el TPI la usa para paginación y
ordenamiento, según las convenciones de su sección 6.1.

El **fragmento**, que empieza en `#`, merece un párrafo propio porque tiene una
propiedad que sorprende: **nunca se envía al servidor**. Es de uso exclusivo del
cliente. El navegador lo usa para desplazarse hasta un elemento de la página ya
recibida, y ninguna aplicación de servidor puede leerlo, porque jamás le llega.

*(Ver Figura 1.3: anatomía de una URL.)*

> **⚠️ OJO ACÁ**
> Que el fragmento no viaje al servidor tiene una consecuencia que te va a ahorrar
> un rato de desconcierto: **si mandás información sensible después del `#`, el
> servidor no la va a ver nunca.** No es que llegue y se ignore. No llega.
>
> Y al revés: todo lo que ponés en la cadena de consulta —después del `?`— **sí
> viaja, y queda registrado en los logs del servidor y en el historial del
> navegador**. Nunca pongas una contraseña ni un token ahí. Esas cosas van en el
> cuerpo de la petición o en un encabezado, que no se registran de la misma manera.

---

## 1.7. El navegador por dentro: del byte al píxel

### 1.7.1. Del texto al DOM

Lo que llega por la red es una secuencia de bytes. Lo que el código de este módulo
va a manipular es otra cosa: una estructura de datos en memoria. El proceso que
convierte lo primero en lo segundo se llama **parseo**, y su resultado es el
**Document Object Model**, el DOM.

El parser lee el texto, reconoce las etiquetas y construye un árbol de nodos. Cada
elemento del documento es un nodo, cada texto es un nodo, y la anidación del
marcado se convierte en la relación padre-hijo del árbol.

Acá se manifiesta la tercera decisión de diseño de la sección 1.2 —la tolerancia al
error— y conviene verla en acción, porque es contraintuitiva. Si el documento tiene
una etiqueta sin cerrar, o cerrada en el orden equivocado, o directamente
inventada, **el parser no falla**. Aplica un conjunto de reglas de recuperación
definidas en la norma y produce un árbol igual. El árbol puede no ser el que el
autor esperaba, pero es un árbol válido, y la página se muestra.

La contracara es que **un error de marcado no produce ningún mensaje de error**.
Simplemente aparece algo distinto de lo esperado, sin explicación. El Capítulo 4
vuelve sobre esto: es una de las razones por las que conviene construir los nodos
por programa en lugar de armar cadenas de texto con marcado adentro.

> **💡 PARA ENTENDER**
> Acá hay una distinción que si la agarrás ahora te ahorra meses de confusión:
> **el HTML no es el DOM.**
>
> El HTML es el texto que viajó por la red. El DOM es la estructura que el navegador
> construyó a partir de ese texto. Son dos cosas distintas, en dos momentos
> distintos.
>
> ¿Por qué importa tanto? Porque a partir del Capítulo 4 vas a modificar el DOM con
> JavaScript, y cuando lo hagas **el HTML original no cambia**. Si mirás el código
> fuente de la página con Ctrl+U vas a seguir viendo el texto que llegó, sin tus
> cambios. Y si mirás el panel Elements de las herramientas de desarrollo vas a ver
> el DOM actual, con tus cambios.
>
> Muchísima gente pierde tardes enteras porque mira uno y cree que está mirando el
> otro. Vos ya no.

### 1.7.2. De los estilos al píxel

Con el DOM construido, el navegador todavía no puede dibujar nada, porque no sabe
cómo se ve cada nodo. Necesita las reglas de estilo, y con ellas arma una segunda
estructura, el **CSSOM**, que es el equivalente del DOM para las hojas de estilo.

De la combinación de ambos sale el **árbol de render**, que contiene únicamente lo
que se va a dibujar. Un nodo con `display: none` está en el DOM pero no en el árbol
de render: existe, se puede consultar por programa, y no ocupa lugar.

Sobre ese árbol se ejecutan dos etapas más. La **disposición** —o *layout*— calcula
la geometría: posición y tamaño de cada caja. El **pintado** convierte esa
geometría en píxeles.

*(Ver Figura 1.4: del byte al píxel, las etapas del renderizado.)*

Este recorrido explica dos comportamientos que de otra manera parecen arbitrarios:

**Por qué las hojas de estilo bloquean el pintado.** El navegador no dibuja hasta
tener el CSSOM completo. Si dibujara antes, mostraría el documento sin estilos y
después saltaría a la versión con estilos, produciendo un parpadeo. Prefiere
esperar.

**Por qué un script en medio del documento detiene el parseo.** Un script puede
modificar el DOM, incluso agregar contenido en el punto donde está. El parser no
puede seguir construyendo un árbol que el script está por cambiar, así que se
detiene, ejecuta el script y recién después continúa. De ahí salen los atributos
`defer` y `async`, que el Capítulo 3 estudia, y la costumbre de poner los scripts
al final del documento.

---

## 1.8. Anatomía del documento HTML

Un documento HTML mínimo y correcto tiene esta forma:

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Food Store — Catálogo</title>
    <link rel="stylesheet" href="/estilos.css">
  </head>
  <body>
    <h1>Catálogo</h1>
    <script type="module" src="/main.js"></script>
  </body>
</html>
```

Cada línea de la cabecera está por una razón concreta, y ninguna es ceremonial.

**`<!DOCTYPE html>`** no declara una versión: activa el **modo estándar** de
renderizado. Sin esa línea el navegador entra en *quirks mode*, un modo de
compatibilidad que reproduce el comportamiento de navegadores de los años noventa,
con un modelo de caja distinto del actual. Es la primera línea del documento
porque tiene que ser lo primero que el parser vea.

**`lang="es"`** declara el idioma del contenido. Lo usan los lectores de pantalla
para elegir la pronunciación, los correctores ortográficos y los buscadores. Su
ausencia no rompe nada visible, y por eso se olvida.

**`<meta charset="utf-8">`** declara la codificación de caracteres, y debe estar
dentro de los primeros 1024 bytes del documento. La razón es circular y por eso hay
que declararlo tan al principio: **para leer el documento hay que saber cómo están
codificados sus caracteres**, y esa información está en el propio documento. Si
falta, el navegador adivina, y cuando adivina mal aparecen los caracteres
partidos que todo el mundo reconoce.

**`<meta name="viewport" ...>`** indica al navegador móvil que use el ancho real
del dispositivo. Sin esta línea, un teléfono simula una pantalla de escritorio de
unos 980 píxeles y reduce todo, con el resultado de que ningún diseño responsive
funciona. El Capítulo 2 lo retoma.

**`<title>`** es el título del documento: aparece en la pestaña, en el historial,
en los favoritos y en los resultados de búsqueda. Es también lo primero que anuncia
un lector de pantalla al cargar la página.

> **⚠️ OJO ACÁ**
> `charset` tiene que ir **arriba de todo**, dentro del primer kilobyte. No es una
> superstición: si el navegador ya empezó a interpretar el documento con la
> codificación equivocada, cuando encuentre tu declaración tiene que descartar todo
> lo que hizo y empezar de nuevo.
>
> Y por si hace falta decirlo: **usá UTF-8 siempre.** Es la única codificación que
> cubre los acentos, la eñe y cualquier otro alfabeto sin sorpresas. Cualquier otra
> elección te va a dar problemas y no te va a dar ninguna ventaja.

---

## 1.9. HTML semántico y el árbol de accesibilidad

### 1.9.1. Por qué la etiqueta correcta no es decoración

Con CSS suficiente, un `<div>` puede verse igual que un `<button>`. Como se ven
igual, es tentador concluir que da lo mismo cuál se use. **No da lo mismo, y la
razón no es estética.**

El navegador construye, además del DOM, una segunda estructura derivada: el **árbol
de accesibilidad**. Es la representación del documento que reciben las tecnologías
de asistencia —lectores de pantalla, navegación por teclado, software de control
por voz—, y en ese árbol cada nodo tiene un **rol**, un **nombre** y un **estado**.
Ese rol sale de la etiqueta.

Un `<button>` llega al árbol de accesibilidad con el rol de botón. Como
consecuencia, y sin que nadie escriba una línea de código: recibe foco al tabular,
se activa con Enter y con la barra espaciadora, un lector de pantalla lo anuncia
como botón, y el software de control por voz responde a la orden "hacé clic en" con
su texto.

Un `<div>` con un manejador de clic no tiene nada de eso. No recibe foco. No
responde al teclado. Un lector de pantalla lo anuncia como texto, si es que lo
anuncia. **Todo ese comportamiento hay que reimplementarlo a mano**, y
reimplementarlo bien es sorprendentemente difícil.

De ahí sale una regla que conviene adoptar sin discutir: **usar el elemento cuyo
significado corresponda a la función, y ajustar la apariencia con CSS.** Es menos
trabajo y funciona mejor.

Los elementos estructurales siguen la misma lógica. `<header>`, `<nav>`, `<main>`,
`<article>`, `<section>`, `<aside>` y `<footer>` no se ven distinto de un `<div>`,
pero producen **puntos de referencia** en el árbol de accesibilidad. Un lector de
pantalla puede saltar directamente al contenido principal si existe un `<main>`;
si todo son `<div>`, el usuario tiene que recorrer el documento entero cada vez.

*(Ver Figura 1.6: el árbol de accesibilidad en las herramientas de desarrollo.)*

### 1.9.2. Formularios

Los formularios concentran la mayor densidad de semántica del HTML, y también la
mayor cantidad de errores.

La pieza central es la asociación entre una etiqueta y su campo. Escribir el texto
al lado del campo no alcanza: hay que vincularlos explícitamente, con el atributo
`for` de la etiqueta apuntando al `id` del campo, o anidando el campo dentro de la
etiqueta.

```html
<label for="email">Correo electrónico</label>
<input type="email" id="email" name="email" required>
```

Esa asociación produce tres efectos. El lector de pantalla anuncia el nombre del
campo al enfocarlo, en lugar de decir simplemente "campo de texto". El clic sobre
la etiqueta lleva el foco al campo, lo que agranda el área de interacción. Y el
mensaje de validación del navegador puede nombrar el campo.

El atributo `type` del campo también hace más de lo que parece: determina el
teclado que aparece en un dispositivo móvil, habilita la validación integrada del
navegador y define qué sugerencias de autocompletado ofrece.

> **⚠️ OJO ACÁ**
> Ahora la parte que más importa, y que el TPI dice con todas las letras en su regla
> **RN-F04**: **la validación del navegador es comodidad, no seguridad.**
>
> El atributo `required` y el `type="email"` le avisan al usuario que se equivocó
> antes de mandar el formulario. Eso está muy bien y hay que ponerlo. Pero cualquiera
> puede desactivarlo desde las herramientas de desarrollo en cinco segundos, o
> directamente mandar la petición sin pasar por tu formulario.
>
> **El servidor tiene que validar todo de nuevo, siempre, sin excepción.** En el TPI
> eso son los esquemas de la sección 7. Si alguna vez pensás "esto ya lo validé en el
> frontend, no hace falta atrás", pará: acabás de abrir un agujero.

---

## 1.10. Estudio de caso: leer la especificación de la API del TPI

Todo lo anterior converge en un ejercicio concreto. La sección 6 del TPI describe
setenta endpoints repartidos en once módulos, y cada uno se especifica con una fila
de tabla. Esta es la primera fila del módulo de autenticación:

| Método | Endpoint | Body / Params | Response | Auth |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/auth/login` | `{ email, password }` | 200 TokenResponse | No — con límite |

A esta altura del capítulo esa fila es completamente legible, y conviene
desarmarla para comprobarlo.

**`POST`** es el método, y por la sección 1.4.2 sabemos que no es seguro ni
idempotente. Que un login sea `POST` y no `GET` no es una convención arbitraria: las
credenciales no pueden viajar en la ruta, porque la ruta queda registrada en logs e
historial.

**`/api/v1/auth/login`** es el componente de ruta del URI de la sección 1.6. El
`v1` es una decisión de diseño de la API: versionar en la ruta permite publicar una
versión nueva sin romper los clientes de la anterior.

**`{ email, password }`** describe el cuerpo, que viaja después de la línea en
blanco de la sección 1.5, en formato JSON declarado por `Content-Type`.

**`200 TokenResponse`** es el código de estado de la familia `2xx` más la forma del
cuerpo de la respuesta, especificada en la sección 7 del TPI. Ese es el contrato que
el Capítulo 6 va a traducir a tipos de TypeScript.

**`No — con límite`** dice que el endpoint no exige autenticación —lógico, es el
que la produce— pero está sujeto al límite de intentos de la sección 4.4, que
responde con el `429` y el `Retry-After` de la sección 1.4.3.

Una sola fila de tabla, y adentro estaban la semántica de los métodos, la anatomía
del URI, la estructura de la petición, las familias de códigos y el manejo del
límite. **La sección 6 completa del TPI son setenta filas como esta.**

> **💡 PARA ENTENDER**
> Este es el punto del capítulo, y quiero que quede claro: **no aprendiste HTTP para
> saber HTTP. Lo aprendiste para poder leer la consigna.**
>
> Cuando en el Capítulo 6 le pidas a un agente de IA que te genere el cliente de la
> API, el agente va a producir código que compila y parece correcto. Vos vas a tener
> que decidir si está bien. Y para decidir eso hace falta saber si ese `POST` lleva
> clave de idempotencia, si distingue un 401 de un 403, y si respeta el
> `Retry-After` de un 429.
>
> El agente escribe rápido. **Vos tenés que saber qué mirar.** Eso es lo que estamos
> construyendo.

---

## 1.11. Herramientas de diagnóstico

El navegador incluye el instrumental necesario para observar todo lo descrito. Se
abre con F12 y las pestañas que importan en este capítulo son cuatro.

**Network / Red** lista todas las peticiones con su método, su código de estado, su
tamaño y su duración. Al seleccionar una se ven sus encabezados de petición y de
respuesta, tal como se describieron en la sección 1.5. Conviene habilitar la opción
de conservar el registro entre navegaciones, porque de lo contrario una redirección
borra la evidencia de lo que se quería observar.

**Elements / Elementos** muestra el DOM actual, con las modificaciones que hayan
hecho los scripts. No muestra el HTML original: para eso está `Ctrl+U`, que pide al
servidor el documento tal como llegó. Comparar ambos es el ejercicio que separa los
dos conceptos de la sección 1.7.1.

**Console / Consola** informa errores de script y permite ejecutar código contra la
página. Se usa a partir del Capítulo 3.

**Accessibility / Accesibilidad**, dentro del panel de elementos, muestra el árbol
de accesibilidad de la sección 1.9: el rol, el nombre y el estado que las
tecnologías de asistencia reciben de cada nodo.

Fuera del navegador, `curl` emite peticiones desde la línea de comandos. Su utilidad
principal es aislar: si una petición funciona con `curl` y no desde la página, el
problema está en el código del cliente y no en el servidor.

```bash
curl -i https://foodstore.example/api/v1/productos
curl -i -X POST https://foodstore.example/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"alguien@example.com","password":"secreto"}'
```

La opción `-i` incluye los encabezados de respuesta en la salida, que es
justamente lo que interesa observar.

*(Ver Figura 1.5: el panel Network de las herramientas de desarrollo.)*

---

## 1.12. Seguridad y evolución del protocolo

El protocolo descrito hasta acá tiene una carencia que en 1991 no se consideró
problema y hoy es inaceptable: **HTTP viaja en texto plano.** Cualquiera con acceso
al camino entre cliente y servidor puede leer el contenido, y también modificarlo
sin que ninguna de las dos partes lo note.

**HTTPS** resuelve las dos cosas envolviendo HTTP en TLS. El protocolo de
aplicación no cambia en absoluto: las mismas peticiones, los mismos encabezados,
los mismos códigos. Lo que cambia es que el canal está cifrado y que el servidor
presenta un certificado que acredita su identidad ante una autoridad reconocida.
Ese certificado autentica al servidor, no al contenido: **HTTPS garantiza con quién
se está hablando y que nadie escuchó, no que lo dicho sea verdad.**

Sobre esa base se agregaron **encabezados de respuesta** que instruyen al navegador
a restringir su propio comportamiento. Son una capa defensiva importante porque
actúan aunque la aplicación tenga errores. El TPI los especifica en su sección
16.5, y los tres principales son:

- **`Strict-Transport-Security`** ordena al navegador usar exclusivamente HTTPS con
  ese dominio durante un período determinado, lo que cierra la ventana de la
  primera visita por HTTP.
- **`Content-Security-Policy`** declara de qué orígenes se admite cargar scripts,
  estilos e imágenes. Es la defensa de fondo contra la ejecución de código
  inyectado, y el Capítulo 4 la retoma al estudiar XSS.
- **`X-Content-Type-Options: nosniff`** impide que el navegador ignore el
  `Content-Type` declarado y trate de deducir el tipo por el contenido, un
  comportamiento heredado que se usó para hacer pasar scripts por imágenes.

En cuanto a las versiones del protocolo, la evolución responde siempre al mismo
problema. **HTTP/1.1**, de 1997, mantiene la conexión abierta entre peticiones pero
las atiende en orden estricto: una petición lenta bloquea a las que están detrás.
**HTTP/2**, de 2015, multiplexa varias peticiones sobre una conexión y comprime los
encabezados. **HTTP/3**, normado en 2022, reemplaza TCP por QUIC, que corre sobre
UDP y elimina el bloqueo de cabecera de línea que persistía en la capa de
transporte.

Lo relevante para este módulo es que **la semántica no cambió en ninguna de las
tres**. Los métodos, los códigos y los encabezados de la sección 1.4 son idénticos
en las tres versiones. Cambió cómo se transportan los bytes, no qué significan.

> **📌 NOTA**
> Que la semántica no haya cambiado en treinta años no es casualidad: es la primera
> decisión de diseño de la sección 1.2 dando frutos.
>
> Y hay algo práctico ahí para vos: casi todo lo que aprendas de HTTP te va a seguir
> sirviendo dentro de diez años. Es de las inversiones más rentables que podés hacer
> en esta carrera. **Las herramientas cambian todo el tiempo; los protocolos, casi
> nunca.**

---

## 1.13. Verificación

Antes de cerrar la clase, cada alumno debe poder completar las siguientes
comprobaciones. No son ejercicios: son el criterio para saber si el capítulo se
entendió.

1. Abrir las herramientas de desarrollo en cualquier sitio, ubicar la petición del
   documento principal y **nombrar tres encabezados de petición y tres de respuesta**
   explicando qué informa cada uno.
2. Provocar deliberadamente un `404` pidiendo una ruta inexistente del mismo sitio, y
   distinguir en el panel de red esa respuesta de un fallo de conexión.
3. Comparar el resultado de `Ctrl+U` con el panel de elementos en un sitio con
   scripts, y **señalar al menos una diferencia** entre ambos.
4. Escribir un documento HTML mínimo con las cinco líneas de cabecera de la sección
   1.8 y explicar por qué está cada una.
5. Recorrer con la tecla Tab un formulario propio y verificar que todos los campos
   reciben foco en un orden razonable.
6. Emitir una petición con `curl -i` y localizar en la salida la línea de estado, los
   encabezados y el cuerpo.
7. Tomar una fila cualquiera de la sección 6 del TPI y **explicar sus cinco columnas**
   como se hizo en la sección 1.10.

---

## 1.14. Errores frecuentes

**Confundir el HTML con el DOM.** Es el error conceptual más extendido y el que más
tiempo hace perder. Se manifiesta cuando alguien busca en el código fuente un
elemento que agregó por programa, no lo encuentra y concluye que su código no
funcionó. El código funcionó: está mirando el lugar equivocado (sección 1.7.1).

**Tratar todos los `4xx` igual.** Enviar al usuario a la pantalla de login ante un
`403` es el caso típico. El usuario ya está autenticado; lo que falta es permiso.
Volver a pedirle la contraseña no cambia nada y lo desconcierta (sección 1.4.3).

**Suponer que la validación del cliente protege el servidor.** Es la regla RN-F04
del TPI, y el error se comete casi siempre por optimización: "esto ya lo validé
antes". La validación del cliente mejora la experiencia y no aporta ninguna
garantía (sección 1.9.2).

**Reintentar un `POST` sin clave de idempotencia.** Ante una respuesta que no
llega, la reacción natural es reintentar. Sin clave de idempotencia eso puede
duplicar un pedido, y el usuario recibe dos veces la misma comida y un cargo doble
(sección 1.4.2).

**Omitir `<meta charset>` o ponerlo tarde.** Produce acentos y eñes partidos, y el
diagnóstico es engañoso porque el archivo se ve bien en el editor: el problema está
en cómo lo interpreta el navegador, no en cómo se guardó (sección 1.8).

**Usar `<div>` con manejador de clic en lugar de `<button>`.** El resultado se ve
idéntico y es inutilizable con teclado o lector de pantalla. Suele descubrirse
tarde, cuando rehacerlo cuesta mucho más (sección 1.9.1).

**Poner datos sensibles en la cadena de consulta.** Quedan en los logs del
servidor, en el historial del navegador y en el encabezado `Referer` de la
navegación siguiente (sección 1.6).

**Creer que HTTPS valida el contenido.** HTTPS acredita la identidad del servidor y
protege el canal. Un sitio con certificado válido puede mentir con total
comodidad (sección 1.12).

---

## 1.15. Actividades

1. **Reconstruir el recorrido.** Elegir un sitio de uso cotidiano, abrir el panel de
   red y documentar las primeras cinco peticiones: método, ruta, código de estado y
   tipo de contenido. Indicar cuáles corresponden al paso 4 de la sección 1.3 y
   cuáles al paso 6.

2. **Clasificar métodos.** Para cada uno de los endpoints de la sección 6.8 del TPI
   —el módulo de pedidos— determinar si el método es seguro, si es idempotente, y
   justificar en una línea si esa clasificación es la adecuada para lo que el
   endpoint hace.

3. **Diagnóstico de códigos.** Redactar, para cada uno de los códigos `400`, `401`,
   `403`, `404`, `409`, `422`, `429` y `500`, una situación concreta del dominio del
   TPI que lo produzca y qué debería hacer el cliente al recibirlo.

4. **Documento semántico.** Escribir la estructura HTML de una página de catálogo de
   productos usando exclusivamente elementos semánticos, sin ningún `<div>`.
   Verificar el resultado en el panel de accesibilidad y anotar qué rol recibió cada
   elemento.

5. **Comparación DOM/HTML.** En un sitio con contenido dinámico, capturar el código
   fuente original y el DOM actual, y señalar tres diferencias explicando el origen
   de cada una. *(Requiere un sitio que cargue contenido por script.)*

6. **Exploración: peticiones sin navegador.** Reproducir con `curl` una petición
   observada en el panel de red, incluyendo sus encabezados, y comparar la respuesta
   obtenida con la que mostró el navegador. Relacionar lo observado con la
   afirmación de la sección 1.4.1 sobre la ausencia de estado: ¿por qué la petición
   funciona igual fuera del navegador? *(Requiere `curl` instalado.)*

7. **Exploración: el costo de la tolerancia.** Escribir deliberadamente un documento
   HTML con errores de marcado —etiquetas sin cerrar, anidación cruzada, atributos
   inventados— y comparar en el panel de elementos el árbol que el navegador
   construyó con el que se esperaba. Relacionar lo observado con la tercera decisión
   de diseño de la sección 1.2 y explicar qué se ganó y qué se perdió con esa
   decisión.

---

## 1.16. Síntesis

1. La web nació para resolver un problema de **recuperación de información
   distribuida sin coordinación central**. Sus cuatro decisiones de diseño
   —identificadores universales, protocolo sin estado, tolerancia al error de
   formato y enlaces sin integridad referencial— explican todo lo observable en
   este módulo, incluidas sus molestias.

2. Las alternativas técnicamente superiores fracasaron porque **exigían
   coordinación**. La web resignó garantías a cambio de escalar, y esa es la clase
   de intercambio que hay que saber identificar en cualquier tecnología.

3. **HTTP no tiene estado.** El servidor no recuerda nada entre peticiones, y por
   eso escala replicándose. La contracara es que cada petición debe traer consigo lo
   necesario para reconstruir el contexto: de ahí el token en cada llamada.

4. La semántica de los métodos no es formalidad. **`POST` no es idempotente**, y de
   esa propiedad —no de una preferencia del enunciado— sale la exigencia de una
   clave de idempotencia en el checkout, que es la regla RN-F07 del TPI.

5. **Un código de estado es información de diagnóstico.** La familia `4xx` dice que
   la petición estaba mal y reintentarla no sirve; `5xx` dice que el servidor falló.
   Y no recibir respuesta no es lo mismo que recibir un `500`: en un caso la
   petición llegó y en el otro no.

6. **El HTML no es el DOM.** El primero es el texto que llegó; el segundo es la
   estructura que el navegador construyó. Todo el trabajo de los capítulos
   siguientes ocurre sobre el segundo.

7. El navegador **nunca rechaza marcado inválido**: lo recupera en silencio. Por eso
   un error de marcado no produce mensaje de error, y por eso ninguna validación del
   cliente constituye una garantía.

8. **La etiqueta correcta no es decoración**: determina el rol en el árbol de
   accesibilidad, y con él el comportamiento de teclado, foco y lectores de
   pantalla. Un `<div>` estilizado como botón obliga a reimplementar a mano todo lo
   que `<button>` trae gratis.

9. **HTTPS acredita identidad y protege el canal; no valida contenido.** Los
   encabezados de seguridad agregan una capa que actúa aunque la aplicación tenga
   errores.

10. La **semántica de HTTP no cambió en treinta años** pese a tres versiones del
    transporte. Lo aprendido acá sigue siendo válido mucho después de que las
    herramientas de moda hayan sido reemplazadas.

---

## 1.17. Referencias y lecturas complementarias

Las fuentes normativas del protocolo son las RFC del IETF, de acceso libre en
`rfc-editor.org`. La especificación vigente de HTTP es la **RFC 9110** (*HTTP
Semantics*, 2022), que reemplazó a la conocida RFC 2616 y define los métodos, los
códigos de estado y la clasificación de seguridad e idempotencia usada en la
sección 1.4.2; la acompañan la **RFC 9111** sobre caché y la **RFC 9112** sobre la
sintaxis de HTTP/1.1. Las versiones posteriores del transporte están en la **RFC
9113** (HTTP/2) y la **RFC 9114** (HTTP/3), esta última sobre el protocolo QUIC de
la **RFC 9000**. La sintaxis del identificador uniforme de recurso descrita en la
sección 1.6 corresponde a la **RFC 3986**. Para el contexto histórico, la **RFC
1945** documenta HTTP/1.0 tal como se usaba de hecho en 1996, y su lectura muestra
con claridad qué problemas motivaron la versión siguiente.

La especificación de HTML no es una RFC sino un estándar viviente mantenido por el
WHATWG, disponible en `html.spec.whatwg.org`; sus secciones sobre el algoritmo de
parseo documentan las reglas de recuperación de errores mencionadas en la sección
1.7.1. Las pautas de accesibilidad son las **WCAG 2.2** del W3C, y la
especificación **WAI-ARIA** define el modelo de roles, nombres y estados del árbol
de accesibilidad de la sección 1.9.

Como bibliografía de estudio, el capítulo de capa de aplicación de Kurose y Ross,
*Computer Networking: A Top-Down Approach* (8.ª edición, Pearson, 2021) presenta
HTTP con el mismo enfoque descendente de este capítulo y es la referencia más
accesible para quien viene de programación y no de redes. Para el detalle
operativo del protocolo, Grigorik, *High Performance Browser Networking*
(O'Reilly, 2013, de lectura libre en `hpbn.co`) explica el recorrido completo de
una petición y las razones de rendimiento detrás de cada versión del protocolo.
Sobre el diseño del navegador, Garsiel y Irish, *How Browsers Work* (2011)
describe el pipeline de renderizado de la sección 1.7 con más profundidad que
cualquier documentación de producto. Y para la historia del proyecto, el relato de
su autor en Berners-Lee, *Weaving the Web* (Harper, 1999) documenta de primera mano
las decisiones de diseño de la sección 1.2 y las alternativas que se
descartaron.

---

**Continúa en:** Capítulo 2 — CSS: el modelo de caja, el flujo y la cascada, donde
se estudia cómo el navegador decide el aspecto de cada nodo del DOM construido en
la sección 1.7, y se introduce Tailwind, la herramienta de estilos que el TPI
declara en su stack.
