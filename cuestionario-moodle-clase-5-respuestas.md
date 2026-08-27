# Clave de corrección — Cuestionario Clase 5 (Red interna y prácticas de desarrollo)

> **Documento del docente. No publicar en el aula.**
> Estas son las respuestas de las 31 preguntas de `cuestionario-moodle-clase-5.xml`.
> Se genera desde la misma fuente que el XML, así que si el banco cambia, esta clave cambia con él.

- **Cuestionario:** `Clase 5 - Autoevaluación: red interna, persistencia e integración continua`
- **Curso:** campustest.frm.utn.edu.ar → curso 14 → sección 30 «Actividades 🧩»
- **31 preguntas** en 13 páginas · 1 punto cada una, escaladas a 10
- El orden de abajo es el **orden real del cuestionario** (paginación de `cuestionario-moodle-clase-5.md` §3.1)

En Moodle el alumno ve todo esto solo: cada opción incorrecta tiene su propia explicación. Esta clave sirve para revisar el banco antes de publicarlo y para tener las respuestas a mano en clase.

---

## Resumen

| # | Pág | Tipo | Respuesta correcta | Apunte |
|---|---|---|---|---|
| **C5-01** | 1 | Opción múltiple | Que un contenedor que hoy es 172.17.0.3 puede ser 172.17.0.5 mañana: escribir esa direcci… | §5.2 |
| **C5-06** | 1 | Opción múltiple | El aislamiento entre proyectos: dos proyectos en el mismo VPS no se ven entre sí, aunque… | §2.8, §5.4.2 |
| **C5-04** | 2 | Opción múltiple | No pueden: el frontend no se ejecuta en el servidor. El servidor solo entrega el archivo;… | §5.3 |
| **C5-05** | 2 | Múltiples correctas | La API llamando a la base de datos + La API llamando a una caché o una cola de mensajes + La API llamando a otro microservicio del mismo proyecto | §5.3.1 |
| **C5-31** | 3 | Verdadero/Falso | **FALSO** | §5.2, §5.5 |
| **C5-03** | 3 | Respuesta corta | `calculadora_db` | §5.4.1 |
| **C5-02** | 4 | Emparejar | _(emparejamiento — ver detalle)_ | §5.2 |
| **C5-07** | 5 | Opción múltiple | Nada y ninguno: deliberadamente vacío | §2.8.3, §5.5 |
| **C5-08** | 5 | Opción múltiple | El host es un nombre interno que solo existe en esa red, y el puerto 5432 es interno: no… | §3.7.2, §5.5.1 |
| **C5-09** | 6 | Opción múltiple | Degradación elegante: ante la falla de un componente el sistema no deja de funcionar, sin… | §5.6.1 |
| **C5-10** | 6 | Opción múltiple | Porque 503 afirma «el servicio existe, sé lo que me pedís, y no puedo dártelo ahora porqu… | §5.6.2 |
| **C5-11** | 6 | Opción múltiple | Porque un health check que solo dice «estoy vivo» sirve de poco: el que sirve es el que i… | §5.6.2 |
| **C5-12** | 6 | Opción múltiple | Análisis de dependencias: la base no es crítica —es un registro de lo que ya se hizo— y t… | §5.6.3 |
| **C5-13** | 7 | Opción múltiple | Marcadores de posición del controlador: la consulta y los valores viajan por separado y e… | §5.6.4 |
| **C5-14** | 8 | Opción múltiple | Que la base atiende consultas de la API por la red interna y es simultáneamente inalcanza… | §2.8.2, §5.7.2 |
| **C5-15** | 9 | Opción múltiple | Porque todo lo que un contenedor escribe va a su capa efímera, que se descarta al elimina… | §5.7.3 |
| **C5-16** | 9 | Emparejar | _(emparejamiento — ver detalle)_ | §5.7.3 |
| **C5-17** | 10 | Opción múltiple | No: queda en el historial y es recuperable por cualquiera que clone. La única respuesta c… | §5.8.1 |
| **C5-18** | 10 | Opción múltiple | Porque deciden cosas distintas: uno qué entra al control de versiones y el otro qué se en… | §5.8.1 |
| **C5-19** | 10 | Opción múltiple | Porque cada paquete instalado en la imagen de producción es peso y superficie de vulnerab… | §5.8.3 |
| **C5-20** | 11 | Opción múltiple | Que si integrar el trabajo de varias personas es doloroso, la respuesta no es integrar me… | §3.2, §5.9 |
| **C5-21** | 11 | Opción múltiple | Porque una advertencia que se puede ignorar se ignora, sobre todo bajo presión de entrega… | §5.9.1 |
| **C5-22** | 11 | Opción múltiple | Entrega continua: todo cambio integrado queda listo para desplegar y el despliegue lo dis… | §5.9.2 |
| **C5-23** | 11 | Opción múltiple | Porque conectar el despliegue automático sin pruebas corriendo solo automatiza la llegada… | §5.9.2 |
| **C5-24** | 12 | Opción múltiple | Las copias de seguridad: desde que existe la base, una pérdida de datos es definitiva | §5.10 |
| **C5-30** | 12 | Opción múltiple | Un nombre estable delante de algo inestable: el DNS lo hizo para internet en 1983, Docker… | §5.2 |
| **C5-25** | 13 | Opción múltiple | El nombre de host interno está mal escrito en la cadena de conexión | §5.12 |
| **C5-26** | 13 | Opción múltiple | Redesplegar: las variables se leen al arrancar el proceso | §5.12 |
| **C5-27** | 13 | Opción múltiple | El servicio db no tiene volumen: todo se está escribiendo en la capa efímera del contened… | §5.7.3, §5.12 |
| **C5-28** | 13 | Opción múltiple | No: es el comportamiento esperado. Son redes distintas, y ese aislamiento es la propiedad… | §5.4.2, §5.12 |
| **C5-29** | 13 | Opción múltiple | Hay una dependencia instalada solo localmente que nadie declaró en los archivos de requis… | §3.2, §5.9, §5.12 |

## Cobertura del capítulo

| Sección del apunte | Preguntas que la evalúan |
|---|---|
| §2.8 | C5-06 |
| §2.8.2 | C5-14 |
| §2.8.3 | C5-07 |
| §3.2 | C5-20, C5-29 |
| §3.7.2 | C5-08 |
| §5.2 | C5-01, C5-02, C5-30, C5-31 |
| §5.3 | C5-04 |
| §5.3.1 | C5-05 |
| §5.4.1 | C5-03 |
| §5.4.2 | C5-06, C5-28 |
| §5.5 | C5-07, C5-31 |
| §5.5.1 | C5-08 |
| §5.6.1 | C5-09 |
| §5.6.2 | C5-10, C5-11 |
| §5.6.3 | C5-12 |
| §5.6.4 | C5-13 |
| §5.7.2 | C5-14 |
| §5.7.3 | C5-15, C5-16, C5-27 |
| §5.8.1 | C5-17, C5-18 |
| §5.8.3 | C5-19 |
| §5.9 | C5-20, C5-29 |
| §5.9.1 | C5-21 |
| §5.9.2 | C5-22, C5-23 |
| §5.10 | C5-24 |
| §5.12 | C5-25, C5-26, C5-27, C5-28, C5-29 |

---

## Detalle por página

### Página 1 — Por qué existe la red interna

#### C5-01 · El problema que resuelve la red interna

*Opción múltiple*

Cada contenedor tiene su propia dirección IP, asignada del rango privado en el orden en que arrancan. ¿Qué problema crea eso?

- **✅** Que un contenedor que hoy es 172.17.0.3 puede ser 172.17.0.5 mañana: escribir esa dirección en un archivo de configuración garantiza que el sistema se rompa sin que nadie lo toque
  - <sub>Correcto. El aislamiento resuelve un problema y crea inmediatamente otro: si cada contenedor tiene su propia dirección y esa dirección cambia, ¿cómo hace uno para encontrar a otro?</sub>
- ❌ Que las direcciones privadas no son alcanzables desde internet
  - <sub>Eso no es un problema: **es la propiedad buscada**. El problema es la inestabilidad, no la privacidad.</sub>
- ❌ Que se agotan las direcciones disponibles con pocos contenedores
  - <sub>El rango `172.17.0.0/16` da más de 65.000 direcciones. La escasez no es el problema.</sub>
- ❌ Que dos contenedores pueden recibir la misma dirección y colisionar
  - <sub>Docker no asigna duplicados. El problema es que la dirección de *uno* cambia entre reinicios.</sub>

> **Por qué.** Fijate que es literalmente el mismo problema del capítulo 1, un piso más abajo: hay una dirección que cambia y un nombre que no. **Docker resolvió adentro de un servidor el mismo problema que el DNS resolvió para internet entera, con la misma solución, cuarenta años después.** *(Apunte §5.2)*

#### C5-06 · Qué se gana con la red interna

*Opción múltiple*

¿Cuál de estas ventajas de la red interna es la que la convierte en un mecanismo de **seguridad** y no solo de conectividad?

- **✅** El aislamiento entre proyectos: dos proyectos en el mismo VPS no se ven entre sí, aunque compartan servidor, núcleo y motor de Docker
  - <sub>Correcto: es el principio de mínimo privilegio (§2.12.1) aplicado a la topología de red.</sub>
- ❌ La menor latencia, porque el tráfico no sale del servidor
  - <sub>Es una ventaja real, pero de rendimiento.</sub>
- ❌ Que no consume tráfico público, relevante en planes con cuota
  - <sub>También rendimiento y costo, no seguridad.</sub>
- ❌ Que no pasa por Traefik, evitando la sobrecarga del proxy y de TLS
  - <sub>Ventaja de rendimiento. Que no haya TLS entre contenedores de la misma red es aceptable justamente porque esa red es un límite de alcance.</sub>

> **Por qué.** Volvé a §2.8, la de Docker salteándose el firewall. **La red interna no resuelve ese problema: lo elimina.** Un puerto que nunca se publicó no puede quedar mal protegido, porque no hay nada que proteger. Es la diferencia entre poner un candado bueno y no tener puerta. *(Apunte §5.4.2)*

---

### Página 2 — Quién ejecuta el código

#### C5-04 · Quién ejecuta el código

*Opción múltiple*

«Si el frontend y la API están en el mismo servidor, ¿por qué la API tiene que estar publicada en internet? ¿No podrían hablarse por adentro?»

- **✅** No pueden: el frontend **no se ejecuta en el servidor**. El servidor solo entrega el archivo; el código corre en el navegador del visitante, que no está en la red interna
  - <sub>Exacto. Cuando un visitante en Córdoba abre la calculadora, el `fetch` se ejecuta en su máquina. El DNS embebido solo responde a quien está dentro de la red, y el navegador del visitante está a mil kilómetros.</sub>
- ❌ Podrían, pero Easypanel no lo permite por razones de seguridad
  - <sub>No es una restricción de Easypanel: es físicamente imposible. No hay configuración que lo arregle.</sub>
- ❌ No pueden porque están en proyectos distintos de Easypanel
  - <sub>Están en el mismo proyecto. El problema no es la red del servidor: es que el frontend no corre en el servidor.</sub>
- ❌ Podrían si el frontend usara el nombre interno en lugar del dominio público
  - <sub>El navegador del visitante no puede resolver `calculadora_api`: ese nombre no existe fuera de la red del proyecto.</sub>

> **Por qué.** **Grabate esta pregunta, porque sirve para toda tu carrera: ¿quién ejecuta este código?** Si la respuesta es «el navegador del usuario», está afuera, no confíes en él, y todo lo que necesite tiene que ser público. Si es «un proceso mío en el servidor», está adentro, y ahí sí podés usar la red interna. *(Apunte §5.3)*

#### C5-05 · Cuándo aplica la red interna

*Múltiples correctas*

¿En cuáles de estos casos **sí** corresponde usar la red interna? (marcá todas las que correspondan)

- **✅** La API llamando a la base de datos
  - <sub>Sí: los dos extremos son procesos del servidor.</sub>
- **✅** La API llamando a una caché o una cola de mensajes
  - <sub>Sí: mismo caso, ambos adentro.</sub>
- **✅** La API llamando a otro microservicio del mismo proyecto
  - <sub>Sí: ambos son procesos del servidor y comparten la red.</sub>
- ❌ El navegador del visitante llamando a la API
  - <sub>No: requiere dominio público. El navegador está afuera y no hay forma de que esté adentro.</sub>

> **Por qué.** La regla es simple y no tiene excepciones: la red interna aplica **cuando ambos extremos son procesos del servidor**. *(Apunte §5.3.1)*

---

### Página 3 — Publicar y comunicar

#### C5-31 · Publicar un puerto y comunicarse por la red interna

*Verdadero/Falso*

Para que la API pueda conectarse a la base de datos, el servicio `db` tiene que publicar el puerto 5432.

- ❌ **Verdadero**
- **✅** **Falso**

> **Por qué.** **Falso.** La comunicación entre contenedores de una misma red **no requiere publicar nada**: el mapeo `-p` sirve exclusivamente para exponer un servicio hacia afuera del anfitrión. Son dos mecanismos distintos y ortogonales que se suelen confundir — y de esa confusión salen la mitad de las bases de datos expuestas a internet del mundo. *(Apunte §5.2 y §5.5)*

#### C5-03 · El nombre interno del servicio

*Respuesta corta*

El proyecto se llama `calculadora` y el servicio de base de datos se llama `db`. ¿Qué nombre hay que poner como *host* en la cadena de conexión? (escribilo tal cual)

Respuestas aceptadas (sin distinguir mayúsculas): `calculadora_db`

> **Por qué.** El formato es `<nombre_del_proyecto>_<nombre_del_servicio>`. Ese nombre **solo existe dentro de esa red**: no es un dominio, no está en ninguna zona DNS pública, y consultarlo desde afuera no devuelve nada. Que no resuelva no es una limitación: es la propiedad buscada. *(Apunte §5.4.1)*

---

### Página 4 — Las decisiones de diseño

#### C5-02 · Las tres decisiones del modelo de red

*Emparejar*

Emparejá cada decisión de diseño del modelo de red actual de Docker con su consecuencia.

| Se empareja | Con |
|---|---|
| **Redes definidas por el usuario** | La red deja de ser conectividad y pasa a ser un límite de alcance: una frontera de seguridad |
| **Descubrimiento de servicios por DNS** | Un servidor DNS embebido en 127.0.0.11 resuelve nombres estables a direcciones cambiantes |
| **Publicar un puerto es opcional y ortogonal** | La comunicación entre contenedores de una red no requiere publicar nada: -p es solo para exponer hacia afuera |

> **Por qué.** De la confusión entre los dos mecanismos de la tercera fila salen **la mitad de las bases de datos expuestas a internet del mundo**. El mecanismo anterior, los enlaces (`--link`) de 2014, está formalmente obsoleto: era unidireccional y estático. *(Apunte §5.2)*

---

### Página 5 — La base de datos

#### C5-07 · Cómo se configura el servicio de base de datos

*Opción múltiple*

Al crear el servicio `db` de PostgreSQL, ¿qué se carga en «Domains & Proxy» y qué puerto se publica?

- **✅** Nada y ninguno: deliberadamente vacío
  - <sub>Correcto, y esas dos filas son el contenido de la clase. Un servicio sin dominio y sin puerto publicado es, desde afuera, **inexistente**: no hay enrutador de Traefik que lo alcance (§4.8.1) ni regla de traducción de direcciones que lo exponga (§2.8.1). Y sin embargo funciona perfectamente para quien lo necesita.</sub>
- ❌ Un subdominio `db.tudominio.com` y el puerto 5432
  - <sub>Eso lo dejaría accesible desde internet. Un PostgreSQL expuesto lo encuentran los escáneres automáticos en cuestión de horas (§2.9.1).</sub>
- ❌ Ningún dominio, pero sí el puerto 5432 para poder administrarlo
  - <sub>Publicar el puerto ya lo expone: recordá que ufw no protege los puertos publicados por Docker (§2.8.1).</sub>
- ❌ Un dominio interno terminado en `.local`
  - <sub>El nombre interno no es un dominio ni lleva sufijo: es `proyecto_servicio`, y lo resuelve el DNS embebido.</sub>

> **Por qué.** Si necesitás inspeccionar la base con una herramienta de escritorio, se hace por un **túnel SSH**: `ssh -L 5432:calculadora_db:5432 root@tudominio.com`. Eso hace pasar la conexión por el canal cifrado de SSH, ya autenticado por clave, sin abrir nada nuevo. Es la segunda estrategia de la tabla de §2.8.3. *(Apunte §5.5)*

#### C5-08 · La cadena de conexión

*Opción múltiple*

En `DATABASE_URL=postgres://usuario:clave@calculadora_db:5432/calculadora`, ¿qué hay que notar sobre el host y el puerto?

- **✅** El host es un nombre interno que solo existe en esa red, y el puerto 5432 es interno: no está publicado
  - <sub>Correcto. Si escribís `calculadora_db` en el navegador no resuelve, y **está bien que no resuelva**: esa es exactamente la propiedad que queremos.</sub>
- ❌ El host debe ser el dominio público del servicio de base de datos
  - <sub>El servicio de base de datos no tiene dominio público, y no debe tenerlo.</sub>
- ❌ El puerto 5432 tiene que abrirse en ufw para que la API pueda conectarse
  - <sub>ufw filtra tráfico que *entra al servidor*. La comunicación entre contenedores de la misma red no pasa por ahí.</sub>
- ❌ El host puede ser la IP del contenedor, que es más rápida de resolver
  - <sub>Es exactamente lo que hay que evitar: esa IP cambia entre redespliegues. Para eso existe el nombre.</sub>

> **Por qué.** Esta cadena es también un buen ejemplo del principio de configuración de §3.7.2: la misma imagen del backend funciona con base de datos y sin ella, en la notebook y en producción, y lo único que cambia es una variable. *(Apunte §5.5.1)*

---

### Página 6 — Degradación elegante

#### C5-09 · Degradación elegante

*Opción múltiple*

La API está diseñada para que `DATABASE_URL` sea **opcional**: sin ella funciona igual, solo que sin historial. ¿Cómo se llama ese patrón y por qué se eligió?

- **✅** Degradación elegante: ante la falla de un componente el sistema no deja de funcionar, sino que reduce su funcionalidad de forma controlada y previsible
  - <sub>Correcto. Su contrario es el **fallo en cascada**, en el que la caída de una dependencia secundaria arrastra al servicio entero.</sub>
- ❌ Tolerancia a fallos por redundancia: se replica la base para que nunca falte
  - <sub>No hay réplica: hay una funcionalidad que se apaga sola cuando su dependencia no está.</sub>
- ❌ Inyección de dependencias: la base se pasa como parámetro configurable
  - <sub>La inyección de dependencias es un patrón de diseño de código, no de comportamiento ante fallas.</sub>
- ❌ Arranque perezoso: la conexión se establece solo cuando se necesita
  - <sub>Eso describe *cuándo* se conecta, no qué pasa si no puede.</sub>

> **Por qué.** Tres razones concretas: el desarrollo local no necesita levantar un Postgres para tocar una línea; las Clases 1 a 4 siguen siendo válidas y el despliegue de la semana pasada no se rompe; y es el patrón correcto. **Si la base se cae, la calculadora tiene que seguir calculando.** *(Apunte §5.6.1)*

#### C5-10 · Por qué 503 y no 500

*Opción múltiple*

Sin base de datos, `/api/historial` devuelve **503**. ¿Por qué ese código y no 500?

- **✅** Porque 503 afirma «el servicio existe, sé lo que me pedís, y no puedo dártelo ahora porque una dependencia no está disponible» — y eso es verdad; 500 afirma «algo se rompió y no sé qué», que no lo es
  - <sub>Correcto. Un cliente que recibe 503 sabe que tiene sentido reintentar más tarde; uno que recibe 500 no sabe nada. **El código de estado debe decir la verdad.**</sub>
- ❌ Porque 500 está reservado para errores de sintaxis del servidor
  - <sub>500 es el error genérico de servidor: cubre cualquier fallo inesperado, no solo de sintaxis.</sub>
- ❌ Porque 503 hace que el navegador reintente automáticamente
  - <sub>El navegador no reintenta solo. Lo que cambia es la *información* que recibe quien consume la API.</sub>
- ❌ Porque 500 dispararía una alerta en el monitoreo y 503 no
  - <sub>Los dos deberían monitorearse. La diferencia es semántica, no operativa.</sub>

> **Por qué.** La diferencia entre familias de códigos es **información de diagnóstico**. Es el mismo criterio que en la Clase 1 separaba NXDOMAIN de un timeout. *(Apunte §5.6.2)*

#### C5-11 · Un health check útil

*Opción múltiple*

El control de salud pasa a devolver `{"estado":"ok","persistencia":true}` en lugar de solo `{"estado":"ok"}`. ¿Por qué importa?

- **✅** Porque un health check que solo dice «estoy vivo» sirve de poco: el que sirve es el que informa de qué depende y cómo está cada dependencia
  - <sub>Correcto. Cuando tengas monitoreo, esa es la URL que se consulta cada treinta segundos.</sub>
- ❌ Porque permite al frontend ocultar el botón de historial
  - <sub>Podría usarse para eso, pero no es la razón por la que la práctica es estándar.</sub>
- ❌ Porque Easypanel lo usa para decidir si reinicia el contenedor
  - <sub>Si el health check fallara por la base, Easypanel reiniciaría un servicio que está sano. Justamente por eso `estado` sigue en `ok`.</sub>
- ❌ Porque es un requisito del protocolo HTTP para los endpoints de estado
  - <sub>HTTP no define ningún endpoint de estado: es una convención de la industria.</sub>

> **Por qué.** *(Apunte §5.6.2)*

#### C5-12 · Por qué el guardado no puede tumbar el cálculo

*Opción múltiple*

Si la base no está disponible, la operación se calcula, se responde correctamente y el fallo queda en el log. ¿Cuál es el razonamiento?

- **✅** Análisis de dependencias: la base no es crítica —es un registro de lo que ya se hizo— y tratarla como crítica ataría la disponibilidad del servicio principal a la del secundario
  - <sub>Correcto. **Una funcionalidad secundaria nunca puede romper la principal.** Guardar el historial es secundario; calcular es lo que la aplicación hace.</sub>
- ❌ Que los errores de base de datos son siempre transitorios y no vale la pena reportarlos
  - <sub>No son siempre transitorios, y sí se reportan: quedan en el log del servidor.</sub>
- ❌ Que el usuario no debe enterarse nunca de los errores internos
  - <sub>No es ocultamiento: es que ese fallo *no afecta* lo que el usuario pidió.</sub>
- ❌ Que FastAPI captura automáticamente las excepciones de la capa de datos
  - <sub>No las captura solo: es una decisión explícita de cómo se escribió el código.</sub>

> **Por qué.** Es un criterio de diseño que vale para todo lo que hagas de acá en adelante. Si por no poder guardar una fila la calculadora deja de calcular, el diseño está mal. *(Apunte §5.6.3)*

---

### Página 7 — Inyección SQL

#### C5-13 · Consultas parametrizadas

*Opción múltiple*

En `cur.execute("INSERT ... VALUES (%s, %s)", (a, b))`, ¿qué son esos `%s`?

- **✅** Marcadores de posición del controlador: la consulta y los valores viajan por separado y el motor los trata como datos, jamás como instrucciones
  - <sub>Correcto, y es el detalle que casi siempre se malinterpreta: **no son formato de cadena de Python**. No se reemplazan por texto antes de enviar nada.</sub>
- ❌ Formato de cadena de Python, equivalente a usar el operador %
  - <sub>Parece equivalente y **es un agujero de seguridad**: ahí el valor sí se mezcla con la instrucción antes de salir, y quien controle el valor controla la consulta.</sub>
- ❌ Comodines de SQL que el motor expande según el tipo de dato
  - <sub>SQL no tiene esa sintaxis. Los marcadores los define el controlador (psycopg, en este caso).</sub>
- ❌ Placeholders opcionales: escribir una f-string produce el mismo resultado
  - <sub>Produce el mismo resultado *cuando los datos son inocentes*. Con un valor hostil, produce una inyección.</sub>

> **Por qué.** Esa clase de falla se llama **inyección** y encabeza desde hace veinte años todas las listas de vulnerabilidades más frecuentes. No es exótica: es la más común y la más barata de evitar. Cuando escribas SQL, mirá qué separa los datos de la instrucción: si el valor se pegó al texto con un `+`, un `%` o un `f"..."`, eso es inyección esperando a alguien que la encuentre. *(Apunte §5.6.4)*

---

### Página 8 — La verificación del aislamiento

#### C5-14 · La verificación central de la clase

*Opción múltiple*

El historial funciona perfecto en el navegador y al mismo tiempo `nmap -Pn -p 5432 tudominio.com` informa el puerto cerrado o filtrado. ¿Qué demuestra eso?

- **✅** Que la base atiende consultas de la API por la red interna y es simultáneamente inalcanzable desde internet: ambas afirmaciones son ciertas al mismo tiempo
  - <sub>Correcto, y si de toda la clase te llevás una sola imagen, que sea esta: las dos ventanas lado a lado.</sub>
- ❌ Que nmap no puede detectar puertos protegidos por Docker
  - <sub>nmap detecta perfectamente los puertos publicados por Docker — ese fue todo el problema de §2.8. Acá está cerrado porque **nunca se publicó**.</sub>
- ❌ Que el firewall está filtrando correctamente el puerto 5432
  - <sub>El firewall no tiene nada que filtrar: no hay ningún proceso publicado en ese puerto hacia afuera.</sub>
- ❌ Que la API está usando una base de datos externa, no la del proyecto
  - <sub>Usa la del proyecto, alcanzándola por su nombre interno.</sub>

> **Por qué.** Esta verificación es del mismo tipo que la de §2.8.2 y por el mismo motivo: es la **única que constituye evidencia externa**. Cualquier comprobación hecha desde adentro del servidor describiría intenciones. *(Apunte §5.7.2)*

---

### Página 9 — Estado y persistencia

#### C5-15 · Por qué la base necesita un volumen

*Opción múltiple*

Sin volumen, cada redespliegue vaciaría la base. ¿Por qué?

- **✅** Porque todo lo que un contenedor escribe va a su capa efímera, que se descarta al eliminarlo; un volumen es un punto del árbol que no pertenece a esa capa
  - <sub>Correcto: la razón está en el modelo de §3.3.2. El volumen es almacenamiento gestionado por Docker que existe fuera del sistema de archivos del contenedor y sobrevive a su destrucción.</sub>
- ❌ Porque PostgreSQL borra sus datos al recibir SIGTERM
  - <sub>PostgreSQL cierra ordenadamente y conserva todo. El problema es dónde estaba escribiendo.</sub>
- ❌ Porque Easypanel recrea la base de datos en cada despliegue
  - <sub>Easypanel no toca los datos: recrea el *contenedor*.</sub>
- ❌ Porque la imagen de PostgreSQL no incluye almacenamiento persistente
  - <sub>Ninguna imagen lo incluye: las imágenes son inmutables por definición.</sub>

> **Por qué.** De ahí sale la distinción entre servicios **sin estado** (api, web: se destruyen y recrean sin consecuencias, lo importante vive en el repositorio) y **con estado** (db: no sin perder datos, lo importante vive en el volumen). *(Apunte §5.7.3)*

#### C5-16 · Servicios con estado y sin estado

*Emparejar*

Emparejá cada afirmación con el tipo de servicio que describe.

| Se empareja | Con |
|---|---|
| **Se puede destruir y recrear sin consecuencias** | Sin estado (api, web) |
| **Se puede escalar a varias copias trivialmente** | Sin estado (api, web) |
| **No se puede recrear sin perder datos** | Con estado (db) |
| **Lo importante vive en un volumen, no en el repositorio** | Con estado (db) |

> **Por qué.** La regla operativa la enuncia la metodología de los doce factores como **procesos sin estado**: la aplicación no guarda nada localmente y todo el estado vive en servicios de respaldo declarados como dependencias. Eso es lo que permite redesplegar la API veinte veces por día sin ninguna consecuencia. Y ahora pensá lo que implica: **a partir del momento en que hay un volumen con datos, existe algo que se puede perder.** Ahí las copias de seguridad dejan de ser un tema teórico. *(Apunte §5.7.3)*

---

### Página 10 — Prácticas de repositorio

#### C5-17 · Un secreto versionado por error

*Opción múltiple*

Alguien subió una contraseña al repositorio y en el commit siguiente la borró. ¿Alcanza?

- **✅** No: queda en el historial y es recuperable por cualquiera que clone. La única respuesta correcta es **rotar la credencial**
  - <sub>Correcto. Es el mismo fenómeno que las capas de Docker (§3.3.2): un artefacto inmutable y encadenado no se edita, se tapa. Reescribir el historial es un parche, no una solución.</sub>
- ❌ Sí, si el repositorio es privado y solo lo ven los integrantes del grupo
  - <sub>Un repositorio privado hoy puede volverse público mañana, y cualquier integrante que ya clonó tiene el historial completo.</sub>
- ❌ Sí, siempre que se haga un force push para reescribir el historial
  - <sub>Reescribir el historial es un parche: los clones existentes lo conservan, y los servicios que lo indexaron también.</sub>
- ❌ No hace falta hacer nada si la contraseña era de un entorno de prueba
  - <sub>Los entornos de prueba suelen compartir credenciales con producción más de lo que nadie admite. Se rota igual.</sub>

> **Por qué.** Un secreto que salió de tu máquina es un secreto quemado. *(Apunte §5.8.1)*

#### C5-18 · .gitignore y .dockerignore

*Opción múltiple*

¿Por qué son dos archivos distintos y no uno solo?

- **✅** Porque deciden cosas distintas: uno qué entra al control de versiones y el otro qué se envía al contexto de construcción. Un archivo puede estar bien excluido de uno y filtrarse por el otro
  - <sub>Correcto, y esa última frase es la que importa: son dos superficies de filtración independientes.</sub>
- ❌ Porque Git y Docker usan sintaxis de patrones incompatibles
  - <sub>La sintaxis es muy parecida. El motivo es de propósito, no de formato.</sub>
- ❌ Porque el .dockerignore es opcional y el .gitignore obligatorio
  - <sub>Los dos son opcionales técnicamente, y los dos hacen falta en la práctica.</sub>
- ❌ Porque el .dockerignore solo funciona en el directorio raíz del repositorio
  - <sub>Ubicación aparte, eso no explica por qué no podrían unificarse.</sub>

> **Por qué.** Ojo con un detalle del proyecto: hasta esta clase el `.gitignore` estaba en el directorio superior, **que no es un repositorio**. O sea: no protegía nada. Que no haya basura versionada es casualidad, no diseño. *(Apunte §5.8.1)*

#### C5-19 · Separación de dependencias

*Opción múltiple*

¿Por qué conviene separar `requirements-dev.txt` de `requirements.txt`?

- **✅** Porque cada paquete instalado en la imagen de producción es peso y superficie de vulnerabilidades heredada: una herramienta de pruebas no tiene razón para correr en un servidor expuesto
  - <sub>Correcto, y es exactamente el mismo argumento con que se eligió la imagen base en §3.5.1. No es solo prolijidad.</sub>
- ❌ Porque pytest entra en conflicto con uvicorn en tiempo de ejecución
  - <sub>No hay conflicto: simplemente no hace falta que esté.</sub>
- ❌ Porque así la construcción de la imagen es más rápida
  - <sub>Es un efecto secundario menor. El argumento del capítulo es de superficie de ataque.</sub>
- ❌ Porque GitHub Actions solo lee archivos que terminan en -dev.txt
  - <sub>Lee cualquier archivo que se le indique en el flujo.</sub>

> **Por qué.** *(Apunte §5.8.3)*

---

### Página 11 — Integración continua

#### C5-20 · Por qué integración continua

*Opción múltiple*

La integración continua se formuló en los años noventa con una premisa contraintuitiva para la época. ¿Cuál?

- **✅** Que si integrar el trabajo de varias personas es doloroso, la respuesta no es integrar menos seguido sino mucho más seguido, en fragmentos chicos y con verificación automática
  - <sub>Correcto: el dolor de integrar crece con el tamaño del cambio; achicando el cambio, desaparece.</sub>
- ❌ Que las pruebas debían escribirse después del código para no condicionar el diseño
  - <sub>Es casi lo opuesto a lo que propone la programación extrema, de donde viene la práctica.</sub>
- ❌ Que cada equipo debía tener su propia rama de larga duración
  - <sub>Las ramas de larga duración son justamente lo que la integración continua busca evitar.</sub>
- ❌ Que la integración debía hacerla una persona dedicada a tiempo completo
  - <sub>La propuesta es automatizarla, no asignarle una persona.</sub>

> **Por qué.** Un beneficio adicional que suele pasarse por alto: el flujo instala las dependencias en una **máquina limpia**, distinta de la de cualquier integrante. Eso detecta las dependencias que alguien tiene instaladas localmente y se olvidó de declarar — el mismo problema que motivó los contenedores en §3.2. *(Apunte §5.9)*

#### C5-21 · Informar contra bloquear

*Opción múltiple*

La acción de GitHub por sí sola ejecuta las pruebas y muestra el resultado, pero no impide nada. ¿Por qué hace falta además la regla de protección de rama?

- **✅** Porque una advertencia que se puede ignorar se ignora, sobre todo bajo presión de entrega, que es precisamente cuando más falta hace. Un control que bloquea no depende de la disciplina de nadie
  - <sub>Correcto, y esa distinción entre **informar y bloquear** es la que hace que el mecanismo funcione.</sub>
- ❌ Porque sin la regla las pruebas no llegan a ejecutarse
  - <sub>Se ejecutan igual: la acción corre en cada push y en cada pull request. Lo que falta es la consecuencia.</sub>
- ❌ Porque GitHub cobra por las acciones si no hay protección de rama
  - <sub>El cobro depende de los minutos de ejecución, no de las reglas de protección.</sub>
- ❌ Porque la protección de rama es lo que dispara el despliegue automático
  - <sub>El despliegue lo dispara el webhook, que es otra cosa.</sub>

> **Por qué.** Acá se cierra un círculo que arrancó en la primera clase de la materia: un test que corrés solo cuando te acordás no es una red de seguridad. Un test que corre automáticamente **y bloquea la integración**, sí. *(Apunte §5.9.1)*

#### C5-22 · Entrega continua y despliegue continuo

*Opción múltiple*

Los dos términos se usan como sinónimos y no lo son. ¿Cuál es la diferencia?

- **✅** Entrega continua: todo cambio integrado queda listo para desplegar y el despliegue lo dispara una persona. Despliegue continuo: se despliega solo
  - <sub>Correcto. Lo que se configura en esta clase con el webhook es **despliegue continuo**, que es apropiado para un práctico y para muchos productos reales, y que exige más confianza en la verificación automática.</sub>
- ❌ Entrega continua es para bibliotecas y despliegue continuo para aplicaciones web
  - <sub>La distinción no es por tipo de producto sino por quién dispara el despliegue.</sub>
- ❌ Entrega continua incluye las pruebas y despliegue continuo no
  - <sub>Los dos se apoyan en la verificación automática. Sin ella, ninguno de los dos tiene sentido.</sub>
- ❌ Son efectivamente sinónimos en la práctica moderna
  - <sub>La industria los distingue con precisión, y la diferencia importa a la hora de decidir cuánta confianza depositás en la automatización.</sub>

> **Por qué.** *(Apunte §5.9.2)*

#### C5-23 · El orden correcto

*Opción múltiple*

¿Por qué el capítulo insiste en configurar primero la integración continua y recién después el despliegue automático?

- **✅** Porque conectar el despliegue automático sin pruebas corriendo solo automatiza la llegada de errores a producción, más rápido y con menos supervisión
  - <sub>Exacto. **La automatización sin verificación no es una mejora.**</sub>
- ❌ Porque el webhook de Easypanel necesita que la acción exista para funcionar
  - <sub>Son independientes: el webhook responde a los push, sin saber nada de las acciones.</sub>
- ❌ Porque GitHub no permite configurar un webhook sin flujos definidos
  - <sub>Lo permite perfectamente.</sub>
- ❌ Porque el orden inverso duplicaría los despliegues
  - <sub>No hay duplicación. El problema es de calidad de lo que llega a producción, no de cantidad.</sub>

> **Por qué.** *(Apunte §5.9.2)*

---

### Página 12 — Lo que falta

#### C5-24 · Lo que falta y ya está vencido

*Opción múltiple*

De todo lo que este despliegue todavía no tiene, ¿cuál es lo **único que ya es urgente**?

- **✅** Las copias de seguridad: desde que existe la base, una pérdida de datos es definitiva
  - <sub>Correcto. La regla clásica es **3-2-1**: tres copias, en dos medios distintos, con una fuera del sitio. En este despliegue hay una copia, en un medio, en el mismo lugar.</sub>
- ❌ La supervisión, porque sin ella no se detecta una caída
  - <sub>Importante, pero pasa a ser urgente *cuando alguien dependa del servicio*. La pérdida de datos, en cambio, ya es irreversible hoy.</sub>
- ❌ La limitación de tasa, porque cualquiera puede saturar la API
  - <sub>Pasa a ser urgente cuando cada petición tenga un costo.</sub>
- ❌ El entorno de pruebas, porque hoy se prueba en producción
  - <sub>Pasa a ser urgente cuando haya usuarios reales.</sub>

> **Por qué.** Y la parte que más se descuida no es hacer la copia sino **probar la restauración**: una copia que nunca se restauró no es una copia de seguridad, es una suposición. Ninguna de estas cosas hacía falta para aprender el flujo. Todas hacen falta el día que alguien dependa de que esto funcione — y **esa transición no se anuncia**. *(Apunte §5.10)*

#### C5-30 · El patrón que se repite

*Opción múltiple*

El capítulo señala un patrón que aparece dos veces en el módulo, en dos escalas distintas. ¿Cuál es?

- **✅** Un nombre estable delante de algo inestable: el DNS lo hizo para internet en 1983, Docker lo hizo adentro de un servidor en 2016
  - <sub>Correcto. **Cuando veas ese patrón —un nombre estable delante de algo inestable— ya sabés qué problema está resolviendo.**</sub>
- ❌ Una lista blanca declarada por el servidor y aplicada por el cliente
  - <sub>Ese patrón también aparece (CORS, CSP, CAA), pero no es el que el capítulo señala acá.</sub>
- ❌ Una capa efímera sobre un artefacto inmutable
  - <sub>Aparece en las capas de Docker y en el historial de Git, pero tampoco es el de esta sección.</sub>
- ❌ Un control que bloquea en lugar de informar
  - <sub>Es la idea de §5.9.1, no la analogía entre el DNS y el DNS embebido.</sub>

> **Por qué.** Es una de las cosas más valiosas que deja el módulo: reconocer una solución conocida en un contexto nuevo. *(Apunte §5.2)*

---

### Página 13 — Diagnóstico

#### C5-25 · could not translate host name

*Opción múltiple*

La API arranca y el log muestra `could not translate host name`. ¿Qué pasó?

- **✅** El nombre de host interno está mal escrito en la cadena de conexión
  - <sub>Correcto. Conviene copiar la cadena que muestra el propio panel de Easypanel al crear el servicio: los nombres varían según la versión y ese valor siempre es el vigente.</sub>
- ❌ La base de datos todavía no terminó de arrancar
  - <sub>Ese caso da `connection refused`: el nombre *sí* se resolvió, y no había nadie escuchando todavía.</sub>
- ❌ Falta abrir el puerto 5432 en el firewall
  - <sub>El tráfico entre contenedores de la misma red no pasa por el firewall del anfitrión.</sub>
- ❌ El DNS público no tiene un registro para ese nombre
  - <sub>Y no debe tenerlo: ese nombre solo existe dentro de la red del proyecto.</sub>

> **Por qué.** Distinguí los dos síntomas: **no se pudo resolver el nombre** (está mal escrito) contra **conexión rechazada** (se resolvió, pero nadie atiende todavía). Es la misma distinción entre NXDOMAIN y un timeout de la Clase 1. *(Apunte §5.12)*

#### C5-26 · persistencia: false con la variable cargada

*Opción múltiple*

Se cargó `DATABASE_URL` en el servicio api y `/api/salud` sigue informando `persistencia: false`. ¿Qué falta?

- **✅** Redesplegar: las variables se leen al arrancar el proceso
  - <sub>Correcto. Es exactamente el mismo tropiezo que en la Clase 4 con `ORIGENES_PERMITIDOS`.</sub>
- ❌ Reiniciar el servicio db para que acepte conexiones nuevas
  - <sub>La base acepta conexiones desde que arrancó. El que no leyó la variable es el otro servicio.</sub>
- ❌ Crear la tabla del historial a mano
  - <sub>Si el problema fuera la tabla, la conexión estaría establecida y `persistencia` sería `true`.</sub>
- ❌ Agregar el servicio db a la red del proyecto
  - <sub>Todo servicio creado dentro de un proyecto ya está en su red.</sub>

> **Por qué.** *(Apunte §5.12)*

#### C5-27 · El historial se vacía en cada despliegue

*Opción múltiple*

Los datos del historial desaparecen cada vez que se redespliega. ¿Cuál es la causa?

- **✅** El servicio db no tiene volumen: todo se está escribiendo en la capa efímera del contenedor
  - <sub>Correcto. Se revisa el almacenamiento del servicio db en el panel.</sub>
- ❌ La API está recreando la tabla en cada arranque
  - <sub>Es posible en general, pero el capítulo señala el volumen como causa: es lo que se revisa primero.</sub>
- ❌ PostgreSQL vacía la base cuando cambia la contraseña
  - <sub>No hace nada parecido.</sub>
- ❌ El redespliegue de api borra los datos de db
  - <sub>Son contenedores independientes: redesplegar uno no toca al otro.</sub>

> **Por qué.** Compruébalo al revés: hacé operaciones, redesplegá **api** y volvé a pedir el historial. Los datos siguen ahí, porque el estado no vive en api. *(Apunte §5.7.3 y §5.12)*

#### C5-28 · El nombre interno no resuelve desde otro proyecto

*Opción múltiple*

Un servicio de *otro* proyecto de Easypanel intenta usar `calculadora_db` y no resuelve. ¿Es un error?

- **✅** No: es el comportamiento esperado. Son redes distintas, y ese aislamiento es la propiedad buscada. Si de verdad tienen que hablarse, el servicio va movido al mismo proyecto
  - <sub>Correcto. Es la fila «aislamiento entre proyectos» de §5.4.2, funcionando.</sub>
- ❌ Sí: hay que agregar un registro DNS para ese nombre
  - <sub>Ese nombre no vive en ninguna zona DNS pública, y no debe vivir.</sub>
- ❌ Sí: falta abrir el puerto 5432 entre los dos proyectos
  - <sub>Publicar el puerto lo expondría a internet, que es exactamente lo que se quiere evitar.</sub>
- ❌ No, pero se arregla usando la IP del contenedor en lugar del nombre
  - <sub>Además de frágil, tampoco funcionaría: las redes están aisladas a nivel de red, no de resolución de nombres.</sub>

> **Por qué.** Dos proyectos en el mismo VPS no se ven entre sí aunque compartan servidor, núcleo y motor de Docker. *(Apunte §5.4.2 y §5.12)*

#### C5-29 · Las pruebas pasan en local y fallan en la acción

*Opción múltiple*

Las pruebas pasan en la notebook de un integrante y fallan en GitHub Actions al instalar. ¿Qué está ocurriendo casi siempre?

- **✅** Hay una dependencia instalada solo localmente que nadie declaró en los archivos de requisitos
  - <sub>Correcto, y detectar eso es un beneficio del flujo por sí solo: instala en una máquina limpia. **Un proyecto que solo se construye en la máquina de quien lo escribió no está terminado.**</sub>
- ❌ La versión de Python de GitHub es incompatible con el proyecto
  - <sub>El flujo fija la versión explícitamente con `setup-python`.</sub>
- ❌ Las acciones de GitHub no soportan pytest
  - <sub>Lo soportan sin ningún problema.</sub>
- ❌ Falta configurar la protección de rama
  - <sub>La protección de rama decide si se puede fusionar, no si la instalación funciona.</sub>

> **Por qué.** Es el mismo problema que motivó los contenedores en §3.2: «en mi máquina anda». *(Apunte §5.9 y §5.12)*

---

## Las cuatro que más se van a errar

Según lo que el capítulo señala como contraintuitivo:

1. **C5-04** — por qué la API necesita dominio público. La intuición dice «están en el mismo servidor, que se hablen por adentro». **El frontend no se ejecuta en el servidor.**
2. **C5-13** — los `%s` de la consulta. El distractor «equivale a usar el operador %» se lleva a casi todos, y es exactamente la confusión que produce inyecciones.
3. **C5-10** — por qué 503 y no 500. Muchos no distinguen las familias de códigos: 503 dice la verdad («falta una dependencia»), 500 no.
4. **C5-03** — la respuesta corta del nombre interno. O entendieron el formato `proyecto_servicio` y que ese nombre solo existe adentro, o no contestan.

Si al revisar los intentos ves que una de estas tiene menos del 50 % de acierto, no es un problema del grupo: es un tema para retomar en la clase siguiente.
