# Capítulo 5 — Autenticación y autorización: JWT, RBAC y bcrypt

*Unidad de estudio · Edición ampliada con fundamentos teóricos*

## 5.1. Alcance de la clase

Esta clase responde dos preguntas que suelen tratarse como una sola y no lo son.
**Autenticación** es establecer quién es alguien. **Autorización** es decidir qué
puede hacer. Un sistema puede saber perfectamente quién sos y negarte todo, y esa
distinción —que del lado del cliente se ve como la diferencia entre un `401` y un
`403`— acá se convierte en dos mecanismos separados con reglas propias.

Hay una coincidencia de calendario que esta clase debe aprovechar deliberadamente.
**Esta misma semana, la otra mitad de la cursada estudia el token desde el
navegador**: dónde guardarlo, por qué ninguna opción es gratis, y por qué las
guardas de ruta son usabilidad y no seguridad. Ese último punto es la regla RN-F04
del TPI, y su garante son tres casos de prueba —TST-06, TST-07 y TST-27— que
**ejercitan el backend salteándose la interfaz por completo.**

Eso significa que esta clase y aquella son las dos mitades de la misma
demostración: **allá se aprende que el cliente no protege nada; acá se construye lo
único que sí protege.** Vale la pena que los dos docentes lo digan con esas
palabras.

El capítulo también cobra dos reglas de la clase 3 sobre el único caso del sistema
donde aparecen. **EA-02** —ninguna operación bloqueante desde una corrutina— y
**EA-06** —nada de trabajo de procesador sin ceder— existen, en la práctica, casi
exclusivamente por bcrypt. Y el TPI da el número que lo explica todo:

> bcrypt con factor de costo 12 consume del orden de **trescientos milisegundos de
> procesador por verificación**. En un proceso asincrónico, trescientos
> milisegundos de procesador dentro de una corrutina son trescientos milisegundos
> en los que el bucle de eventos **no atiende absolutamente nada**: ni el catálogo
> público, ni las conexiones abiertas, ni el chequeo de salud.

Hay además una decisión de modelado en esta clase que vale por sí sola, y que
conviene anticipar porque enseña a pensar: el TPI declara que **`SISTEMA` no es un
rol**, y explica por qué modelarlo como tal habría sido un error. La sección 5.8 lo
desarrolla.

Al finalizar la clase, el alumno debe poder **implementar el flujo de autenticación
completo**, explicar qué garantiza un token firmado y qué no, y justificar por qué
la autorización consulta la base en cada petición aunque el token ya traiga los
roles.

**Contenidos**

1. Origen y objetivos de diseño de la autenticación sin estado.
2. Anatomía de un token firmado.
3. Por qué el hashing de contraseñas es deliberadamente lento.
4. El flujo de autenticación, paso a paso.
5. bcrypt fuera del bucle de eventos y su semáforo.
6. Los cuatro roles y su alcance.
7. Por qué `SISTEMA` no es un rol.
8. Asignaciones con vigencia y revocación.
9. La autorización que consulta la base en cada petición.
10. Cambio obligatorio de contraseña y los dos routers.
11. Herramientas de diagnóstico.
12. Seguridad y evolución.

---

## 5.2. Del Basic al token: origen y diseño

El problema es viejo: un protocolo sin estado necesita que cada petición diga de
parte de quién viene. Hubo tres respuestas, y cada una resignó algo distinto.

**Primera: mandar la contraseña en cada petición.** La autenticación básica de
HTTP, normada desde los noventa, hace exactamente eso: adjunta usuario y contraseña
codificados en cada llamada. Es simple, no necesita nada del servidor y tiene un
defecto que hoy resulta escandaloso: **la contraseña viaja una y otra vez**, y basta
comprometer una sola petición para tenerla.

Hay un detalle que conviene aclarar porque se malinterpreta permanentemente: esa
codificación **no es cifrado**. Es una transformación reversible que cualquiera
deshace en un segundo. Sin cifrado del canal, la contraseña viaja legible.

**Segunda: la sesión en el servidor.** El servidor guarda una tabla de sesiones
activas y le da al cliente un identificador. Cada petición trae ese identificador y
el servidor busca a quién corresponde. La contraseña viaja **una sola vez**, y el
servidor puede **cerrar una sesión** cuando quiera, borrando su fila.

Lo que resigna es lo que el Capítulo 1 estableció como decisión central de HTTP:
**el estado.** Si el servidor recuerda sesiones, todas las peticiones de un usuario
tienen que ir a la máquina que las guardó, o hay que compartir esa tabla entre
todas. Con un servidor no se nota; con veinte detrás de un balanceador, es el
problema principal.

**Tercera: el token firmado.** La idea, normada como JWT en 2015, invierte el
planteo: en lugar de que el servidor recuerde quién es cada uno, **el cliente lleva
consigo la afirmación**, y el servidor sólo verifica que esa afirmación no fue
alterada.

Eso lo consigue una **firma criptográfica**: el servidor firma el contenido con una
clave que sólo él conoce, y al recibirlo verifica la firma. Si alguien cambió un
solo carácter, la firma no coincide.

La ventaja es exactamente la que se resignaba antes: **el servidor no guarda nada**,
así que cualquier instancia puede atender cualquier petición. El TPI lo declara en
su sección 5.1: el backend **no almacena sesiones ni listas de tokens**.

Y lo que resigna —porque siempre se resigna algo— es la contracara: **si el servidor
no guarda nada, tampoco puede olvidar nada.** Un token emitido es válido hasta que
expira, y no hay forma de invalidarlo sin reintroducir el estado que se quería
evitar. La sección 5.9 muestra cómo el TPI convive con eso.

*(Ver Figura 5.1: los tres esquemas y qué resigna cada uno.)*

De ese recorrido salen las cuatro decisiones de diseño del capítulo.

**Primera: el servidor no guarda sesiones.** Cada petición se basta a sí misma.

**Segunda: la firma garantiza integridad, no confidencialidad.** El contenido del
token **se puede leer**. La sección 5.3 desarrolla lo que eso implica.

**Tercera: el hash de contraseña es lento a propósito.** No es una carencia de la
herramienta: es su propósito, y la sección 5.4 explica por qué.

**Cuarta: la autorización se decide en la base, no en el token.** Es la decisión
menos obvia y la más importante de este capítulo. La sección 5.9 la desarrolla.

> **💡 PARA ENTENDER**
> Fijate el patrón, que ya viste tres veces en este módulo:
>
> **La sesión en servidor puede cerrar sesiones y no escala. El token escala y no
> puede cerrar sesiones.**
>
> No hay una tercera opción que tenga las dos cosas. Todo lo que se hace para
> "revocar un JWT" —listas negras, tokens cortos con refresco, versionado— es
> **reintroducir estado del servidor de alguna forma**, aceptando parte del costo que
> se quería evitar.
>
> Por eso la pregunta correcta no es *"¿cuál es mejor?"* sino **"¿qué me duele menos
> perder?"**. En el TPI duele menos no poder revocar al instante que no poder
> escalar, y por eso el token gana.
>
> Y ojo con esto: **la decisión trae consecuencias que aparecen después.** Cuando en
> la sección 5.9 veas que la autorización consulta la base en cada petición, vas a
> entender que es exactamente el precio de esta decisión, pagado en cuotas.

---

## 5.3. Anatomía de un token

Un token firmado tiene **tres partes separadas por puntos**, cada una codificada:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 . eyJzdWIiOiI0MiIsImV4cCI6MTc2N30 . dBjftJeZ4CV
        encabezado                            contenido                     firma
```

| Parte | Qué lleva | Ejemplo |
| --- | --- | --- |
| **Encabezado** | El algoritmo de firma y el tipo | `{"alg": "HS256", "typ": "JWT"}` |
| **Contenido** | Las afirmaciones sobre el portador | `{"sub": "42", "exp": 1767225600}` |
| **Firma** | El resultado de firmar las dos anteriores | Bytes |

*(Ver Figura 5.2: las tres partes y qué garantiza cada una.)*

Las afirmaciones del contenido tienen nombres normados, y conviene conocer cuatro:

| Nombre | Significa | En el TPI |
| --- | --- | --- |
| `sub` | El sujeto: de quién habla el token | El identificador del usuario |
| `exp` | Cuándo expira | Según la variable de vigencia declarada |
| `iat` | Cuándo se emitió | Usado en la sección 5.10 |
| `jti` | Un identificador único del token | Permite listas de revocación |

Y acá va lo más importante del capítulo, porque **es lo que más gente entiende mal**:

> **El contenido de un token no está cifrado. Está codificado.**

Cualquiera que tenga el token puede leer su contenido completo sin la clave. La
codificación no protege nada: sólo hace que el texto viaje bien por HTTP.

Lo que la firma garantiza es otra cosa, y son dos:

- **Integridad**: nadie cambió el contenido después de emitido.
- **Autenticidad**: lo emitió quien tiene la clave.

**No garantiza confidencialidad.** De ahí una regla que no admite excepciones: **en
el contenido de un token no va nada que no pueda ser público.** Ni contraseñas, ni
datos sensibles, ni información que el propio portador no deba conocer.

> **⚠️ OJO ACÁ**
> Hacé esto ahora mismo, porque es de las cosas que hay que ver una vez para no
> olvidarse nunca:
>
> 1. Tomá cualquier token —el tuyo, de cualquier sistema donde hayas iniciado sesión—.
> 2. Copiá la parte del medio, entre los dos puntos.
> 3. Decodificala. En la consola del navegador: `atob("...")`.
>
> **Lo leés entero.** Sin clave, sin nada.
>
> Ahora pensá qué significa eso para lo que vas a escribir. Si en el token metés el
> correo, el rol y el identificador, **todo eso es público** para cualquiera que
> tenga el token, incluido el propio usuario.
>
> A veces está perfectamente bien —el usuario ya sabe su correo—. Y a veces no: si
> metés un campo interno como el nivel de descuento que le corresponde o una marca de
> cliente problemático, **acabás de publicárselo.**
>
> Regla sin excepciones: **si no lo pondrías en una respuesta visible para ese
> usuario, no va en el token.**

---

## 5.4. Por qué el hash de contraseña es lento

Las contraseñas no se guardan. Se guarda el resultado de aplicarles una función que
no se puede revertir, de modo que quien acceda a la base **no obtenga las
contraseñas**.

Y acá aparece la primera intuición equivocada. Una función de hash criptográfico
como las de la familia SHA parece lo indicado: es irreversible y está bien
estudiada. **No sirve, y la razón es contraintuitiva: es demasiado rápida.**

Esas funciones están diseñadas para procesar grandes volúmenes de datos a máxima
velocidad. Una placa gráfica moderna calcula **miles de millones por segundo**. Si
un atacante obtiene la base, no necesita revertir nada: prueba contraseñas
candidatas hasta que un hash coincida. Con esa velocidad, cualquier contraseña
razonable cae en horas.

**bcrypt** —publicado en 1999 por Niels Provos y David Mazières— invierte
deliberadamente esa propiedad. Fue diseñado para ser **lento y difícil de acelerar
con hardware especializado**, y tiene un parámetro que ajusta cuánto: el factor de
costo. Cada incremento **duplica** el trabajo.

El TPI declara factor **12**, y de ahí sale el número de la sección 5.1:
aproximadamente **trescientos milisegundos** por verificación.

Trescientos milisegundos para verificar una contraseña suena inaceptable hasta que
se hace la cuenta del otro lado:

| | Con SHA rápido | **Con bcrypt costo 12** |
| --- | --- | --- |
| Verificar un login legítimo | Instantáneo | **0,3 s** — imperceptible |
| Probar mil millones de candidatas | Segundos | **Diez años** |

Esa asimetría es todo el punto: **la lentitud molesta una vez por login y arruina un
ataque por fuerza bruta.**

bcrypt incorpora además una **sal** —un valor aleatorio distinto por contraseña— que
se guarda dentro del propio hash. Su efecto es que **dos usuarios con la misma
contraseña tienen hashes distintos**, lo que impide precalcular una tabla de hashes
comunes y usarla contra toda la base de una vez.

Vale ver cómo se lee un hash de bcrypt, porque lleva todo adentro:

```
$2b$12$LQv3c1yqBWVHxkd0LHAkCO.Yl6X8Yh9lRqLxJKQ2vQe3nZ8Vv5rGa
```

| Segmento | Valor en el ejemplo | Qué es |
| --- | --- | --- |
| Primero | `2b` | La variante del algoritmo |
| Segundo | `12` | **El factor de costo** |
| Tercero | `LQv3c1yqBWVHxkd0LHAkCO` | La sal, de 22 caracteres |
| Resto | `Yl6X8Yh9lRqLxJKQ2vQe3nZ8Vv5rGa` | El hash propiamente dicho |

Esa autodescripción tiene una consecuencia práctica valiosa: **el sistema puede
verificar contraseñas guardadas con distintos factores de costo**, porque cada hash
dice con cuál se generó. Eso permite subir el factor —como la sección 5.12 anticipa
que habrá que hacer— **sin invalidar las contraseñas existentes**: las viejas se
siguen verificando con su costo original, y se rehashean con el nuevo la próxima vez
que alguien inicie sesión.

> **📌 NOTA**
> Que el hash sea lento a propósito es de las pocas cosas en informática donde
> **"más lento" es la característica y no el defecto.** Vale la pena tenerlo claro
> porque va a chocar con todo lo demás que aprendiste.
>
> Y de ahí sale un corolario que te va a servir para leer código ajeno:
>
> **Si ves una contraseña hasheada con SHA-256, MD5 o cualquier cosa rápida, eso está
> mal.** No "es mejorable": está mal, y es de los errores más serios que puede tener
> un sistema.
>
> No importa cuánto se haya complicado el resto —tres vueltas de hash, una sal
> propia, concatenaciones raras—. **Si la función base es rápida, sigue siendo
> rápida**, y un atacante con la base en la mano prueba millones de candidatas por
> segundo.
>
> Hay algoritmos más nuevos y mejores que bcrypt —argon2 ganó una competencia
> internacional en 2015 por eso— pero todos comparten la misma idea: **ser caros a
> propósito.** El TPI usa bcrypt, que sigue siendo perfectamente aceptable.

---

## 5.5. El flujo de autenticación

La sección 5.1 del TPI describe el inicio de sesión en once pasos. Los primeros
tres son los que concentran las decisiones:

**Uno.** El cliente envía sus credenciales. La petición llega al Service con el
correo y **la dirección de red resuelta según la configuración de intermediarios de
confianza** —un detalle que importa porque si el servicio está detrás de un
balanceador, la dirección que se ve directamente es la del balanceador y no la del
cliente—.

**Dos.** **Antes de tocar la contraseña**, el Service consulta el límite de
intentos. Si se superó, responde `429` con el encabezado que indica cuánto esperar,
**sin haber calculado ningún hash**.

**Tres.** Recién ahí se verifica la credencial, con bcrypt fuera del bucle. Si es
correcta, se emite el token.

*(Ver Figura 5.3: el flujo completo, con el punto donde se decide sin calcular.)*

El orden de los pasos dos y tres no es casual, y el TPI lo señala explícitamente al
final de su sección 5.5:

> **El orden sigue importando.** El límite de intentos se evalúa antes que todo
> esto. El semáforo protege el caso legítimo —muchos inicios de sesión
> simultáneos—; **el límite protege del abuso deliberado. Ninguno de los dos
> reemplaza al otro.**

Vale desarmar por qué. Si el límite se evaluara después de verificar la contraseña,
un atacante que envía mil intentos por segundo obligaría al servidor a **calcular
mil hashes de trescientos milisegundos cada uno** antes de rechazarlos. El costo del
ataque sería ridículo y el del servidor, enorme.

Evaluando primero, un intento rechazado cuesta **una consulta**, y el atacante no
consigue nada.

> **💡 PARA ENTENDER**
> Este es un principio que vale para cualquier sistema y que casi nunca se enseña:
>
> **Poné las validaciones baratas antes que las caras.**
>
> Verificar un límite de intentos: una consulta, microsegundos.
> Verificar una contraseña con bcrypt: **trescientos milisegundos**.
>
> Si invertís el orden, le regalás al atacante una forma de hacerte trabajar mil
> veces más de lo que le cuesta a él. **Eso tiene nombre: se llama amplificación**, y
> es la base de muchísimos ataques de denegación de servicio.
>
> La pregunta que te tenés que hacer al ordenar validaciones es siempre la misma:
> **¿qué le cuesta a él y qué me cuesta a mí?** Si le cuesta menos a él, tenés un
> problema aunque el sistema "funcione".

---

## 5.6. bcrypt fuera del bucle

Acá se cobran EA-02 y EA-06 sobre el único caso del sistema donde aparecen. El TPI
enuncia la regla sin ninguna flexibilidad:

> Toda invocación a Passlib —**hash y verificación**— se ejecuta con
> `await anyio.to_thread.run_sync()`. **No hay ninguna excepción y no hay ninguna
> llamada directa en el código.**

```python
from anyio import to_thread

async def verificar_password(plano: str, hasheado: str) -> bool:
    async with _semaforo_bcrypt:
        return await to_thread.run_sync(pwd_context.verify, plano, hasheado)
```

Dos piezas, y la segunda es la que sorprende.

**El hilo aparte** resuelve EA-02: el trabajo de procesador ocurre fuera del bucle,
que sigue atendiendo mientras tanto.

**El semáforo** resuelve un problema que el hilo no resuelve. Sacar bcrypt a un hilo
evita bloquear el bucle, pero **no impide que cien inicios de sesión simultáneos
lancen cien hilos** haciendo un cálculo deliberadamente caro. El TPI acota eso:

> Las llamadas al hilo pasan por un semáforo de tantos permisos como declare la
> configuración. **Con cuatro permisos, cuatro núcleos ocupados como máximo** y el
> resto del proceso sigue respondiendo.

*(Ver Figura 5.4: bcrypt dentro del bucle, en un hilo, y en un hilo con semáforo.)*

Y hay una observación del TPI sobre por qué ese semáforo funciona bien acá y no en
un sistema sincrónico, que merece leerse dos veces:

> **Por qué el semáforo acota lo que promete.** En asincrónico, quien espera un
> permiso es **una corrutina**: cuesta memoria y nada más, a diferencia de un hilo
> que espera un permiso y **sigue ocupando su lugar en un grupo de hilos**.

En un sistema con hilos, cien peticiones esperando un permiso son cien hilos
bloqueados, que además ocupan el grupo del que salen todas las demás operaciones.
El límite protege el procesador y **agota otro recurso**.

Acá no: las que esperan son corrutinas, y una corrutina esperando no ocupa nada más
que memoria. **El límite acota exactamente lo que dice acotar**, sin efectos
laterales.

> **⚠️ OJO ACÁ**
> Hacé la cuenta antes de seguir, porque es la que justifica todo esto:
>
> - Un login = **0,3 segundos** de procesador puro.
> - Sin sacarlo a un hilo: **tres logins por segundo saturan el proceso completo.**
> - No "lo ponen lento": lo **detienen**. Ni el catálogo, ni el chequeo de salud, ni
>   las conexiones de eventos abiertas.
>
> Y ahora la parte que engaña. **En tu máquina, probando solo, tres logins por
> segundo no van a pasar jamás.** Vas a escribir `pwd_context.verify(...)` sin `await
> to_thread`, va a andar perfecto, y vas a pensar que la regla es exagerada.
>
> Se rompe el primer día de uso real, cuando treinta personas entran a la vez al
> empezar el turno. Y el síntoma no va a ser "el login está lento": va a ser **la
> aplicación entera no responde**, incluidos los usuarios que ya estaban adentro
> mirando su pedido.
>
> Por eso el TPI dice "no hay ninguna excepción y no hay ninguna llamada directa en
> el código". **Es la única de las ocho reglas EA que se puede verificar con un
> grep**, igual que EA-03: buscá `pwd_context` sin `to_thread` cerca.

---

## 5.7. Los cuatro roles

El TPI define **cuatro roles acumulables** —un usuario puede tener más de uno—, y
establece antes que nada un principio que ordena todo lo demás:

> Todo endpoint que opera sobre un recurso propio —direcciones y pedidos propios—
> exige **únicamente estar autenticado y ser el propietario**, no un rol en
> particular. **El administrador puede comprar como cualquier otro usuario.**

Esa última frase resuelve una confusión habitual: los roles otorgan capacidades
sobre **lo ajeno**, no sobre lo propio. Nadie necesita un rol para ver su propio
pedido.

| Rol | Puede | **No puede** |
| --- | --- | --- |
| **ADMIN** | CRUD de usuarios, categorías, productos, galerías e ingredientes; ver todos los pedidos; estadísticas; ajuste manual de stock | No tiene restricciones de rol, pero **sigue sujeto a la matriz de transiciones y a las reglas de negocio** |
| **STOCK** | Leer productos e ingredientes con cantidad exacta, cambiar disponibilidad, ajustar stock, ver movimientos | **No crea, edita ni elimina** productos, ingredientes ni categorías: sólo mueve existencias. No administra usuarios ni ve estadísticas |
| **PEDIDOS** | Ver todos los pedidos con detalle e historial, ejecutar transiciones autorizadas, reclasificar modalidad en pendiente | No administra el catálogo, no ve estadísticas, y **nunca mueve stock por un endpoint propio**: eso lo produce la transición de estado |
| **CLIENT** | Catálogo, carrito, crear pedidos, consultar y seguir los propios, cancelar mientras estén pendientes | Sólo accede a sus propios datos. **Es el rol que el registro asigna automáticamente** |

Dos filas merecen comentario porque enseñan a leer una matriz de permisos.

**El administrador no está por encima de las reglas de negocio.** Puede ver todo y
administrar todo, y **sigue sujeto a la matriz de transiciones**: no puede llevar un
pedido entregado a pendiente porque ningún rol puede, no porque le falte permiso.
Los permisos y las reglas del dominio son dos capas distintas.

**El gestor de pedidos nunca mueve stock directamente.** Puede provocar movimientos
—al avanzar un estado—, pero no existe un endpoint donde él escriba stock. Eso es
coherente con lo que la clase 1 mencionó y la clase 7 desarrolla: **el stock tiene un
único punto de escritura.**

> **💡 PARA ENTENDER**
> De esa tabla, la fila del administrador enseña una distinción que se confunde
> siempre:
>
> **Tener todos los permisos no es estar por encima de las reglas.**
>
> El administrador puede ver cualquier pedido y ejecutar transiciones. Y **no puede
> llevar un pedido entregado de vuelta a pendiente** — no porque le falte un permiso,
> sino porque **ningún actor puede**: la matriz de transiciones no lo contempla.
>
> Son dos capas distintas y hay que tenerlas separadas en la cabeza:
>
> - **Permisos:** *¿este actor puede intentar esta operación?*
> - **Reglas de negocio:** *¿esta operación tiene sentido en este estado?*
>
> Un sistema que las mezcla termina con un rol "superadministrador" que puede
> saltearse las reglas del dominio, y ese rol **es la puerta por la que se cuelan
> todas las inconsistencias**: alguien lo usa para "arreglar" un caso raro, y deja
> los datos en un estado que ninguna otra parte del sistema espera.

---

## 5.8. Por qué `SISTEMA` no es un rol

Esta sección trata una decisión de modelado que ocupa un párrafo del TPI y enseña
más que muchas páginas.

La matriz de transiciones de la sección 3.5 incluye un actor llamado `SISTEMA`: es
quien ejecuta, por ejemplo, la expiración automática de un pedido que nadie
confirmó. Parece natural modelarlo como un quinto rol. El TPI dice que no:

> **`SISTEMA` no es un rol.** No aparece en esta tabla ni en la tabla de roles. Un
> rol es algo que **se le asigna a un usuario** y que la verificación de permisos
> comprueba; `SISTEMA` no se le puede asignar a nadie, **no se puede autenticar con
> él**, y no existe ninguna fila de usuario que lo tenga. Es **una marca en el
> historial** que dice "esta transición no la ejecutó una persona".

Y da la razón por la que la alternativa era peor:

> Modelarlo como rol habría exigido crear un usuario de sistema, y **un usuario que
> existe pero con el que nadie puede entrar es una fila que en algún momento alguien
> va a intentar usar para otra cosa.**

> **💡 PARA ENTENDER**
> Esa última frase es de las mejores del TPI y vale para cualquier sistema que
> escribas:
>
> **Un usuario de sistema es una puerta que dejaste abierta y anotaste que no se usa.**
>
> Pensá cómo termina siempre. Creás `usuario_sistema` para que las tareas
> automáticas tengan bajo qué actuar. Al mes, alguien necesita correr un script y
> **usa esa cuenta porque ya existe y tiene permisos**. A los seis meses hay tres
> integraciones usándola. Al año nadie sabe qué hace cada cosa con esa cuenta, y
> **no la podés desactivar** porque algo se rompe.
>
> La alternativa del TPI es más simple y más segura: **`SISTEMA` es un dato, no una
> identidad.** Es un valor en una columna del historial que dice quién ejecutó una
> transición. No tiene contraseña, no tiene permisos, y **no hay forma de entrar con
> él.**
>
> La pregunta de diseño que te llevás: cuando estés por crear una entidad "técnica"
> —un usuario de sistema, una cuenta genérica, un rol especial—, preguntate si lo que
> necesitás es **una identidad o un dato**. Casi siempre es un dato.

---

## 5.9. Vigencia: la autorización se decide en la base

Acá está la decisión más importante del capítulo, y es la que responde al costo que
la sección 5.2 anunció.

El TPI declara que las asignaciones de rol **tienen vigencia**: pueden revocarse y
pueden vencer. La consulta que las evalúa filtra por dos condiciones —que no esté
revocada y que no haya expirado—, y de ahí sale la regla que gobierna todo:

> **Roles incluidos en el token.** El token incorpora únicamente los roles vigentes
> al momento de emitirlo, y **son informativos para la interfaz. Nunca son fuente de
> autorización.**
>
> **Expiración durante la sesión.** La autorización **consulta la base en cada
> petición**, de modo que una asignación revocada o vencida deja de otorgar permisos
> **de inmediato, aun con un token todavía vigente.**

Esa es la respuesta del TPI al problema de la sección 5.2 —que un token emitido no
se puede invalidar—. **No intenta invalidar el token: hace que el token no decida
nada.**

El token sigue siendo válido: sigue diciendo quién sos, y eso no cambió. Lo que
cambió es qué podés hacer, y eso **no vive en el token sino en la base**, donde sí se
puede modificar en cualquier momento.

Y la contracara para el frontend es exacta: los roles que vienen en el token sirven
para **decidir qué botones mostrar** —que es usabilidad— y no sirven para nada más.
**Es RN-F04 vista desde este lado**, y por eso sus garantes le pegan al backend
directamente.

Las demás reglas de vigencia que el TPI declara:

| Regla | Qué establece |
| --- | --- |
| **Asignación** | Sólo un administrador asigna o revoca roles a terceros. Queda registro de quién lo hizo |
| **Revocación** | El borrado **escribe una fecha de revocación; la fila no se borra**. El historial de quién tuvo qué rol se conserva completo |
| **Reasignación** | Asignar un rol vencido crea una fila nueva y cierra la anterior **en la misma transacción**. Si ya hay una abierta, responde `409` |
| **Auto-registro** | El registro inserta la asignación del rol de cliente **en la misma transacción** que crea el usuario |
| **Autoprotección** | Un administrador **no puede eliminarse ni revocarse su propio rol**, y el sistema rechaza lo que dejaría cero administradores activos |

Dos merecen desarrollo.

**El auto-registro y la transacción.** El TPI aclara: *"Sin esa inserción, el usuario
recién registrado no puede comprar."* Crear el usuario y asignarle su rol son **una
sola operación de negocio**, y si la segunda falla, la primera no debe quedar. Es
exactamente el problema que la clase 6 resuelve con el Unit of Work — y conviene
notarlo ahora, porque es la primera vez en el módulo que aparece una operación que
**no tiene sentido a medias**.

**La autoprotección.** Un administrador que se revoca su propio rol deja un sistema
sin nadie que pueda administrarlo, y recuperarlo exige tocar la base a mano. Es una
de esas situaciones donde **la corrección del sistema depende de que exista al menos
uno de algo**, y el TPI la declara explícitamente en lugar de confiar en que nadie
lo haga.

> **⚠️ OJO ACÁ**
> La autoprotección parece una precaución exagerada hasta que ves lo fácil que es
> quedarse afuera:
>
> Hay dos administradores. Uno se va de la empresa y le revocan el rol. El que queda
> está probando la pantalla de roles y **se revoca el suyo para ver qué pasa.**
>
> Listo. **Cero administradores.** Nadie puede asignar roles, porque asignar roles
> requiere ser administrador. La única salida es entrar a la base a mano y escribir
> una fila.
>
> Y fijate que ninguno de los dos hizo nada raro: el primero se fue, el segundo probó
> un botón. **El sistema quedó inutilizable por dos operaciones perfectamente
> válidas.**
>
> Por eso el TPI no dice "tené cuidado": declara que **el sistema rechaza la operación
> que dejaría cero administradores activos**. Es la misma idea que venís viendo desde
> el frontend: **una regla que depende de que alguien se acuerde, falla.**

> **📌 NOTA**
> Fijate en la última regla de la tabla, la del historial que conserva el rol como
> instantánea. El TPI lo dice así:
>
> > Una transición ejecutada el viernes a las 23:59 **sigue diciendo bajo qué rol se
> > autorizó**, aunque el lunes ese rol ya no exista.
>
> Eso es lo mismo que viste en la clase 4 con el precio del producto: **el registro
> guarda lo que era cierto en ese momento**, no lo que es cierto ahora.
>
> Y la razón es idéntica. Si el historial resolviera el rol consultando la asignación
> actual, **revocarle un rol a alguien reescribiría todo lo que esa persona hizo en
> el pasado**. Una auditoría de lo que pasó en marzo daría resultados distintos según
> el día en que la corras.
>
> Es la distinción de la clase 4 otra vez: **lo que describe cambia, lo que registra
> no.** Y cuando dudes de si un dato hay que copiarlo o referenciarlo, esa es la
> pregunta.

---

## 5.10. Cambio obligatorio de contraseña

El sistema puede marcar que un usuario **debe cambiar su contraseña** —por ejemplo,
tras un reseteo administrativo—, y mientras esa marca esté activa el acceso queda
restringido a un puñado de endpoints.

La implementación es donde está la lección, porque el TPI resuelve una limitación
real del marco de trabajo:

> **Dos routers montados en la aplicación.** El router abierto contiene los
> endpoints públicos y los cuatro exceptuados; el router protegido se monta con la
> dependencia de verificación y contiene todo lo demás. **No se resuelve con
> exclusiones**: FastAPI **acumula** las dependencias de aplicación, router y ruta, y
> **no ofrece ningún mecanismo para quitar una en un endpoint concreto.**

*(Ver Figura 5.5: los dos routers y qué endpoint cae en cada uno.)*

Vale detenerse en esa frase, porque describe una restricción de la herramienta y la
decisión que provoca. La forma intuitiva sería poner la dependencia a nivel de
aplicación y **excluir** los cuatro endpoints que deben seguir funcionando. **Eso no
se puede hacer**: las dependencias se suman hacia abajo y no hay forma de restar.

La salida es estructural: **dos routers, y cada endpoint se monta en el que
corresponde.** Es un caso claro de una arquitectura determinada por lo que la
herramienta permite, y saber por qué está así evita que alguien lo "simplifique"
más adelante.

Los cuatro exceptuados son los mínimos para poder salir del estado: iniciar sesión,
registrarse, consultar la propia sesión y **cambiar la contraseña**. Y el alcance del
bloqueo incluye un detalle que muestra rigor: **el endpoint de eventos también
rechaza**, en el momento de establecer la conexión.

> **📌 NOTA**
> Ese detalle del endpoint de eventos parece menor y muestra cómo se piensa un
> bloqueo completo.
>
> Es fácil acordarse de bloquear los endpoints normales: llegan, pasan por la
> dependencia, se rechazan. **El canal de eventos es distinto porque es una conexión
> que queda abierta**, y si nadie lo contempla, alguien con el cambio de contraseña
> pendiente **igual sigue recibiendo eventos en vivo.**
>
> No es un agujero de seguridad grave — son sus propios pedidos. Pero es una
> **inconsistencia**: el sistema dice "no podés hacer nada hasta que cambies la
> contraseña" y al mismo tiempo le está mandando datos.
>
> Cuando armes un bloqueo de este tipo, la pregunta es: **¿qué caminos hacia mis
> datos no pasan por donde puse la verificación?** Casi siempre hay uno que se
> escapa, y suele ser el que no se parece a los demás.

La salida del estado tiene una sutileza que conviene notar. Al confirmar la
contraseña nueva, la marca se desactiva, se registra el momento del cambio, y el
endpoint **devuelve un token nuevo cuya marca de emisión es igual o posterior**, de
modo que —en palabras del TPI— *"la sesión continúa"*. El usuario no tiene que
volver a iniciar sesión.

---

## 5.11. Herramientas de diagnóstico

**Decodificar un token** es la primera verificación y se hace sin herramientas: la
parte del medio es texto codificado. Existen sitios que lo hacen visualmente y
conviene una advertencia: **nunca pegar un token de producción en un sitio de
terceros.** Para eso alcanza una línea en la consola.

*(Ver Figura 5.6: un token decodificado, con sus tres partes.)*

**La documentación interactiva** permite autenticarse y ejecutar endpoints
protegidos desde el navegador. Es la forma más rápida de verificar que una
dependencia de rol hace lo que debe: iniciar sesión con un usuario sin el rol
requerido y comprobar que responde `403` y no `401`.

**Los registros del servidor** deben mostrar los intentos fallidos con su motivo. Y
acá una regla de diagnóstico que es también de seguridad: el registro puede decir
*"contraseña incorrecta para el usuario X"*, pero **la respuesta al cliente no**. La
sección 5.12 explica por qué.

**Medir cuánto tarda una verificación** es la comprobación de la sección 5.6: si un
login tarda del orden de trescientos milisegundos, el factor de costo está bien
puesto. Si tarda cinco, alguien lo bajó.

**Contar hilos activos durante varios logins simultáneos** verifica el semáforo. Sin
él, veinte logins simultáneos producen veinte hilos; con él, tantos como permisos
haya declarados.

> **🧪 EXPERIMENTO**
> Este experimento hace visible por qué existe el semáforo, y se hace en cinco
> minutos.
>
> 1. Implementá la verificación **sin** sacar bcrypt a un hilo. Medí cuánto tarda un
>    login. Anotá el número.
> 2. Ahora, **mientras hacés un login**, pedí desde otra pestaña cualquier endpoint
>    público —el catálogo, o el chequeo de salud—.
>
> **No responde hasta que el login termina.** Ni siquiera el chequeo de salud, que
> es lo que un orquestador usa para saber si tu servicio está vivo.
>
> 3. Sacalo a un hilo con `to_thread.run_sync`. Repetí el paso 2: **ahora el catálogo
>    responde al instante.**
> 4. Último paso, y es el que muestra el semáforo: lanzá **veinte logins
>    simultáneos** y volvé a pedir el catálogo.
>
> Sin semáforo, veinte hilos compitiendo por los núcleos: el catálogo vuelve a
> ponerse lento. Con cuatro permisos, veinte logins se procesan de a cuatro y **el
> resto del sistema sigue respondiendo normalmente.**
>
> Los tres pasos muestran tres cosas distintas: **el hilo salva al bucle, el semáforo
> salva a los núcleos, y el límite de intentos —que ya está antes— salva de los dos
> al abuso deliberado.**

---

## 5.12. Seguridad y evolución

Cuatro consideraciones cierran el capítulo, y son las más importantes del módulo
hasta acá.

**Los mensajes de error no revelan si un usuario existe.** Responder "ese correo no
está registrado" ante uno y "contraseña incorrecta" ante otro le permite a un
atacante **enumerar cuentas** sin adivinar ninguna contraseña. La respuesta al
cliente debe ser la misma en los dos casos. En los registros del servidor, en
cambio, conviene distinguirlos.

**El tiempo de respuesta también revela.** Si un correo inexistente responde al
instante y uno existente tarda trescientos milisegundos —porque calculó el hash—,
la diferencia **es medible** y permite lo mismo que el mensaje. La defensa es
verificar contra un hash ficticio cuando el usuario no existe, de modo que el tiempo
sea equivalente.

**El token no se puede invalidar, y eso hay que decirlo.** Un usuario que cierra
sesión borra su token del navegador, y ese token **sigue siendo válido hasta que
expira**. Si alguien lo capturó antes, el cierre de sesión no lo detiene. Es la
consecuencia directa de la decisión de la sección 5.2, y la mitigación del TPI es la
de la sección 5.9: aunque el token siga siendo válido, **la autorización se
reevalúa contra la base en cada petición**.

**La cadena es tan fuerte como su eslabón más débil, y el más débil suele estar
afuera.** Un sistema con bcrypt de costo 12, tokens firmados y roles con vigencia
no sirve de nada si el reseteo de contraseña manda un enlace que no expira, o si la
clave de firma está en el repositorio. Eso último merece énfasis: **la clave con la
que se firman los tokens es el secreto más importante del sistema**, porque quien la
tenga puede fabricar un token válido para cualquier usuario con cualquier rol.

Sobre la evolución, tres observaciones. La primera es que **el factor de costo se
revisa con el tiempo**: lo que hoy son trescientos milisegundos, con el hardware de
dentro de cinco años serán treinta, y el parámetro habrá que subirlo. Es un valor
que **caduca**, y conviene tenerlo declarado como configuración y no fijo en el
código.

La segunda es que existen algoritmos posteriores a bcrypt —**argon2** ganó una
competencia internacional en 2015— diseñados para resistir mejor el hardware
especializado. bcrypt sigue siendo aceptable, y la migración entre uno y otro es
posible porque el hash guarda con qué algoritmo se generó.

Y la tercera: **la industria se mueve hacia no tener contraseñas.** Las llaves de
acceso basadas en criptografía de clave pública eliminan el problema de raíz —no
hay nada que hashear ni que robar de la base—. Ese es probablemente el futuro, y
entender por qué las contraseñas son difíciles es lo que permite valorarlo.

---

## 5.13. Verificación

1. Decodificar un token y **leer su contenido sin la clave**, explicando qué
   garantiza la firma y qué no.
2. Alterar un carácter del contenido y verificar que **la firma deja de validar**.
3. Medir cuánto tarda una verificación de contraseña y **comprobar que es del orden
   de trescientos milisegundos**.
4. Verificar sin sacar bcrypt a un hilo y comprobar que **el chequeo de salud deja
   de responder** mientras tanto.
5. Lanzar veinte inicios de sesión simultáneos **con y sin semáforo**, y documentar
   la diferencia.
6. Provocar un `401` y un `403` y explicar **cuál corresponde a cada situación**.
7. Revocar un rol a un usuario con sesión abierta y verificar que **pierde permisos
   en la petición siguiente**, con el mismo token.
8. Intentar que un administrador se revoque su propio rol y verificar el rechazo.
9. Activar la marca de cambio de contraseña y comprobar que **los cuatro endpoints
   exceptuados siguen funcionando** y el resto no.

---

## 5.14. Errores frecuentes

**Guardar contraseñas con un hash rápido.** Una función de la familia SHA es
demasiado veloz: un atacante con la base prueba miles de millones por segundo
(sección 5.4).

**Llamar a bcrypt directamente desde una corrutina.** Bloquea el bucle trescientos
milisegundos por verificación. Viola EA-02 y EA-06 (sección 5.6).

**Sacar bcrypt a un hilo y no acotar la concurrencia.** Cien logins simultáneos
lanzan cien hilos con un cálculo caro cada uno (sección 5.6).

**Evaluar el límite de intentos después de verificar la contraseña.** Le regala al
atacante una amplificación: le cuesta una petición y al servidor un cálculo caro
(sección 5.5).

**Poner datos sensibles en el contenido del token.** No está cifrado: cualquiera con
el token lo lee (sección 5.3).

**Autorizar según los roles que vienen en el token.** El TPI es explícito: son
informativos y **nunca fuente de autorización**. Un rol revocado seguiría otorgando
permisos hasta que el token expire (sección 5.9).

**Modelar un actor técnico como un usuario del sistema.** Una cuenta que existe y con
la que nadie debería entrar termina usándose para otra cosa (sección 5.8).

**Borrar la fila al revocar un rol.** Se pierde el historial de quién tuvo qué y
hasta cuándo (sección 5.9).

**Resolver el rol del historial consultando la asignación actual.** Revocar un rol
reescribiría el pasado (sección 5.9).

**Crear el usuario y asignarle su rol en operaciones separadas.** Si la segunda
falla, queda un usuario que no puede comprar (sección 5.9).

**Distinguir en la respuesta entre usuario inexistente y contraseña incorrecta.**
Permite enumerar cuentas sin adivinar ninguna contraseña (sección 5.12).

**Poner la clave de firma en el repositorio.** Quien la tenga puede fabricar un token
válido para cualquier usuario con cualquier rol (sección 5.12).

---

## 5.15. Actividades

1. **El token por dentro.** Emitir un token, decodificar sus tres partes y
   documentar cada afirmación de su contenido. Alterar el contenido y verificar el
   rechazo. Explicar por qué la alteración se detecta sin que el servidor guarde nada.

2. **El costo medido.** Medir el tiempo de verificación con factores de costo 8, 10
   y 12, y construir la tabla de la sección 5.4 con datos propios: cuánto tarda un
   login legítimo y cuánto tardaría probar mil millones de candidatas en cada caso.

3. **Las tres capas de defensa.** Implementar el flujo de login con las tres piezas
   —límite de intentos, hilo aparte y semáforo—, y demostrar con mediciones qué
   protege cada una. Documentar qué pasa si se quita cada una por separado.

4. **La autorización que no está en el token.** Implementar la verificación de roles
   consultando la base. Iniciar sesión, revocar el rol desde otra sesión, y demostrar
   que **el mismo token pierde permisos en la petición siguiente**. Explicar por qué
   eso no sería posible si la autorización leyera el token.

5. **Los dos routers.** Implementar el cambio obligatorio de contraseña con la
   estructura que el TPI declara. Intentar resolverlo con exclusiones y documentar
   por qué no se puede. Verificar que los cuatro exceptuados funcionan.

6. **Exploración: la enumeración de cuentas.** Implementar un login que responda
   mensajes distintos según si el usuario existe, y medir además los tiempos de
   respuesta en los dos casos. Documentar cómo se podría enumerar cuentas con cada
   una de las dos vías. Corregir ambas y verificar que las respuestas son
   indistinguibles en contenido **y en tiempo**.

7. **Exploración: los dos lados del mismo token.** Junto con alguien del turno de
   frontend, seguir un token completo: dónde se emite, cómo viaja, dónde se guarda,
   qué decide de cada lado. Documentar **qué decisión toma el frontend con los roles
   del token y qué decisión toma el backend**, y relacionarlo con RN-F04 y con sus
   tres garantes. *(Requiere coordinar con la otra mitad de la cursada.)*

---

## 5.16. Síntesis

1. **Autenticación y autorización son dos cosas**: quién sos y qué podés hacer. Del
   lado del cliente se ven como la diferencia entre un `401` y un `403`.

2. Los tres esquemas históricos resignaron cosas distintas: la contraseña en cada
   petición la expone; la sesión en servidor **puede cerrarse y no escala**; el token
   **escala y no se puede invalidar.** No hay una opción que tenga las dos.

3. **El contenido de un token no está cifrado: está codificado.** La firma garantiza
   integridad y autenticidad, no confidencialidad. Nada que no pueda ser público va
   ahí.

4. El hash de contraseña **es lento a propósito**, y eso no es un defecto: es la
   característica. Una función rápida permite probar miles de millones de candidatas
   por segundo.

5. **Trescientos milisegundos de procesador dentro de una corrutina detienen el
   proceso entero.** Tres logins por segundo saturan el servidor si bcrypt no sale a
   un hilo.

6. **El hilo salva al bucle; el semáforo salva a los núcleos; el límite de intentos
   —evaluado antes que todo— salva del abuso deliberado.** Ninguno reemplaza a otro.

7. Las validaciones **baratas van antes que las caras.** Invertir ese orden regala
   una amplificación: al atacante le cuesta una petición y al servidor un cálculo de
   trescientos milisegundos.

8. Los roles otorgan capacidades **sobre lo ajeno**, no sobre lo propio: nadie
   necesita un rol para ver su propio pedido, y el administrador compra como
   cualquiera.

9. **`SISTEMA` es un dato, no una identidad.** Un usuario que existe y con el que
   nadie debería entrar termina usándose para otra cosa.

10. **Los roles del token son informativos y nunca fuente de autorización.** La
    autorización consulta la base en cada petición, y esa es la respuesta del TPI al
    problema de no poder invalidar un token.

11. El historial guarda el rol **como instantánea**: si lo resolviera consultando la
    asignación actual, revocar un rol reescribiría el pasado. Es la misma distinción
    de la clase 4 entre lo que describe y lo que registra.

12. **Las dependencias del marco de trabajo se suman y no se restan**, y de esa
    limitación sale la estructura de dos routers. Saber por qué está así evita que
    alguien la "simplifique".

---

## 5.17. Referencias y lecturas complementarias

Las fuentes normativas son varias RFC del IETF. La autenticación básica está en la
**RFC 7617** y conviene leerla aunque sea para confirmar que la codificación que usa
no es cifrado. El token firmado corresponde a la **RFC 7519** (*JSON Web Token*,
2015), que define las afirmaciones registradas de la sección 5.3, y se apoya en la
**RFC 7515** para la firma y en la **RFC 7518** para los algoritmos; la **RFC 8725**
recopila las buenas prácticas y sus advertencias sobre la elección del algoritmo
merecen lectura. Los códigos de estado y la semántica de `401` y `403` están en la
**RFC 9110**, y el encabezado de reintento que la sección 5.5 menciona también.

Sobre el hashing de contraseñas, el artículo original de Provos y Mazières *A
Future-Adaptable Password Scheme* (USENIX, 1999) explica por qué la adaptabilidad
del costo era el punto central del diseño, y sigue siendo la mejor fuente sobre la
idea. La **OWASP Password Storage Cheat Sheet** es la referencia práctica
actualizada, con los parámetros recomendados para cada algoritmo y el criterio para
elegir entre ellos; su sección sobre argon2 explica qué mejora respecto de bcrypt.
Y la **OWASP Authentication Cheat Sheet** cubre en detalle los cuatro problemas de
la sección 5.12, incluida la enumeración por tiempos de respuesta.

Como bibliografía de estudio, Ferguson, Schneier y Kohno, *Cryptography Engineering*
(Wiley, 2010) explica qué garantiza una firma y qué no con el rigor que la sección
5.3 resume en dos líneas, y su capítulo sobre gestión de claves es pertinente a la
advertencia final sobre el secreto de firma. Para la práctica de diseñar
autorización, el capítulo correspondiente de Bishop, *Computer Security: Art and
Science* (2.ª edición, Addison-Wesley, 2018) trata los modelos de control de acceso
basado en roles con la formalidad que este capítulo aplica de manera intuitiva.

Del TPI, este capítulo se apoya en la sección **5** completa —sus cinco
subsecciones—, y toca además la **4.4** por el límite de intentos que la sección 5.5
menciona y la **3.5** por la matriz de transiciones donde aparece el actor de la
sección 5.8.

---

**Continúa en:** Capítulo 6 — Repositorios, Unit of Work y transacciones, donde la
operación de esta clase que "no tiene sentido a medias" —crear un usuario y
asignarle su rol— encuentra el mecanismo que la vuelve atómica, y donde el patrón
llega recién después de que el problema ya se sintió.
