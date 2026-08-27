# Clave de corrección — Cuestionario Clase 1 (DNS y dominio propio)

> **Documento del docente. No publicar en el aula.**
> Estas son las respuestas de las 31 preguntas de `cuestionario-moodle-clase-1.xml`.
> Se genera desde la misma fuente que el XML, así que si el banco cambia, esta clave cambia con él.

- **Cuestionario:** `Clase 1 – Autoevaluación: DNS y dominio propio`
- **Curso:** campustest.frm.utn.edu.ar → curso 14 → sección 30 «Actividades 🧩»
- **31 preguntas** en 11 páginas · 1 punto cada una, escaladas a 10
- El orden de abajo es el **orden real del cuestionario** (paginación de `cuestionario-moodle-clase-1.md` §3.1)

En Moodle el alumno ve todo esto solo: cada opción incorrecta tiene su propia explicación. Esta clave sirve para revisar el banco antes de publicarlo y para tener las respuestas a mano en clase.

---

## Resumen

| # | Pág | Tipo | Respuesta correcta | Apunte |
|---|---|---|---|---|
| **C1-01** | 1 | Respuesta corta | `/etc/hosts` o `etc/hosts` o `/etc/hosts/` | §1.2 |
| **C1-02** | 1 | Opción múltiple | Que el protocolo FTP resultó inseguro para transferir el archivo | §1.2 |
| **C1-03** | 1 | Opción múltiple | Que renuncia deliberadamente a que todos vean el mismo dato en el mismo instante, a cambi… | §1.2, §1.8 |
| **C1-04** | 1 | Emparejar | _(emparejamiento — ver detalle)_ | §1.2 |
| **C1-05** | 2 | Opción múltiple | Que la petición nunca llegó a emitirse hacia el servidor: el fallo ocurrió antes, en la r… | §1.1, §1.3 |
| **C1-06** | 2 | Opción múltiple | La cabecera Host del pedido HTTP, que el proxy inverso lee para decidir a qué servicio in… | §1.3 |
| **C1-07** | 2 | Opción múltiple | Porque el servidor necesita saber qué certificado presentar, y el certificado es justamen… | §1.3 |
| **C1-08** | 3 | Opción múltiple | El dominio es un subárbol completo; la zona es la porción que una organización administra… | §1.4.1, §1.7 |
| **C1-09** | 3 | Opción múltiple | Son 13 identidades lógicas, cada una replicada hoy en cientos de instancias físicas distr… | §1.4.2 |
| **C1-10** | 3 | Opción múltiple | El autoritativo posee los datos de su zona y responde solo sobre ella; el recursivo no po… | §1.4.3 |
| **C1-11** | 4 | Emparejar | _(emparejamiento — ver detalle)_ | §1.4.2, §1.4.3 |
| **C1-12** | 4 | Opción múltiple | NOERROR, con cero respuestas | §1.5 |
| **C1-14** | 4 | Opción múltiple | NXDOMAIN es una respuesta —alguien contestó «ese nombre no existe»—; un timeout no es una… | §1.5, §1.9.1 |
| **C1-13** | 5 | Emparejar | _(emparejamiento — ver detalle)_ | §1.5, §1.9.1 |
| **C1-15** | 5 | Opción múltiple | Que quien responde es el servidor autoritativo de la zona: el dato viene del origen y no… | §1.5, §1.10 |
| **C1-16** | 6 | Opción múltiple | No: el vértice requiere obligatoriamente registros NS y SOA, y un CNAME no puede convivir… | §1.6.1 |
| **C1-17** | 6 | Opción múltiple | Un registro CAA que no incluye a la autoridad certificadora que se está usando | §1.6.2 |
| **C1-19** | 7 | Opción múltiple | Los NS del dominio están delegados a otro proveedor: Namecheap no es autoritativo para es… | §1.7 |
| **C1-20** | 7 | Emparejar | _(emparejamiento — ver detalle)_ | §1.7 |
| **C1-21** | 7 | Opción múltiple | Registry = quien opera un TLD completo (Verisign para .com) · Registrar = la empresa mino… | §1.7 |
| **C1-22** | 8 | Respuesta corta | `300` | §1.8, §1.14 |
| **C1-23** | 8 | Opción múltiple | Porque el DNS no tiene ningún mecanismo de difusión: los autoritativos se actualizan al i… | §1.8 |
| **C1-24** | 9 | Opción múltiple | La reducción del TTL también es un cambio, y las cachés la descubren recién cuando expira… | §1.8 |
| **C1-25** | 9 | Opción múltiple | Caché negativa: el resolver memorizó que el nombre no existía y lo va a seguir contestand… | §1.8, §1.8.1 |
| **C1-26** | 10 | Opción múltiple | Filtrado confirmado: el bloqueo está en el resolver de su proveedor, no en el dominio | §1.9.2 |
| **C1-27** | 10 | Opción múltiple | Porque la aplicación seguiría siendo inaccesible para cualquier visitante cuyo proveedor… | §1.9.3 |
| **C1-28** | 10 | Verdadero/Falso | **FALSO** | §1.12.1 |
| **C1-29** | 10 | Opción múltiple | El registro es un A con nombre , se carga en el panel y no necesita nada más; el certific… | §1.12 |
| **C1-18** | 11 | Múltiples correctas | Un registro A con nombre  apuntando a la IP del VPS + Un registro A con nombre @ apuntando a la IP del VPS | §1.12.1, §1.14 |
| **C1-30** | 11 | Opción múltiple | Porque están viendo cachés distintas —hasta cuatro capas, cada una con su propio reloj— y… | §1.8.1, §1.10 |
| **C1-31** | 11 | Opción múltiple | DNSSEC autentica las respuestas pero no las cifra; DoT y DoH cifran el canal hasta el res… | §1.11 |

## Cobertura del capítulo

| Sección del apunte | Preguntas que la evalúan |
|---|---|
| §1.1 | C1-05 |
| §1.2 | C1-01, C1-02, C1-03, C1-04 |
| §1.3 | C1-05, C1-06, C1-07 |
| §1.4.1 | C1-08 |
| §1.4.2 | C1-09, C1-11 |
| §1.4.3 | C1-10, C1-11 |
| §1.5 | C1-12, C1-13, C1-14, C1-15 |
| §1.6.1 | C1-16 |
| §1.6.2 | C1-17 |
| §1.7 | C1-08, C1-19, C1-20, C1-21 |
| §1.8 | C1-03, C1-22, C1-23, C1-24, C1-25 |
| §1.8.1 | C1-25, C1-30 |
| §1.9.1 | C1-13, C1-14 |
| §1.9.2 | C1-26 |
| §1.9.3 | C1-27 |
| §1.10 | C1-15, C1-30 |
| §1.11 | C1-31 |
| §1.12 | C1-29 |
| §1.12.1 | C1-18, C1-28 |
| §1.14 | C1-18, C1-22 |

---

## Detalle por página

### Página 1 — El origen del DNS

#### C1-01 · El vestigio de HOSTS.TXT

*Respuesta corta*

El archivo `HOSTS.TXT` de ARPANET dejó un descendiente que sigue vivo en todos los sistemas operativos y que **tiene prioridad sobre cualquier consulta a la red**. En un sistema Unix, ¿cuál es su ruta completa? (escribila tal cual)

Respuestas aceptadas (sin distinguir mayúsculas): `/etc/hosts`, `etc/hosts`, `/etc/hosts/`

> **Por qué.** En Windows es `C:\Windows\System32\drivers\etc\hosts`. Que tenga prioridad sobre la red no es un detalle: es la razón por la que un nombre puede resolver distinto en tu máquina que en la del resto del mundo. *(Apunte §1.2)*

#### C1-02 · Por qué colapsó HOSTS.TXT

*Opción múltiple*

`HOSTS.TXT` era un único archivo de texto mantenido a mano por una oficina en Stanford y descargado por FTP. ¿Cuál de estas **no** fue una de las causas de su colapso?

- **✅** Que el protocolo FTP resultó inseguro para transferir el archivo
  - <sub>Correcto: esa **no** fue una causa. El problema nunca fue la seguridad del transporte, sino la escala y la coherencia.</sub>
- ❌ El archivo crecía sin límite y el tráfico para descargarlo se multiplicaba
  - <sub>Esa sí fue una causa: es el problema de escala de cualquier lista centralizada.</sub>
- ❌ Los nombres empezaron a colisionar porque no había autoridad que garantizara unicidad
  - <sub>Esa sí fue una causa, y es la que el DNS resuelve distribuyendo la autoridad.</sub>
- ❌ La copia que cada máquina tenía estaba siempre desactualizada respecto de la realidad
  - <sub>Esa sí fue una causa: es el problema de coherencia de una lista copiada a mano.</sub>

> **Por qué.** Todo sistema centralizado de nombres colapsa por escala. La moraleja no es anecdótica: es el problema que las tres decisiones de 1983 vinieron a resolver. *(Apunte §1.2)*

#### C1-03 · Qué significa coherencia eventual

*Opción múltiple*

El DNS «acepta la coherencia eventual a cambio de escala». ¿Qué quiere decir eso exactamente?

- **✅** Que renuncia deliberadamente a que todos vean el mismo dato en el mismo instante, a cambio de que el 99 % de las consultas se responda desde una copia cercana
  - <sub>Exacto. Es un compromiso de diseño, no una limitación: disponibilidad y escala por encima de consistencia instantánea.</sub>
- ❌ Que los datos terminan siendo coherentes recién cuando el administrador los sincroniza a mano
  - <sub>Nadie sincroniza nada a mano. La coherencia llega sola, cuando expiran las copias.</sub>
- ❌ Que un cambio se propaga activamente de servidor en servidor hasta llegar a todos
  - <sub>El DNS **no tiene ningún mecanismo de difusión**: nadie notifica a nadie. Lo que ocurre es que cada copia expira por su cuenta.</sub>
- ❌ Que las respuestas pueden llegar con errores que se corrigen en la siguiente consulta
  - <sub>No hay errores: las respuestas son correctas, solo que pueden ser *viejas*. Son cosas distintas.</sub>

> **Por qué.** Este compromiso —disponibilidad y escala por encima de consistencia instantánea— es el mismo que van a estudiar después en bases de datos distribuidas. Cada vez que «un cambio no se ve» o «a un compañero le anda y a otro no», están observando una decisión de 1983, no un error. *(Apunte §1.2 y §1.8)*

#### C1-04 · Las tres decisiones de diseño de 1983

*Emparejar*

Emparejá cada decisión de diseño del DNS con la consecuencia que se observa en este práctico.

| Se empareja | Con |
|---|---|
| **Distribuir la autoridad, no los datos** | Los registros se cargan donde apuntan los NS: cargarlos en otro panel no da error, simplemente no hace nada |
| **Aceptar la coherencia eventual** | Un cambio tarda en verse, y a un compañero le anda mientras a otro no |
| **Registros de recursos tipados y extensibles** | El mismo nombre lleva a la vez A, TXT y CAA; y cuando apareció IPv6 se agregó AAAA sin tocar el protocolo |

> **Por qué.** Nadie posee la base de datos completa, y la unicidad de los nombres queda garantizada **por construcción**: dentro de `utn.edu.ar` la universidad decide sin consultarle a nadie, y ningún externo puede crear nombres ahí. *(Apunte §1.2)*

---

### Página 2 — Del navegador al servidor

#### C1-05 · El log vacío

*Opción múltiple*

Un grupo reporta que su sitio no carga. Entran al servidor y el log del proxy inverso está completamente vacío. ¿Qué información aporta ese log vacío?

- **✅** Que la petición nunca llegó a emitirse hacia el servidor: el fallo ocurrió antes, en la resolución del nombre
  - <sub>Exacto. La resolución es previa e independiente de la conexión: si falla la operación 1, las otras cuatro no se ejecutan. El servidor no está «sin actividad»: está ciego.</sub>
- ❌ Que el servidor está caído y hay que reiniciar el servicio
  - <sub>Un servicio caído igual deja rastro: el sistema registra que no pudo atender. Un log *vacío* dice algo más fuerte: que nadie golpeó la puerta.</sub>
- ❌ Que el certificado TLS no se emitió correctamente
  - <sub>Un fallo de TLS ocurre en la operación 3, cuando la conexión ya se estableció. Deja rastro.</sub>
- ❌ Que el firewall está descartando los paquetes entrantes
  - <sub>Es plausible y también daría log vacío — pero el capítulo señala al DNS como **primer** sospechoso, porque es el único tramo que no ocurre ni en el servidor ni en el código.</sub>

> **Por qué.** Fijate en la consecuencia probatoria: el log del servidor solo puede atestiguar sobre las operaciones 2 a 5. Cuando algo no anda y el servidor no dice nada, el DNS es el primer sospechoso, no el último. *(Apunte §1.1 y §1.3)*

#### C1-06 · Alojamiento virtual

*Opción múltiple*

Un mismo VPS, con una única dirección IP, atiende `calculadora.tudominio.me` y `api.tudominio.me`. ¿Qué mecanismo lo hace posible?

- **✅** La cabecera `Host` del pedido HTTP, que el proxy inverso lee para decidir a qué servicio interno entregar la petición
  - <sub>Correcto: es el alojamiento virtual (*virtual hosting*). Sin él, cada sitio web del mundo necesitaría una IP exclusiva, algo imposible dada la escasez de direcciones IPv4.</sub>
- ❌ El registro comodín `*` del panel DNS
  - <sub>El comodín hace que los dos nombres *resuelvan* a la misma IP. Pero una vez que el paquete llegó, algo tiene que decidir cuál de los dos servicios responde: eso es otra cosa.</sub>
- ❌ Que cada servicio escucha en un puerto distinto
  - <sub>Los dos se sirven por el 443. Si dependiera del puerto, el usuario tendría que escribirlo en la URL.</sub>
- ❌ La extensión SNI de TLS, que enruta la petición al servicio correcto
  - <sub>SNI le dice al servidor *qué certificado presentar*, en la operación 3. El enrutamiento al servicio interno lo decide el proxy leyendo `Host`, en la operación 4.</sub>

> **Por qué.** Es la técnica que hace posible que el VPS del práctico aloje varios dominios con una sola IP. *(Apunte §1.3)*

#### C1-07 · El nombre antes del cifrado

*Opción múltiple*

Durante la negociación TLS el navegador declara el nombre del sitio **en texto plano**, antes de que exista canal cifrado. ¿Por qué es inevitable?

- **✅** Porque el servidor necesita saber qué certificado presentar, y el certificado es justamente el material con el que se establece el canal cifrado
  - <sub>Exacto: es un problema de huevo y gallina que la extensión SNI resuelve enviando el nombre en claro.</sub>
- ❌ Porque el protocolo TLS todavía no soporta cifrar esa parte del saludo
  - <sub>No es una carencia técnica pendiente: es una dependencia lógica. Sin saber el nombre no se puede elegir el certificado, y sin certificado no hay cifrado.</sub>
- ❌ Porque el nombre ya viajó en claro en la consulta DNS, así que da igual
  - <sub>Que ya haya viajado en claro no explica *por qué* TLS lo necesita. Son dos momentos independientes.</sub>
- ❌ Porque la cabecera `Host` se envía antes que el saludo TLS
  - <sub>Al revés: `Host` viaja en la operación 4, ya dentro del canal cifrado. SNI viaja en la 3.</sub>

> **Por qué.** Es un detalle que reaparece en la Clase 4, cuando cada servicio obtenga su propio certificado. *(Apunte §1.3)*

---

### Página 3 — La jerarquía de nombres

#### C1-08 · Dominio y zona

*Opción múltiple*

¿Cuál es la diferencia entre **dominio** y **zona**?

- **✅** El dominio es un subárbol completo; la zona es la porción que una organización administra efectivamente, y termina donde empieza una delegación
  - <sub>Correcto. El operador de `com` no administra los registros de `tudominio.com`: su zona contiene apenas la anotación de a quién le delegó ese subárbol.</sub>
- ❌ Son sinónimos: «zona» es el término técnico y «dominio» el comercial
  - <sub>No son sinónimos, y confundirlos es lo que lleva a cargar registros en el panel equivocado.</sub>
- ❌ El dominio es lo que se compra al registrador; la zona es lo que se paga aparte
  - <sub>No hay nada que pagar aparte. La distinción es estructural, no comercial.</sub>
- ❌ La zona incluye los subdominios y el dominio no
  - <sub>Justo al revés en cuanto a alcance: el dominio, en sentido amplio, incluye todo el subárbol. La zona *corta* ese subárbol donde hay una delegación.</sub>

> **Por qué.** La delegación es el acto administrativo que corta el árbol en zonas. De esta distinción sale toda la sección de delegación. *(Apunte §1.4.1 y §1.7)*

#### C1-09 · Los 13 servidores raíz

*Opción múltiple*

Se dice que la raíz del DNS tiene «13 servidores». ¿Qué significa eso con precisión?

- **✅** Son 13 identidades lógicas, cada una replicada hoy en cientos de instancias físicas distribuidas por el mundo mediante anycast
  - <sub>Correcto. El número 13 es un límite heredado del tamaño máximo que podía tener una respuesta DNS sobre UDP en el diseño original. Hay instancias en América del Sur, Argentina incluida: consultar «la raíz» no implica cruzar el océano.</sub>
- ❌ Son 13 máquinas físicas repartidas entre Estados Unidos y Europa
  - <sub>Si fueran 13 máquinas, el DNS mundial sería absurdamente frágil. Son 13 *nombres*, con cientos de instancias detrás.</sub>
- ❌ Son 13 empresas que se reparten la administración del espacio de nombres
  - <sub>Hay 12 organizaciones operadoras, pero el 13 no cuenta empresas: cuenta identidades de servidor (`a` a `m`.root-servers.net).</sub>
- ❌ Son 13 copias de la base de datos completa de todos los dominios de internet
  - <sub>**Nadie** tiene la base completa. La raíz solo sabe quién administra cada dominio de primer nivel.</sub>

> **Por qué.** Anycast es una técnica de enrutamiento donde muchas máquinas comparten la misma dirección IP y la red entrega cada consulta a la instancia más cercana. *(Apunte §1.4.2)*

#### C1-10 · Autoritativo y recursivo

*Opción múltiple*

Un servidor autoritativo y un resolver recursivo cumplen funciones opuestas. ¿Cuál es la descripción correcta?

- **✅** El autoritativo posee los datos de su zona y responde solo sobre ella; el recursivo no posee ningún dato propio, pero sabe encontrar cualquiera
  - <sub>Exacto. El recursivo recorre la jerarquía con consultas iterativas, consolida el recorrido en una única respuesta, la guarda en caché y la devuelve.</sub>
- ❌ El autoritativo atiende a los usuarios finales y el recursivo atiende a otros servidores
  - <sub>Es al revés: el usuario final habla con el *recursivo*, y nunca consulta la jerarquía directamente.</sub>
- ❌ El recursivo guarda una copia completa de la zona y el autoritativo la genera
  - <sub>El recursivo no guarda zonas: guarda respuestas sueltas en caché, cada una con su TTL.</sub>
- ❌ Son el mismo servidor cumpliendo dos roles según quién pregunte
  - <sub>Son funciones opuestas y conviene no mezclarlas: uno tiene los datos, el otro sabe buscarlos.</sub>

> **Por qué.** El equipo del usuario ejecuta apenas un **stub resolver**: una pieza mínima del sistema operativo que sabe hacer una sola cosa, delegarle todo el recorrido al recursivo y esperar la respuesta final. *(Apunte §1.4.3)*

---

### Página 4 — Autoridad y respuestas

#### C1-11 · Los tres niveles de autoridad

*Emparejar*

Emparejá cada nivel de la jerarquía del DNS con lo que efectivamente sabe.

| Se empareja | Con |
|---|---|
| **Servidores raíz** | Quién administra cada dominio de primer nivel |
| **Operador del TLD (.com, .ar, .me)** | Qué servidores de nombres administran cada dominio registrado |
| **Servidor autoritativo de la zona** | Los registros concretos del dominio: las direcciones IP y todo lo demás |
| **Resolver recursivo** | Ningún dato propio: sabe recorrer la jerarquía y guarda en caché lo que encuentra |

> **Por qué.** Ninguno de estos niveles es consultado directamente por el navegador. Y ninguno tiene la base completa: cada uno conoce su renglón y a quién le pasó la posta. *(Apunte §1.4.2 y §1.4.3)*

#### C1-12 · Nombre sin el tipo pedido

*Opción múltiple*

Consultás un registro de tipo TXT en un nombre que **existe** pero que no tiene ningún TXT cargado. ¿Qué código de respuesta devuelve el servidor?

- **✅** NOERROR, con cero respuestas
  - <sub>Correcto, y es la trampa clásica: NOERROR significa que la consulta se procesó correctamente; **no** garantiza que haya registros en la respuesta.</sub>
- ❌ NXDOMAIN, porque no encontró lo que buscaba
  - <sub>NXDOMAIN afirma algo mucho más fuerte: que *el nombre no existe*. Acá el nombre existe perfectamente.</sub>
- ❌ SERVFAIL, porque no pudo completar la consulta
  - <sub>SERVFAIL indica un fallo del servidor: un problema interno, con la zona, o una validación de seguridad que no pasó. Acá no falló nada.</sub>
- ❌ REFUSED, porque el tipo de registro no está permitido
  - <sub>REFUSED es una negativa por política: el servidor reconoce la consulta como válida y decide no atenderla.</sub>

> **Por qué.** Leer bien el RCODE convierte la salida de `dig` de un texto críptico en un informe preciso. *(Apunte §1.5)*

#### C1-14 · NXDOMAIN contra timeout

*Opción múltiple*

Diagnosticando un nombre que no anda, ¿cuál es la diferencia entre recibir NXDOMAIN y que la consulta agote el tiempo de espera?

- **✅** NXDOMAIN es una respuesta —alguien contestó «ese nombre no existe»—; un timeout no es una respuesta: nadie contestó nada
  - <sub>Exacto, y separa dos problemas completamente distintos: un resolver que filtra contesta rápido; uno caído o inalcanzable no contesta nada.</sub>
- ❌ Son dos formas de informar lo mismo: que el nombre no se pudo resolver
  - <sub>Confundirlos lleva a una explicación técnica perfectamente equivocada de un problema perfectamente real.</sub>
- ❌ NXDOMAIN indica un problema del servidor y el timeout un problema del nombre
  - <sub>Justo al revés en cuanto a quién falla: NXDOMAIN habla del *nombre*; el timeout habla del *resolver*.</sub>
- ❌ El timeout es más grave porque significa que el dominio fue dado de baja
  - <sub>Un timeout no dice absolutamente nada sobre el dominio. Solo dice que el resolver no contestó.</sub>

> **Por qué.** Por eso el procedimiento de diagnóstico empieza con una prueba de control: antes de medir el fenómeno hay que verificar el instrumento. *(Apunte §1.5 y §1.9.1)*

---

### Página 5 — Códigos e indicadores

#### C1-13 · Códigos de respuesta (RCODE)

*Emparejar*

Emparejá cada código de respuesta del mensaje DNS con su significado exacto.

| Se empareja | Con |
|---|---|
| **NOERROR** | La consulta se procesó correctamente — pero puede venir con cero registros |
| **SERVFAIL** | El servidor no pudo procesar la consulta: fallo interno, problema con la zona o validación de seguridad que no pasó |
| **NXDOMAIN** | El nombre consultado no existe en la zona autoritativa, o eso afirma quien responde |
| **REFUSED** | El servidor reconoce la consulta como válida pero decide por política no atenderla |

> **Por qué.** Los RCODE no son una curiosidad de protocolo: son información de diagnóstico de primera calidad. Un resolver que filtra suele contestar NXDOMAIN o REFUSED — *rápido*, porque tiene la respuesta lista. *(Apunte §1.5 y §1.9.1)*

#### C1-15 · El indicador AA

*Opción múltiple*

En la salida de `dig`, ¿qué significa que aparezca el indicador `aa`?

- **✅** Que quien responde es el servidor autoritativo de la zona: el dato viene del origen y no de una caché
  - <sub>Correcto (*Authoritative Answer*). Cuando consultás a un resolver público como 8.8.8.8, ese indicador normalmente **no** aparece: la respuesta salió de su caché.</sub>
- ❌ Que la respuesta fue validada criptográficamente con DNSSEC
  - <sub>Esa es la flag `ad` (*authenticated data*). Son cosas distintas: una habla del origen, la otra de la firma.</sub>
- ❌ Que el resolver ofrece servicio recursivo
  - <sub>Esa es `ra` (*Recursion Available*), la confirmación de que el resolver se hace cargo del recorrido completo.</sub>
- ❌ Que la respuesta vino truncada y hay que reintentar por TCP
  - <sub>Esa es `tc` (*truncated*), que aparece cuando la respuesta no entra en el límite de UDP.</sub>

> **Por qué.** Buscá siempre dos datos en cada salida: el **status** (¿NOERROR, NXDOMAIN, SERVFAIL?) y **quién respondió** (la línea SERVER). *(Apunte §1.5 y §1.10)*

---

### Página 6 — Tipos de registro

#### C1-16 · CNAME en el vértice

*Opción múltiple*

Un grupo quiere apuntar `tudominio.me` (el dominio raíz pelado) con un CNAME, y promete no cargar ningún otro registro con ese nombre. ¿Funciona?

- **✅** No: el vértice requiere obligatoriamente registros NS y SOA, y un CNAME no puede convivir con ningún otro registro
  - <sub>Correcto. La condición «que no haya otros registros» es **imposible de cumplir** en el vértice. Por eso el dominio raíz siempre se apunta con un registro A.</sub>
- ❌ Sí, mientras efectivamente no cargue ningún otro registro con ese nombre
  - <sub>No depende de su voluntad: NS y SOA existen en el vértice por definición de zona, no porque alguien los cargue.</sub>
- ❌ Sí, pero solo si el proveedor DNS tiene activado el aplanamiento de CNAME
  - <sub>Ojo: ALIAS, ANAME y *CNAME flattening* existen y son válidos, pero son extensiones propietarias que **simulan** el comportamiento del lado del servidor. No son estándar, y no es que el CNAME «funcione».</sub>
- ❌ No, porque los CNAME solo se admiten en subdominios de tercer nivel o más
  - <sub>No hay una regla de niveles. La restricción es sobre la coexistencia con otros registros.</sub>

> **Por qué.** La restricción es lógica, no caprichosa: el CNAME afirma «este nombre es, a todos los efectos, aquel otro», y admitir datos propios simultáneos volvería ambigua toda consulta. *(Apunte §1.6.1)*

#### C1-17 · El certificado que nunca llega

*Opción múltiple*

El DNS resuelve perfecto, el servicio está sano, y sin embargo el certificado nunca se emite. El log de Traefik no dice nada útil. ¿Cuál es el primer sospechoso?

- **✅** Un registro CAA que no incluye a la autoridad certificadora que se está usando
  - <sub>Correcto. Toda autoridad certificadora está obligada a consultar los CAA del nombre antes de emitir y a negarse si no figura. Es de los pocos errores que no dejan rastro útil.</sub>
- ❌ Un TTL demasiado alto en el registro A
  - <sub>Un TTL alto retrasa que se vea un cambio, pero si el DNS «resuelve perfecto» ese cambio ya se ve.</sub>
- ❌ La falta de un registro AAAA para IPv6
  - <sub>El AAAA solo hace falta si el VPS tiene IPv6 asignada, y su ausencia no bloquea la emisión.</sub>
- ❌ Caché negativa en el resolver del proveedor
  - <sub>La caché negativa haría que el nombre *no* resolviera. Acá resuelve.</sub>

> **Por qué.** Los dominios recién registrados normalmente no traen CAA, así que este caso aparece sobre todo con dominios reutilizados de un proyecto viejo o del trabajo. Se consulta con `nslookup -type=CAA tudominio.me`. *(Apunte §1.6.2)*

---

### Página 7 — Delegación

#### C1-19 · Dónde se cargan los registros

*Opción múltiple*

Un grupo compró el dominio en Namecheap, cargó ahí el registro comodín, lo ve en la tabla con todos los datos correctos, y el dominio no resuelve ni después de tres horas. ¿Qué pasó?

- **✅** Los NS del dominio están delegados a otro proveedor: Namecheap no es autoritativo para esa zona, así que el panel muestra registros que el mundo no consulta
  - <sub>Correcto, y es el error número uno del capítulo. Cargar los registros en el lugar equivocado **no produce ningún error**: simplemente no tiene efecto.</sub>
- ❌ Falta esperar a que el cambio propague por la red
  - <sub>La «propagación» no existe como proceso, y además un dominio nuevo que nunca fue consultado resuelve casi de inmediato: no hay caché previa que expirar.</sub>
- ❌ El TTL quedó demasiado alto y hay que esperar a que expire
  - <sub>Un TTL alto retrasa ver un *cambio*. Si el nombre nunca resolvió, no hay valor viejo cacheado que estorbe.</sub>
- ❌ Namecheap tarda hasta 24 horas en activar los dominios nuevos
  - <sub>El registro del dominio y la publicación de sus registros son cosas distintas. Si los NS apuntan a Namecheap, sus registros toman efecto enseguida.</sub>

> **Por qué.** Por eso la verificación previa obligatoria, **antes de tocar nada**, es `nslookup -type=NS tudominio.me`. *(Apunte §1.7)*

#### C1-20 · Leer los NS para saber dónde cargar

*Emparejar*

`nslookup -type=NS` devuelve estos servidores de nombres. Emparejá cada respuesta con el panel donde hay que cargar los registros.

| Se empareja | Con |
|---|---|
| **dns1.registrar-servers.com** | Namecheap |
| **ns1.dns-parking.com** | Hostinger |
| **xxx.ns.cloudflare.com** | Cloudflare |

> **Por qué.** Los registros se cargan **en el panel del proveedor al que apuntan los NS**, no necesariamente donde se compró el dominio. Registrador y proveedor de DNS son funciones separables, y eso es exactamente lo que los NS expresan. *(Apunte §1.7)*

#### C1-21 · Registry, registrar y registrant

*Opción múltiple*

La industria separa tres roles que el lenguaje cotidiano mezcla. ¿Cuál es la correspondencia correcta?

- **✅** Registry = quien opera un TLD completo (Verisign para .com) · Registrar = la empresa minorista donde se compra (Namecheap) · Registrant = quien tiene los derechos sobre el nombre
  - <sub>Correcto. La consecuencia clave es que registrador y proveedor de DNS son funciones separables: comprar el dominio en un lugar y administrar sus registros en otro es una configuración perfectamente normal.</sub>
- ❌ Registry = la base de datos WHOIS · Registrar = el servidor autoritativo · Registrant = el resolver del usuario
  - <sub>Mezcla roles comerciales con piezas técnicas. Registry, registrar y registrant son los tres *organizaciones o personas*.</sub>
- ❌ Registry = el titular · Registrar = el operador del TLD · Registrant = el revendedor
  - <sub>Están invertidos: el *registrant* es el titular y el *registry* el operador del TLD.</sub>
- ❌ Los tres nombran a la misma empresa según el trámite que esté haciendo
  - <sub>Son tres actores distintos. NIC Argentina opera `.ar`, vos comprás en un registrador y el titular sos vos.</sub>

> **Por qué.** De esta separación sale la regla operativa central: los registros se cargan donde apuntan los NS. *(Apunte §1.7)*

---

### Página 8 — TTL y propagación

#### C1-22 · El TTL del práctico

*Respuesta corta*

El práctico pide bajar el TTL de los registros durante la cursada. ¿A cuántos **segundos**? (escribí solo el número)

Respuestas aceptadas (sin distinguir mayúsculas): `300`

> **Por qué.** Son 5 minutos. Ojo con los paneles: Namecheap no pide el número sino que ofrece una lista desplegable (*Automatic, 1 min, 5 min, 30 min*), así que los 300 segundos son la opción «5 min». Es la misma magnitud expresada de dos maneras. *(Apunte §1.8 y §1.14)*

#### C1-23 · La propagación no existe

*Opción múltiple*

«Hay que esperar a que propague.» ¿Por qué la expresión es engañosa?

- **✅** Porque el DNS no tiene ningún mecanismo de difusión: los autoritativos se actualizan al instante y lo que demora es la expiración de las copias en caché
  - <sub>Exacto. La «propagación» no es un proceso: es la suma de millones de expiraciones independientes. Cada resolver descubre el valor nuevo cuando su copia vieja expira.</sub>
- ❌ Porque en realidad la propagación es instantánea y el problema es el navegador
  - <sub>El navegador es solo una de las cuatro capas de caché. También están el sistema operativo, el router doméstico y el resolver del proveedor, que no se puede vaciar.</sub>
- ❌ Porque el cambio se difunde de servidor en servidor pero muy lentamente
  - <sub>No se difunde en absoluto: **nadie notifica a nadie**. Esa es toda la diferencia.</sub>
- ❌ Porque solo propagan los registros de tipo A, y no los demás
  - <sub>El TTL y la caché funcionan igual para todos los tipos de registro.</sub>

> **Por qué.** Dos consecuencias operativas: un dominio nuevo, que nunca fue consultado, resuelve casi de inmediato; y un registro modificado puede tardar hasta el **TTL anterior** en reflejarse. *(Apunte §1.8)*

---

### Página 9 — Caché

#### C1-24 · Bajar el TTL antes de un cambio

*Opción múltiple*

Un grupo va a mudar su dominio a otra IP y baja el TTL a 300 segundos justo antes de hacer el cambio. ¿Qué va a pasar?

- **✅** La reducción del TTL también es un cambio, y las cachés la descubren recién cuando expira el TTL viejo: hay que bajarlo con anticipación
  - <sub>Correcto. La técnica estándar es reducir el TTL con al menos un día de anticipación al cambio previsto, y restaurarlo una vez verificado el valor nuevo.</sub>
- ❌ El cambio se va a ver en cinco minutos en todo el mundo
  - <sub>Los resolvers que ya tenían el registro cacheado con el TTL viejo ni se enteraron de que bajaste el TTL. Siguen con su reloj anterior.</sub>
- ❌ El cambio se va a ver instantáneamente porque bajar el TTL vacía las cachés
  - <sub>Nada vacía las cachés ajenas. No existe forma de hacerlo: solo se puede esperar.</sub>
- ❌ No cambia nada, porque el TTL solo afecta a los resolvers públicos
  - <sub>El TTL gobierna todas las capas de caché por igual.</sub>

> **Por qué.** Nótese la lógica temporal: no se puede acelerar retroactivamente algo que ya fue copiado. *(Apunte §1.8)*

#### C1-25 · Caché negativa

*Opción múltiple*

Un grupo consultó `api.tudominio.me` mientras discutía cómo cargar el registro. Diez minutos después lo crea correctamente, vuelve a consultar, y sigue recibiendo NXDOMAIN. Verifican el panel tres veces y está bien. ¿Qué pasó?

- **✅** Caché negativa: el resolver memorizó que el nombre no existía y lo va a seguir contestando durante el tiempo que fija el SOA de la zona
  - <sub>Correcto. Los resolvers no solo recuerdan las respuestas afirmativas: también recuerdan los NXDOMAIN. Consultar «para ver si ya está» antes de tiempo puede, literalmente, demorar el momento en que se lo ve.</sub>
- ❌ El registro se cargó en el panel equivocado
  - <sub>Es plausible en general, pero acá el dato clave es la *consulta previa a la creación*: eso apunta directo a la caché negativa. Se confirma consultando a otro resolver.</sub>
- ❌ Falta esperar a que el registro propague desde el autoritativo
  - <sub>El autoritativo ya tiene el dato: se actualiza al instante. Lo que sobra es una copia *negativa* en el resolver.</sub>
- ❌ El TTL del registro nuevo es demasiado alto
  - <sub>El TTL del registro nuevo gobierna cuánto durará la respuesta afirmativa una vez obtenida. Lo que estorba acá es el TTL *negativo*, que fija el SOA.</sub>

> **Por qué.** `ipconfig /flushdns` limpia las capas locales, pero **no** la del proveedor, que no se puede vaciar. Lo que sí funciona es consultar a otro resolver mientras tanto. *(Apunte §1.8 y §1.8.1)*

---

### Página 10 — Filtrado y comodín

#### C1-26 · Confirmar el filtrado

*Opción múltiple*

Una estudiante corre las cuatro consultas de control desde su casa. Obtiene: `google.com` **resuelve** · la zona de la plataforma **no resuelve** · el nombre autogenerado **no resuelve** · el mismo nombre contra 8.8.8.8 **resuelve**. ¿Qué puede afirmar?

- **✅** Filtrado confirmado: el bloqueo está en el resolver de su proveedor, no en el dominio
  - <sub>Correcto, y es la única combinación que lo autoriza. La primera consulta prueba que el resolver está vivo; la segunda muestra que el bloqueo alcanza a la zona entera; la cuarta aísla la variable con otro instrumento.</sub>
- ❌ Que su resolver está caído o es inalcanzable
  - <sub>Si estuviera caído, `google.com` tampoco resolvería. Esa primera consulta es justamente la prueba de control que descarta esta hipótesis.</sub>
- ❌ Que el dominio de la plataforma fue dado de baja
  - <sub>Contra 8.8.8.8 el nombre resuelve perfecto. El dominio existe y funciona.</sub>
- ❌ Que hay un problema de caché en su equipo y basta con hacer flush
  - <sub>Una caché local no explica que otro resolver, consultado desde el mismo equipo y en el mismo momento, sí responda.</sub>

> **Por qué.** El método es el experimental clásico: **antes de medir el fenómeno hay que verificar el instrumento**. Por eso son cuatro consultas y no dos. *(Apunte §1.9.2)*

#### C1-27 · Por qué no alcanza con cambiar el resolver

*Opción múltiple*

«El filtrado se arregla poniendo 8.8.8.8 como DNS en la máquina.» ¿Por qué eso resuelve el síntoma pero no es una solución?

- **✅** Porque la aplicación seguiría siendo inaccesible para cualquier visitante cuyo proveedor aplique el mismo filtrado, y quien publica no controla los resolvers de sus visitantes
  - <sub>Exacto. El error de razonamiento es confundir la propia experiencia de acceso con la accesibilidad del servicio.</sub>
- ❌ Porque 8.8.8.8 también termina aplicando el filtrado al cabo de unas semanas
  - <sub>Las listas cambian, sí, pero el problema de fondo no es ese: es que la solución solo arregla *tu* máquina.</sub>
- ❌ Porque cambiar el resolver rompe la resolución del resto de los dominios
  - <sub>No rompe nada: 8.8.8.8 resuelve todo perfectamente. El problema es de alcance, no de funcionamiento.</sub>
- ❌ Porque el proveedor puede detectar el cambio y bloquearlo
  - <sub>No es lo que el capítulo señala. La cuestión es quién controla qué.</sub>

> **Por qué.** La única variable que está del lado del que publica es la **reputación del nombre**, y un dominio propio delegado a una zona limpia es la forma de controlarla. Por eso el dominio propio no es un adorno: es un requisito. *(Apunte §1.9.3)*

#### C1-28 · Alcance del comodín

*Verdadero/Falso*

El registro comodín `*` también hace resolver al dominio raíz pelado (`tudominio.me`, sin subdominio).

- ❌ **Verdadero**
- **✅** **Falso**

> **Por qué.** **Falso.** `*.tudominio.me` **no incluye** a `tudominio.me`. Por eso el práctico pide dos registros y no uno: el comodín para los subdominios y el registro con nombre `@` para el vértice. En cambio, el comodín sí cubre nombres de varios niveles: `a.b.tudominio.me` resuelve, si ningún nombre intermedio existe explícitamente. *(Apunte §1.12.1)*

#### C1-29 · Comodín DNS y certificado comodín

*Opción múltiple*

¿Cuál es la diferencia entre un **registro DNS comodín** y un **certificado TLS comodín**?

- **✅** El registro es un A con nombre `*`, se carga en el panel y no necesita nada más; el certificado exige el desafío DNS-01 con un token de API del proveedor DNS
  - <sub>Correcto. El primero es trivial y se usa en este módulo; el segundo tiene dificultad considerable y **no** hace falta acá, porque cada servicio de Easypanel pide su propio certificado individual por el desafío HTTP-01, que es automático.</sub>
- ❌ Son dos nombres para lo mismo: el registro comodín genera el certificado comodín
  - <sub>Son sistemas distintos que comparten el símbolo `*`. Confundirlos es la fuente de error más común de la clase.</sub>
- ❌ El certificado comodín se carga en el panel DNS y el registro en Traefik
  - <sub>Está invertido: el registro va en el panel DNS; el certificado lo gestiona Traefik.</sub>
- ❌ El registro comodín cubre un solo nivel y el certificado cubre todos
  - <sub>Es exactamente al revés: el **registro** cubre varios niveles (`a.b.dominio`), y el **certificado** `*.dominio.com` cubre un solo nivel de etiqueta.</sub>

> **Por qué.** Si leen la documentación de Easypanel sobre *wildcard domains* y se frenan pensando que necesitan un *certificate resolver* con credenciales de API: eso es para el certificado comodín, no para el registro. Con el registro `*` tipo A alcanza y sobra. *(Apunte §1.12)*

---

### Página 11 — Cierre: registros y verificación

#### C1-18 · Los dos registros del práctico

*Múltiples correctas*

¿Qué registros hay que cargar en el panel DNS para que funcione todo el práctico? (marcá todas las que correspondan)

- **✅** Un registro **A** con nombre `*` apuntando a la IP del VPS
  - <sub>Sí: el comodín hace que cualquier subdominio resuelva, sin volver a tocar el panel nunca más.</sub>
- **✅** Un registro **A** con nombre `@` apuntando a la IP del VPS
  - <sub>Sí: el comodín **no cubre el dominio raíz**, y `@` significa «el dominio raíz, sin subdominio».</sub>
- ❌ Un registro **CNAME** con nombre `www` apuntando al dominio raíz
  - <sub>No hace falta: el comodín ya cubre `www` y cualquier otro subdominio que se inventen.</sub>
- ❌ Un registro **A** por cada subdominio que vaya a publicarse
  - <sub>Eso es exactamente lo que el comodín viene a evitar. Un registro explícito solo hace falta si algún subdominio tiene que apuntar a otra dirección.</sub>

> **Por qué.** Con esos dos registros, `calculadora`, `api`, `easypanel` y cualquier nombre que se inventen en el futuro resuelven sin tocar el panel. TTL en **300** durante el práctico. *(Apunte §1.12.1 y §1.14)*

#### C1-30 · «A mí me anda»

*Opción múltiple*

Un estudiante dice que el sitio anda y tres compañeros dicen que no. Están todos en la misma aula. ¿Cómo puede ser que los cuatro digan la verdad?

- **✅** Porque están viendo cachés distintas —hasta cuatro capas, cada una con su propio reloj— y eventualmente resolvers distintos
  - <sub>Correcto: navegador, sistema operativo, router doméstico y resolver del proveedor. No las comparten todas. Además, un navegador con DoH activo esquiva el resolver de la red.</sub>
- ❌ Es imposible: si resuelve para uno tiene que resolver para todos
  - <sub>El DNS no es una guía telefónica universal: es lo que te dice el que te atiende, y cada uno puede tener una copia distinta.</sub>
- ❌ Porque el servidor atiende a algunos usuarios y a otros no según la carga
  - <sub>Si el problema fuera del servidor, habría rastro en su log. En este escenario el fallo ocurre antes de llegar ahí.</sub>
- ❌ Porque los tres que no pueden entrar tienen el navegador desactualizado
  - <sub>La versión del navegador no cambia lo que responde un resolver.</sub>

> **Por qué.** De acá sale la regla operativa: **«a mí me anda» no es una verificación**. Es una muestra de tamaño uno, tomada desde un solo resolver, con una sola caché. La verificación de verdad es **dnschecker.org**, que consulta decenas de resolvers del mundo. *(Apunte §1.8.1 y §1.10)*

#### C1-31 · DNSSEC, DoT y DoH

*Opción múltiple*

¿Cuál de estas afirmaciones sobre las tres extensiones de seguridad del DNS es correcta?

- **✅** DNSSEC autentica las respuestas pero no las cifra; DoT y DoH cifran el canal hasta el resolver, que sigue viendo todas las consultas
  - <sub>Correcto. Ninguna de las tres elimina al intermediario: **redistribuyen la confianza**. La pregunta «¿quién ve mis consultas DNS?» nunca tiene respuesta «nadie»: tiene respuesta «el que vos elegiste como resolver».</sub>
- ❌ DNSSEC cifra las consultas y por eso impide que el proveedor las lea
  - <sub>DNSSEC **autentica, no cifra**. Las consultas siguen siendo visibles para cualquier observador de la red.</sub>
- ❌ DoH impide el filtrado del proveedor para todos los visitantes del sitio
  - <sub>Un estudiante con DoH esquiva el filtrado *de su propia conexión*. Pero el que publica un servicio no puede exigirle DoH a sus visitantes.</sub>
- ❌ DNSSEC impide que un resolver se niegue a responder
  - <sub>No lo impide: un resolver siempre puede negarse. Lo que DNSSEC sí impide, en zonas firmadas y ante resolvers que validan, es la variante más grave: la **respuesta falsificada**.</sub>

> **Por qué.** Detalle que conecta con los RCODE: cuando la validación DNSSEC falla —firma vencida, cadena rota— el resolver validante responde **SERVFAIL**. Es otro de los significados posibles de ese código. *(Apunte §1.11)*

---

## Las cuatro que más se van a errar

Según lo que el capítulo señala como contraintuitivo:

1. **C1-12** — nombre que existe pero sin el tipo pedido. Casi todos contestan NXDOMAIN. Es **NOERROR con cero respuestas**, y esa distinción es la que separa «no existe» de «no hay».
2. **C1-16** — CNAME en el vértice. El distractor «sí, mientras no cargue otros registros» se lleva a los que memorizaron la regla sin entender que NS y SOA están ahí por definición.
3. **C1-24** — bajar el TTL justo antes del cambio. Es contraintuitivo: la baja del TTL también tarda el TTL viejo en verse.
4. **C1-29** — registro comodín contra certificado comodín. El capítulo lo llama «la confusión más común de esta clase», y el distractor de los niveles invertidos es el filtro fino.

Si al revisar los intentos ves que una de estas tiene menos del 50 % de acierto, no es un problema del grupo: es un tema para retomar en la clase siguiente.
