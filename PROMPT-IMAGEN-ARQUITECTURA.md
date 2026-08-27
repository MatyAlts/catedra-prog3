# Prompt para generar la imagen de arquitectura del módulo

Diagrama de arquitectura general del módulo de deploy a VPS, con el mismo lenguaje
visual que la imagen de referencia del back-end con FastAPI (`imagen.png`).

## Cómo usarlo

1. Abrí ChatGPT y **adjuntá `imagen.png`** (la referencia de estilo).
2. Pegá el prompt de abajo en el mismo mensaje.
3. Iterá sobre el texto: los generadores escriben mal las palabras. Ver
   [Advertencias](#advertencias) al final.

---

## Prompt

```
Usá la imagen adjunta como REFERENCIA ESTRICTA DE ESTILO. Generá un diagrama
técnico nuevo con el MISMO lenguaje visual, pero con otro contenido.

ESTILO (replicar exactamente):
- Formato horizontal, aprox. 950x430 px, fondo blanco puro.
- Ilustración vectorial plana, sin sombras realistas, sin degradés, sin 3D.
- Un panel central grande de esquinas muy redondeadas, azul marino oscuro
  (#123A63), con un borde exterior fino celeste claro (#9EC5E8).
- Dentro del panel, sub-cajas redondeadas: una negra (#1A1A1A) para el
  componente principal y una gris azulada (#4A5A6A) para el secundario.
- Iconos de línea (line icons) monocromáticos en verde menta (#5FD3B0) y
  rojo coral (#E15C5C), tamaño chico, con su rótulo debajo.
- Tipografía sans-serif geométrica (tipo Montserrat/Poppins). Títulos en
  MAYÚSCULAS y negrita. Texto blanco dentro del panel azul, texto negro
  fuera del panel. Aclaraciones entre paréntesis en tamaño menor.
- Flechas negras finas, rectas, con punta sólida.
- Todo el texto en español, sin faltas de ortografía y con tildes correctas.

CONTENIDO DEL DIAGRAMA (de izquierda a derecha):

1) EXTREMO IZQUIERDO: icono de monitor + celular (mismo estilo que la
   referencia), rótulo debajo: "CLIENTE" y en línea menor "(Navegador)".

2) ENTRE EL CLIENTE Y EL PANEL, dos flechas horizontales:
   - Flecha superior (del cliente al panel) con el texto encima:
     "HTTPS" en negrita, y debajo "https://calculadora.midominio.me".
     Encima de todo, una fila de tres chips redondeados de colores planos con
     texto blanco: "DNS" (azul), "TLS" (verde), "443" (naranja).
   - Flecha inferior (del panel al cliente) con el texto "Respuesta" y, debajo,
     un badge negro con las palabras "HTML / JSON" en amarillo.

3) ANTES DEL PANEL, arriba de la flecha superior, una caja blanca chica con
   borde gris y el texto: "DNS" en negrita y debajo
   "(Registro A + comodín *.midominio.me → IP del VPS)".

4) PANEL CENTRAL AZUL, con el título arriba en blanco y mayúsculas:
   "VPS (Hostinger)" y en línea menor "Easypanel".
   Dentro del panel:
   - Caja negra grande a la izquierda con el texto blanco en negrita
     "TRAEFIK" y debajo, más chico, "(Proxy inverso)".
   - A su derecha, una caja gris azulada conectada por una flecha blanca, con
     el texto "CONTENEDORES DOCKER" en negrita y debajo, en tres renglones:
     "Frontend", "API (FastAPI)", "PostgreSQL".
   - En la fila inferior del panel, dos íconos con rótulo, separados:
     * Ícono verde menta de red/nodos conectados, rótulo "RED INTERNA" y
       debajo "(Postgres sin puerto público)".
     * Ícono rojo coral de escudo, rótulo "FIREWALL (UFW)" y debajo
       "(22, 80, 443)".

5) EXTREMO DERECHO: una flecha negra saliendo del panel hacia la derecha,
   con el texto en negrita "CERTIFICADO HTTPS" y debajo, más chico,
   "(Let's Encrypt automático)".

Composición limpia, mucho aire entre elementos, alineación horizontal
equilibrada, sin elementos decorativos extra.
```

---

## Advertencias

**El texto va a salir mal.** Es el talón de Aquiles de los generadores de imagen.
Vas a tener que iterar pidiendo correcciones puntuales, del estilo:

> Corregí el texto de la caja negra: dice "TRAEFK" y debe decir "TRAEFIK".
> El resto de la imagen no lo toques.

Prepárate para tres o cuatro vueltas. Si la imagen va impresa en el material,
el camino más rápido es generar el layout y el estilo con el modelo y después
corregir los textos a mano en un editor vectorial.

**Un diagrama por idea.** Este es el diagrama de arquitectura general del módulo:
el que va al principio y responde "¿adónde vamos?". No metas los cinco temas de
las cinco clases acá. Para los diagramas por clase, mantené el mismo panel azul,
los mismos colores y los mismos íconos, y cambiá solo el contenido: así los cinco
se leen como una familia y no como cinco imágenes sueltas.

## Paleta de referencia

| Elemento | Color |
|---|---|
| Panel principal | `#123A63` |
| Borde del panel | `#9EC5E8` |
| Caja del componente principal | `#1A1A1A` |
| Caja del componente secundario | `#4A5A6A` |
| Ícono positivo / red | `#5FD3B0` |
| Ícono de alerta / seguridad | `#E15C5C` |
| Fondo | Blanco puro |
