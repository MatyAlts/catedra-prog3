# Capítulo 2 — Contratos: schemas, validación y CRUD

*Unidad de estudio · Edición ampliada con fundamentos teóricos*

## 2.1. Alcance de la clase

El capítulo anterior terminó con una afirmación que conviene tomar en serio: **la
especificación de la API se deriva del código y por lo tanto no puede
desactualizarse.** Este capítulo es el que convierte esa afirmación en algo con
consecuencias, porque estudia **qué se declara** para que esa especificación diga
lo correcto.

La palabra que ordena la clase es **contrato**. Un contrato es un acuerdo entre dos
partes sobre qué se manda, qué se devuelve y qué pasa cuando algo no cumple.
Cuando las dos partes son dos equipos —como en esta cursada, donde una mitad
escribe el servidor y la otra el cliente— ese acuerdo deja de ser un detalle
técnico y pasa a ser **el principal punto de fricción del proyecto**.

Hay una razón concreta para que esta clase sea la segunda y no la sexta. Al
terminarla, el backend tiene **un contrato publicado y navegable**, aunque todavía
no haya base de datos. La otra mitad de la cursada está esa semana con hojas de
estilo y no lo necesita todavía; cuando lo necesite —cuatro semanas después, al
tipar el contrato en TypeScript— **va a existir hace un mes y va a estar
corriendo.** Tipar contra algo que responde es una situación muy distinta de tipar
contra una tabla de un documento.

El capítulo también introduce una decisión del TPI que sorprende a todo el mundo la
primera vez y que se enuncia acá aunque no haya persistencia:

> **Todos los importes son `DECIMAL(10,2)` y viajan en JSON como cadena decimal**
> —`"1234.50"`—. El tipo TypeScript espejo es `string`.

Esa es la mitad de arriba de una regla que la otra mitad de la cursada estudia como
RN-F08. Acá se ve por qué el servidor la impone.

Al finalizar la clase, el alumno debe poder **escribir los schemas de cualquier
módulo de la sección 7 del TPI**, implementar su CRUD con los verbos y los códigos
de estado correctos, y explicar por qué hacen falta tres modelos por entidad y no
uno.

**Contenidos**

1. Origen y objetivos de diseño del contrato entre sistemas.
2. Anatomía de un modelo: campos, restricciones y anotaciones.
3. Qué ocurre durante la validación, y en qué orden.
4. El `422` y la lectura de su cuerpo.
5. Modelos segregados: por qué tres y no uno.
6. Actualización parcial: el campo ausente y el campo nulo.
7. El dinero y las cantidades: por qué viajan como texto.
8. Los verbos del TPI y por qué `PUT` no se usa.
9. Colecciones: envoltorio, paginación y ordenamiento.
10. Errores: el formato normado y el catálogo de códigos.
11. Observabilidad: el identificador de petición.
12. Herramientas de diagnóstico.

---

## 2.2. Por qué existe el contrato: origen y diseño

Cuando dos sistemas se hablan, alguien tiene que decidir qué significa cada campo.
La historia de cómo se resolvió eso tiene tres etapas, y de cada una queda algo.

**Primera etapa: el contrato rígido y generado.** A principios de los 2000, el
enfoque dominante para servicios web fue SOAP, con contratos escritos en WSDL. La
propuesta era fuerte: el contrato es un documento formal, y a partir de él **se
generan automáticamente el cliente y el servidor**. Nada podía desajustarse, porque
las dos partes salían del mismo archivo.

Funcionó y se abandonó, y el motivo es instructivo. El contrato era **enorme y
frágil**: cambiar un campo obligaba a regenerar y redesplegar todo, los documentos
eran ilegibles para un humano, y el acoplamiento entre las partes era tan fuerte
que evolucionar por separado se volvía imposible. **Se había resuelto el desajuste
al precio de que nada pudiera moverse.**

**Segunda etapa: sin contrato formal.** El estilo REST, que se impuso después, no
traía ningún mecanismo de contrato. La API era un conjunto de rutas que devolvían
JSON, y **la documentación se escribía a mano en un archivo aparte**.

Eso resolvió la rigidez y creó el problema opuesto, que es el que este módulo
combate: **un documento escrito a mano se desactualiza el día que alguien cambia un
campo y no lo actualiza.** Y a partir de ese momento el documento no avisa que
miente: sigue ahí, prolijo, describiendo algo que ya no existe. El cliente
implementa contra la mentira y el error aparece en integración.

**Tercera etapa: el contrato derivado del código.** En 2011, Tony Tam publicó
**Swagger**, con una idea intermedia: que la especificación se genere a partir del
código, en un formato legible tanto por humanos como por herramientas. En 2015 el
proyecto se donó a la Linux Foundation y pasó a llamarse **OpenAPI**; su versión
3.1, de 2021, se alineó con JSON Schema.

La combinación gana las dos cosas: **el contrato no se puede desactualizar** —porque
no existe separado del código— y **no acopla** —porque no se generan las dos partes
del mismo archivo, sino que cada una lo lee y decide qué hacer—.

Falta la otra mitad de la historia: **cómo se declaran esas formas.** Durante años
la validación se programaba a mano, con condicionales que revisaban cada campo. En
2017, Samuel Colvin publicó **Pydantic**, con una propuesta distinta: **usar las
anotaciones de tipo del propio lenguaje** —que existían desde Python 3.5 y hasta
entonces eran sólo documentación— para validar en tiempo de ejecución. Su versión 2,
de 2023, reescribió el núcleo en Rust y lo volvió lo bastante rápido para no ser un
costo.

De ese recorrido salen las cuatro decisiones de diseño que gobiernan el capítulo.

**Primera: el tipo es la validación.** No se declara y además se valida: **declarar
es validar**. Es lo que el Capítulo 1 señaló al decir que las anotaciones dejaron de
ser documentación y pasaron a ser comportamiento.

**Segunda: el contrato se deriva del código.** Es la lección de las tres etapas.

**Tercera: fallar temprano y con detalle.** Si la entrada no cumple, se rechaza
**antes** de que corra la lógica, y el rechazo dice exactamente qué campo falló, qué
se esperaba y qué llegó.

**Cuarta: entrada y salida son cosas distintas.** El modelo con el que se recibe no
es el modelo con el que se responde, y ninguno de los dos es la tabla. La sección
2.6 desarrolla por qué.

*(Ver Figura 2.1: del contrato generado al contrato derivado.)*

> **💡 PARA ENTENDER**
> Fijate en el patrón, porque es el mismo que vas a encontrar en toda la carrera:
>
> **SOAP resolvió el desajuste haciendo que nada pudiera moverse. REST resolvió la
> rigidez perdiendo la garantía. OpenAPI busca el punto medio.**
>
> Nadie inventó nada mágico. Cada etapa **resignó algo distinto**, y la que ganó fue
> la que resignó lo que menos dolía en ese momento.
>
> Y ojo con la trampa: no es que OpenAPI sea "la solución definitiva". Es la solución
> a los problemas de las dos anteriores, con sus propios costos —que el contrato
> depende de que vos declares bien los tipos, por ejemplo—.
>
> **La pregunta que te tenés que hacer con cada herramienta es siempre la misma:
> ¿qué resignó para funcionar?** Si no lo ves, todavía no la entendiste.

---

## 2.3. Anatomía de un modelo

Un modelo declara la forma de un dato:

```python
from decimal import Decimal
from typing import Annotated
from pydantic import BaseModel, Field

class ProductoCreate(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=120)]
    descripcion: Annotated[str | None, Field(max_length=500)] = None
    precio: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]
    categoria_id: Annotated[int, Field(gt=0)]
    disponible: bool = True
```

Cada línea declara cuatro cosas a la vez, y conviene tenerlas separadas:

| Elemento | En `nombre` | Qué determina |
| --- | --- | --- |
| Nombre del campo | `nombre` | La clave en el JSON |
| Tipo | `str` | Qué se acepta y a qué se convierte |
| Restricciones | `min_length=1, max_length=120` | Qué valores son válidos dentro del tipo |
| Valor por defecto | *(no tiene)* | Si el campo es obligatorio o no |

La última fila es la que más confusión genera, y la regla es simple: **un campo sin
valor por defecto es obligatorio.** `descripcion` tiene `= None`, así que se puede
omitir. `nombre` no tiene, así que omitirlo produce un error.

Nótese que **`str | None` y "opcional" no son lo mismo.** El tipo dice qué valores
admite; el valor por defecto dice si se puede omitir. Un campo puede ser
`str | None` y obligatorio a la vez —hay que mandarlo, y puede ser nulo—, y eso, que
parece una sutileza, es exactamente lo que la sección 2.6 va a necesitar.

> **⚠️ OJO ACÁ**
> Esta distinción confunde a todo el mundo, así que mirá las cuatro combinaciones
> juntas y quedate con la tabla:
>
> ```python
> a: str                    # obligatorio, no admite nulo
> b: str | None             # OBLIGATORIO, admite nulo   ← el que sorprende
> c: str = "x"              # opcional, no admite nulo
> d: str | None = None      # opcional, admite nulo
> ```
>
> El caso `b` es el que nadie espera: **hay que mandarlo sí o sí, pero podés mandar
> `null`.** Si te olvidás de poner `= None`, tu campo "opcional" no es opcional y el
> cliente se come un `422` que no entiende.
>
> La regla, y no tiene excepciones:
>
> - **El tipo** responde *¿qué valores acepto?*
> - **El valor por defecto** responde *¿se puede omitir?*
>
> Son dos preguntas distintas. Que la respuesta a las dos suela ser `None` es lo que
> hace que se confundan.

Las restricciones más usadas:

| Restricción | Aplica a | Ejemplo del dominio |
| --- | --- | --- |
| `gt`, `ge`, `lt`, `le` | Números | `gt=0` para un precio |
| `min_length`, `max_length` | Textos y listas | `max_length=120` para un nombre |
| `pattern` | Textos | Un código de unidad |
| `max_digits`, `decimal_places` | Decimales | `DECIMAL(10,2)` para importes |

Y para valores cerrados —un conjunto fijo de opciones— corresponde una
enumeración:

```python
from enum import StrEnum

class EstadoPedido(StrEnum):
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    EN_PREPARACION = "en_preparacion"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"
```

Eso hace tres cosas: **rechaza** cualquier valor fuera de la lista, **documenta** los
cinco valores en la especificación, y —esto es lo que conviene señalar— **es
exactamente lo que la otra mitad de la cursada escribe como unión literal en
TypeScript.** Los dos lados expresan la misma restricción con la herramienta de su
lenguaje, y la especificación de OpenAPI es lo que los mantiene alineados.

### 2.3.1. Cuando la restricción no entra en un campo

Las restricciones declarativas cubren la mayoría de los casos, pero no todos. Dos
situaciones se les escapan, y para cada una hay una herramienta.

**Una regla sobre un solo campo que no es una restricción estándar.** Por ejemplo,
que un nombre no sea sólo espacios en blanco:

```python
from pydantic import field_validator

class ProductoCreate(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=120)]

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, v: str) -> str:
        limpio = v.strip()
        if not limpio:
            raise ValueError("El nombre no puede ser sólo espacios")
        return limpio          # devolver el valor normalizado
```

Nótese que el validador **devuelve un valor**, y ese valor es el que queda. Sirve
tanto para rechazar como para normalizar: recortar espacios, pasar a minúsculas,
unificar formato. Normalizar en el borde evita que cada consulta después tenga que
contemplar variantes.

**Una regla que involucra dos campos a la vez.** Ninguna restricción de campo puede
expresar "la fecha de fin tiene que ser posterior a la de inicio", porque necesita
ver los dos. Para eso existe la validación a nivel de modelo, que corre **después**
de que todos los campos se validaron por separado:

```python
from pydantic import model_validator

class RangoDeFechas(BaseModel):
    desde: date
    hasta: date

    @model_validator(mode="after")
    def rango_coherente(self):
        if self.hasta < self.desde:
            raise ValueError("hasta no puede ser anterior a desde")
        return self
```

El TPI usa este par de fechas en varios endpoints de estadísticas, y su sección 6.1
agrega una precisión que conviene retener: **los pares `desde` y `hasta` son fechas
civiles interpretadas en la zona horaria de la aplicación**, mientras que todas las
marcas de tiempo se almacenan y se devuelven en UTC. Son dos cosas distintas
viviendo en la misma petición.

Y una advertencia de criterio: **estas herramientas son para reglas del contrato, no
para reglas de negocio.** Que un nombre no sea espacios es del contrato. Que un
producto no se pueda vender sin stock es del dominio, y va en el Service. Meter
reglas de negocio en el schema las vuelve imposibles de probar sin construir una
petición HTTP.

---

## 2.4. Qué ocurre durante la validación

Al llegar una petición, el marco de trabajo ejecuta cuatro pasos **antes** de que el
handler corra. Conocer el orden importa, porque explica algunos comportamientos que
sorprenden.

1. **Parseo.** El cuerpo se interpreta según su `Content-Type`. Si el JSON está mal
   formado, el error es de sintaxis y no llega a la validación.
2. **Coerción.** Los valores se convierten al tipo declarado cuando la conversión es
   inequívoca. La cadena `"5"` se convierte a `5` para un campo `int`.
3. **Validación.** Se comprueban las restricciones sobre los valores ya convertidos.
4. **Construcción.** Se arma la instancia del modelo, que es lo que recibe el
   handler.

*(Ver Figura 2.2: los cuatro pasos y dónde nace el 422.)*

El paso 2 merece atención porque es una decisión de diseño, no un descuido. Por
defecto, el modo es **permisivo**: si un valor se puede convertir sin ambigüedad, se
convierte. Eso es razonable para HTTP, donde **todo llega como texto**: un parámetro
de consulta es siempre una cadena, y exigir que el cliente distinga tipos que la
URL no puede expresar sería absurdo.

Pero tiene una contracara que conviene conocer: **la coerción puede ocultar un error
del cliente.** Si alguien manda `"1234.50"` donde va un `Decimal`, se acepta. Si
manda `1234.5` como número de punto flotante, también —y ahí ya se perdió precisión
antes de llegar—. Por eso el TPI declara que **los importes viajan como cadena**: no
es sólo para el cliente, es para que no haya conversión intermedia por punto
flotante. La sección 2.7 lo desarrolla.

Cuando la validación falla, la respuesta es un **`422`** con el detalle:

```json
{
  "detail": [
    {
      "type": "greater_than",
      "loc": ["body", "precio"],
      "msg": "Input should be greater than 0",
      "input": "-100.00"
    }
  ]
}
```

Cuatro campos, y los cuatro sirven: **`loc`** dice dónde —cuerpo, ruta, consulta— y
qué campo; **`type`** es un código estable, apto para comparar por programa;
**`msg`** es para una persona; **`input`** es lo que efectivamente llegó.

Y hay algo que ese cuerpo enseña sin proponérselo: **es una lista.** La validación
no se detiene en el primer error, sino que reporta todos los que encuentra. Un
formulario con cuatro campos mal cargados recibe los cuatro de una vez, y no
obliga al usuario a corregir de a uno.

> **⚠️ OJO ACÁ**
> Sobre la coerción hay una cosa que te va a morder, así que anticipala:
>
> **Que un valor se acepte no significa que el cliente lo haya mandado bien.**
>
> ```python
> class Filtro(BaseModel):
>     activo: bool
>
> # Todo esto se acepta y vale True:
> {"activo": true}     {"activo": "true"}     {"activo": 1}     {"activo": "yes"}
> ```
>
> Eso está bien para HTTP —de una URL todo llega como texto— y está mal cuando
> disimula un bug del cliente. Si el frontend te manda `"yes"` porque alguien
> concatenó mal, vos nunca te enterás: lo aceptaste.
>
> Y ojo con el caso feo: **si el cliente te manda un importe como número JSON en vez
> de cadena, se acepta igual** — y para cuando llegó a tu modelo, JavaScript ya lo
> convirtió a punto flotante y le comió precisión. Por eso el TPI declara `string` de
> los dos lados: no es una preferencia, es cerrar esa puerta.
>
> Cuando quieras que no haya coerción, existe el modo estricto. Usalo donde importe.

---

## 2.5. Modelos segregados: por qué tres y no uno

La tentación natural es escribir un solo modelo por entidad y usarlo para todo.
Conviene ver por qué no funciona antes de aceptar la alternativa.

Un `Producto` tiene identificador, nombre, precio, fecha de creación, y quizá un
campo interno de costo que no debe salir nunca. Con un solo modelo aparecen tres
problemas a la vez:

**Al crear** no se manda el identificador —lo asigna el servidor— ni la fecha de
creación. Si el modelo los declara obligatorios, crear es imposible; si los declara
opcionales, la especificación dice que el cliente **podría** mandarlos, que es
mentira.

**Al actualizar** no se mandan todos los campos, sino los que cambian. Un modelo con
campos obligatorios no sirve para eso.

**Al responder** hay campos que no deben salir. Un modelo compartido los expone, y
esa clase de filtración no produce ningún error: simplemente el dato viaja.

De ahí la práctica que el temario oficial nombra como **modelos segregados** y que
el TPI aplica en su sección 7:

| Modelo | Para qué | Qué tiene |
| --- | --- | --- |
| **`Create`** | Entrada al crear | Sólo lo que el cliente aporta. Campos obligatorios |
| **`Update`** | Entrada al modificar | Lo mismo, **todo opcional** |
| **`Public`** | Salida | Lo que se puede mostrar. Incluye lo que genera el servidor |

```python
class ProductoBase(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=120)]
    precio: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]

class ProductoCreate(ProductoBase):
    categoria_id: Annotated[int, Field(gt=0)]

class ProductoUpdate(BaseModel):
    nombre: Annotated[str | None, Field(min_length=1, max_length=120)] = None
    precio: Annotated[Decimal | None, Field(gt=0)] = None

class ProductoPublic(ProductoBase):
    id: int
    creado_en: datetime
    # el costo interno no está: no sale nunca
```

*(Ver Figura 2.3: los tres modelos y qué campo aparece en cada uno.)*

Y del lado del endpoint, `response_model` cierra el círculo:

```python
@app.get("/productos/{producto_id}", response_model=ProductoPublic)
async def obtener_producto(producto_id: int):
    ...
```

Eso no es documentación: **el marco de trabajo filtra la respuesta contra ese
modelo.** Si el objeto devuelto trae campos de más, **no salen**. Es una red de
seguridad real, y por eso el TPI la declara en su sección 7.

> **💡 PARA ENTENDER**
> `response_model` es de las cosas más subestimadas del marco de trabajo, y te
> explico por qué te conviene usarlo siempre.
>
> **Filtra la salida aunque tu código se equivoque.**
>
> Pensá el caso concreto: hoy el modelo de la tabla no tiene ningún campo sensible.
> Dentro de tres meses alguien agrega `costo_interno` para calcular márgenes. Si el
> endpoint devuelve el objeto tal cual, **ese campo empieza a viajar al cliente ese
> mismo día**, sin que nadie lo note.
>
> Con `response_model`, no sale. Nadie tuvo que acordarse de nada.
>
> Es la misma idea que tus compañeros del turno de frontend ven en su última clase:
> **las reglas que dependen de que alguien se acuerde fallan; las que hacen que
> equivocarse sea difícil, no.**

---

## 2.6. Actualización parcial: ausente contra nulo

Acá aparece un problema que parece de detalle y no lo es, y el TPI lo resuelve
explícitamente en su sección 6.1.

Cuando llega una modificación parcial, hay **tres situaciones distintas** para cada
campo, y sólo dos son fáciles:

| El cliente... | Significa | Qué hay que hacer |
| --- | --- | --- |
| Manda `{"nombre": "Napolitana"}` | "Cambiá el nombre a esto" | Actualizar |
| **No manda `nombre`** | "No toques el nombre" | **Dejarlo intacto** |
| Manda `{"nombre": null}` | "Vaciá el nombre" | Poner nulo |

La segunda y la tercera fila **se ven iguales** si sólo se mira el objeto ya
construido: en las dos, `modelo.nombre` vale `None`. Y son órdenes opuestas.

La distinción se resuelve preguntando **qué campos vinieron efectivamente**, y el
TPI declara cómo:

> Los schemas `Update` tienen **todos sus campos opcionales** y el Service aplica
> **`model_dump(exclude_unset=True)`**. Omitir un campo lo deja intacto; enviarlo
> explícitamente lo cambia.

```python
datos = producto_update.model_dump(exclude_unset=True)
for campo, valor in datos.items():
    setattr(producto, campo, valor)
```

`exclude_unset=True` devuelve **sólo los campos que el cliente mandó**. Si no mandó
`nombre`, no aparece en el diccionario y el bucle no lo toca. Si lo mandó como
nulo, aparece con valor nulo y se aplica.

> **⚠️ OJO ACÁ**
> Este es el bug más elegante y más difícil de encontrar de todo el capítulo, así
> que mirá bien:
>
> ```python
> # MAL: model_dump() sin exclude_unset devuelve TODOS los campos
> datos = producto_update.model_dump()
> for campo, valor in datos.items():
>     setattr(producto, campo, valor)
> ```
>
> El cliente mandó `{"precio": "5000.00"}` para cambiar sólo el precio. Pero
> `model_dump()` sin argumentos devuelve **todos los campos del modelo**, y los que
> el cliente no mandó valen `None` por ser opcionales.
>
> **Resultado: le cambiaste el precio y le borraste el nombre, la descripción y la
> categoría.**
>
> Y lo peor es cómo se manifiesta. El endpoint devuelve `200`. No hay excepción, no
> hay log de error. Alguien entra tres días después y ve productos sin nombre, y
> nadie puede reconstruir qué pasó.
>
> **Un solo argumento separa una actualización parcial de un borrado silencioso.**
> Por eso el TPI lo declara en la sección 6.1 en vez de dejarlo a criterio.

---

## 2.7. El dinero y las cantidades

El TPI es taxativo en su sección 6.1, y conviene citarlo entero porque cada parte
tiene su razón:

> Todos los importes son **`DECIMAL(10,2)`** en la moneda declarada, y viajan en JSON
> como **cadena decimal** —`"1234.50"`—. **El tipo TypeScript espejo es `string`.**

Y para las cantidades de insumo:

> Las cantidades de receta y de stock de insumo son **`DECIMAL(12,3)`** y viajan
> también como cadena decimal, **acompañadas siempre del código de la unidad**.

Tres decisiones, tres razones distintas.

**Por qué `Decimal` y no punto flotante.** El formato de punto flotante representa
los números en base dos, y hay decimales que en base dos son periódicos. `0.1` es
uno de ellos. Sumar importes en punto flotante acumula diferencias de centavos que
después no cierran contra la facturación. `Decimal` representa exactamente lo que se
le da.

**Por qué viaja como cadena.** Porque JSON no distingue entre un entero, un decimal
y un punto flotante: tiene un solo tipo numérico. Si el importe viajara como número,
**el cliente lo convertiría a punto flotante al parsearlo**, y el error aparecería
del otro lado sin que el servidor pudiera hacer nada. Mandarlo como texto garantiza
que llegue exactamente igual.

**Por qué la cantidad viaja con su unidad.** Un `"1.500"` no significa nada por sí
solo: puede ser un kilo y medio o mil quinientos gramos. El TPI exige que la unidad
acompañe al número siempre, y eso elimina una clase entera de errores.

*(Ver Figura 2.4: el importe de la base al cliente, y dónde se convierte.)*

> **📌 NOTA**
> Guardá esto porque es el mejor ejemplo del módulo de **una decisión que atraviesa
> los dos lados del sistema.**
>
> Vos declarás `Decimal` en el modelo y `string` en el schema. Tus compañeros del
> turno de frontend declaran `total: string` en TypeScript y tienen prohibido operar
> con ese valor. **Es la misma decisión, tomada dos veces, por la misma razón.**
>
> Y del lado de ellos hay un detalle que te va a interesar: el TPI dice que el
> garante de esa regla **es el tipo de TypeScript**, porque si dijera `number` el
> compilador dejaría escribir `total * cantidad`. Diciendo `string`, lo rechaza — no
> porque entienda de dinero, sino porque no se puede multiplicar texto.
>
> Fijate lo que eso significa: **la restricción la impone el tipo, no la disciplina
> de quien escribe.** Y de este lado pasa igual: `Decimal` no te deja perder
> precisión aunque quieras.

---

## 2.8. Los verbos y sus códigos

El TPI declara en su sección 6.1 qué verbo se usa para qué, y hay una decisión que
conviene destacar porque contradice lo que se enseña habitualmente:

> `POST` crea o ejecuta un comando, `GET` lee, `DELETE` borra. **`PATCH` modifica de
> forma parcial y es el verbo de toda actualización. No se usa `PUT`: ningún
> endpoint reemplaza el recurso completo.**

La razón es coherente con la sección 2.6. `PUT` significa "reemplazá el recurso por
esto", y por lo tanto exige mandarlo **entero**: si un campo falta, se borra. En una
interfaz real casi nunca se manda todo, así que un `PUT` mal usado —mandando sólo
lo que cambió— borra el resto. **El TPI evita el problema quitando el verbo.**

Y los códigos de estado, que el Capítulo 1 de la otra mitad de la cursada estudia
desde el lado del cliente:

| Situación | Código | Detalle |
| --- | --- | --- |
| Lectura exitosa | `200` | |
| Creación exitosa | `201` | Con `Location` apuntando al recurso creado |
| Borrado exitoso | `204` | Sin cuerpo |
| Entrada inválida | `422` | El de la sección 2.4 |
| No autenticado | `401` | Falta la credencial o no vale |
| Autenticado sin permiso | `403` | La credencial vale, el rol no alcanza |
| No existe | `404` | |
| Conflicto de estado | `409` | Por ejemplo, stock insuficiente |

La distinción entre `401` y `403` merece énfasis porque se maltrata todo el tiempo:
**`401` dice "no sé quién sos"; `403` dice "sé quién sos y no te alcanza".** Un
cliente que los trata igual manda al login a alguien que ya inició sesión.

> **📌 NOTA**
> Sobre el `201` hay un detalle que casi nadie pone y el TPI sí pide: **el encabezado
> `Location`.**
>
> ```python
> @app.post("/productos", status_code=201)
> async def crear_producto(datos: ProductoCreate, response: Response):
>     producto = _crear(datos)
>     response.headers["Location"] = f"/api/v1/productos/{producto.id}"
>     return producto
> ```
>
> ¿Para qué sirve? Para que el cliente sepa **dónde quedó** lo que acaba de crear, sin
> tener que armar la URL por su cuenta adivinando el formato.
>
> Parece poco. Pero fijate el efecto: si mañana las rutas cambian de
> `/productos/{id}` a `/catalogo/productos/{id}`, un cliente que usa `Location` sigue
> funcionando. Uno que arma la URL a mano, no.
>
> Es el mismo principio de todo el capítulo: **cuanto menos tenga que adivinar el
> cliente, menos se puede romper.**

---

## 2.9. Colecciones: envoltorio, paginación y ordenamiento

Devolver una lista suelta funciona hasta que la lista crece. El TPI lo resuelve con
una convención declarada:

> Toda colección cuyo tamaño puede crecer con el uso devuelve el envoltorio
> **`{ items, total, page, size, pages }`**.

Los cuatro campos que acompañan a `items` son los que el cliente necesita para
dibujar un paginador, y no se pueden deducir de la lista: **cuántos hay en total,
en qué página está, de qué tamaño, y cuántas páginas hay.**

Las reglas de paginación del TPI:

| Regla | Valor |
| --- | --- |
| Tamaño por defecto | 20 |
| Tamaño máximo | **100** |
| Página máxima | El `pages` de esa consulta; más allá responde **`422`** |
| El `total` | **Respeta los filtros activos** |

Dos de esas filas son decisiones y no detalles.

**El tamaño máximo existe para protegerse.** Sin él, un cliente puede pedir un
millón de registros y el servidor intenta cumplir: arma la consulta, la trae a
memoria, la serializa. No hace falta mala intención —alcanza con un error de
tipeo— y el efecto es el mismo que un ataque.

**El `total` respeta los filtros.** Si hay un filtro por categoría, el total es el de
esa categoría y no el de la tabla. Suena obvio y se equivoca seguido, porque
calcular el total sin filtros es más fácil.

> **⚠️ OJO ACÁ**
> El bug del total sin filtrar es de los que llegan a producción y nadie reporta
> como bug, porque **el sistema no falla: miente despacio.**
>
> El usuario filtra por "Empanadas", ve 8 productos en pantalla, y el paginador le
> dice **"1 de 12 páginas"**. Hace clic en la página 2 y no hay nada. Vuelve, prueba
> la 3, tampoco.
>
> No hay error, no hay excepción, no hay nada en los logs. Simplemente el paginador
> está contando los 240 productos de la tabla en vez de los 8 que cumplen el filtro.
>
> La causa es siempre la misma y es la vía fácil: se arma la consulta con filtros
> para traer los ítems, y el conteo se hace aparte **sobre la tabla entera** porque
> es una línea más corta.
>
> **Regla: el conteo y la búsqueda salen de la misma consulta filtrada.** Si escribís
> dos consultas distintas, la segunda tiene que llevar exactamente los mismos filtros
> que la primera.

Para el orden, el TPI usa una convención compacta:

> Parámetro `sort` con el nombre del campo, **precedido de un guion para orden
> descendente**.

Así, `sort=nombre` ordena ascendente y `sort=-creado_en` descendente. Y cada
endpoint **declara en su tabla qué campos son ordenables**, lo que no es un detalle
de comodidad: aceptar un nombre de campo arbitrario del cliente y meterlo en una
consulta es exactamente la puerta que la sección 2.13 estudia.

Los parámetros de consulta se declaran como los demás, y por lo tanto **se validan
igual**:

```python
@app.get("/productos", response_model=Pagina[ProductoPublic])
async def listar_productos(
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
    sort: Annotated[str | None, Query(pattern=r"^-?(nombre|precio|creado_en)$")] = None,
    categoria_id: Annotated[int | None, Query(gt=0)] = None,
    q: Annotated[str | None, Query(min_length=2, max_length=80)] = None,
):
    ...
```

Cinco decisiones en cinco líneas, y ninguna es cosmética. El `le=100` **es** el
límite de tamaño de la tabla anterior, declarado donde se aplica. El `pattern` del
ordenamiento **es** la lista blanca de campos ordenables: lo que no está en esa
expresión no llega a la consulta. El `ge=1` de la página evita el cero y los
negativos. Y el mínimo de dos caracteres en la búsqueda evita que una sola letra
recorra la tabla entera.

Nótese que **la lista blanca vive en el mismo lugar que la documentación**: quien
lea la especificación va a ver exactamente qué valores admite `sort`, sin que nadie
lo escriba aparte.

---

## 2.10. Errores: un formato normado

El TPI no inventa su formato de error: adopta uno normado.

> Formato de error conforme a la **RFC 9457**, `Content-Type:
> application/problem+json`.

Esa norma —*Problem Details for HTTP APIs*— define una forma estándar para
describir un error, con campos como `type`, `title`, `status`, `detail` e
`instance`. Adoptarla tiene una ventaja concreta sobre inventar un formato propio:
**cualquier cliente que la conozca sabe leer el error sin documentación
adicional.**

Sobre esa base, la sección 14.1 del TPI define un **catálogo de códigos de error**:
una lista donde cada situación del dominio tiene un código estable, su código HTTP y
la descripción de cuándo se produce.

La existencia de ese catálogo es una decisión de diseño con consecuencias para las
dos mitades de la cursada, y conviene entender cuál:

**El cliente puede distinguir casos por un código y no por el texto del mensaje.**
Comparar textos es frágil —cambian, se corrigen, se traducen— y un código no. Con
catálogo, el cliente puede mostrar una pantalla distinta ante "stock insuficiente"
que ante "producto no disponible", y esa lógica no se rompe cuando alguien mejora
la redacción del mensaje.

Del lado del servidor, eso se traduce en una regla que el Capítulo 1 ya adelantó:
**el Router no traduce excepciones.** El Service lanza excepciones de dominio, y un
manejador global —que la clase 8 estudia— las convierte al formato normado. La
razón es la de siempre: con setenta endpoints traduciendo por su cuenta, basta con
que uno difiera.

En esta clase, sin base de datos todavía, alcanza con `HTTPException` para los casos
simples:

```python
@app.get("/productos/{producto_id}", response_model=ProductoPublic)
async def obtener_producto(producto_id: int):
    producto = _almacen.get(producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto
```

Eso es correcto para un CRUD en memoria y **deja de serlo apenas aparece el
Service**. La razón se ve mejor con un ejemplo del dominio: cuando el Service de
pedidos detecta que no hay stock, no puede lanzar una excepción HTTP, porque **el
Service no sabe que existe HTTP**. La misma función la invoca una tarea del worker,
donde no hay ninguna petición que responder.

Lo que el Service lanza es una excepción de dominio:

```python
class StockInsuficiente(ErrorDeDominio):
    codigo = "STOCK_INSUFICIENTE"
    estado_http = 409
```

Y el manejador global la traduce, una sola vez, para todos los endpoints. Esta clase
usa `HTTPException` porque todavía no hay Service; **la clase 8 hace el cambio y
explica por qué era inevitable.**

> **📌 NOTA**
> Una decisión de esta sección que vale para cualquier API que escribas:
>
> **Un mensaje de error es para una persona. Un código de error es para un
> programa.** Hacen falta los dos y no se reemplazan.
>
> Si sólo mandás mensaje, el cliente termina haciendo
> `if (error.message.includes("stock"))`, y eso se rompe el día que alguien corrige
> una tilde.
>
> Si sólo mandás código, la persona que abre las herramientas de desarrollo ve
> `ERR_4021` y no sabe qué pasó.
>
> Y hay un tercer nivel que casi nadie pone y es el que más ayuda: **qué puede hacer
> el cliente al respecto.** No es lo mismo "no hay stock" —esperá o cambiá el
> producto— que "el pedido ya fue entregado" —no hay nada que hacer—. Esa distinción
> es la que permite del otro lado mostrar un botón de reintentar o no mostrarlo.

---

## 2.11. Observabilidad: el identificador de petición

El TPI declara una convención que parece menor y resuelve un problema grande:

> Todas las respuestas llevan el encabezado **`X-Request-Id`**, que también aparece
> en cada línea de log de esa petición **y viaja hasta las tareas que la petición
> encoló.**

El problema que resuelve es concreto. Un usuario reporta que algo falló. En los
registros del servidor hay miles de líneas de decenas de peticiones simultáneas, y
sin un identificador **no hay forma de saber cuáles corresponden a la suya.**

Con un identificador que viaja en la respuesta, ese usuario —o el frontend, que lo
puede registrar— aporta un dato que permite filtrar los registros y ver **sólo esa
petición**, de punta a punta.

Y la última parte de la cita es la que más vale: **el identificador viaja hasta las
tareas.** Una petición puede encolar trabajo que se ejecuta minutos después en otro
proceso; sin ese arrastre, un error en el worker es imposible de atar a lo que lo
originó. Es la regla TB-06, que la clase 8 desarrolla.

---

## 2.12. Herramientas de diagnóstico

**La documentación interactiva** vuelve a ser la herramienta principal, y ahora con
más para mirar: cada endpoint muestra el schema de entrada con sus restricciones,
el de salida, y los códigos de error posibles. Ejecutar desde ahí con datos
inválidos es la forma más rápida de verificar que la validación hace lo que se
espera.

*(Ver Figura 2.5: un `422` y su detalle en la documentación interactiva.)*

**La especificación en crudo** es lo que hay que abrir cuando el frontend reporta un
desajuste. Es el contrato, y la discusión se resuelve ahí.

*(Ver Figura 2.6: el fragmento de la especificación correspondiente a un schema.)*

**El propio modelo, en una consola de Python**, es la forma más rápida de probar una
validación sin levantar el servidor:

```python
>>> ProductoCreate.model_validate({"nombre": "", "precio": "-1"})
ValidationError: 2 validation errors for ProductoCreate
```

Dos errores, no uno: la validación reporta todo lo que encuentra.

Y **`model_json_schema()`** devuelve el esquema del modelo, que es literalmente lo
que aparece en la especificación. Es útil para verificar que una restricción quedó
declarada donde se pensaba.

> **💡 PARA ENTENDER**
> Un hábito que te va a servir toda la carrera y que casi nadie adopta: **probá tus
> modelos en la consola antes de levantar el servidor.**
>
> ```python
> >>> from app.schemas import ProductoCreate
> >>> ProductoCreate.model_validate({"nombre": "Milanesa", "precio": "4750.00",
> ...                                "categoria_id": 3})
> ProductoCreate(nombre='Milanesa', precio=Decimal('4750.00'), categoria_id=3)
> ```
>
> Fijate lo que ganaste: **el ciclo de prueba pasó de "levantar el servidor, abrir el
> navegador, armar el cuerpo, mandar" a una línea.**
>
> Y hay algo más importante que la velocidad. Un modelo se puede probar **sin FastAPI,
> sin servidor y sin red**, porque es una clase común de Python. Eso significa que
> también se puede testear así, y los tests de tus schemas van a correr en
> milisegundos.
>
> Es la misma idea de la actividad 8 que viste en la clase 1: **lo que no depende de
> nada se prueba solo.** Tus schemas no dependen de nada. Aprovechalo.

> **🧪 EXPERIMENTO**
> El experimento de esta clase demuestra por qué el contrato importa, y conviene
> hacerlo de a dos.
>
> 1. Escribí `ProductoCreate` con sus restricciones y levantá el proyecto.
> 2. Abrí la documentación interactiva y **mandá cinco cuerpos inválidos distintos**:
>    nombre vacío, precio negativo, precio con tres decimales, categoría cero, y un
>    campo de más que no existe en el modelo.
> 3. Anotá qué respondió cada uno. Fijate especialmente en el último.
> 4. Ahora mandá **dos errores a la vez** y contá cuántos te reporta.
>
> Cinco validaciones que no escribiste, y un cuerpo de error que dice exactamente qué
> falló en cada caso.
>
> 5. Último paso, y es el que importa: **pasale la URL de la documentación a alguien
>    del turno de frontend y pedile que arme el cuerpo correcto sin que le expliques
>    nada.**
>
> Si puede hacerlo, tu contrato está bien. Si tiene que preguntarte algo, **eso que
> te preguntó es lo que falta declarar** — y es mejor descubrirlo hoy que en la
> semana de integración.

---

## 2.13. Seguridad y evolución

Tres consideraciones cierran el capítulo.

**El modelo de salida es un control de seguridad, no una comodidad.** `response_model`
filtra lo que sale aunque el objeto traiga de más. Sin él, cada campo que alguien
agregue al modelo de datos **empieza a viajar al cliente el día que se agrega**, sin
que nadie lo decida.

**Los campos que el cliente no debería poder fijar no van en el modelo de entrada.**
Es el mismo principio del lado contrario: si el modelo `Create` incluye
`es_administrador`, el cliente lo puede mandar. Y no hace falta que la interfaz lo
ofrezca: alcanza con emitir la petición a mano, que es exactamente lo que hace quien
quiere atacar el sistema.

**Un parámetro que nombra un campo de la base es una superficie de ataque.** El
ordenamiento de la sección 2.9 recibe un nombre de campo del cliente; si ese nombre
se interpola en una consulta sin validar contra una lista blanca, se abre la puerta
a una inyección. Por eso el TPI exige que **cada endpoint declare qué campos son
ordenables**: la lista blanca no es documentación, es la defensa.

Sobre la evolución, dos observaciones. La primera es que el formato de error
adoptado —la RFC 9457— es de 2023 y reemplazó a una norma anterior de 2016; elegir
un estándar en lugar de un formato propio significa que **el sistema se beneficia de
esa evolución sin cambiar nada**.

La segunda es que la validación declarativa está corriéndose hacia los bordes en
todo el ecosistema: el mismo enfoque que acá valida una petición HTTP se usa para
validar configuración, mensajes de una cola y respuestas de servicios externos. Lo
que se aprende en esta clase **no es específico de la web**.

---

## 2.14. Verificación

1. Escribir un modelo con cinco restricciones distintas y **verificar cada una** con
   un valor que la viole.
2. Provocar un `422` y **leer los cuatro campos** de su detalle, explicando qué
   aporta cada uno.
3. Mandar dos errores en la misma petición y verificar que **se reportan los dos**.
4. Escribir los tres modelos segregados de una entidad y justificar **campo por
   campo** por qué está o no está en cada uno.
5. Implementar una actualización parcial con `exclude_unset=True`, y **demostrar el
   bug** que aparece sin ese argumento.
6. Declarar un importe como `Decimal` y verificar que **sale como cadena** en el
   JSON.
7. Implementar el envoltorio de colección con paginación, y verificar que el `total`
   **respeta un filtro activo**.
8. Pedir una página más allá del máximo y verificar que responde `422`.
9. Devolver un objeto con un campo de más y **verificar que `response_model` lo
   filtra**.

---

## 2.15. Errores frecuentes

**Usar un solo modelo para entrada y salida.** Obliga a declarar opcionales campos
que el servidor genera, y expone campos que no deberían salir (sección 2.5).

**Olvidar `exclude_unset=True` en una actualización parcial.** Borra silenciosamente
todos los campos que el cliente no mandó, y responde `200` (sección 2.6).

**Confundir "puede ser nulo" con "se puede omitir".** El tipo dice qué valores
admite; el valor por defecto dice si es obligatorio (sección 2.3).

**Declarar un importe como `float`.** Reintroduce el error de punto flotante que
`Decimal` evita (sección 2.7).

**Devolver el importe como número JSON.** El cliente lo convierte a punto flotante al
parsearlo, y la precisión se pierde del otro lado (sección 2.7).

**Usar `PUT` para una modificación parcial.** Reemplaza el recurso completo, así que
los campos ausentes se borran. El TPI directamente no usa `PUT` (sección 2.8).

**Tratar `401` y `403` como lo mismo.** Manda al login a alguien que ya inició sesión
(sección 2.8).

**Devolver una lista suelta en lugar del envoltorio.** El cliente no puede dibujar un
paginador sin el total y las páginas (sección 2.9).

**Calcular el `total` sin los filtros activos.** El paginador miente (sección 2.9).

**No limitar el tamaño de página.** Un cliente puede pedir un millón de registros, y
alcanza con un error de tipeo (sección 2.9).

**Interpolar el campo de ordenamiento sin lista blanca.** Es una superficie de
inyección (secciones 2.9 y 2.13).

**Distinguir errores por el texto del mensaje.** Se rompe cuando alguien corrige la
redacción. Para eso está el código (sección 2.10).

**Omitir `response_model`.** Cada campo que se agregue al modelo de datos empieza a
viajar al cliente sin que nadie lo decida (sección 2.13).

---

## 2.16. Actividades

1. **Los tres modelos.** Tomar la entidad `Producto` de la sección 7 del TPI y
   escribir sus tres modelos segregados completos, con todas las restricciones que el
   documento declara. Justificar campo por campo su presencia o ausencia en cada uno.

2. **El bug del `model_dump`.** Implementar una actualización parcial de las dos
   formas —con y sin `exclude_unset`—, ejecutar la misma petición contra ambas y
   documentar el resultado. Explicar por qué la versión incorrecta responde `200`.

3. **El contrato completo de un módulo.** Implementar el CRUD en memoria del módulo
   `categorias` del TPI, con los verbos correctos, los códigos de estado de la
   sección 2.8, el envoltorio de colección y el ordenamiento. Exportar la
   especificación y **compararla con la tabla de la sección 6.5 del TPI**.

4. **El dinero de punta a punta.** Escribir un endpoint que devuelva un importe y
   verificar en el JSON crudo que sale como cadena. Después, en la consola del
   navegador, hacer `JSON.parse` de esa respuesta y comprobar qué tipo llega.
   Repetir declarando el importe como número y **documentar la diferencia**.

5. **Errores con código.** Definir cinco códigos de error propios para el módulo de
   productos, en el formato de la RFC 9457, y escribir el cliente mínimo que
   distinga entre ellos **sin leer el texto del mensaje**.

6. **Exploración: el contrato como interfaz entre equipos.** Junto con alguien del
   turno de frontend, implementar un endpoint y pedirle que escriba el cliente
   **usando únicamente la documentación interactiva**, sin conversar. Documentar cada
   pregunta que hizo falta hacer igual, y para cada una, qué habría que declarar en
   el schema para que no hiciera falta. *(Requiere coordinar con la otra mitad de la
   cursada.)*

7. **Exploración: los límites de la coerción.** Para un modelo con campos de tipo
   `int`, `bool`, `Decimal` y `datetime`, probar diez entradas ambiguas y documentar
   cuáles se aceptan y a qué valor se convierten. Repetir en modo estricto y comparar.
   Relacionar lo observado con la decisión de la sección 2.7 sobre por qué los
   importes viajan como cadena.

---

## 2.17. Síntesis

1. La historia del contrato entre sistemas tiene tres etapas, y cada una **resignó
   algo distinto**: el contrato generado eliminó el desajuste al precio de que nada
   pudiera moverse; REST recuperó la flexibilidad perdiendo la garantía; la
   especificación derivada del código busca las dos cosas.

2. **Declarar es validar.** Las anotaciones de tipo dejaron de ser documentación y
   pasaron a ser comportamiento: validan, convierten y documentan a la vez.

3. La validación ocurre **antes** del handler y reporta **todos** los errores que
   encuentra, no el primero.

4. La coerción es deliberada —de una URL todo llega como texto— y tiene una
   contracara: **puede disimular un error del cliente**.

5. **El tipo dice qué valores admite; el valor por defecto dice si es obligatorio.**
   Son dos cosas distintas y confundirlas rompe la actualización parcial.

6. Hacen falta **tres modelos y no uno**: lo que el cliente aporta, lo que puede
   cambiar y lo que se le muestra. Un modelo compartido obliga a mentir en la
   especificación y expone campos que no deben salir.

7. **`exclude_unset=True` separa una actualización parcial de un borrado
   silencioso.** Sin él, los campos que el cliente no mandó se pisan con nulo, y la
   respuesta es `200`.

8. **El dinero es `Decimal` adentro y cadena afuera**, y las dos mitades tienen su
   razón: exactitud del lado del servidor, y que el cliente no lo convierta a punto
   flotante al parsearlo.

9. El TPI **no usa `PUT`**, porque reemplazar el recurso completo borra lo que no se
   mandó. `PATCH` es el verbo de toda actualización.

10. Un **mensaje de error es para una persona y un código es para un programa**.
    Hacen falta los dos, y comparar textos es frágil.

11. El **identificador de petición** convierte miles de líneas de registro en las
    diez que corresponden a un problema concreto, y viaja hasta las tareas que esa
    petición encoló.

---

## 2.18. Referencias y lecturas complementarias

Las fuentes normativas de este capítulo son tres. El formato de error corresponde a
la **RFC 9457**, *Problem Details for HTTP APIs* (2023), que reemplazó a la RFC 7807
y define los campos que el TPI adopta en su sección 6.1. Los códigos de estado y la
semántica de los métodos están en la **RFC 9110**, ya citada por la otra mitad de la
cursada; su sección sobre `PATCH` remite a la **RFC 5789**, que lo introdujo y
explica en qué se diferencia de `PUT`. Y el formato de la especificación que el
marco de trabajo genera es **OpenAPI 3.1**, mantenido por la OpenAPI Initiative y
alineado desde esa versión con **JSON Schema**, cuya especificación conviene tener a
mano para entender cómo se traduce cada restricción.

Como documentación de referencia, la de **Pydantic** en `docs.pydantic.dev` es la
fuente para todo lo de las secciones 2.3 a 2.6, y su página sobre modos de
validación explica con precisión qué convierte y qué no. La documentación de FastAPI
sobre modelos de respuesta y sobre parámetros de consulta cubre lo que acá se trató
en las secciones 2.5 y 2.9. Para el contexto histórico de la sección 2.2, la entrada
del proyecto OpenAPI sobre su propia historia documenta el paso de Swagger a la
Linux Foundation en 2015.

Como bibliografía de estudio, el capítulo sobre diseño de APIs de Masse, *REST API
Design Rulebook* (O'Reilly, 2011) sigue siendo útil para las convenciones de la
sección 2.9, aunque conviene leerlo sabiendo que es anterior a OpenAPI. Y para el
problema general de la evolución de contratos entre servicios, el capítulo cuarto de
Kleppmann, *Designing Data-Intensive Applications* (O'Reilly, 2017) trata la
compatibilidad hacia adelante y hacia atrás con una profundidad que excede este
módulo pero que responde la pregunta que todo el mundo hace al final de esta clase:
qué pasa cuando el contrato tiene que cambiar.

Del TPI, este capítulo se apoya en la sección **6.1** —las convenciones globales,
que conviene leer entera y tener a mano—, en la sección **7** con los schemas de
cada módulo, y en la **14.1** con el catálogo de errores.

---

**Continúa en:** Capítulo 3 — El bucle de eventos del servidor, donde se estudia por
qué todos los handlers de este proyecto son asincrónicos, qué significa exactamente
que una línea "bloquee", y de dónde salen las ocho reglas que el TPI declara juntas
en su sección 1.4.
