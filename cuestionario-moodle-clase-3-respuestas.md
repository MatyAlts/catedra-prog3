# Clave de corrección — Cuestionario Clase 3 (Docker: la receta reproducible)

> **Documento del docente. No publicar en el aula.**
> Estas son las respuestas de las 31 preguntas de `cuestionario-moodle-clase-3.xml`.
> Se genera desde la misma fuente que el XML, así que si el banco cambia, esta clave cambia con él.

- **Cuestionario:** `Clase 3 - Autoevaluación: Docker, imágenes y capas`
- **Curso:** campustest.frm.utn.edu.ar → curso 14 → sección 30 «Actividades 🧩»
- **31 preguntas** en 12 páginas · 1 punto cada una, escaladas a 10
- El orden de abajo es el **orden real del cuestionario** (paginación de `cuestionario-moodle-clase-3.md` §3.1)

En Moodle el alumno ve todo esto solo: cada opción incorrecta tiene su propia explicación. Esta clave sirve para revisar el banco antes de publicarlo y para tener las respuestas a mano en clase.

---

## Resumen

| # | Pág | Tipo | Respuesta correcta | Apunte |
|---|---|---|---|---|
| **C3-01** | 1 | Opción múltiple | Que el programa no es autosuficiente: depende de un contexto —versiones, bibliotecas, var… | §3.2 |
| **C3-02** | 1 | Opción múltiple | No fue tecnológico sino de empaquetado y experiencia de uso: receta declarativa, imagen e… | §3.2 |
| **C3-04** | 2 | Opción múltiple | Un proceso común y corriente al que se le aplicaron espacios de nombres y grupos de contr… | §3.3.1 |
| **C3-05** | 2 | Opción múltiple | Limitan y contabilizan cuánto procesador, memoria, disco y red puede consumir el conjunto… | §3.3.1 |
| **C3-03** | 2 | Emparejar | _(emparejamiento — ver detalle)_ | §3.3.1, §3.5.6 |
| **C3-06** | 3 | Verdadero/Falso | **FALSO** | §3.3.2, §3.6 |
| **C3-07** | 3 | Opción múltiple | Se perdió: vivía en la capa de escritura efímera, que se descarta al eliminar el contened… | §3.3.2 |
| **C3-08** | 4 | Emparejar | _(emparejamiento — ver detalle)_ | §3.3.3 |
| **C3-09** | 4 | Opción múltiple | Docker Desktop levanta una máquina virtual Linux y corre los contenedores adentro | §3.3.3 |
| **C3-10** | 5 | Opción múltiple | «Enviá el contenido de este directorio al motor de construcción»: es el contexto de const… | §3.4.1 |
| **C3-11** | 5 | Opción múltiple | Porque ese archivo nunca se envió al motor: está fuera del contexto de construcción | §3.4.1 |
| **C3-12** | 6 | Verdadero/Falso | **FALSO** | §3.5.4 |
| **C3-13** | 6 | Emparejar | _(emparejamiento — ver detalle)_ | §3.4.2 |
| **C3-14** | 7 | Opción múltiple | Todas las capas siguientes se invalidan también, aunque su texto no haya cambiado: el cac… | §3.4.3 |
| **C3-15** | 7 | Opción múltiple | Cualquier cambio en main.py —incluso una coma— invalidaría esa capa y obligaría a volver… | §3.5.3 |
| **C3-16** | 7 | Opción múltiple | ...impide que pip guarde dentro de la imagen una copia de los paquetes descargados; no ti… | §3.5.3 |
| **C3-17** | 8 | Respuesta corta | `0.0.0.0` | §3.5.5 |
| **C3-18** | 8 | Opción múltiple | El contenedor arranca, el log dice «Uvicorn running on http://127.0.0.1:8000», no hay nin… | §3.5.5 |
| **C3-19** | 9 | Opción múltiple | El proceso número 1 pasa a ser el intérprete de comandos, que no reenvía SIGTERM: la apli… | §3.5.6 |
| **C3-20** | 9 | Opción múltiple | Evitar filtraciones: que un archivo .env con credenciales no termine dentro de la imagen | §3.6 |
| **C3-21** | 10 | Opción múltiple | Porque la imagen oficial de nginx ya trae el suyo y se hereda: no hace falta cambiar cómo… | §3.7 |
| **C3-22** | 10 | Opción múltiple | Porque Windows no guarda el permiso de ejecución: sin esa línea, el script se copia sin p… | §3.7.1 |
| **C3-23** | 10 | Opción múltiple | Para que una sola imagen sirva para todos los entornos: la URL viene de una variable y no… | §3.7.2 |
| **C3-24** | 11 | Respuesta corta | `python:3.12-slim` o `python:3.12-slim ` o `FROM python:3.12-slim` | §3.5.1 |
| **C3-25** | 11 | Opción múltiple | Porque fija el tamaño de partida, las bibliotecas disponibles y —esto se subestima siempr… | §3.5.1 |
| **C3-26** | 11 | Opción múltiple | Cada capa de la imagen, la instrucción que la creó y cuánto pesa: es la ventana directa a… | §3.8.3 |
| **C3-27** | 12 | Opción múltiple | Que los formatos se estandarizaron en 2015 y la imagen puede ejecutarse con Docker, Podma… | §3.9.1 |
| **C3-28** | 12 | Opción múltiple | Que las herramientas necesarias para construir —compiladores, empaquetadores— no queden e… | §3.9.2 |
| **C3-29** | 12 | Opción múltiple | Que latest no significa «la más nueva»: es solo la etiqueta por omisión y apunta a lo que… | §3.9.4 |
| **C3-30** | 12 | Opción múltiple | Porque es más privilegio del necesario: si un atacante ejecuta código adentro, prefiere e… | §3.9.3 |
| **C3-31** | 12 | Opción múltiple | Por el primer error: Docker sigue imprimiendo mensajes después de romperse y el final de… | §3.11 |

## Cobertura del capítulo

| Sección del apunte | Preguntas que la evalúan |
|---|---|
| §3.2 | C3-01, C3-02 |
| §3.3.1 | C3-03, C3-04, C3-05 |
| §3.3.2 | C3-06, C3-07 |
| §3.3.3 | C3-08, C3-09 |
| §3.4.1 | C3-10, C3-11 |
| §3.4.2 | C3-13 |
| §3.4.3 | C3-14 |
| §3.5.1 | C3-24, C3-25 |
| §3.5.3 | C3-15, C3-16 |
| §3.5.4 | C3-12 |
| §3.5.5 | C3-17, C3-18 |
| §3.5.6 | C3-03, C3-19 |
| §3.6 | C3-06, C3-20 |
| §3.7 | C3-21 |
| §3.7.1 | C3-22 |
| §3.7.2 | C3-23 |
| §3.8.3 | C3-26 |
| §3.9.1 | C3-27 |
| §3.9.2 | C3-28 |
| §3.9.3 | C3-30 |
| §3.9.4 | C3-29 |
| §3.11 | C3-31 |

---

## Detalle por página

### Página 1 — Por qué existen los contenedores

#### C3-01 · Qué problema resuelven los contenedores

*Opción múltiple*

«En mi máquina anda». ¿Qué describe exactamente esa frase, y qué vinieron a resolver los contenedores?

- **✅** Que el programa no es autosuficiente: depende de un contexto —versiones, bibliotecas, variables— que nadie escribió en ninguna parte
  - <sub>Exacto. El problema no es el programa: es que su entorno es conocimiento tácito. Los contenedores lo convierten en un artefacto versionado.</sub>
- ❌ Que el programador no probó su código antes de entregarlo
  - <sub>El código puede estar perfectamente probado y fallar igual en otro equipo. El problema no es de calidad del código sino de reproducibilidad del entorno.</sub>
- ❌ Que faltaba estandarizar el lenguaje de programación entre equipos
  - <sub>Ocurre dentro del mismo lenguaje y la misma versión del programa: basta con que difiera una biblioteca del sistema.</sub>
- ❌ Que los servidores de producción usan sistemas operativos distintos al de desarrollo
  - <sub>Pasa también entre dos equipos con el mismo sistema operativo. La diferencia puede ser un paquete instalado hace meses que nadie recuerda.</sub>

> **Por qué.** La receta pasa a ser la misma en tu máquina y en el servidor: Easypanel va a ejecutar en el VPS exactamente el mismo archivo que corriste en tu notebook. **La máquina pasó a ser parte del código.** *(Apunte §3.2)*

#### C3-02 · Cuál fue el aporte de Docker

*Opción múltiple*

Para 2013 el núcleo de Linux ya tenía todos los mecanismos de aislamiento, documentados y gratis. ¿Cuál fue entonces el aporte de Docker?

- **✅** No fue tecnológico sino de empaquetado y experiencia de uso: receta declarativa, imagen en capas y reutilización del núcleo del anfitrión
  - <sub>Correcto, y es importante decirlo con precisión porque explica por qué se impuso tan rápido. Montar namespaces y cgroups a mano exigía un conocimiento profundo del núcleo.</sub>
- ❌ Inventó los espacios de nombres y los grupos de control del núcleo de Linux
  - <sub>Los cgroups los desarrolló Google desde 2006 y entraron al núcleo en 2008; los namespaces venían generalizando la idea de `chroot`, que es de 1979.</sub>
- ❌ Creó la primera tecnología capaz de aislar procesos en Unix
  - <sub>`chroot` es de 1979, las *jails* de FreeBSD de 2000 y las *zones* de Solaris de 2004. Docker llegó último.</sub>
- ❌ Reemplazó a las máquinas virtuales con una tecnología incompatible
  - <sub>No compiten: se apilan. El VPS del práctico es una máquina virtual, y adentro corren contenedores.</sub>

> **Por qué.** Sus tres decisiones de diseño: la receta es un archivo de texto declarativo y versionable; el resultado es una imagen en capas direccionada por contenido; y se reutiliza el núcleo del anfitrión. *(Apunte §3.2)*

---

### Página 2 — El modelo formal

#### C3-04 · Qué es un contenedor

*Opción múltiple*

Formalmente, ¿qué **es** un contenedor?

- **✅** Un proceso común y corriente al que se le aplicaron espacios de nombres y grupos de control
  - <sub>Correcto, y entender eso disuelve buena parte de la magia aparente: no existe una estructura de datos «contenedor» en el núcleo ni una llamada al sistema que lo cree.</sub>
- ❌ Una máquina virtual liviana con su propio núcleo reducido
  - <sub>No tiene núcleo propio: comparte el del anfitrión. Esa es justamente la tercera decisión de diseño de Docker.</sub>
- ❌ Una entidad del núcleo de Linux creada por una llamada al sistema específica
  - <sub>No existe tal llamada. Hay `clone()` con banderas de namespaces y escritura en el sistema de archivos de cgroups, pero ninguna crea «un contenedor».</sub>
- ❌ Un sistema de archivos empaquetado e inmutable
  - <sub>Eso es la **imagen**. El contenedor es una *ejecución* de una imagen.</sub>

> **Por qué.** Los espacios de nombres responden «¿qué ve este proceso?»; los grupos de control, «¿cuánto puede consumir?». Nada más. *(Apunte §3.3.1)*

#### C3-05 · Para qué sirven los grupos de control

*Opción múltiple*

¿Qué aportan los *cgroups* que los espacios de nombres no aportan?

- **✅** Limitan y contabilizan cuánto procesador, memoria, disco y red puede consumir el conjunto de procesos
  - <sub>Correcto. Sin ellos, un contenedor con una fuga de memoria se llevaría puesto el servidor entero.</sub>
- ❌ Impiden que un contenedor vea los procesos de otro
  - <sub>Eso lo hace el espacio de nombres `pid`. Los cgroups no ocultan nada: miden y limitan.</sub>
- ❌ Le dan al contenedor su propia dirección IP
  - <sub>Eso es el espacio de nombres `net`.</sub>
- ❌ Cifran el sistema de archivos del contenedor
  - <sub>No hay cifrado involucrado en el modelo de contenedores.</sub>

> **Por qué.** Dos familias de mecanismos, dos preguntas distintas: **qué ve** (namespaces) y **cuánto consume** (cgroups). *(Apunte §3.3.1)*

#### C3-03 · Espacios de nombres

*Emparejar*

Emparejá cada espacio de nombres con el efecto observable que produce dentro del contenedor.

| Se empareja | Con |
|---|---|
| **mnt** | El contenedor tiene su propio árbol de archivos, su propio / |
| **pid** | El proceso principal del contenedor es el número 1 |
| **net** | El contenedor tiene su propia IP, y por eso su tráfico va por FORWARD y no por INPUT |
| **uts** | hostname devuelve el identificador del contenedor y no el del servidor |
| **user** | Se puede ser root adentro sin serlo afuera |

> **Por qué.** El espacio de nombres de red es literalmente la razón del problema de la sección 2.8: para el núcleo, un contenedor **es otra máquina**. Y el de procesos explica por qué el comando de `CMD` es el PID 1, con las consecuencias sobre señales de §3.5.6. *(Apunte §3.3.1)*

---

### Página 3 — Imágenes y capas

#### C3-06 · Un secreto borrado en una capa posterior

*Verdadero/Falso*

Si en un paso del Dockerfile copiaste un archivo con credenciales y en un paso posterior lo borraste, ese archivo ya no está en la imagen.

- ❌ **Verdadero**
- **✅** **Falso**

> **Por qué.** **Falso, y es grave.** Una capa no se puede editar, **solo tapar**. La capa que contiene el archivo sigue estando en la imagen, es extraíble con herramientas comunes y viaja con la imagen a donde sea que la publiques. Borrar un secreto en una capa siguiente no lo elimina: lo esconde. Y si eso pasó, borrar el archivo no alcanza: **la credencial hay que rotarla**. Un secreto que salió de tu máquina es un secreto quemado. *(Apunte §3.3.2 y §3.6)*

#### C3-07 · La capa efímera

*Opción múltiple*

Un contenedor escribe un archivo mientras corre. Se elimina el contenedor y se crea otro a partir de la misma imagen. ¿Qué pasó con ese archivo?

- **✅** Se perdió: vivía en la capa de escritura efímera, que se descarta al eliminar el contenedor
  - <sub>Correcto. Ese es exactamente el problema que resuelven los volúmenes, y es el contenido de la Clase 5.</sub>
- ❌ Quedó guardado en la imagen y el contenedor nuevo lo encuentra
  - <sub>**Las imágenes no cambian nunca.** De una misma imagen pueden ejecutarse muchos contenedores independientes y ninguno afecta a los demás ni a la imagen.</sub>
- ❌ Se escribió en el sistema de archivos del servidor anfitrión
  - <sub>Salvo que haya un volumen o un montaje explícito, el contenedor escribe en su propia capa, no en el anfitrión.</sub>
- ❌ Quedó en la última capa del Dockerfile, tapando la anterior
  - <sub>Las capas del Dockerfile se fijan al construir. Lo que el contenedor escribe al ejecutarse va a una capa aparte, efímera.</sub>

> **Por qué.** Sobre las capas de la imagen se agrega al ejecutar una capa de escritura con la técnica de **copia al escribir**: el archivo original permanece intacto y se copia hacia arriba solo cuando alguien lo toca. *(Apunte §3.3.2)*

---

### Página 4 — Contenedor y máquina virtual

#### C3-08 · Contenedor frente a máquina virtual

*Emparejar*

Emparejá cada característica con la tecnología que le corresponde.

| Se empareja | Con |
|---|---|
| **Virtualiza el hardware, con un núcleo propio por máquina** | Máquina virtual |
| **Virtualiza el espacio de nombres del sistema operativo y comparte el núcleo** | Contenedor |
| **Arranca en decenas de segundos y pesa gigabytes** | Máquina virtual |
| **Arranca en milisegundos y pesa megabytes** | Contenedor |
| **Aislamiento fuerte, impuesto por el procesador** | Máquina virtual |

> **Por qué.** Que el aislamiento del contenedor sea «menor» no significa que sea débil: significa que su superficie de ataque es el núcleo de Linux, que es enorme, en lugar de la interfaz del procesador, que es diminuta. Importa saberlo cuando alguien propone correr código de terceros no confiable: ahí la respuesta ya no es un contenedor. *(Apunte §3.3.3)*

#### C3-09 · Contenedores Linux sobre Windows

*Opción múltiple*

Un compañero corre contenedores Linux en su notebook con Windows. ¿Qué está pasando realmente?

- **✅** Docker Desktop levanta una máquina virtual Linux y corre los contenedores adentro
  - <sub>Correcto: las dos tecnologías no compiten, se **apilan**. Es exactamente lo mismo que pasa en el práctico: el VPS es una máquina virtual y adentro corren contenedores.</sub>
- ❌ Windows puede ejecutar binarios de Linux desde que existe WSL, sin virtualización
  - <sub>WSL2 también es virtualización: corre un núcleo Linux real en una máquina virtual liviana.</sub>
- ❌ Docker traduce las llamadas al sistema de Linux a llamadas de Windows
  - <sub>No hay traducción de llamadas al sistema. Un contenedor necesita un núcleo Linux de verdad.</sub>
- ❌ Los contenedores son independientes del sistema operativo por diseño
  - <sub>Justo al revés: comparten el núcleo del anfitrión, así que dependen de que ese núcleo sea el correcto.</sub>

> **Por qué.** «No existen contenedores Linux sobre Windows» en sentido estricto. Es la consecuencia directa de la fila «puede correr otro sistema operativo» de la tabla comparativa. *(Apunte §3.3.3)*

---

### Página 5 — El contexto de construcción

#### C3-10 · El punto de docker build

*Opción múltiple*

En `docker build .`, ¿qué significa exactamente ese punto final?

- **✅** «Enviá el contenido de este directorio al motor de construcción»: es el contexto de construcción
  - <sub>Correcto, y la operación es una **transferencia real**, aunque el motor esté en la misma máquina.</sub>
- ❌ «Construí acá», es decir, dejá la imagen en el directorio actual
  - <sub>La imagen no se deja en ningún directorio: queda en el almacén local de Docker.</sub>
- ❌ Que se use el Dockerfile del directorio actual
  - <sub>Eso ocurre por omisión, pero se puede cambiar con `-f`. El punto indica otra cosa: el contexto.</sub>
- ❌ Que la construcción no use caché
  - <sub>Eso es `--no-cache`, una bandera distinta.</sub>

> **Por qué.** De acá salen dos comportamientos frecuentes: la construcción no puede acceder a ningún archivo fuera del contexto, y todo lo que esté en el directorio se transfiere aunque ninguna instrucción lo use. *(Apunte §3.4.1)*

#### C3-11 · COPY fuera del contexto

*Opción múltiple*

Un `COPY ../otro-proyecto/config.json .` falla siempre. ¿Por qué?

- **✅** Porque ese archivo nunca se envió al motor: está fuera del contexto de construcción
  - <sub>Exacto. No es una restricción arbitraria de seguridad: el motor literalmente no tiene ese archivo.</sub>
- ❌ Porque Docker prohíbe las rutas relativas por razones de seguridad
  - <sub>Las rutas relativas funcionan perfectamente *dentro* del contexto. El problema es salir de él.</sub>
- ❌ Porque falta declararlo en el .dockerignore
  - <sub>El `.dockerignore` *excluye* archivos del contexto; no puede incluir archivos de afuera.</sub>
- ❌ Porque COPY solo admite archivos, no rutas con directorios
  - <sub>COPY admite directorios y rutas anidadas sin problema.</sub>

> **Por qué.** La solución cuando de verdad hace falta compartir archivos entre proyectos es mover el contexto un nivel arriba, o reorganizar el repositorio. *(Apunte §3.4.1)*

---

### Página 6 — Capas y metadatos

#### C3-12 · EXPOSE

*Verdadero/Falso*

La instrucción `EXPOSE 8000` abre el puerto 8000 para que se pueda acceder al contenedor.

- ❌ **Verdadero**
- **✅** **Falso**

> **Por qué.** **Falso. EXPOSE no abre nada: es documentación.** Le avisa a quien lea el archivo, y a herramientas como Easypanel, en qué puerto escucha la aplicación. Si lo borrás, el contenedor funciona exactamente igual. Que sea metadato no significa que sea inútil: Easypanel lo lee para proponer a qué puerto enrutar, y `docker run -P` publica automáticamente todos los puertos declarados. Es información que otras herramientas consumen; lo que no hace es actuar por sí misma sobre la red. *(Apunte §3.5.4)*

#### C3-13 · ¿Qué instrucción crea una capa?

*Emparejar*

Emparejá cada instrucción del Dockerfile con lo que produce.

| Se empareja | Con |
|---|---|
| **RUN** | Crea capa: ejecuta un comando y guarda el resultado en el sistema de archivos |
| **COPY** | Crea capa: agrega archivos al sistema de archivos |
| **WORKDIR** | Solo metadato: fija el directorio de trabajo, no ejecuta nada |
| **ENV** | Solo metadato: define una variable de entorno de la imagen |
| **CMD** | Solo metadato: declara el proceso de arranque |

> **Por qué.** Distinguirlas importa por dos motivos. Práctico: solo las que crean capa **pesan**, y por eso conviene encadenar comandos en un único RUN con `&&`. Conceptual: las de metadato **no ejecutan nada** —EXPOSE no abre un puerto, ENV no configura el sistema operativo del anfitrión— y esperar que lo hagan es una fuente clásica de confusión. *(Apunte §3.4.2)*

---

### Página 7 — El caché de capas

#### C3-14 · La regla de invalidación del caché

*Opción múltiple*

¿Qué ocurre cuando se invalida una capa intermedia del Dockerfile?

- **✅** Todas las capas siguientes se invalidan también, aunque su texto no haya cambiado: el caché es una cadena
  - <sub>Correcto. No se puede reutilizar el eslabón número cinco si el cuatro se rompió. Esa propiedad en cascada es la que convierte el orden de las instrucciones en una decisión de ingeniería.</sub>
- ❌ Solo se reconstruye esa capa; las siguientes salen del caché si su texto no cambió
  - <sub>Sería así si el caché fuera un conjunto. Es una **cadena**: la clave de cada capa incluye la identidad de la anterior.</sub>
- ❌ Docker reordena las instrucciones para aprovechar el caché al máximo
  - <sub>Docker **nunca** reordena: ejecuta en el orden escrito. Ordenar bien es trabajo de quien escribe el archivo.</sub>
- ❌ Se invalidan también las capas anteriores, para garantizar coherencia
  - <sub>Las anteriores no dependen de la que cambió, así que se siguen reutilizando.</sub>

> **Por qué.** Para la mayoría de las instrucciones la clave del caché es el texto literal más la identidad de la capa anterior; para COPY y ADD incluye además un **resumen del contenido** de los archivos copiados. *(Apunte §3.4.3)*

#### C3-15 · El orden de copiado

*Opción múltiple*

El Dockerfile del backend copia `requirements.txt`, instala las dependencias, y recién después copia `main.py`. Si se copiara todo junto en un solo COPY, ¿qué cambiaría?

- **✅** Cualquier cambio en main.py —incluso una coma— invalidaría esa capa y obligaría a volver a descargar todas las dependencias
  - <sub>Exacto. La imagen resultante sería idéntica; lo que cambia es **cuánto cuesta producirla la próxima vez**. La diferencia es de dos órdenes de magnitud.</sub>
- ❌ La imagen final sería más grande porque tendría una capa más
  - <sub>Sería incluso una capa *menos*. El tamaño no es el problema: el problema es el tiempo de reconstrucción.</sub>
- ❌ No cambiaría nada: Docker detecta qué archivos cambiaron realmente
  - <sub>Docker calcula un resumen del **conjunto** copiado por la instrucción. Si cambia un byte de cualquiera, cambia la clave de esa capa.</sub>
- ❌ Fallaría la instalación porque pip no encontraría requirements.txt
  - <sub>Lo encontraría perfectamente. El resultado funcional sería idéntico.</sub>

> **Por qué.** El patrón se repite en toda la ingeniería: **lo que cambia poco va arriba, lo que cambia mucho va abajo**. Las dependencias cambian una vez por mes; el código, veinte veces por día. *(Apunte §3.5.3)*

#### C3-16 · Los dos cachés que se confunden

*Opción múltiple*

La opción `--no-cache-dir` de `pip install`...

- **✅** ...impide que pip guarde dentro de la imagen una copia de los paquetes descargados; no tiene nada que ver con el caché de capas de Docker
  - <sub>Correcto. Son dos cachés diferentes, con nombres parecidos, que no tienen relación entre sí. Como esos archivos no se van a volver a usar, solo agregarían peso a la capa.</sub>
- ❌ ...desactiva el caché de capas de Docker para esa instrucción
  - <sub>Eso sería `docker build --no-cache`, que es otra cosa por completo.</sub>
- ❌ ...fuerza a pip a descargar siempre la última versión de cada paquete
  - <sub>Las versiones las fija `requirements.txt`. La bandera solo afecta dónde guarda pip lo que descargó.</sub>
- ❌ ...acelera la instalación al no verificar los paquetes ya instalados
  - <sub>No acelera nada: al contrario, si se reinstalara en la misma capa tendría que volver a descargar.</sub>

> **Por qué.** Es un buen ejemplo de por qué conviene leer qué hace cada bandera en vez de copiarla de un tutorial. *(Apunte §3.5.3)*

---

### Página 8 — La interfaz de escucha

#### C3-17 · La interfaz de escucha dentro del contenedor

*Respuesta corta*

El `CMD` del backend arranca uvicorn con `--host`. ¿Qué dirección tiene que ir ahí para que el servicio sea alcanzable desde afuera del contenedor? (escribí solo la dirección)

Respuestas aceptadas (sin distinguir mayúsculas): `0.0.0.0`

> **Por qué.** Es el error más frecuente al llevar una API a un contenedor. El contenedor tiene su propio espacio de nombres de red y su propia interfaz de bucle local: escuchar en `127.0.0.1` es escuchar en un lugar al que nadie más puede llegar, ni siquiera el anfitrión. *(Apunte §3.5.5)*

#### C3-18 · El fallo que no parece un fallo

*Opción múltiple*

Un grupo dejó `--host 127.0.0.1` en el CMD. ¿Qué van a observar?

- **✅** El contenedor arranca, el log dice «Uvicorn running on http://127.0.0.1:8000», no hay ningún error, y el servicio no contesta nunca
  - <sub>Exacto, y por eso es especialmente cruel: no se parece a un fallo. En la Clase 4 se manifiesta como un **502 Bad Gateway** y manda a buscar el problema a cualquier lado menos al correcto.</sub>
- ❌ El contenedor no arranca y el log muestra un error de dirección inválida
  - <sub>La dirección es perfectamente válida. El proceso arranca sin la menor queja.</sub>
- ❌ Docker rechaza la construcción de la imagen
  - <sub>El CMD ni siquiera se ejecuta al construir: es metadato. Se ejecuta al correr el contenedor.</sub>
- ❌ Funciona igual, porque Docker redirige el tráfico al bucle local del contenedor
  - <sub>Docker no redirige nada hacia el bucle local del contenedor. Ese lugar es inalcanzable desde afuera por definición.</sub>

> **Por qué.** Es la distinción de interfaces de la sección 2.6.1, ahora adentro del contenedor. *(Apunte §3.5.5)*

---

### Página 9 — Señales y secretos

#### C3-19 · Forma de ejecución y forma de intérprete

*Opción múltiple*

¿Cuál es la consecuencia real de escribir `CMD uvicorn main:app` (forma de intérprete) en lugar de `CMD ["uvicorn", "main:app"]` (forma de ejecución)?

- **✅** El proceso número 1 pasa a ser el intérprete de comandos, que no reenvía SIGTERM: la aplicación nunca se entera de que la están apagando
  - <sub>Correcto. El síntoma visible es que cada `docker stop` tarda exactamente diez segundos: es el plazo de gracia venciendo antes del SIGKILL.</sub>
- ❌ La aplicación no puede leer variables de entorno
  - <sub>Las lee en las dos formas. De hecho la forma de intérprete *agrega* expansión de variables.</sub>
- ❌ Docker no puede determinar el puerto de escucha
  - <sub>El puerto no sale del CMD: sale de los argumentos de la aplicación y, como documentación, de EXPOSE.</sub>
- ❌ Es puramente cosmético: las dos formas se comportan igual
  - <sub>Parece cosmético y no lo es. La diferencia está en el apagado, y se manifiesta en cada detención del contenedor.</sub>

> **Por qué.** La regla: usar siempre la forma de ejecución, salvo que se necesite expresamente una funcionalidad del intérprete —expansión de variables, tuberías, redirecciones—, en cuyo caso lo correcto es escribir un script y llamarlo desde la forma de ejecución. Un contenedor bien escrito se detiene en menos de un segundo. *(Apunte §3.5.6)*

#### C3-20 · La función seria del .dockerignore

*Opción múltiple*

El `.dockerignore` cumple tres funciones. ¿Cuál es la que pertenece a otra categoría que las demás?

- **✅** Evitar filtraciones: que un archivo `.env` con credenciales no termine dentro de la imagen
  - <sub>Correcto. Las otras dos —reducir el tamaño y preservar el caché— son de rendimiento; esta es de seguridad, y es irreversible: la capa que contiene el secreto viaja con la imagen a donde sea que la publiques.</sub>
- ❌ Reducir el tamaño del contexto excluyendo `__pycache__/` y `.venv/`
  - <sub>Importante, pero es una cuestión de rendimiento: la construcción tarda más.</sub>
- ❌ Preservar el caché evitando que un archivo temporal invalide la capa de COPY
  - <sub>También rendimiento: hace que las reconstrucciones sean más lentas de lo necesario.</sub>
- ❌ Impedir que Docker acceda a archivos fuera del directorio del proyecto
  - <sub>Eso ya lo impide el propio concepto de contexto de construcción, sin necesidad de `.dockerignore`.</sub>

> **Por qué.** La mayoría de los tutoriales lo presenta como una optimización menor. En realidad gobierna qué tan rápido y **qué tan seguro** es construir. *(Apunte §3.6)*

---

### Página 10 — El Dockerfile del frontend

#### C3-21 · Por qué el frontend no tiene CMD

*Opción múltiple*

El Dockerfile del frontend no declara ningún `CMD`. ¿Por qué funciona igual?

- **✅** Porque la imagen oficial de nginx ya trae el suyo y se hereda: no hace falta cambiar cómo arranca nginx, solo poner archivos donde nginx los busca
  - <sub>Correcto. Las instrucciones de metadato se heredan de la imagen base salvo que se sobrescriban.</sub>
- ❌ Porque las imágenes basadas en Alpine no necesitan comando de arranque
  - <sub>La distribución base no tiene nada que ver: todo contenedor necesita un proceso que ejecutar.</sub>
- ❌ Porque los contenedores que solo sirven archivos no ejecutan ningún proceso
  - <sub>nginx **es** un proceso, y es el PID 1 del contenedor. Se puede comprobar con `ps aux` adentro.</sub>
- ❌ Porque Easypanel se lo inyecta al desplegar
  - <sub>Easypanel no inyecta comandos de arranque; construye la imagen tal como está escrita.</sub>

> **Por qué.** Y fijate en algo más grande: el frontend **no ejecuta nada en el servidor**. El JavaScript de la calculadora corre en la máquina del visitante. Esa observación es la que en la Clase 5 explica por qué el frontend no puede usar la red interna aunque quisiera. *(Apunte §3.7)*

#### C3-22 · Por qué el chmod +x

*Opción múltiple*

El Dockerfile del frontend incluye `RUN chmod +x /docker-entrypoint.d/40-generar-config.sh`. ¿Por qué hace falta?

- **✅** Porque Windows no guarda el permiso de ejecución: sin esa línea, el script se copia sin permiso, nginx lo ignora en silencio y config.js no se genera
  - <sub>Correcto. Sin el chmod explícito, este proyecto funciona en Linux y falla en Windows. El contenedor arranca perfecto y la aplicación no anda.</sub>
- ❌ Porque Docker quita los permisos de ejecución a todos los archivos copiados
  - <sub>Docker preserva los permisos que traía el archivo en el contexto. El problema es el origen, no Docker.</sub>
- ❌ Porque nginx exige permisos 777 en su directorio de arranque
  - <sub>No exige 777 ni nada parecido: solo ejecuta los archivos que *tienen* permiso de ejecución.</sub>
- ❌ Porque el script tiene que poder escribir en /usr/share/nginx/html
  - <sub>El permiso de escritura sobre el destino es otro asunto; el `+x` es sobre el propio script.</sub>

> **Por qué.** La imagen oficial de nginx ejecuta automáticamente todos los archivos de `/docker-entrypoint.d/` en orden alfabético —de ahí el prefijo `40-`— pero **solo los que tienen permiso de ejecución**. Es una convención de esa imagen, no una regla de Docker. *(Apunte §3.7.1)*

#### C3-23 · Configuración en tiempo de arranque

*Opción múltiple*

¿Por qué `config.js` se genera al **arrancar** el contenedor y no al construirlo?

- **✅** Para que una sola imagen sirva para todos los entornos: la URL viene de una variable y no queda grabada adentro
  - <sub>Correcto. Si se generara al construir, haría falta una imagen distinta por cada entorno — y eso mezcla configuración con código, y construcción con ejecución.</sub>
- ❌ Porque al construir todavía no existe el archivo index.html
  - <sub>El index.html se copia en la construcción, antes. No es una cuestión de orden.</sub>
- ❌ Porque nginx no puede leer archivos generados durante la construcción
  - <sub>Los lee perfectamente: todo lo que quede en la imagen está disponible al ejecutar.</sub>
- ❌ Porque las variables de entorno no existen durante la construcción
  - <sub>Sí existen (con `ARG` y `ENV`). El motivo no es técnico sino de diseño.</sub>

> **Por qué.** Es la metodología de los **doce factores**: la configuración se almacena en el entorno, separada del código; y construcción, publicación y ejecución son tres momentos distintos. **Si tenés que reconstruir para cambiar de entorno, algo está mal diseñado.** *(Apunte §3.7.2)*

---

### Página 11 — Imagen base e inspección

#### C3-24 · La imagen base del backend

*Respuesta corta*

El backend parte de una variante reducida de Debian con Python ya instalado, de unos 150 MB. Escribí la etiqueta completa de esa imagen base, tal como aparece en el `FROM`.

Respuestas aceptadas (sin distinguir mayúsculas): `python:3.12-slim`, `python:3.12-slim `, `FROM python:3.12-slim`

> **Por qué.** La imagen completa `python:3.12` pesa ~1 GB y trae herramientas de compilación; `python:3.12-alpine` pesa ~50 MB pero usa **musl** en lugar de glibc, así que los paquetes binarios precompilados no sirven y pip tiene que compilarlos: construcciones mucho más lentas y a veces fallidas. *(Apunte §3.5.1)*

#### C3-25 · Por qué importa la imagen base

*Opción múltiple*

El capítulo dice que la elección de la imagen base es «la decisión de mayor impacto de todo el archivo». ¿Por qué?

- **✅** Porque fija el tamaño de partida, las bibliotecas disponibles y —esto se subestima siempre— la superficie de vulnerabilidades heredada
  - <sub>Correcto: una imagen base con doscientos paquetes instalados trae las vulnerabilidades de esos doscientos paquetes, se usen o no. Es economía del mecanismo (§2.12.1) aplicada acá: la imagen más chica que alcance.</sub>
- ❌ Porque determina qué lenguaje de programación se puede usar
  - <sub>Se puede instalar cualquier cosa sobre cualquier base. Lo que cambia es cuánto trabajo cuesta.</sub>
- ❌ Porque una vez elegida no se puede cambiar sin rehacer el proyecto
  - <sub>Se cambia editando una línea y reconstruyendo.</sub>
- ❌ Porque define el sistema operativo del servidor anfitrión
  - <sub>El anfitrión tiene su propio sistema operativo, independiente de la imagen. Lo que sí se comparte es el *núcleo*.</sub>

> **Por qué.** La regla es la misma que en seguridad: lo que no está, no puede fallar ni ser explotado. *(Apunte §3.5.1)*

#### C3-26 · docker history

*Opción múltiple*

¿Qué muestra `docker history` y para qué sirve?

- **✅** Cada capa de la imagen, la instrucción que la creó y cuánto pesa: es la ventana directa al modelo de capas
  - <sub>Correcto. Es la herramienta con la que se descubre que una imagen de 900 MB tiene 700 MB en un solo `RUN apt-get install`, y también con la que se comprueba que un archivo que se creía borrado sigue ahí.</sub>
- ❌ El historial de comandos ejecutados dentro del contenedor
  - <sub>Eso sería el historial del intérprete, dentro del contenedor. `docker history` habla de la *imagen*.</sub>
- ❌ Los despliegues anteriores de la imagen en el registro
  - <sub>Eso es la lista de etiquetas y digests del registro, otra cosa.</sub>
- ❌ Los cambios que el contenedor hizo sobre su capa efímera
  - <sub>Eso es `docker diff`.</sub>

> **Por qué.** Los otros comandos de inspección: `docker ps`, `docker logs -f`, `docker exec -it <id> sh` y `docker inspect`. *(Apunte §3.8.3)*

---

### Página 12 — Ecosistema y buenas prácticas

#### C3-27 · El estándar OCI

*Opción múltiple*

¿Qué significa que hoy se hable de «imagen OCI» y no de «imagen de Docker»?

- **✅** Que los formatos se estandarizaron en 2015 y la imagen puede ejecutarse con Docker, Podman, containerd o cualquier motor conforme
  - <sub>Correcto. El Dockerfile que se escribe en esta clase no ata el proyecto a ninguna empresa, y esa es exactamente la garantía que la estandarización buscaba.</sub>
- ❌ Que Docker dejó de existir como producto y fue reemplazado por OCI
  - <sub>Docker sigue existiendo perfectamente. Lo que cambió es que el formato ya no le pertenece.</sub>
- ❌ Que las imágenes OCI son incompatibles con las de Docker
  - <sub>Son lo mismo: «imagen de Docker» es hoy un nombre histórico para una imagen OCI.</sub>
- ❌ Que hace falta convertir las imágenes antes de publicarlas en un registro
  - <sub>No hay conversión: la especificación de distribución también está estandarizada.</sub>

> **Por qué.** La Open Container Initiative publica tres especificaciones: imagen, ejecución y distribución. *(Apunte §3.9.1)*

#### C3-28 · Construcción multietapa

*Opción múltiple*

¿Qué problema resuelve una construcción multietapa (varios `FROM` en el mismo archivo)?

- **✅** Que las herramientas necesarias para construir —compiladores, empaquetadores— no queden en la imagen final cargando peso y superficie de ataque
  - <sub>Correcto: se hace el trabajo pesado en la primera etapa y se copia a la última solo el resultado, con `COPY --from=`. Este proyecto no la necesita porque el frontend es HTML sin compilación, pero es el patrón que aparece en el primer proyecto con React, Vue o Angular.</sub>
- ❌ Que se puedan construir imágenes para varios sistemas operativos a la vez
  - <sub>Eso es la construcción multiplataforma (`buildx`), otra funcionalidad.</sub>
- ❌ Que la construcción se paralelice entre varias máquinas
  - <sub>Las etapas pueden paralelizarse si son independientes, pero ese no es el objetivo del patrón.</sub>
- ❌ Que se pueda volver a una etapa anterior si la última falla
  - <sub>No hay «volver atrás»: si una etapa falla, la construcción falla.</sub>

> **Por qué.** El resultado: la imagen final contiene nginx y los archivos generados — ni Node, ni `node_modules`, ni el código fuente. *(Apunte §3.9.2)*

#### C3-29 · Por qué latest es una trampa

*Opción múltiple*

¿Cuál es el problema real de escribir `FROM python:latest`?

- **✅** Que `latest` no significa «la más nueva»: es solo la etiqueta por omisión y apunta a lo que el publicador decida, que puede cambiar sin aviso
  - <sub>Correcto. Un `FROM python:latest` puede construir hoy con Python 3.12 y dentro de tres meses con 3.14, rompiendo el proyecto sin que nadie haya tocado una línea.</sub>
- ❌ Que descarga siempre la versión más reciente y por eso las construcciones son lentas
  - <sub>El problema no es la velocidad sino la **imprevisibilidad**: no sabés qué te va a tocar.</sub>
- ❌ Que `latest` incluye versiones beta e inestables del lenguaje
  - <sub>No necesariamente. El punto es que el contenido de esa etiqueta lo decide un tercero.</sub>
- ❌ Que Docker Hub cobra por el uso de la etiqueta latest
  - <sub>No hay ningún cargo asociado a una etiqueta en particular.</sub>

> **Por qué.** La práctica correcta es fijar la versión y, en contextos que exigen reproducibilidad exacta, fijar el resumen criptográfico (`python@sha256:...`), que por construcción no puede cambiar. La misma lógica aplica a `requirements.txt`: versiones exactas con `==`. **Una construcción reproducible no es la que funciona: es la que vuelve a funcionar igual.** *(Apunte §3.9.4)*

#### C3-30 · No correr como root

*Opción múltiple*

¿Por qué conviene agregar `USER` al Dockerfile, y dónde va?

- **✅** Porque es más privilegio del necesario: si un atacante ejecuta código adentro, prefiere encontrar un usuario sin permisos. Va después de las instrucciones que necesitan privilegios y antes del CMD
  - <sub>Correcto: es mínimo privilegio (§2.12.1) aplicado adentro de la imagen. Gracias al espacio de nombres de usuario, ser root adentro no equivale a serlo en el anfitrión — pero sigue siendo innecesario.</sub>
- ❌ Porque sin USER el contenedor tiene privilegios de root sobre el servidor anfitrión
  - <sub>No los tiene, justamente por el espacio de nombres `user`. La razón es de mínimo privilegio, no de escalada directa.</sub>
- ❌ Porque Docker se niega a ejecutar contenedores como root desde 2020
  - <sub>Por omisión el proceso corre como root dentro del contenedor, y Docker no se queja.</sub>
- ❌ Va al principio del archivo, antes del FROM
  - <sub>Antes del FROM no puede ir nada. Y si va antes de instalar paquetes, la instalación falla por falta de permisos.</sub>

> **Por qué.** *(Apunte §3.9.3)*

#### C3-31 · Diagnosticar una construcción fallida

*Opción múltiple*

Falla un `docker build` y la salida es larga. ¿Por dónde se empieza a leer?

- **✅** Por el primer error: Docker sigue imprimiendo mensajes después de romperse y el final de la salida suele ser ruido
  - <sub>Correcto: el primer error es la **causa**; el resto es consecuencia. Este consejo, que parece obvio, es el que más tiempo ahorra en la Clase 4.</sub>
- ❌ Por el último error, que es el que finalmente detuvo la construcción
  - <sub>El último suele ser un mensaje genérico de «el proceso terminó con código 1», que no dice nada sobre la causa.</sub>
- ❌ Por el resumen final que Docker imprime con el conteo de capas
  - <sub>Si la construcción falló, no hay resumen de capas.</sub>
- ❌ Por los mensajes en amarillo, que son los importantes
  - <sub>Los amarillos son advertencias; el error es lo que rompió la cadena.</sub>

> **Por qué.** Es el mismo criterio que se aplica a cualquier traza de error encadenada: la primera línea que falló es la que explica; las siguientes solo propagan. *(Apunte §3.11)*

---

## Las cuatro que más se van a errar

Según lo que el capítulo señala como contraintuitivo:

1. **C3-06** — el secreto borrado en una capa posterior. Casi todos contestan que desaparece. Una capa **no se puede editar, solo tapar**, y la credencial hay que rotarla.
2. **C3-17** — la respuesta corta de la interfaz de escucha. O sabés por qué `127.0.0.1` no sirve dentro de un contenedor, o no contestás. Es el error que en la Clase 4 aparece como 502.
3. **C3-12** — EXPOSE. La intuición dice que abre el puerto. Es documentación: si lo borrás, el contenedor funciona igual.
4. **C3-19** — forma de ejecución contra forma de intérprete. El distractor «es puramente cosmético» se lleva a casi todos los que nunca vieron un `docker stop` tardar diez segundos.

Si al revisar los intentos ves que una de estas tiene menos del 50 % de acierto, no es un problema del grupo: es un tema para retomar en la clase siguiente.
