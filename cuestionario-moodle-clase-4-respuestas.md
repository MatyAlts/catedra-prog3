# Clave de corrección — Cuestionario Clase 4 (El despliegue)

> **Documento del docente. No publicar en el aula.**
> Estas son las respuestas de las 31 preguntas de `cuestionario-moodle-clase-4.xml`.
> Se genera desde la misma fuente que el XML, así que si el banco cambia, esta clave cambia con él.

- **Cuestionario:** `Clase 4 - Autoevaluación: proxy inverso, certificados y CORS`
- **Curso:** campustest.frm.utn.edu.ar → curso 14 → sección 30 «Actividades 🧩»
- **31 preguntas** en 12 páginas · 1 punto cada una, escaladas a 10
- El orden de abajo es el **orden real del cuestionario** (paginación de `cuestionario-moodle-clase-4.md` §3.1)

En Moodle el alumno ve todo esto solo: cada opción incorrecta tiene su propia explicación. Esta clave sirve para revisar el banco antes de publicarlo y para tener las respuestas a mano en clase.

---

## Resumen

| # | Pág | Tipo | Respuesta correcta | Apunte |
|---|---|---|---|---|
| **C4-01** | 1 | Opción múltiple | La petición no decía a qué sitio iba dirigida, así que cada sitio web del mundo necesitab… | §4.2 |
| **C4-02** | 1 | Opción múltiple | Porque el servidor tenía que elegir el certificado antes de poder leer la cabecera Host,… | §4.2, §4.8.2 |
| **C4-03** | 1 | Opción múltiple | Un proxy común representa al cliente ante muchos servidores; un proxy inverso representa… | §4.2 |
| **C4-04** | 1 | Opción múltiple | En lugar de leer un archivo, descubre la configuración observando el entorno: consulta al… | §4.2 |
| **C4-05** | 2 | Emparejar | _(emparejamiento — ver detalle)_ | §4.3 |
| **C4-06** | 2 | Opción múltiple | Porque no existe ningún estado del servidor producido a mano que no esté en el código: si… | §4.3.1 |
| **C4-07** | 3 | Respuesta corta | `/` o `\` o `/ ` o `raiz` o `raíz` | §3.4.1, §4.4, §4.7.1 |
| **C4-28** | 3 | Opción múltiple | Que son dos programas independientes que no comparten nada salvo el formato del JSON, y e… | §4.4 |
| **C4-29** | 3 | Opción múltiple | Solo los dos del proyecto, nunca «All repositories» | §4.6 |
| **C4-09** | 4 | Opción múltiple | 404: ningún enrutador coincidió, el nombre no está asociado a ningún servicio. 502: el en… | §3.5.5, §4.8.1, §4.14 |
| **C4-10** | 4 | Opción múltiple | Es el puerto interno del contenedor: le dice a Traefik a qué puerto entregar el tráfico,… | §4.7.3, §4.9.3 |
| **C4-08** | 5 | Emparejar | _(emparejamiento — ver detalle)_ | §4.8.1 |
| **C4-12** | 6 | Opción múltiple | Que el dominio resuelva hacia el VPS (Clase 1) y que el puerto 80 esté abierto (Clase 2) | §4.8.3 |
| **C4-26** | 6 | Opción múltiple | Se cerró el puerto 80 después del despliegue inicial: la renovación también lo necesita | §4.8.3, §4.14 |
| **C4-11** | 7 | Emparejar | _(emparejamiento — ver detalle)_ | §1.12.2, §4.8.3 |
| **C4-31** | 7 | Opción múltiple | Que los dominios autogenerados pasan a ser subdominios del dominio propio, que ningún pro… | §4.5.1 |
| **C4-13** | 8 | Opción múltiple | https://api.tudominio.com | §4.9.2 |
| **C4-25** | 8 | Opción múltiple | config.js no se generó, así que el frontend quedó con un valor por defecto: falta cargar… | §4.9.4, §4.14 |
| **C4-14** | 9 | Opción múltiple | El esquema, el anfitrión y el puerto, comparados literalmente | §4.10.1 |
| **C4-15** | 9 | Opción múltiple | Contra que un sitio cualquiera lea, en tu nombre, los datos que otro sitio te devuelve us… | §4.10.2 |
| **C4-16** | 9 | Opción múltiple | El servidor de destino, declarándolo en cabeceras de respuesta que el navegador lee y apl… | §4.10.2 |
| **C4-17** | 10 | Opción múltiple | Porque el Content-Type: application/json no es uno de los tipos históricos de los formula… | §4.10.3, §4.11.1 |
| **C4-18** | 10 | Múltiples correctas | http://calculadora.tudominio.com + https://calculadora.tudominio.com/ + https://www.calculadora.tudominio.com | §4.10.4 |
| **C4-19** | 11 | Verdadero/Falso | **FALSO** | §4.10.5 |
| **C4-20** | 11 | Opción múltiple | Los dos: el servidor contestó correctamente y el navegador descartó la respuesta porque n… | §4.10.5 |
| **C4-21** | 11 | Opción múltiple | Redesplegar: las variables de entorno se leen al arrancar el proceso | §4.12 |
| **C4-30** | 11 | Opción múltiple | Porque esa página está servida por el mismo origen que la API: no hay dos orígenes involu… | §4.7.4 |
| **C4-22** | 12 | Opción múltiple | Que el navegador ni siquiera emite la primera petición insegura: la redirección todavía i… | §4.13.1 |
| **C4-23** | 12 | Opción múltiple | Se degrada silenciosamente: el navegador intenta QUIC, no recibe respuesta y vuelve a HTT… | §4.13.2 |
| **C4-24** | 12 | Opción múltiple | El frontend se sirve por HTTPS y API_URL quedó en http:// | §4.14 |
| **C4-27** | 12 | Opción múltiple | Diagnosticar siempre a partir del mensaje exacto de la consola del navegador, nunca del c… | §4.1, §4.14 |

## Cobertura del capítulo

| Sección del apunte | Preguntas que la evalúan |
|---|---|
| §1.12.2 | C4-11 |
| §3.4.1 | C4-07 |
| §3.5.5 | C4-09 |
| §4.1 | C4-27 |
| §4.2 | C4-01, C4-02, C4-03, C4-04 |
| §4.3 | C4-05 |
| §4.3.1 | C4-06 |
| §4.4 | C4-07, C4-28 |
| §4.5.1 | C4-31 |
| §4.6 | C4-29 |
| §4.7.1 | C4-07 |
| §4.7.3 | C4-10 |
| §4.7.4 | C4-30 |
| §4.8.1 | C4-08, C4-09 |
| §4.8.2 | C4-02 |
| §4.8.3 | C4-11, C4-12, C4-26 |
| §4.9.2 | C4-13 |
| §4.9.3 | C4-10 |
| §4.9.4 | C4-25 |
| §4.10.1 | C4-14 |
| §4.10.2 | C4-15, C4-16 |
| §4.10.3 | C4-17 |
| §4.10.4 | C4-18 |
| §4.10.5 | C4-19, C4-20 |
| §4.11.1 | C4-17 |
| §4.12 | C4-21 |
| §4.13.1 | C4-22 |
| §4.13.2 | C4-23 |
| §4.14 | C4-09, C4-24, C4-25, C4-26, C4-27 |

---

## Detalle por página

### Página 1 — Por qué existe el proxy inverso

#### C4-01 · La carencia de HTTP/1.0

*Opción múltiple*

La primera versión masiva de HTTP tenía una carencia que hoy parece increíble. ¿Cuál era, y qué consecuencia estructural tenía?

- **✅** La petición no decía a qué sitio iba dirigida, así que cada sitio web del mundo necesitaba su propia dirección IP
  - <sub>Correcto. El cliente abría una conexión a una IP y pedía `GET /index.html`; el servidor no tenía forma de saber si el usuario había escrito empresa-a.com o empresa-b.com. Con 4.300 millones de direcciones y una web creciendo exponencialmente, ese modelo tenía fecha de vencimiento.</sub>
- ❌ No soportaba cifrado, así que todo el tráfico viajaba en texto plano
  - <sub>Cierto pero no es la carencia que da origen al alojamiento virtual. HTTPS llegó después y trajo su propio problema, que resolvió SNI.</sub>
- ❌ No permitía más de una petición por conexión
  - <sub>Ese es el problema que resolvió HTTP/2 multiplexando, en 2015. Otro asunto y otra época.</sub>
- ❌ No incluía códigos de estado para informar errores
  - <sub>Los códigos de estado existen desde el principio.</sub>

> **Por qué.** HTTP/1.1, en 1997, lo resolvió con una decisión mínima y enorme: **hizo obligatoria la cabecera Host**. La técnica se llama alojamiento virtual y es la que sostiene económicamente a la web tal como la conocemos. *(Apunte §4.2)*

#### C4-02 · Qué resolvió SNI

*Opción múltiple*

Cuando apareció el cifrado, el alojamiento virtual y HTTPS fueron incompatibles durante años. ¿Por qué, y cómo se resolvió?

- **✅** Porque el servidor tenía que elegir el certificado antes de poder leer la cabecera Host, que viaja cifrada; SNI hace que el cliente declare el nombre en claro al inicio del saludo
  - <sub>Exacto: un problema de huevo y gallina. La extensión SNI se incorporó a TLS en 2003 y es la razón por la que hoy un VPS de diez dólares puede alojar veinte sitios con certificado propio.</sub>
- ❌ Porque los certificados no podían emitirse para más de un dominio
  - <sub>Los certificados multi-dominio existen, pero no es el problema: el problema era *elegir* cuál presentar antes de saber qué pidió el cliente.</sub>
- ❌ Porque el cifrado consumía demasiados recursos para varios sitios a la vez
  - <sub>Es una cuestión lógica, no de rendimiento.</sub>
- ❌ Porque cada sitio necesitaba su propio puerto además de su propio certificado
  - <sub>Todos comparten el 443. La distinción la hace el nombre, no el puerto.</sub>

> **Por qué.** En una conexión HTTPS el nombre viaja **dos veces**: primero en claro en el SNI, para elegir el certificado; después cifrado, en la cabecera Host. Un desacuerdo entre ambos es una anomalía que los proxies modernos rechazan. *(Apunte §4.2 y §4.8.2)*

#### C4-03 · Qué es un proxy inverso

*Opción múltiple*

¿Cuál es la diferencia entre un proxy común y un proxy inverso?

- **✅** Un proxy común representa al cliente ante muchos servidores; un proxy inverso representa a muchos servidores ante todos los clientes
  - <sub>Correcto. El proxy inverso ocupa los puertos 80 y 443, termina el cifrado, lee el nombre solicitado y reparte hacia el proceso interno que corresponda.</sub>
- ❌ Un proxy inverso solo funciona con HTTPS y el común solo con HTTP
  - <sub>Los dos manejan ambos. La diferencia es a quién representan.</sub>
- ❌ Un proxy inverso está dentro de la red del cliente y el común en la del servidor
  - <sub>Está exactamente al revés.</sub>
- ❌ Un proxy inverso cachea respuestas y el común no
  - <sub>El cacheo lo pueden hacer los dos; no es lo que los define.</sub>

> **Por qué.** La ventaja no es solo el reparto: al concentrar la terminación TLS en un único lugar, los certificados se gestionan una vez y **las aplicaciones internas quedan liberadas de saber nada sobre criptografía**. *(Apunte §4.2)*

#### C4-04 · Qué hace distinto a Traefik

*Opción múltiple*

Los proxies inversos clásicos —nginx, Apache— se configuran con archivos que hay que editar y recargar. ¿Qué cambió Traefik?

- **✅** En lugar de leer un archivo, descubre la configuración observando el entorno: consulta al motor de Docker qué contenedores existen y qué etiquetas tienen
  - <sub>Correcto. Con contenedores que nacen y mueren permanentemente, el modelo de archivo no escala. Cuando Easypanel levanta un contenedor nuevo con la etiqueta correcta, nadie edita ni recarga nada: Traefik ya lo vio.</sub>
- ❌ Reemplazó los archivos de texto por una base de datos de configuración
  - <sub>No hay base de datos: hay observación del entorno en tiempo real.</sub>
- ❌ Es más rápido porque está escrito en Go en lugar de C
  - <sub>El lenguaje no es lo relevante. Lo relevante es el modelo de configuración.</sub>
- ❌ Incluye un certificado comodín preinstalado para cualquier dominio
  - <sub>No existe tal cosa. Traefik pide certificados a Let's Encrypt por ACME, dominio por dominio.</sub>

> **Por qué.** Quedate con la idea que ordena todo el capítulo: **hay un solo proceso atendiendo el 80 y el 443 de tu servidor, y no es tu aplicación. Es Traefik.** Todo lo que configures en «Domains & Proxy» no le está hablando a tu aplicación: le está hablando al portero. *(Apunte §4.2)*

---

### Página 2 — Qué hace Easypanel

#### C4-05 · Los tres componentes de Easypanel

*Emparejar*

Easypanel es una interfaz sobre tres componentes que ya existían. Emparejá cada uno con lo que ocurre si falla.

| Se empareja | Con |
|---|---|
| **Docker** | La construcción no termina |
| **Traefik** | 502, 404, o el dominio directamente no responde |
| **Let's Encrypt** | El sitio queda sin HTTPS |

> **Por qué.** Easypanel no aporta funcionalidad sino una **capa de traducción**: convierte lo del formulario en etiquetas de Docker, variables de entorno y órdenes de construcción. Su costo es que, cuando falla, el error aparece expresado en el vocabulario del componente subyacente y no en el del formulario que completaste. Diagnosticar es preguntarse: **¿esto es problema de Docker, de Traefik o del certificado?** *(Apunte §4.3)*

#### C4-06 · El repositorio como única fuente de verdad

*Opción múltiple*

Easypanel no recibe archivos cargados manualmente: clona un repositorio. ¿Por qué es una decisión de arquitectura y no de comodidad?

- **✅** Porque no existe ningún estado del servidor producido a mano que no esté en el código: si el servidor se pierde entero, se reconstruye clonando y desplegando
  - <sub>Correcto. Es la misma idea de la sección 3.2 —el entorno es un artefacto versionado— llevada al despliegue completo.</sub>
- ❌ Porque subir archivos por FTP es inseguro
  - <sub>La seguridad del transporte no es el punto; el punto es la reproducibilidad.</sub>
- ❌ Porque Docker solo puede construir desde repositorios Git
  - <sub>Docker construye desde cualquier directorio. La restricción la impone Easypanel a propósito.</sub>
- ❌ Porque así se ahorra espacio en disco en el servidor
  - <sub>El repositorio se clona igual en el servidor: no se ahorra nada.</sub>

> **Por qué.** Si Easypanel no encuentra un Dockerfile intenta deducir el tipo de aplicación con Nixpacks o Buildpacks. Funciona bien para proyectos estándar, pero es una caja negra: cuando falla, no hay archivo que leer. Este proyecto trae sus propios Dockerfile justamente para no depender de eso. *(Apunte §4.3.1)*

---

### Página 3 — Repositorios y construcción

#### C4-07 · El Build path

*Respuesta corta*

El proyecto está en dos repositorios independientes, cada uno con la aplicación en su raíz. ¿Qué valor va en el campo **Build path** de Easypanel? (escribí solo el valor)

Respuestas aceptadas (sin distinguir mayúsculas): `/`, `\`, `/ `, `raiz`, `raíz`

> **Por qué.** Va `/`, no `/backend` ni `/frontend`. Si seguís una guía escrita para monorepositorio y ponés `/backend`, Docker va a buscar un directorio que en ese repositorio no existe, y la construcción falla con un mensaje que **no menciona el Build path por ningún lado**. El Build path es literalmente el contexto de construcción de §3.4.1. *(Apunte §4.4 y §4.7.1)*

#### C4-28 · Polirepositorio

*Opción múltiple*

El proyecto usa dos repositorios independientes en lugar de uno solo. ¿Cuál es el argumento del capítulo?

- **✅** Que son dos programas independientes que no comparten nada salvo el formato del JSON, y es lo habitual cuando frontend y backend los mantienen equipos distintos
  - <sub>Correcto. Meterlos en el mismo repositorio contradiría el mensaje que el README viene dando desde el principio.</sub>
- ❌ Que un monorepositorio no permite desplegar servicios por separado
  - <sub>Sí lo permite, con filtros por ruta. La elección no es técnica sino organizativa.</sub>
- ❌ Que Easypanel no soporta monorepositorios
  - <sub>Los soporta: bastaría con poner `/backend` en el Build path.</sub>
- ❌ Que los repositorios grandes son más lentos de clonar
  - <sub>No es el argumento del capítulo, y a esta escala sería irrelevante.</sub>

> **Por qué.** La elección entre mono y polirepositorio es una de las discusiones recurrentes de la ingeniería de software y **no tiene respuesta universal**: depende de si los componentes se despliegan juntos, de si los mantienen los mismos equipos y de qué tan acoplados están sus cambios. *(Apunte §4.4)*

#### C4-29 · Acceso a los repositorios de GitHub

*Opción múltiple*

Al conectar Easypanel con GitHub, ¿qué repositorios conviene autorizar?

- **✅** Solo los dos del proyecto, nunca «All repositories»
  - <sub>Correcto: es mínimo privilegio (§2.12.1) aplicado acá. Si mañana el servidor queda comprometido, el atacante llega **hasta donde vos le dijiste que llegara**. Darle acceso a todos tus repositorios para ahorrar dos clics es el tipo de decisión que se lamenta después.</sub>
- ❌ Todos, porque después es engorroso agregar repositorios de a uno
  - <sub>Agregar uno más lleva treinta segundos. Recuperarse de una filtración, no.</sub>
- ❌ Solo los públicos, porque los privados no se pueden clonar
  - <sub>Los privados se clonan perfectamente: para eso está la autorización.</sub>
- ❌ Ninguno: conviene usar una clave de despliegue por repositorio
  - <sub>Es una alternativa válida en otros contextos, pero no es lo que plantea el capítulo para este flujo.</sub>

> **Por qué.** *(Apunte §4.6)*

---

### Página 4 — Cómo decide Traefik

#### C4-09 · 404 contra 502

*Opción múltiple*

En el modelo de Traefik, ¿qué distingue un **404** de un **502**?

- **✅** 404: ningún enrutador coincidió, el nombre no está asociado a ningún servicio. 502: el enrutador coincidió y el servicio no contestó o contestó algo inválido
  - <sub>Correcto, y no es casual que sean dos errores distintos: cada uno señala una **etapa distinta de la cadena**. El 404 es un problema de configuración de dominio; el 502, de puerto o de interfaz de escucha.</sub>
- ❌ 404: el archivo no existe en el servidor. 502: el servidor está caído
  - <sub>Ese es el significado genérico de HTTP. Acá los emite **Traefik**, y su significado es más específico: hablan de la cadena de enrutamiento.</sub>
- ❌ 404: el certificado no se emitió. 502: el DNS no resuelve
  - <sub>Si el DNS no resuelve, no llega ninguna petición y no hay código de estado que ver.</sub>
- ❌ Son intercambiables: dependen de la versión de Traefik
  - <sub>Confundirlos manda a buscar el problema al lugar equivocado, que es exactamente lo que hay que evitar.</sub>

> **Por qué.** Un 502 con el puerto correcto en el formulario apunta a otra cosa: el proceso está escuchando en `127.0.0.1` en lugar de `0.0.0.0` (§3.5.5). *(Apunte §4.8.1 y §4.14)*

#### C4-10 · El puerto de Domains & Proxy

*Opción múltiple*

En «Domains & Proxy» se carga el puerto 8000 para la API. ¿Qué significa ese número?

- **✅** Es el puerto **interno del contenedor**: le dice a Traefik a qué puerto entregar el tráfico, sin abrir nada en el VPS
  - <sub>Correcto. Si corrés `nmap` desde afuera, el 8000 sigue cerrado. Traefik entra por el 443 y reparte por adentro.</sub>
- ❌ Es el puerto que se abre en el firewall del VPS para ese servicio
  - <sub>No se abre ningún puerto. Los únicos abiertos siguen siendo 22, 80 y 443.</sub>
- ❌ Es el puerto público por el que los visitantes acceden al servicio
  - <sub>Los visitantes entran por el 443. Nadie escribe `:8000` en la URL.</sub>
- ❌ Es el puerto que Docker publica hacia el anfitrión con -p
  - <sub>No hay publicación con `-p`: la comunicación es por la red interna del proyecto.</sub>

> **Por qué.** En el frontend ese valor es **80**, no 8000, porque nginx escucha en el 80. Es el error más repetido de la clase: se copia la configuración del backend y se cambia solo el dominio. El síntoma es un 502. *(Apunte §4.7.3 y §4.9.3)*

---

### Página 5 — El modelo de enrutamiento

#### C4-08 · El modelo de Traefik

*Emparejar*

Emparejá cada concepto del modelo de Traefik con lo que es en este proyecto.

| Se empareja | Con |
|---|---|
| **Punto de entrada (entrypoint)** | Un puerto en el que Traefik escucha: el 80 y el 443 |
| **Enrutador (router)** | Una regla que decide qué peticiones toma: Host(api.tudominio.com) |
| **Middleware** | Una transformación intermedia opcional: la redirección de HTTP a HTTPS |
| **Servicio (service)** | El destino interno al que se entrega: el contenedor api, puerto 8000 |

> **Por qué.** La secuencia es: llega una petición a un punto de entrada, se evalúan los enrutadores hasta encontrar uno cuya regla coincida, se aplican sus middlewares, y se entrega al servicio. Esa cadena explica de forma exacta los dos códigos de error más frecuentes del capítulo. *(Apunte §4.8.1)*

---

### Página 6 — Certificados: el protocolo ACME

#### C4-12 · Los dos requisitos del certificado

*Opción múltiple*

El certificado no se emite. Antes de tocar un solo botón del panel, ¿qué dos cosas hay que verificar?

- **✅** Que el dominio resuelva hacia el VPS (Clase 1) y que el puerto 80 esté abierto (Clase 2)
  - <sub>Correcto: el 90 % de las veces es una de esas dos, y ninguna se arregla desde Easypanel. `nslookup` del dominio y `nmap` del puerto 80. Si esos dos dan bien, entonces sí, mirá los logs de Traefik.</sub>
- ❌ Que el puerto 443 esté abierto y que el servicio esté corriendo
  - <sub>El desafío HTTP-01 se valida por el **puerto 80**, no por el 443. Y el servicio puede estar caído: el certificado se emite igual.</sub>
- ❌ Que el registro CAA autorice a Traefik y que el TTL sea bajo
  - <sub>El CAA autoriza *autoridades certificadoras*, no proxies. Y el TTL no interviene en la emisión.</sub>
- ❌ Que el dominio esté registrado a nombre del titular en el WHOIS
  - <sub>Let's Encrypt no consulta el WHOIS: comprueba control técnico, no titularidad registral.</sub>

> **Por qué.** Los certificados duran **90 días** y la renovación se intenta a los 60. Esa duración corta es deliberada: obliga a que la renovación esté automatizada. Consecuencia práctica: **el puerto 80 tiene que quedar abierto para siempre**, no solo el día del despliegue. *(Apunte §4.8.3)*

#### C4-26 · El certificado dejó de renovarse

*Opción múltiple*

Todo funcionó tres meses y de golpe el sitio queda sin HTTPS. ¿Cuál es la causa más probable?

- **✅** Se cerró el puerto 80 después del despliegue inicial: la renovación también lo necesita
  - <sub>Correcto. Los certificados duran 90 días y la renovación usa el mismo desafío HTTP-01 que la emisión. El puerto 80 tiene que quedar abierto **para siempre**.</sub>
- ❌ Let's Encrypt dio de baja el dominio por inactividad
  - <sub>Let's Encrypt no da de baja dominios: emite y renueva mientras se pueda validar.</sub>
- ❌ El registro DNS expiró y hay que volver a cargarlo
  - <sub>Los registros DNS no expiran solos. El TTL gobierna la caché, no la existencia del registro.</sub>
- ❌ Traefik necesita reiniciarse cada 90 días
  - <sub>Traefik renueva solo, sin reinicio, si puede completar el desafío.</sub>

> **Por qué.** Es exactamente el tipo de fallo que aparece meses después de que alguien «ordenó» el firewall. *(Apunte §4.8.3 y §4.14)*

---

### Página 7 — Los desafíos de ACME

#### C4-11 · Los desafíos de ACME

*Emparejar*

Emparejá cada desafío del protocolo ACME con lo que pide demostrar.

| Se empareja | Con |
|---|---|
| **HTTP-01** | Control del servidor al que apunta el nombre: servir un archivo por el puerto 80 |
| **DNS-01** | Control de la zona DNS: publicar un registro TXT con un valor dado |
| **TLS-ALPN-01** | Control del servicio TLS: responder el saludo TLS de una forma particular |

> **Por qué.** Traefik usa **HTTP-01**. El DNS-01 es el que se mencionó en §1.12.2 al explicar el certificado comodín: como no requiere conectarse al servidor sino publicar un registro en la zona, es el único que puede validar un nombre con asterisco, y por eso exige credenciales de API del proveedor DNS. *(Apunte §4.8.3)*

#### C4-31 · El dominio predeterminado del panel

*Opción múltiple*

Configurar el dominio propio como dominio predeterminado de Easypanel (Settings → Domain) tiene un efecto que conecta con la Clase 1. ¿Cuál?

- **✅** Que los dominios autogenerados pasan a ser subdominios del dominio propio, que ningún proveedor filtra, en lugar de subdominios de easypanel.host
  - <sub>Correcto: combinado con el registro comodín, elimina de raíz el problema de resolución descrito en §1.9.</sub>
- ❌ Que se emite un certificado comodín para todos los servicios de una vez
  - <sub>Cada servicio sigue pidiendo su propio certificado individual por HTTP-01.</sub>
- ❌ Que ya no hace falta cargar el registro comodín en el panel DNS
  - <sub>Al contrario: el comodín es lo que hace que esos subdominios resuelvan.</sub>
- ❌ Que el panel deja de ser accesible por la IP del VPS
  - <sub>Eso es un paso aparte de la Clase 2: cerrar el acceso directo por el puerto 3000.</sub>

> **Por qué.** *(Apunte §4.5.1)*

---

### Página 8 — El frontend y su variable

#### C4-13 · API_URL del frontend

*Opción múltiple*

¿Cuál de estos valores de `API_URL` es el correcto para el servicio web?

- **✅** `https://api.tudominio.com`
  - <sub>Correcto: con `https://`, sin barra al final y sin la ruta del endpoint.</sub>
- ❌ `http://api.tudominio.com`
  - <sub>Con `http://` el navegador bloquea el pedido por **contenido mixto**: una página segura no puede consumir un recurso inseguro.</sub>
- ❌ `https://api.tudominio.com/`
  - <sub>La barra final rompe: el JavaScript le concatena `/api/calcular` y queda una doble barra.</sub>
- ❌ `https://api.tudominio.com/api/calcular`
  - <sub>Va el dominio pelado, no la ruta del endpoint: el código la agrega.</sub>

> **Por qué.** Los tres detalles rompen el despliegue, y ninguno da un mensaje que mencione la variable. *(Apunte §4.9.2)*

#### C4-25 · ERR_CONNECTION_REFUSED hacia 127.0.0.1

*Opción múltiple*

El navegador informa `ERR_CONNECTION_REFUSED` hacia `127.0.0.1` al intentar usar la calculadora publicada. ¿Qué ocurrió?

- **✅** `config.js` no se generó, así que el frontend quedó con un valor por defecto: falta cargar `API_URL` en el servicio web
  - <sub>Correcto. Se verifica en la pestaña Logs del servicio web: debe figurar «config.js generado con API_URL=...». Si aparece el aviso de variable no definida, falta cargarla.</sub>
- ❌ El backend está escuchando en 127.0.0.1 dentro del contenedor
  - <sub>Ese error se manifestaría como un **502** desde Traefik, no como un intento del navegador hacia su propio equipo.</sub>
- ❌ El firewall del VPS está bloqueando el puerto 8000
  - <sub>El navegador está intentando conectarse a `127.0.0.1`, que es la máquina del propio visitante. El VPS ni se enteró.</sub>
- ❌ El certificado del backend no se emitió
  - <sub>Sería un error de certificado, no de conexión rechazada hacia el bucle local.</sub>

> **Por qué.** Fijate en la pista: `127.0.0.1` es *la computadora del visitante*. Que el frontend intente ir ahí significa que nunca recibió la URL real de la API. *(Apunte §4.9.4 y §4.14)*

---

### Página 9 — Orígenes

#### C4-14 · Qué es un origen

*Opción múltiple*

Según la RFC 6454, ¿qué componentes forman un **origen**?

- **✅** El esquema, el anfitrión y el puerto, comparados literalmente
  - <sub>Correcto. Dos URL pertenecen al mismo origen si y solo si coinciden los tres. La **ruta no forma parte** del origen, y la comparación no interpreta nada.</sub>
- ❌ El dominio y el subdominio, sin importar el esquema
  - <sub>El esquema importa: `http://` y `https://` son orígenes distintos aunque el dominio coincida.</sub>
- ❌ El esquema, el anfitrión, el puerto y la ruta
  - <sub>La ruta **no** forma parte del origen. `/index.html` y `/api/x` son el mismo origen.</sub>
- ❌ La dirección IP del servidor y el puerto
  - <sub>Se compara el *nombre*, no la IP. Dos nombres que resuelven a la misma IP son orígenes distintos.</sub>

> **Por qué.** Por eso `tudominio.com` y `www.tudominio.com` son dos anfitriones distintos, aunque para una persona sean «el mismo sitio». *(Apunte §4.10.1)*

#### C4-15 · Por qué existe la política de mismo origen

*Opción múltiple*

¿Contra qué protege la política de mismo origen?

- **✅** Contra que un sitio cualquiera lea, en tu nombre, los datos que otro sitio te devuelve usando tus cookies
  - <sub>Exacto: si estás autenticado en tu banco y abrís otra pestaña con un sitio cualquiera, ese sitio podría hacer una petición al banco y el navegador adjuntaría tus cookies automáticamente. La política impide que el código de ese sitio **lea la respuesta**.</sub>
- ❌ Contra que un servidor reciba peticiones de clientes no autorizados
  - <sub>La petición muchas veces *llega a emitirse*. Lo que se bloquea es la lectura de la respuesta por parte del código, del lado del navegador.</sub>
- ❌ Contra la interceptación del tráfico en la red
  - <sub>De eso se ocupa TLS. La política de mismo origen es del navegador, sobre contenido ya descifrado.</sub>
- ❌ Contra la ejecución de JavaScript malicioso en la página
  - <sub>Eso es CSP. La política de mismo origen no impide ejecutar código: impide leer datos ajenos.</sub>

> **Por qué.** La regla la introdujo Netscape en 1995 y hoy es el pilar de la seguridad del navegador: **el código de un origen no puede leer los datos de otro origen**. *(Apunte §4.10.2)*

#### C4-16 · Quién otorga el permiso en CORS

*Opción múltiple*

En el mecanismo CORS, ¿quién decide si un origen está autorizado?

- **✅** El servidor de destino, declarándolo en cabeceras de respuesta que el navegador lee y aplica
  - <sub>Correcto: el permiso lo otorga el servidor de destino, no el que pide. La API declara qué orígenes están autorizados a leerla; el navegador lee esa declaración y decide.</sub>
- ❌ El navegador, según una lista de dominios confiables del usuario
  - <sub>El navegador *aplica* la política, pero no decide qué orígenes se autorizan: eso lo declara el servidor.</sub>
- ❌ El origen que hace la petición, declarando su identidad
  - <sub>Si el que pide pudiera autoautorizarse, el mecanismo no serviría de nada.</sub>
- ❌ El proxy inverso, en función de la cabecera Host
  - <sub>Traefik no interviene en CORS: son cabeceras que emite la aplicación.</sub>

> **Por qué.** CORS es un mecanismo para **relajar de forma controlada** una política deliberadamente restrictiva, cuando el acceso entre orígenes es legítimo. *(Apunte §4.10.2)*

---

### Página 10 — La verificación previa

#### C4-17 · Por qué hay dos peticiones

*Opción múltiple*

Al hacer una operación en la calculadora, la pestaña Red muestra **dos** peticiones: un OPTIONS y después un POST. ¿Por qué?

- **✅** Porque el `Content-Type: application/json` no es uno de los tipos históricos de los formularios HTML, y eso dispara la verificación previa
  - <sub>Correcto. Se consideran «simples» —y viajan sin preflight— las peticiones GET, HEAD y POST con uno de los tres tipos de contenido históricos. JSON es «cualquier otra cosa».</sub>
- ❌ Porque la primera petición falla y el navegador reintenta automáticamente
  - <sub>El OPTIONS no falla: debe dar 200. Son dos peticiones con propósitos distintos, no un reintento.</sub>
- ❌ Porque el frontend envía los datos dos veces por seguridad
  - <sub>El OPTIONS no lleva los datos: pregunta si la petición real va a ser autorizada.</sub>
- ❌ Porque HTTP/2 multiplexa las peticiones en pares
  - <sub>La multiplexación no duplica peticiones. Esto es CORS, no transporte.</sub>

> **Por qué.** Si el preflight no autoriza explícitamente el origen, el método y las cabeceras solicitadas, **la petición real nunca se emite**. Que aparezcan exactamente dos, y en ese orden, es la confirmación empírica de que todo está bien. *(Apunte §4.10.3 y §4.11.1)*

#### C4-18 · Qué cuenta como origen distinto

*Múltiples correctas*

El frontend está en `https://calculadora.tudominio.com`. ¿Cuáles de estos valores en `ORIGENES_PERMITIDOS` **fallarían**? (marcá todas las que correspondan)

- **✅** `http://calculadora.tudominio.com`
  - <sub>Falla: el esquema forma parte del origen. http y https son orígenes distintos.</sub>
- **✅** `https://calculadora.tudominio.com/`
  - <sub>Falla: la barra final. El origen se declara sin barra.</sub>
- **✅** `https://www.calculadora.tudominio.com`
  - <sub>Falla: `www.` lo convierte en otro anfitrión. Si hacen falta los dos, se declaran ambos separados por comas.</sub>
- ❌ `https://calculadora.tudominio.com`
  - <sub>Este es el correcto: esquema, anfitrión y puerto implícito coinciden exactamente.</sub>

> **Por qué.** Las tres fallas son consecuencias directas de la definición literal de origen. **No hay excepciones ni tolerancia: la comparación es de cadenas.** *(Apunte §4.10.4)*

---

### Página 11 — Qué protege CORS y qué no

#### C4-19 · CORS protege la API

*Verdadero/Falso*

Configurar `ORIGENES_PERMITIDOS` impide que otros consuman tu API.

- ❌ **Verdadero**
- **✅** **Falso**

> **Por qué.** **Falso, y es el punto que más se malinterpreta. CORS no protege la API.** Es una política que el navegador aplica a favor del usuario, para impedir que un sitio cualquiera lea datos de otro en su nombre. No es un control de acceso del servidor. Un cliente que no sea un navegador —`curl`, un script de Python, otro servidor— ignora CORS por completo, porque no tiene usuario a quien proteger ni cookies ajenas que adjuntar. Si la API tiene que restringir quién la consume, eso se hace con **autenticación y autorización en el servidor**, que es un mecanismo completamente distinto. *(Apunte §4.10.5)*

#### C4-20 · El log dice 200 y el frontend dice que falló

*Opción múltiple*

El log del backend muestra la petición entrando y saliendo con un 200 impecable, y al mismo tiempo el frontend reporta un error de CORS. ¿Quién tiene razón?

- **✅** Los dos: el servidor contestó correctamente y el navegador descartó la respuesta porque no traía el permiso
  - <sub>Exacto. CORS lo aplica el **navegador**, no el servidor. Por eso, si el `fetch` falla pero un `curl` a la misma URL anda, ya sabés dónde mirar. Y no es en el servidor.</sub>
- ❌ El backend: si devolvió 200, el frontend tiene un error de programación
  - <sub>El 200 es real y el error del frontend también. No se contradicen: describen momentos distintos del recorrido.</sub>
- ❌ El frontend: el 200 del log corresponde a otra petición
  - <sub>Corresponde exactamente a esa petición. El servidor la procesó y respondió.</sub>
- ❌ Ninguno: es un problema de red intermitente
  - <sub>No hay nada intermitente: va a fallar todas las veces, de forma perfectamente reproducible.</sub>

> **Por qué.** Es el mismo patrón epistemológico de `ufw status` en la Clase 2: cada herramienta te informa sobre lo que *ella* ve. *(Apunte §4.10.5)*

#### C4-21 · El redespliegue

*Opción múltiple*

Un grupo corrige `ORIGENES_PERMITIDOS`, guarda, prueba, y sigue fallando igual. ¿Qué falta?

- **✅** Redesplegar: las variables de entorno se leen al arrancar el proceso
  - <sub>Correcto. Vas a corregir el valor, guardar, probar, seguir fallando y pensar que pusiste mal el valor. No: te faltó el **Deploy**.</sub>
- ❌ Esperar a que expire la caché del navegador
  - <sub>El navegador no cachea la política de origen del servidor más allá de `Access-Control-Max-Age`, y eso solo afecta al preflight.</sub>
- ❌ Reiniciar Traefik para que tome la configuración nueva
  - <sub>Traefik no interviene en CORS: las cabeceras las emite la aplicación.</sub>
- ❌ Volver a emitir el certificado
  - <sub>El certificado no tiene nada que ver con la autorización de orígenes.</sub>

> **Por qué.** Cambiar una variable de entorno **no tiene efecto hasta el redespliegue**. *(Apunte §4.12)*

#### C4-30 · El experimento de /docs

*Opción múltiple*

Abrir `https://api.tudominio.com/docs` y hacer una operación desde ahí funciona perfecto, sin ningún problema de CORS. ¿Por qué?

- **✅** Porque esa página está servida por el **mismo origen** que la API: no hay dos orígenes involucrados
  - <sub>Exacto, y esa observación es media clase de CORS: el problema nunca fue la API, es la combinación de dos orígenes distintos.</sub>
- ❌ Porque FastAPI desactiva CORS en su documentación interactiva
  - <sub>No desactiva nada. Simplemente no hace falta: no hay cruce de orígenes.</sub>
- ❌ Porque la documentación usa un cliente HTTP distinto al del frontend
  - <sub>Usa `fetch` desde el navegador, igual que el frontend.</sub>
- ❌ Porque el navegador confía en las páginas servidas por HTTPS
  - <sub>El esquema no otorga confianza entre orígenes distintos.</sub>

> **Por qué.** Guardalo, porque en diez minutos van a ver el mismo endpoint fallando desde el frontend. *(Apunte §4.7.4)*

---

### Página 12 — Evolución y diagnóstico

#### C4-22 · HSTS

*Opción múltiple*

¿Qué agrega HSTS respecto de una simple redirección de HTTP a HTTPS?

- **✅** Que el navegador ni siquiera emite la primera petición insegura: la redirección todavía implica una petición que alguien podría interceptar
  - <sub>Correcto, y la diferencia es sutil y significativa. Es el mecanismo detrás de la lista de precarga que se mencionó en §1.13 a propósito de los dominios `.app` y `.dev`.</sub>
- ❌ Que cifra la conexión con un algoritmo más fuerte
  - <sub>HSTS no toca la criptografía: es una directiva de política que el navegador recuerda.</sub>
- ❌ Que impide que el sitio se sirva por HTTP en el servidor
  - <sub>El servidor puede seguir escuchando en el 80 —de hecho debe, para ACME—. Lo que cambia es el comportamiento del *navegador*.</sub>
- ❌ Que agrega el dominio automáticamente a la lista de precarga de los navegadores
  - <sub>La precarga es un trámite aparte que se solicita explícitamente.</sub>

> **Por qué.** La otra cabecera importante es **CSP**, que declara de qué orígenes puede el navegador cargar scripts, estilos e imágenes. Su lógica es la misma de todo el capítulo: una lista blanca declarada por el servidor y aplicada por el cliente. *(Apunte §4.13.1)*

#### C4-23 · HTTP/3 y el firewall

*Opción múltiple*

Un firewall permite TCP en el 443 pero descarta UDP. ¿Qué le pasa a HTTP/3?

- **✅** Se degrada silenciosamente: el navegador intenta QUIC, no recibe respuesta y vuelve a HTTP/2 sobre TCP
  - <sub>Correcto, y es una consecuencia que sorprende a quien viene de la Clase 2. La página carga igual, un poco más lento, y **nada en ningún log dice qué pasó**.</sub>
- ❌ Se bloquea por completo y el sitio no carga
  - <sub>No se bloquea: se degrada. Los navegadores mantienen el camino de respaldo por TCP precisamente para esto.</sub>
- ❌ Funciona igual porque HTTP/3 también corre sobre TCP
  - <sub>HTTP/3 reemplaza TCP por **QUIC**, que corre sobre UDP. Ese es todo el cambio.</sub>
- ❌ Traefik lo detecta y avisa en sus logs
  - <sub>No hay forma de que lo detecte: desde su punto de vista simplemente nunca llegó tráfico QUIC.</sub>

> **Por qué.** Lo que evolucionó es el **transporte**; la semántica de HTTP —la cabecera Host, el modelo de orígenes— es la misma, normada hoy en la RFC 9110. Es un buen ejemplo de una separación de capas bien hecha. *(Apunte §4.13.2)*

#### C4-24 · Mixed Content

*Opción múltiple*

La consola del navegador informa `Mixed Content`. ¿Qué pasó?

- **✅** El frontend se sirve por HTTPS y `API_URL` quedó en `http://`
  - <sub>Correcto: una página segura no puede consumir un recurso inseguro. Se corrige la variable a `https://` y se redespliega.</sub>
- ❌ El certificado del frontend está vencido
  - <sub>Un certificado vencido da otro error, y es sobre el propio sitio, no sobre un recurso.</sub>
- ❌ El dominio tiene registros A y AAAA que apuntan a servidores distintos
  - <sub>Nada que ver: Mixed Content es sobre el esquema de los recursos que la página carga.</sub>
- ❌ El backend responde con un tipo de contenido incorrecto
  - <sub>El tipo de contenido no dispara Mixed Content. El esquema sí.</sub>

> **Por qué.** *(Apunte §4.14)*

#### C4-27 · De dónde partir para diagnosticar

*Opción múltiple*

Casi todos los síntomas de la tabla de errores frecuentes apuntan a un lugar equivocado. ¿Qué criterio propone el capítulo?

- **✅** Diagnosticar siempre a partir del mensaje exacto de la consola del navegador, nunca del comportamiento aparente ni de la intuición
  - <sub>Correcto. Un 502 *parece* un problema del servidor y es un número mal puesto en un formulario. Un error de CORS *parece* un problema de red y es una cadena de texto.</sub>
- ❌ Revisar primero los logs de Traefik, que es el componente central
  - <sub>Traefik puede no tener nada que ver: si el error es de CORS, sus logs muestran un 200 perfecto.</sub>
- ❌ Redesplegar los tres servicios y volver a probar
  - <sub>Redesplegar a ciegas a veces «arregla» sin que nadie entienda qué pasaba, y eso garantiza que vuelva a ocurrir.</sub>
- ❌ Empezar por el componente que se tocó más recientemente
  - <sub>Es una heurística razonable, pero el capítulo propone algo más fuerte: leer el mensaje exacto, que casi siempre nombra la etapa que falló.</sub>

> **Por qué.** Sin el modelo del proxy inverso y el de la política de mismo origen, la tabla de diagnóstico es una lista de recetas para memorizar. Con ellos, es una **consecuencia**. *(Apunte §4.1 y §4.14)*

---

## Las cuatro que más se van a errar

Según lo que el capítulo señala como contraintuitivo:

1. **C4-19** — «CORS protege la API». Es el punto que más se malinterpreta del capítulo, y el experimento con `curl` es la demostración definitiva de que no.
2. **C4-09** — 404 contra 502. El distractor del significado genérico de HTTP se lleva a muchos: acá los emite Traefik y señalan **etapas distintas de la cadena**.
3. **C4-07** — la respuesta corta del Build path. Con repositorios separados va `/`, y el error no menciona el Build path por ningún lado.
4. **C4-12** — los dos requisitos del certificado. Muchos contestan «puerto 443»: el desafío HTTP-01 se valida por el **80**, y lo necesita también en cada renovación.

Si al revisar los intentos ves que una de estas tiene menos del 50 % de acierto, no es un problema del grupo: es un tema para retomar en la clase siguiente.
