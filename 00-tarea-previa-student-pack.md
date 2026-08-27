# Tarea previa — Verificación del GitHub Student Developer Pack

**Programación 3 — Módulo de Despliegue**
**Fecha límite: cuatro semanas antes de la Clase 1.**

---

## Por qué esto se hace ahora y no en clase

Para el módulo de despliegue cada grupo necesita un **nombre de dominio propio**. No es
opcional: sin dominio, la aplicación no se puede publicar con certificado válido, y en
Argentina hay proveedores de internet cuyos servidores DNS directamente no resuelven los
dominios automáticos que genera el panel de despliegue.

Ese dominio se obtiene **gratis por un año** a través del GitHub Student Developer Pack,
un conjunto de beneficios para estudiantes con matrícula vigente.

El problema es el tiempo. **La verificación de la condición de estudiante tarda entre 3
días y 3 semanas**, y en bastantes casos la rechazan y hay que rehacer el trámite. Si se
deja para el día anterior a la clase, no llega.

> **⚠️ OJO ACÁ**
> Esto no es una sugerencia. Si llegás a la Clase 1 sin la verificación aprobada, no vas
> a poder hacer el práctico y vas a arrastrar el problema todo el módulo. Hacelo esta
> semana.

---

## Paso 1 — Cuenta de GitHub en condiciones

Antes de solicitar la verificación, la cuenta tiene que cumplir estos requisitos. Si
falta alguno, la solicitud se rechaza automáticamente.

| Requisito | Dónde se configura |
|---|---|
| Nombre y apellido reales en el perfil | *Settings → Public profile → Name* |
| Correo institucional o personal verificado | *Settings → Emails* |
| Autenticación en dos pasos activada | *Settings → Password and authentication* |
| Al menos algo de actividad en la cuenta | Cualquier repositorio propio |

> **📌 DATO**
> Si tenés correo institucional de la UTN, agregalo y verificalo. La solicitud con
> correo institucional se aprueba más rápido y con menos rechazos que la que solo tiene
> un Gmail.

---

## Paso 2 — Conseguir el comprobante

Se necesita **una** de estas tres cosas, en foto o escaneo legible:

1. **Certificado de alumno regular** emitido por la Facultad (el más confiable).
2. **Constancia de inscripción a materias** del ciclo lectivo en curso.
3. **Credencial estudiantil** con la fecha de vencimiento visible.

Requisitos de la imagen:

- Que se lea **tu nombre completo**.
- Que se lea el **nombre de la institución**.
- Que se lea una **fecha vigente** (del cuatrimestre o año en curso).
- Foto derecha, con buena luz, sin recortes ni dedos tapando datos.

> **⚠️ OJO ACÁ**
> El motivo número uno de rechazo es **la fecha**. Un certificado del año pasado no
> sirve. Un carnet sin fecha de vencimiento tampoco. Revisá que la fecha esté, que se
> lea, y que sea de este ciclo lectivo antes de subir nada.

---

## Paso 3 — Solicitar la verificación

1. Entrar a **https://education.github.com/pack**
2. Hacer clic en **Sign up for Student Developer Pack**.
3. Seleccionar la cuenta de GitHub y el correo institucional, si se tiene.
4. Indicar el nombre de la institución: **Universidad Tecnológica Nacional — Facultad
   Regional Mendoza**.
5. Subir la foto del comprobante.
6. Confirmar el envío.

El sistema puede pedir además compartir la ubicación desde el navegador, para
contrastarla con la de la Facultad Regional declarada. Por eso conviene hacer el trámite
desde tu conexión habitual y **nunca con una VPN encendida**.

---

## Paso 4 — Esperar y responder

La respuesta llega por correo.

| Resultado | Qué hacer |
|---|---|
| **Aprobado** | Listo. Avisar al docente por el campus. |
| **Rechazado** | Leer el motivo, corregirlo y volver a solicitar. Se puede reintentar. |
| **Sin respuesta** | Esperar. Hasta tres semanas es normal y no significa nada malo. |
| **Sin respuesta pasadas 3 semanas** | Volver a solicitar con otro comprobante, y avisar al docente. |

### Motivos de rechazo más frecuentes

| Motivo | Corrección |
|---|---|
| El comprobante no tiene fecha vigente | Pedir un certificado de alumno regular nuevo |
| La foto está borrosa o cortada | Volver a sacarla con buena luz y encuadre completo |
| El nombre del perfil no coincide con el del comprobante | Corregir el nombre en *Settings → Public profile* |
| La cuenta no tiene activada la autenticación en dos pasos | Activarla y reintentar |
| Uso de VPN durante la solicitud | Desactivar la VPN y reintentar |

---

## Paso 5 — Reclamar el dominio

**Este paso se hace en la Clase 1, no antes.** Se explica acá solo para que sepas qué
viene después y no te apures.

Una vez aprobada la verificación, el Pack ofrece un dominio gratuito por un año:

| Proveedor | Qué ofrece |
|---|---|
| **Namecheap** | Un dominio `.me` por un año, con SSL y privacidad de WHOIS |
| **name.com** | Un dominio por un año, más de 25 extensiones (`.live`, `.studio`, `.app`, `.dev`) |
| **.TECH** | Un dominio `.tech` por un año |

En clase vamos a usar **Namecheap con un `.me`**, porque tiene el panel DNS más simple.

> **⚠️ OJO ACÁ**
> No reclames el dominio por tu cuenta antes de la clase. El beneficio es **uno solo** y
> **por un año**: si elegís mal el nombre o el proveedor, no hay vuelta atrás. Esperá a
> que veamos juntos qué conviene.

---

## Qué tenés que traer a la Clase 1

- [ ] Cuenta de GitHub con la verificación **aprobada**.
- [ ] Grupo de 3 o 4 personas ya armado.
- [ ] Una idea del nombre de dominio que querrías (algo corto, sin guiones, fácil de
      dictar en voz alta).
- [ ] Notebook con acceso a una terminal.

---

## Preguntas frecuentes

**¿Y si ya usé el beneficio del dominio el año pasado?**
El beneficio es de un dominio por cuenta. Si ya lo usaste y el dominio sigue activo,
sirve igual para el práctico: no hace falta uno nuevo.

**¿Puedo usar un dominio que ya tengo comprado?**
Sí, siempre que tengas acceso al panel de administración de su zona DNS. Avisale al
docente en la Clase 1, porque hay un detalle a revisar (los registros CAA) que en un
dominio usado puede impedir la emisión del certificado.

**¿Hace falta que los cuatro integrantes del grupo tengan dominio?**
El práctico corre sobre **uno solo**. Pero los cuatro deben hacer el trámite: es un
beneficio personal que les queda para sus propios proyectos, y además funciona como
respaldo si el trámite de alguno se demora.

**¿Qué pasa si no soy alumno regular?**
Hablalo con el docente antes de la fecha límite. Hay alternativas, pero requieren
resolverse con anticipación.

**¿El dominio se renueva gratis el año que viene?**
No. Al año se cobra la tarifa normal de renovación, o se deja vencer. Para el práctico
alcanza y sobra.
