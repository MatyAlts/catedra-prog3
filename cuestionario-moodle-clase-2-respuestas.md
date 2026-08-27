# Clave de corrección — Cuestionario Clase 2 (VPS, puertos y firewall)

> **Documento del docente. No publicar en el aula.**
> Estas son las respuestas de las 31 preguntas de `cuestionario-moodle-clase-2.xml`.
> Se genera desde la misma fuente que el XML, así que si el banco cambia, esta clave cambia con él.

- **Cuestionario:** `Clase 2 – Autoevaluación: la VPS, puertos y firewall`
- **Curso:** campustest.frm.utn.edu.ar → curso 14 → sección 30 «Actividades 🧩»
- **31 preguntas** en 10 páginas · 1 punto cada una, escaladas a 10
- El orden de abajo es el **orden real del cuestionario** (paginación de `cuestionario-moodle-clase-2.md` §3.1)

En Moodle el alumno ve todo esto solo: cada opción incorrecta tiene su propia explicación. Esta clave sirve para revisar el banco antes de publicarlo y para tener las respuestas a mano en clase.

---

## Resumen

| # | Pág | Tipo | Respuesta correcta | Apunte |
|---|---|---|---|---|
| **C2-01** | 1 | Opción múltiple | Que el procesador hace cumplir por hardware la separación de los espacios de memoria | §2.2 |
| **C2-02** | 1 | Opción múltiple | El sobreaprovisionamiento: el proveedor vende más núcleos virtuales que núcleos reales | §2.2 |
| **C2-03** | 1 | Verdadero/Falso | **FALSO** | §2.2, §2.3 |
| **C2-04** | 1 | Opción múltiple | Porque el disco virtual es una imagen: no se actualiza nada, se tira la anterior y se esc… | §2.2, §2.4 |
| **C2-05** | 2 | Opción múltiple | El servidor ante el cliente, presentando su clave de anfitrión | §2.5.1 |
| **C2-06** | 2 | Opción múltiple | Que es vulnerable exactamente una vez —la primera— y a partir de ahí detecta cualquier su… | §2.5.1 |
| **C2-08** | 2 | Verdadero/Falso | **FALSO** | §2.5.5 |
| **C2-07** | 3 | Opción múltiple | Nada secreto: el servidor manda un dato aleatorio y el cliente devuelve ese dato firmado | §2.5.1 |
| **C2-09** | 3 | Opción múltiple | Claves públicas, que solo permiten verificar firmas: no le sirven para entrar a ningún la… | §2.5.1, §2.5.2, §2.9.3 |
| **C2-10** | 3 | Opción múltiple | Que tiene un solo tamaño de clave, así que hay muchas menos formas de configurarlo mal | §2.12.3 |
| **C2-13** | 4 | Respuesta corta | `65535` o `65.535` | §2.6.1 |
| **C2-11** | 4 | Opción múltiple | Porque una conexión se identifica por una tupla de cuatro elementos, y las diez mil difie… | §2.6.1 |
| **C2-12** | 4 | Verdadero/Falso | **VERDADERO** | §2.6.1, §2.12.1 |
| **C2-15** | 4 | Opción múltiple | Porque escuchar por debajo del puerto 1024 requiere privilegios de administrador | §2.6.2 |
| **C2-14** | 5 | Emparejar | _(emparejamiento — ver detalle)_ | §2.6.2 |
| **C2-16** | 5 | Opción múltiple | Únicamente los sockets en estado LISTEN, es decir los que esperan conexiones nuevas | §2.6.3 |
| **C2-18** | 6 | Respuesta corta | `FORWARD` o `forward` | §2.8.1 |
| **C2-19** | 6 | Respuesta corta | `INPUT` o `input` | §2.7.2, §2.8.1 |
| **C2-17** | 7 | Emparejar | _(emparejamiento — ver detalle)_ | §2.7.1 |
| **C2-20** | 7 | Opción múltiple | Tras el DNAT en PREROUTING el destino ya es la IP del contenedor, así que el paquete va p… | §2.8.1 |
| **C2-21** | 7 | Verdadero/Falso | **FALSO** | §2.8.1 |
| **C2-22** | 7 | Opción múltiple | nmap, porque es la única que atraviesa el mismo camino que atravesaría un atacante | §2.8, §2.8.2 |
| **C2-23** | 8 | Opción múltiple | No declarar ningún mapeo de puertos: no publicarlo en absoluto | §2.8.3, §2.12.1 |
| **C2-24** | 8 | Opción múltiple | Habilitaron el firewall antes de permitir el puerto 22: con la política deny incoming, co… | §2.7.2, §2.14 |
| **C2-25** | 8 | Verdadero/Falso | **FALSO** | §2.7.2 |
| **C2-26** | 8 | Múltiples correctas | 80 + 443 | §2.6.3, §2.10 |
| **C2-27** | 9 | Opción múltiple | Que a nadie le interesa la aplicación: les interesan la CPU, el ancho de banda y una dire… | §2.9.1, §2.9.2, §2.9.3 |
| **C2-28** | 9 | Opción múltiple | Eleva el costo del ataque automatizado indiscriminado y mantiene legibles los registros,… | §2.11.1, §2.12.1 |
| **C2-29** | 9 | Opción múltiple | Para que no intente primero un ping de descubrimiento y escanee directamente | §2.8.2 |
| **C2-31** | 9 | Opción múltiple | Valores predeterminados seguros: lo que no está explícitamente permitido debe negarse | §2.9.2, §2.12.1 |
| **C2-30** | 10 | Emparejar | _(emparejamiento — ver detalle)_ | §2.12.1 |

## Cobertura del capítulo

| Sección del apunte | Preguntas que la evalúan |
|---|---|
| §2.2 | C2-01, C2-02, C2-03, C2-04 |
| §2.3 | C2-03 |
| §2.4 | C2-04 |
| §2.5.1 | C2-05, C2-06, C2-07, C2-09 |
| §2.5.2 | C2-09 |
| §2.5.5 | C2-08 |
| §2.6.1 | C2-11, C2-12, C2-13 |
| §2.6.2 | C2-14, C2-15 |
| §2.6.3 | C2-16, C2-26 |
| §2.7.1 | C2-17 |
| §2.7.2 | C2-19, C2-24, C2-25 |
| §2.8 | C2-22 |
| §2.8.1 | C2-18, C2-19, C2-20, C2-21 |
| §2.8.2 | C2-22, C2-29 |
| §2.8.3 | C2-23 |
| §2.9.1 | C2-27 |
| §2.9.2 | C2-27, C2-31 |
| §2.9.3 | C2-09, C2-27 |
| §2.10 | C2-26 |
| §2.11.1 | C2-28 |
| §2.12.1 | C2-12, C2-23, C2-28, C2-30, C2-31 |
| §2.12.3 | C2-10 |
| §2.14 | C2-24 |

---

## Detalle por página

### Página 1 — Virtualización y el VPS

#### C2-01 · Aislamiento entre VPS

*Opción múltiple*

Dos VPS de clientes distintos conviven en el mismo servidor físico. ¿Qué hace que el aislamiento entre ellos sea **real** y no una promesa comercial?

- **✅** Que el procesador hace cumplir por hardware la separación de los espacios de memoria
  - <sub>Exacto. Son espacios de memoria separados que el procesador hace cumplir. Lo que sí se comparte es el hierro: procesador físico, disco y placa de red.</sub>
- ❌ Un contrato de nivel de servicio (SLA) firmado con el proveedor
  - <sub>Un contrato es una promesa, no un mecanismo. El aislamiento del VPS no depende de la buena fe del proveedor: lo impone el hardware.</sub>
- ❌ Que cada VPS tiene su propia dirección IP pública
  - <sub>La IP pública identifica al servidor en la red, pero no aísla nada. Podrías tener IP propia y compartir memoria con el vecino: serían cosas independientes.</sub>
- ❌ Que el hipervisor cifra el disco de cada cliente por separado
  - <sub>El cifrado de disco protege los datos en reposo, que es otro problema. El aislamiento entre máquinas virtuales lo garantiza la separación de memoria impuesta por el procesador.</sub>

> **Por qué.** El VPS es **barato porque compartís hierro** y es **tuyo porque el aislamiento lo hace cumplir el procesador**. Las dos cosas son ciertas al mismo tiempo, y de ahí sale todo lo demás del capítulo. *(Apunte §2.2)*

#### C2-02 · Vecino ruidoso

*Opción múltiple*

El VPS se pone notoriamente más lento durante una tarde, sin que el grupo haya cambiado absolutamente nada. ¿Cuál es la explicación más probable según el capítulo?

- **✅** El sobreaprovisionamiento: el proveedor vende más núcleos virtuales que núcleos reales
  - <sub>Correcto: es el fenómeno del «vecino ruidoso». Los proveedores apuestan a que no todos los clientes estarán al máximo a la vez; cuando la apuesta falla, lo paga el que está usando el servidor en ese momento.</sub>
- ❌ Una falla del hipervisor que hay que reportar al soporte
  - <sub>No hay falla: el sistema está funcionando exactamente como fue diseñado y vendido. El hipervisor está arbitrando recursos escasos, que es su trabajo.</sub>
- ❌ La caché negativa del DNS de la Clase 1
  - <sub>La caché de DNS afecta la resolución de nombres, no el rendimiento del procesador del servidor. Son capas distintas: si el nombre resuelve, el DNS ya hizo su trabajo.</sub>
- ❌ Que el disco virtual es una imagen y no un disco físico real
  - <sub>Que el estado sea un archivo explica por qué reinstalar tarda minutos, no por qué el servidor se pone lento un martes a la tarde.</sub>

> **Por qué.** El aislamiento es real, pero **los recursos se comparten**. Si el servidor se pone lento sin motivo, mirá al vecino. *(Apunte §2.2)*

#### C2-03 · Responsabilidad del proveedor

*Verdadero/Falso*

Si el VPS queda comprometido, el proveedor puede auditar lo que ocurrió dentro del sistema operativo y ayudar a resolverlo.

- ❌ **Verdadero**
- **✅** **Falso**

> **Por qué.** **Falso.** El proveedor responde por el hipervisor, el hardware y la red. Todo lo que pasa dentro del sistema operativo huésped —usuarios, puertos, actualizaciones, servicios expuestos— es del titular. Y el corte no es una postura comercial: es la consecuencia directa de que el proveedor, **por diseño, no puede ver adentro**. El mismo aislamiento que te protege del vecino le impide mirar a él. *(Apunte §2.2 y §2.3)*

#### C2-04 · El estado es un archivo

*Opción múltiple*

¿Por qué «cambiar el sistema operativo» de un VPS tarda tres minutos y no media hora, y por qué la operación no tiene deshacer?

- **✅** Porque el disco virtual es una imagen: no se actualiza nada, se tira la anterior y se escribe otra encima
  - <sub>Exacto. El estado completo de la máquina es un archivo, así que destruir y recrear un servidor es una operación de archivos, no de hardware. Por eso es rápido y por eso es irreversible.</sub>
- ❌ Porque el hipervisor mantiene una copia de seguridad automática permanente
  - <sub>Si hubiera una copia de seguridad automática, la operación **sí** tendría deshacer. Justamente no lo tiene.</sub>
- ❌ Porque Ubuntu se instala más rápido que otros sistemas operativos
  - <sub>No se está instalando nada: se está escribiendo una imagen de disco preparada de antemano. Esa es toda la diferencia.</sub>
- ❌ Porque el proveedor tiene el sistema operativo precargado en memoria RAM
  - <sub>La RAM se borra al reiniciar. Lo que está preparado de antemano es la *imagen de disco*, no un contenido en memoria.</sub>

> **Por qué.** El estado completo de la máquina es un archivo. De ahí salen la velocidad de reinstalación y el carácter destructivo e irreversible de la operación. *(Apunte §2.2 y §2.4)*

---

### Página 2 — SSH: el protocolo

#### C2-05 · Orden de autenticación en SSH

*Opción múltiple*

En una conexión SSH, ¿qué se autentica **primero**?

- **✅** El servidor ante el cliente, presentando su clave de anfitrión
  - <sub>Correcto. La capa de transporte (RFC 4253) establece el canal cifrado y autentica al servidor. Recién sobre ese canal ya seguro ocurre todo lo demás.</sub>
- ❌ El cliente ante el servidor, firmando con su clave privada
  - <sub>Eso ocurre después, en la capa de autenticación (RFC 4252). Primero tenés que saber con quién estás hablando; recién después le mostrás tus credenciales.</sub>
- ❌ Ambos a la vez, en la capa de conexión
  - <sub>La capa de conexión (RFC 4254) es la tercera y no autentica a nadie: multiplexa la sesión interactiva, la copia de archivos y los túneles.</sub>
- ❌ Ninguno: SSH solo cifra, y la autenticación la resuelve el sistema operativo
  - <sub>SSH autentica en las dos direcciones, y por eso existe el archivo `known_hosts`.</sub>

> **Por qué.** El orden es lo que hay que retener: **transporte** (autentica al servidor) → **autenticación** (autentica al cliente) → **conexión**. Todo lo demás ocurre *sobre* un canal que ya es seguro. *(Apunte §2.5.1)*

#### C2-06 · Modelo TOFU

*Opción múltiple*

SSH usa el modelo de «confianza en el primer uso» (TOFU). ¿Qué significa exactamente?

- **✅** Que es vulnerable exactamente una vez —la primera— y a partir de ahí detecta cualquier suplantación
  - <sub>Correcto, y es un compromiso deliberado. Por eso la advertencia posterior de que la clave del anfitrión cambió no es un trámite: o el servidor se reinstaló, o alguien se está interponiendo.</sub>
- ❌ Que la conexión es insegura hasta que se instala un certificado firmado
  - <sub>No hay certificado en juego. SSH no usa autoridades certificadoras como HTTPS: guarda la huella del servidor localmente.</sub>
- ❌ Que la clave del anfitrión se valida contra una autoridad certificadora
  - <sub>Ese es el modelo de HTTPS, no el de SSH. Precisamente porque no hay autoridad que consultar es que existe TOFU.</sub>
- ❌ Que hay que aceptar la huella cada vez que uno se conecta
  - <sub>Se acepta una sola vez y queda guardada en `~/.ssh/known_hosts`. Si te la vuelve a pedir, algo cambió y hay que investigar antes de aceptar.</sub>

> **Por qué.** Todo el valor del modelo está en que **la advertencia se lea**. Aceptarla por reflejo, o borrar la línea de `known_hosts` sin verificar el motivo, convierte la única defensa del esquema en un trámite. *(Apunte §2.5.1)*

#### C2-08 · PermitRootLogin prohibit-password

*Verdadero/Falso*

La directiva `PermitRootLogin prohibit-password` impide entrar al servidor como `root`.

- ❌ **Verdadero**
- **✅** **Falso**

> **Por qué.** **Falso.** Prohíbe entrar como root **con contraseña**. El acceso por clave sigue perfectamente permitido: es el valor predeterminado en las distribuciones modernas y es el adecuado para este práctico, donde el trabajo administrativo es constante. El nombre de la directiva dice exactamente lo que hace; hay que leerlo entero. *(Apunte §2.5.5)*

---

### Página 3 — SSH: las claves

#### C2-07 · Qué viaja en la autenticación por clave

*Opción múltiple*

Cuando te autenticás por clave pública, ¿qué viaja efectivamente por la red?

- **✅** Nada secreto: el servidor manda un dato aleatorio y el cliente devuelve ese dato firmado
  - <sub>Exacto. Es un desafío criptográfico. La clave privada **nunca se transmite**, ni siquiera cifrada.</sub>
- ❌ La clave privada, cifrada con la clave pública del servidor
  - <sub>La clave privada no sale nunca de tu máquina. Si viajara —aunque fuese cifrada— el esquema perdería su propiedad más valiosa.</sub>
- ❌ La clave privada en texto plano, protegida por el canal TLS
  - <sub>Ni en texto plano ni cifrada: no viaja. Además SSH no usa TLS, tiene su propia capa de transporte.</sub>
- ❌ Un hash de la contraseña del usuario
  - <sub>No hay contraseña involucrada. Ese es precisamente el punto de usar claves.</sub>

> **Por qué.** De acá sale la propiedad decisiva: si el servidor entero cae en manos ajenas, el atacante obtiene `authorized_keys` con claves **públicas**, que solo permiten verificar firmas, no producirlas. No le sirven para nada. *(Apunte §2.5.1)*

#### C2-09 · Servidor comprometido y claves

*Opción múltiple*

Un atacante toma control total del servidor y se lleva el archivo `~/.ssh/authorized_keys`. ¿Qué obtuvo?

- **✅** Claves públicas, que solo permiten verificar firmas: no le sirven para entrar a ningún lado
  - <sub>Correcto. Esa es exactamente la ventaja del esquema frente a la contraseña, donde lo guardado del lado del servidor sí es un secreto reutilizable.</sub>
- ❌ Las claves privadas de los cuatro integrantes del grupo
  - <sub>En el servidor no hay ninguna clave privada — y por eso mismo **nunca** hay que copiarle una. Un servidor comprometido con claves privadas adentro no es un servidor comprometido: es todo lo que esas claves abren, comprometido.</sub>
- ❌ Acceso inmediato a todos los equipos desde los que se conectaron los integrantes
  - <sub>Eso sería movimiento lateral, y ocurre cuando hay claves *privadas* guardadas en el servidor. Con solo las públicas, no.</sub>
- ❌ Las contraseñas cifradas de los usuarios del sistema
  - <sub>Las contraseñas del sistema viven en `/etc/shadow`, no en `authorized_keys`. Y en este servidor la autenticación por contraseña está deshabilitada.</sub>

> **Por qué.** Regla de oro: la clave privada **nunca** se copia al servidor, ni se manda por WhatsApp, ni se sube a un repositorio. Hay bots que escanean GitHub buscando exactamente eso y tardan minutos. *(Apunte §2.5.1, §2.5.2 y §2.9.3)*

#### C2-10 · Por qué Ed25519

*Opción múltiple*

El capítulo elige `ssh-keygen -t ed25519` en lugar de RSA de 4096 bits. ¿Cuál es la razón **más importante en la práctica**?

- **✅** Que tiene un solo tamaño de clave, así que hay muchas menos formas de configurarlo mal
  - <sub>Correcto: es economía del mecanismo aplicada a la criptografía. RSA admite tamaños inseguros que siguen siendo aceptados por compatibilidad; Ed25519 no tiene perilla que tocar.</sub>
- ❌ Que RSA ya fue quebrado criptográficamente y no debe usarse
  - <sub>RSA con tamaños adecuados sigue siendo seguro. El problema no es el algoritmo, son las configuraciones débiles que admite.</sub>
- ❌ Que Ed25519 es el único algoritmo que soporta OpenSSH
  - <sub>OpenSSH soporta varios algoritmos, RSA incluido. Por eso hay que elegir.</sub>
- ❌ Que RSA no permite autenticación por desafío criptográfico
  - <sub>Sí la permite: el mecanismo de desafío-firma es el mismo. Lo que cambia es el esquema de firma que hay por debajo.</sub>

> **Por qué.** Ofrece además claves más cortas con seguridad equivalente o superior y firmas más rápidas, pero lo decisivo es lo otro: **menos superficie para equivocarse**. *(Apunte §2.12.3)*

---

### Página 4 — Puertos y sockets

#### C2-13 · Puerto máximo

*Respuesta corta*

Un puerto es un número de 16 bits. Escribí el número de puerto **más alto** que puede existir (solo el número).

Respuestas aceptadas (sin distinguir mayúsculas): `65535`, `65.535`

> **Por qué.** 16 bits dan 65536 valores (0 a 65535), y el rango utilizable va de 1 a 65535. *(Apunte §2.6.1)*

#### C2-11 · El socket como tupla

*Opción múltiple*

Un servidor web atiende diez mil conexiones simultáneas con un único puerto 443. ¿Cómo es posible que no se confundan entre sí?

- **✅** Porque una conexión se identifica por una tupla de cuatro elementos, y las diez mil difieren en el par de origen
  - <sub>Exacto: dirección de origen, puerto de origen, dirección de destino y puerto de destino. No hay diez mil puertos, hay diez mil tuplas.</sub>
- ❌ Porque el servidor asigna internamente un puerto efímero distinto a cada cliente
  - <sub>El puerto efímero lo elige el *cliente* como puerto de origen. El servidor sigue escuchando en el 443 y no reasigna nada.</sub>
- ❌ Porque el proxy inverso serializa las conexiones y las atiende de a una
  - <sub>Se atienden concurrentemente. Si fueran de a una, un sitio con tráfico real sería inusable.</sub>
- ❌ Porque TCP multiplexa varias conexiones dentro de un mismo socket
  - <sub>Cada conexión aceptada genera un **socket nuevo**, ya completo. El socket en escucha es otro objeto distinto, con el origen todavía vacío.</sub>

> **Por qué.** «Un puerto abierto» no es una propiedad del servidor: es un proceso concreto escuchando en una interfaz concreta. *(Apunte §2.6.1)*

#### C2-12 · Escuchar en 127.0.0.1

*Verdadero/Falso*

Un servicio que escucha en `127.0.0.1` es inalcanzable desde internet **aunque el firewall esté apagado** y el puerto figure abierto.

- **✅** **Verdadero**
- ❌ **Falso**

> **Por qué.** **Verdadero.** No hay firewall que valga porque no hay nada que filtrar: sencillamente no hay nadie escuchando del lado de afuera. Es la forma más barata y más robusta de cerrar algo, y es economía del mecanismo en estado puro — ninguna regla que auditar, nada que se pueda configurar mal. *(Apunte §2.6.1 y §2.12.1)*

#### C2-15 · Privilegios y puertos

*Opción múltiple*

Un estudiante levanta su API en el puerto 3000 sin ser administrador, pero no logra levantarla en el 80. ¿Por qué?

- **✅** Porque escuchar por debajo del puerto 1024 requiere privilegios de administrador
  - <sub>Correcto. Es una restricción histórica pensada para que un usuario cualquiera no pudiera hacerse pasar por el servidor web de la máquina.</sub>
- ❌ Porque el puerto 80 está reservado exclusivamente para Apache y Nginx
  - <sub>No hay reserva por programa. Cualquier proceso con privilegios suficientes puede escuchar ahí.</sub>
- ❌ Porque el puerto 80 solo admite tráfico HTTP y su API responde JSON
  - <sub>El número de puerto no impone ningún protocolo: es una convención. Podrías correr SSH en el 80 si quisieras.</sub>
- ❌ Porque el firewall bloquea el puerto 80 por defecto
  - <sub>El firewall descarta paquetes que llegan de afuera; no impide que un proceso local se ponga a escuchar. Son cosas distintas.</sub>

> **Por qué.** Esta es exactamente la razón por la que los servidores de aplicaciones escuchan en 8000, 3000 o 5000 y hay un **proxy inverso** adelante ocupando el 80 y el 443. *(Apunte §2.6.2)*

---

### Página 5 — Rangos y herramientas

#### C2-14 · Rangos de puertos (RFC 6335)

*Emparejar*

Emparejá cada rango de puertos con su descripción correcta según la RFC 6335.

| Se empareja | Con |
|---|---|
| **0 – 1023** | Bien conocidos: los asigna la IANA por trámite formal; hace falta ser administrador para escuchar ahí |
| **1024 – 49151** | Registrados: los asigna la IANA por trámite simplificado (3000, 5432, 6379) |
| **49152 – 65535** | Dinámicos o efímeros: no los asigna nadie, los toma el sistema operativo |
| **Puerto 22** | Bien conocido, asignado a SSH |
| **Puerto 443** | Bien conocido, asignado a HTTPS |

> **Por qué.** Dos consecuencias prácticas: escuchar por debajo de 1024 requiere privilegios de administrador —de ahí que las aplicaciones usen 3000, 5000 u 8000 con un proxy inverso adelante—, y la asignación es una **convención**, no una imposición técnica. *(Apunte §2.6.2)*

#### C2-16 · La bandera -l de ss

*Opción múltiple*

¿Qué pide exactamente la bandera `-l` en `ss -tlnp`?

- **✅** Únicamente los sockets en estado LISTEN, es decir los que esperan conexiones nuevas
  - <sub>Correcto. Sin esa bandera, `ss` muestra además todas las conexiones ESTABLISHED en curso, que son muchas más y responden otra pregunta.</sub>
- ❌ Que se muestren los nombres de los servicios en lugar de los números de puerto
  - <sub>Eso es justamente lo contrario de `-n`, que pide números sin resolver nombres.</sub>
- ❌ Un listado largo, con más columnas de detalle
  - <sub>No es una bandera de formato: filtra por estado del socket.</sub>
- ❌ Los sockets locales de dominio Unix del sistema de archivos
  - <sub>Esos se piden con `-x`. Acá `-t` ya está restringiendo a TCP.</sub>

> **Por qué.** El socket en escucha es **uno**; las conversaciones en curso son **muchas**. Correr el comando con y sin `-l` y mirar cuánto crece la salida es la mejor forma de ver esa diferencia. *(Apunte §2.6.3)*

---

### Página 6 — El recorrido del paquete

#### C2-18 · Cadena del tráfico a contenedores

*Respuesta corta*

Un paquete llega desde internet al puerto publicado de un contenedor Docker. Después de la decisión de enrutamiento, ¿por qué punto de enganche de netfilter sigue su recorrido? (escribí solo el nombre)

Respuestas aceptadas (sin distinguir mayúsculas): `FORWARD`, `forward`

> **Por qué.** Docker reescribe el destino en PREROUTING (tabla `nat`), así que cuando llega la decisión de enrutamiento el paquete **ya no es para esta máquina**: es para el contenedor. Por eso sigue por **FORWARD**, donde Docker registró sus cadenas DOCKER y DOCKER-USER. *(Apunte §2.8.1)*

#### C2-19 · Cadena donde escribe ufw

*Respuesta corta*

¿En qué punto de enganche de netfilter escribe ufw sus reglas de tráfico entrante? (escribí solo el nombre)

Respuestas aceptadas (sin distinguir mayúsculas): `INPUT`, `input`

> **Por qué.** ufw escribe en **INPUT**. Y como el tráfico hacia los contenedores va por FORWARD —y los dos caminos son excluyentes— las reglas de ufw **nunca se evalúan** para ese tráfico. Ese es todo el problema de la sección 2.8. *(Apunte §2.7.2 y §2.8.1)*

---

### Página 7 — netfilter y Docker

#### C2-17 · Puntos de enganche de netfilter

*Emparejar*

Emparejá cada punto de enganche de netfilter con el momento en que se evalúa.

| Se empareja | Con |
|---|---|
| **PREROUTING** | Apenas llega el paquete, antes de decidir a dónde va |
| **INPUT** | El paquete va a un proceso de esta misma máquina |
| **FORWARD** | El paquete atraviesa la máquina hacia otro destino |
| **OUTPUT** | El paquete lo generó un proceso local |
| **POSTROUTING** | Justo antes de salir por la placa de red |

> **Por qué.** La pieza decisiva está entre PREROUTING y los dos siguientes: **la decisión de enrutamiento**. El núcleo mira el destino y se pregunta si el paquete es para él (→ INPUT) o para otro (→ FORWARD). Son caminos **excluyentes**. Toda la sección 2.8 es consecuencia de esto. *(Apunte §2.7.1)*

#### C2-20 · Por qué Docker esquiva a ufw

*Opción múltiple*

Un grupo publicó PostgreSQL con `-p 5432:5432` y corrió `sudo ufw deny 5432`. Un compañero escanea desde afuera y el puerto le aparece **abierto**. ¿Cuál es la explicación correcta?

- **✅** Tras el DNAT en PREROUTING el destino ya es la IP del contenedor, así que el paquete va por FORWARD y nunca pasa por INPUT, donde viven las reglas de ufw
  - <sub>Exacto, y ese es el recorrido completo: PREROUTING (Docker reescribe el destino) → decisión de enrutamiento (no es para esta máquina) → FORWARD → nunca INPUT.</sub>
- ❌ La regla de ufw quedó mal escrita y hay que volver a cargarla
  - <sub>La regla está perfectamente escrita: `ufw status` la muestra. El problema es que esa regla **no se evalúa nunca** para ese tráfico.</sub>
- ❌ El escaneo se hizo antes de que la regla tomara efecto
  - <sub>Las reglas de netfilter toman efecto de inmediato. Esperar más no cambia el resultado.</sub>
- ❌ Docker desactiva la cadena INPUT del sistema al instalarse
  - <sub>INPUT sigue funcionando perfectamente para todo el tráfico dirigido al anfitrión — el SSH del puerto 22, por ejemplo. Lo que ocurre es que el tráfico del contenedor no pasa por ahí.</sub>

> **Por qué.** No es un error de Docker ni una mala configuración de Ubuntu: es la **interacción previsible** de dos programas que escriben reglas en el mismo subsistema, en puntos de enganche distintos. *(Apunte §2.8.1)*

#### C2-21 · ¿Es un bug?

*Verdadero/Falso*

Que Docker se saltee ufw es un error conocido de Ubuntu que se corrige actualizando el sistema.

- ❌ **Verdadero**
- **✅** **Falso**

> **Por qué.** **Falso.** No es un error de nadie: es la consecuencia previsible del recorrido del paquete. Docker incluso documenta la cadena `DOCKER-USER` como el lugar previsto para que el administrador intervenga; lo que no hace es avisar que ufw no la usa. Actualizar no cambia absolutamente nada. *(Apunte §2.8.1)*

#### C2-22 · Qué evidencia vale

*Opción múltiple*

`ufw status` dice que el 3000 no está permitido. `nmap -Pn` desde otra red dice que el 3000 está abierto. ¿Cuál de las dos describe el estado real del servidor?

- **✅** nmap, porque es la única que atraviesa el mismo camino que atravesaría un atacante
  - <sub>Correcto. Cualquier herramienta que corra *dentro* del servidor está describiendo lo que ella cree. Solo la prueba desde afuera describe hechos.</sub>
- ❌ ufw status, porque lee la configuración real del firewall del núcleo
  - <sub>Lee las reglas **de ufw**, que son un subconjunto de las reglas del núcleo. Docker escribió otras que ufw no muestra.</sub>
- ❌ Las dos son igual de válidas y hay que promediar el criterio
  - <sub>Las dos afirmaciones son ciertas, pero no dicen lo mismo. Solo una responde la pregunta «¿el puerto está accesible?».</sub>
- ❌ Ninguna: hay que revisar el panel del proveedor
  - <sub>El proveedor no ve dentro de tu sistema operativo. El firewall del VPS lo administrás vos.</sub>

> **Por qué.** Fijate en la forma del error, porque se repite en toda la ingeniería: **una herramienta te informó sobre sí misma y vos lo leíste como información sobre el sistema**. `ufw status` no dice «el 3000 está cerrado»: dice «yo no tengo ninguna regla que lo abra». *(Apunte §2.8 y §2.8.2)*

---

### Página 8 — Firewall y exposición

#### C2-23 · Estrategia preferida

*Opción múltiple*

Para un PostgreSQL que solo debe ser alcanzable por la API del mismo proyecto, ¿cuál es la estrategia **preferida** según el capítulo?

- **✅** No declarar ningún mapeo de puertos: no publicarlo en absoluto
  - <sub>Correcto. El servicio sigue siendo perfectamente accesible para los demás contenedores del proyecto por la red interna de Docker, que es el contenido de la Clase 5.</sub>
- ❌ Publicarlo con `-p 5432:5432` y bloquearlo con una regla de ufw
  - <sub>Es exactamente lo que **no** funciona: ufw no ve ese tráfico. Y aunque funcionara, seguirías dependiendo de que una regla esté bien escrita.</sub>
- ❌ Publicarlo y escribir reglas de iptables en la cadena DOCKER-USER
  - <sub>Es válido, pero el capítulo lo reserva para casos excepcionales: agrega piezas, reglas que auditar y puntos de fallo.</sub>
- ❌ Publicarlo y protegerlo con una contraseña larga y aleatoria
  - <sub>Una contraseña fuerte es deseable, pero deja el servicio expuesto a internet igual: a escaneos, a vulnerabilidades del propio motor y a fuerza bruta continua.</sub>

> **Por qué.** Economía del mecanismo: no hay regla que auditar, no hay herramienta en la que confiar, no hay nada que se pueda configurar mal. **El puerto más seguro es el que no existe.** *(Apunte §2.8.3 y §2.12.1)*

#### C2-24 · Orden de los comandos de ufw

*Opción múltiple*

Un grupo conectado por SSH corre `sudo ufw enable` y la terminal se congela. No pueden volver a entrar. ¿Qué pasó y cómo se evitaba?

- **✅** Habilitaron el firewall antes de permitir el puerto 22: con la política `deny incoming`, cortó su propia sesión. Se evita permitiendo primero y habilitando después
  - <sub>Correcto. Se sale por la consola de emergencia del proveedor, que no pasa por SSH ni por el firewall. Y la regla es simple: **permitir primero, habilitar después. Siempre.**</sub>
- ❌ El firewall bloqueó el puerto 443 y con él la sesión SSH
  - <sub>SSH no usa el 443, usa el 22. Lo que cortó la sesión fue la política predeterminada de descartar todo lo entrante.</sub>
- ❌ ufw reinició el servicio de red y hay que esperar a que vuelva
  - <sub>ufw no reinicia la red. El bloqueo es permanente hasta que alguien permita el 22.</sub>
- ❌ Se quedaron sin acceso porque `ufw enable` deshabilita la autenticación por clave
  - <sub>El firewall no toca la configuración de SSH. Son subsistemas independientes.</sub>

> **Por qué.** El síntoma delata la causa: la conexión no da «clave rechazada», se queda **colgada** hasta el timeout. Nadie contesta, que es exactamente lo que hace un `deny`. *(Apunte §2.7.2 y §2.14)*

#### C2-25 · El puerto 80 con HTTPS

*Verdadero/Falso*

Si toda la aplicación funciona por HTTPS, el puerto 80 se puede cerrar sin consecuencias.

- ❌ **Verdadero**
- **✅** **Falso**

> **Por qué.** **Falso.** Let's Encrypt valida la titularidad del dominio pidiendo un archivo **por el puerto 80** (desafío HTTP-01). Sin ese puerto abierto no hay certificado, y sin certificado no hay HTTPS. El 80 no está abierto para servir la aplicación: está abierto para redirigir a HTTPS y para que el certificado se emita y se renueve. *(Apunte §2.7.2)*

#### C2-26 · Qué necesita ver el mundo

*Múltiples correctas*

En el VPS del práctico están en escucha los puertos 22 (sshd), 80 (Traefik), 443 (Traefik) y 3000 (Easypanel). ¿Cuáles necesita poder alcanzar **el público general de internet**? (marcá todas las que correspondan)

- **✅** 80
  - <sub>Sí: redirección a HTTPS y validación del certificado de Let's Encrypt.</sub>
- **✅** 443
  - <sub>Sí: es por donde viaja todo el tráfico de la aplicación.</sub>
- ❌ 22
  - <sub>No. El 22 lo necesitan los integrantes del grupo para administrar, no el público. En este práctico se deja abierto, pero no es «para el mundo».</sub>
- ❌ 3000
  - <sub>No. Una vez publicado el panel bajo el dominio propio con HTTPS, el acceso directo por el 3000 tiene que cerrarse: expone la contraseña del administrador en texto plano.</sub>

> **Por qué.** «¿Cuáles de estos necesita ver el mundo entero?» es toda la clase de seguridad resumida en una pregunta. *(Apunte §2.6.3 y §2.10)*

---

### Página 9 — Riesgos y endurecimiento

#### C2-27 · Quién va a querer hackear una calculadora

*Opción múltiple*

«Es una calculadora de la facultad, no tiene datos de nadie. ¿Quién va a querer hackearla?» ¿Cuál es el error de ese razonamiento?

- **✅** Que a nadie le interesa la aplicación: les interesan la CPU, el ancho de banda y una dirección IP limpia
  - <sub>Exacto. La aplicación es irrelevante; el servidor es el botín. Minado de criptomonedas, envío de spam, ataques de denegación de servicio contra terceros y movimiento lateral hacia otros equipos.</sub>
- ❌ Ninguno: efectivamente un servidor sin datos valiosos no es un objetivo
  - <sub>Un VPS recién creado empieza a recibir intentos de acceso **dentro de la primera hora de existir**, sin que nadie conozca su dirección.</sub>
- ❌ Que la calculadora sí guarda datos personales de los alumnos
  - <sub>No es una cuestión de qué datos hay: aunque no hubiera ninguno, el servidor sigue siendo valioso por sus recursos.</sub>
- ❌ Que el ataque vendría de otros estudiantes del curso
  - <sub>El descubrimiento es automático y no selectivo. Nadie te ataca a vos en particular: atacan a todos, todo el tiempo, con herramientas automatizadas.</sub>

> **Por qué.** El espacio IPv4 completo son ~4.300 millones de direcciones y barrerlo entero es cuestión de una hora larga desde un solo equipo. Además el resultado se indexa y se vende (Shodan, Censys): el atacante ni siquiera necesita escanear, le alcanza con consultar. *(Apunte §2.9.1, §2.9.2 y §2.9.3)*

#### C2-28 · Qué aporta fail2ban

*Opción múltiple*

¿Qué hace fail2ban y qué **no** hace?

- **✅** Eleva el costo del ataque automatizado indiscriminado y mantiene legibles los registros, pero no impide un ataque dirigido
  - <sub>Correcto. Quien tenga paciencia puede espaciar los intentos por debajo del umbral o rotar direcciones de origen. Es una capa más, no una defensa.</sub>
- ❌ Impide cualquier intento de acceso no autorizado por SSH
  - <sub>Ninguna herramienta sola hace eso. Y por eso existe la defensa en profundidad: cuatro capas independientes, cada una suponiendo que las otras pueden fallar.</sub>
- ❌ Reemplaza la necesidad de deshabilitar la autenticación por contraseña
  - <sub>Al revés: la medida fuerte es `PasswordAuthentication no`. fail2ban baja el ruido y el consumo, pero no sustituye a la capa que elimina el problema.</sub>
- ❌ Cifra los intentos de conexión para que no puedan ser interceptados
  - <sub>El cifrado ya lo provee SSH en su capa de transporte. fail2ban solo lee registros y bloquea direcciones.</sub>

> **Por qué.** Defensa en profundidad: **ninguna capa se asume infalible**. En este servidor hay al menos cuatro —clave en vez de contraseña, firewall restrictivo, no publicar puertos internos, fail2ban— y cada una supone que las otras pueden fallar. *(Apunte §2.11.1 y §2.12.1)*

#### C2-29 · La bandera -Pn de nmap

*Opción múltiple*

¿Para qué sirve la bandera `-Pn` en `nmap -Pn tudominio.com`?

- **✅** Para que no intente primero un ping de descubrimiento y escanee directamente
  - <sub>Correcto. Muchos proveedores descartan los pings entrantes; sin esa bandera nmap concluiría que el servidor no existe y ni siquiera escanearía.</sub>
- ❌ Para escanear también los puertos UDP además de los TCP
  - <sub>Eso se pide con `-sU`. `-Pn` no cambia qué protocolo se escanea.</sub>
- ❌ Para omitir los puertos privilegiados por debajo de 1024
  - <sub>El rango de puertos se controla con `-p`. `-Pn` no filtra puertos.</sub>
- ❌ Para que el escaneo no quede registrado en los logs del servidor destino
  - <sub>No oculta nada: el escaneo llega igual y puede registrarse. La bandera solo evita el paso previo de descubrimiento.</sub>

> **Por qué.** Sin `-Pn`, el grupo puede quedarse creyendo que no hay nada abierto cuando en realidad nmap ni siquiera llegó a mirar. *(Apunte §2.8.2)*

#### C2-31 · Predeterminados permisivos

*Opción múltiple*

Redis y MongoDB arrancaban históricamente sin autenticación, y eso causó miles de bases secuestradas. ¿Qué principio de diseño violaban?

- **✅** Valores predeterminados seguros: lo que no está explícitamente permitido debe negarse
  - <sub>Correcto. Ambos nacieron pensados para correr en una red interna de confianza; cuando la contenerización volvió trivial exponerlos a internet, ese predeterminado se convirtió en la causa del desastre.</sub>
- ❌ Economía del mecanismo: la protección era demasiado compleja
  - <sub>El problema no era la complejidad, era la ausencia de protección por defecto.</sub>
- ❌ Mínimo privilegio: los procesos corrían como administrador
  - <sub>Aunque corrieran sin privilegios, seguirían aceptando cualquier conexión sin credenciales. El problema era el predeterminado, no los permisos del proceso.</sub>
- ❌ Ninguno: fue un problema de implementación, no de diseño
  - <sub>Fue una decisión de diseño explícita —«esto va en una red de confianza»— que dejó de ser válida cuando cambió el contexto de uso.</sub>

> **Por qué.** La lección permanece aunque las versiones actuales lo hayan corregido: **un predeterminado permisivo se convierte en vulnerabilidad masiva en cuanto cambia el contexto de despliegue**. *(Apunte §2.9.2 y §2.12.1)*

---

### Página 10 — Síntesis: los principios

#### C2-30 · Principios de Saltzer y Schroeder

*Emparejar*

Emparejá cada principio de diseño (Saltzer y Schroeder, 1975) con su aplicación concreta en este capítulo.

| Se empareja | Con |
|---|---|
| **Mínimo privilegio** | El contenedor de la base de datos no publica puertos porque no necesita ser alcanzable desde afuera |
| **Valores predeterminados seguros** | `ufw default deny incoming`: lo que no está explícitamente permitido, se niega |
| **Economía del mecanismo** | «No publicar el puerto» es preferible a «publicarlo y filtrarlo»: no hay regla que auditar |
| **Defensa en profundidad** | Se apilan cuatro capas independientes y cada una supone que las otras pueden fallar |

> **Por qué.** Los tres primeros son de **1975** y siguen describiendo con exactitud los errores que se cometen hoy. Las herramientas cambian todo el tiempo; los principios prácticamente nunca. *(Apunte §2.12.1)*

---

## Las cuatro que más se van a errar

Según lo que el capítulo señala como contraintuitivo:

1. **C2-08** — `PermitRootLogin prohibit-password`. Casi todos leen «prohíbe root». Prohíbe root **con contraseña**; por clave sigue entrando.
2. **C2-18 y C2-19** — las dos de respuesta corta. No se adivinan: o tenés el recorrido del paquete en la cabeza (PREROUTING » decisión de enrutamiento » FORWARD) o no contestás.
3. **C2-22** — cuál evidencia vale, `ufw status` o `nmap`. El distractor «las dos son igual de válidas» es el que se lleva a los que entendieron a medias.
4. **C2-15** — puerto 3000 sin privilegios. Muchos contestan que hace falta ser administrador para cualquier puerto; la frontera está en 1024.

Si al revisar los intentos ves que una de estas tiene menos del 50 % de acierto, no es un problema del grupo: es un tema para retomar en la clase siguiente.
