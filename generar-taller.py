# -*- coding: utf-8 -*-
"""
Generador de PDF de talleres de aula - Programacion 3, UTN FRM.

    /c/Python314/python generar-taller.py taller_clase2

Lee META y CONTENIDO del modulo indicado y emite DOS PDF desde una sola
fuente: la consigna y la clave de correccion. Asi nunca se desincronizan.

Gotcha conocido: las fuentes base de reportlab usan WinAnsi. Cualquier
caracter fuera de cp1252 (flechas, vistos, emoji) se dibuja VACIO y sin
avisar. Por eso el modulo se escanea antes de componer y el script aborta
si encuentra alguno.
"""
import sys
import importlib

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether,
                                PageBreak, Flowable)

BORDO = colors.HexColor('#7B1E2B')
BORDO_CLARO = colors.HexColor('#f8edef')
GRIS_TXT = colors.HexColor('#3f3f46')
GRIS_SUAVE = colors.HexColor('#71717a')
GRIS_LINEA = colors.HexColor('#d4d4d8')
CODE_BG = colors.HexColor('#f4f4f5')
CODE_BORDE = colors.HexColor('#a1a1aa')
NARANJA = colors.HexColor('#B45309')
NARANJA_BG = colors.HexColor('#FFF7ED')
ROJO = colors.HexColor('#B91C1C')
ROJO_BG = colors.HexColor('#FEF2F2')
VERDE = colors.HexColor('#15803D')
VERDE_BG = colors.HexColor('#F0FDF4')

MARGEN = 2.0 * cm
ANCHO_UTIL = A4[0] - 2 * MARGEN


def _p(name, **kw):
    base = dict(fontName='Helvetica', fontSize=9.5, leading=13.5,
                textColor=GRIS_TXT, alignment=TA_JUSTIFY)
    base.update(kw)
    return ParagraphStyle(name, **base)


S = {
    'eyebrow': _p('eyebrow', fontName='Helvetica-Bold', fontSize=8,
                  leading=10, textColor=BORDO, alignment=0),
    'titulo': _p('titulo', fontName='Helvetica-Bold', fontSize=19, leading=22,
                 textColor=colors.HexColor('#18181b'), alignment=0),
    'subtitulo': _p('subtitulo', fontSize=11.5, leading=15,
                    textColor=GRIS_SUAVE, alignment=0),
    'p': _p('p'),
    'meta_k': _p('meta_k', fontName='Helvetica-Bold', fontSize=8.5, leading=11,
                 textColor=BORDO, alignment=0),
    'meta_v': _p('meta_v', fontSize=8.5, leading=11.5, alignment=0),
    'parte': _p('parte', fontName='Helvetica-Bold', fontSize=12, leading=14,
                textColor=colors.white, alignment=0),
    'parte_pts': _p('parte_pts', fontName='Helvetica-Bold', fontSize=8.5,
                    leading=14, textColor=colors.HexColor('#f4d8dc'),
                    alignment=2),
    'sub': _p('sub', fontName='Helvetica-Bold', fontSize=10, leading=13,
              textColor=BORDO, alignment=0),
    'item_num': _p('item_num', fontName='Helvetica-Bold', fontSize=9.5,
                   leading=13.5, textColor=BORDO, alignment=0),
    'item_pts': _p('item_pts', fontName='Helvetica-Oblique', fontSize=8,
                   leading=13.5, textColor=GRIS_SUAVE, alignment=2),
    'code': _p('code', fontName='Courier', fontSize=8.2, leading=11,
               textColor=colors.HexColor('#18181b'), alignment=0),
    'th': _p('th', fontName='Helvetica-Bold', fontSize=7.8, leading=9.5,
             textColor=colors.white, alignment=0),
    'td': _p('td', fontSize=8.2, leading=10.5, alignment=0),
    'td_c': _p('td_c', fontSize=8.2, leading=10.5, alignment=1),
    'nota_t': _p('nota_t', fontName='Helvetica-Bold', fontSize=8.8, leading=11,
                 alignment=0),
    'nota': _p('nota', fontSize=8.8, leading=12),
    'resp_t': _p('resp_t', fontName='Helvetica-Bold', fontSize=8.5, leading=11,
                 textColor=VERDE, alignment=0),
    'resp': _p('resp', fontSize=8.8, leading=12.5),
}


def inline(txt):
    """Marcado minimo: backticks para monoespaciada, ** para negrita."""
    out, i = [], 0
    while True:
        a = txt.find('`', i)
        if a < 0:
            out.append(txt[i:])
            break
        b = txt.find('`', a + 1)
        if b < 0:
            out.append(txt[i:])
            break
        out.append(txt[i:a])
        out.append('<font face="Courier" size="8.6" color="#0f172a">'
                   + txt[a + 1:b] + '</font>')
        i = b + 1
    txt = ''.join(out)
    while '**' in txt:
        txt = txt.replace('**', '<b>', 1)
        if '**' in txt:
            txt = txt.replace('**', '</b>', 1)
        else:
            txt += '</b>'
    return txt


class Regla(Flowable):
    def __init__(self, ancho=ANCHO_UTIL, color=GRIS_LINEA, grosor=0.6):
        Flowable.__init__(self)
        self.ancho, self.color, self.grosor = ancho, color, grosor

    def wrap(self, *a):
        return (self.ancho, self.grosor + 1)

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.grosor)
        self.canv.line(0, 0, self.ancho, 0)


class LineasEscritura(Flowable):
    """Renglones punteados para responder a mano."""

    def __init__(self, n=3, ancho=ANCHO_UTIL, paso=6.2 * mm):
        Flowable.__init__(self)
        self.n, self.ancho, self.paso = n, ancho, paso
        self.altura = n * paso

    def wrap(self, *a):
        return (self.ancho, self.altura + 2 * mm)

    def draw(self):
        self.canv.setStrokeColor(colors.HexColor('#c7c7cc'))
        self.canv.setLineWidth(0.5)
        self.canv.setDash(1, 2)
        y = self.altura
        for _ in range(self.n):
            self.canv.line(0, y, self.ancho, y)
            y -= self.paso
        self.canv.setDash()


def banda_parte(titulo, pts):
    t = Table([[Paragraph(titulo, S['parte']),
                Paragraph(pts or '', S['parte_pts'])]],
              colWidths=[ANCHO_UTIL * 0.72, ANCHO_UTIL * 0.28])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BORDO),
        ('LEFTPADDING', (0, 0), (0, 0), 8),
        ('RIGHTPADDING', (-1, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return [Spacer(1, 6 * mm), t, Spacer(1, 3.5 * mm)]


def bloque_code(txt):
    cuerpo = (txt.replace('&', '&amp;').replace('<', '&lt;')
              .replace(' ', '&nbsp;').replace('\n', '<br/>'))
    t = Table([[Paragraph(cuerpo, S['code'])]], colWidths=[ANCHO_UTIL])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CODE_BG),
        ('LINEBEFORE', (0, 0), (0, -1), 2.2, CODE_BORDE),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    return [t, Spacer(1, 3 * mm)]


_NOTA_COLORES = {
    'naranja': (NARANJA, NARANJA_BG),
    'rojo': (ROJO, ROJO_BG),
    'bordo': (BORDO, BORDO_CLARO),
    'verde': (VERDE, VERDE_BG),
}


def bloque_nota(titulo, texto, tono='naranja'):
    borde, fondo = _NOTA_COLORES[tono]
    st_t = ParagraphStyle('nt', parent=S['nota_t'], textColor=borde)
    filas = []
    if titulo:
        filas.append([Paragraph(inline(titulo), st_t)])
    filas.append([Paragraph(inline(texto), S['nota'])])
    t = Table(filas, colWidths=[ANCHO_UTIL])
    estilo = [
        ('BACKGROUND', (0, 0), (-1, -1), fondo),
        ('LINEBEFORE', (0, 0), (0, -1), 2.5, borde),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]
    estilo.append(('TOPPADDING', (0, 0), (-1, 0), 7))
    estilo.append(('BOTTOMPADDING', (0, -1), (-1, -1), 7))
    t.setStyle(TableStyle(estilo))
    return [t, Spacer(1, 4 * mm)]


def bloque_item(num, texto, pts=None):
    cab = Table([[Paragraph(num, S['item_num']),
                  Paragraph(pts or '', S['item_pts'])]],
                colWidths=[ANCHO_UTIL * 0.5, ANCHO_UTIL * 0.5])
    cab.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))
    t = Table([[cab], [Paragraph(inline(texto), S['p'])]],
              colWidths=[ANCHO_UTIL])
    t.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    return [Spacer(1, 3.5 * mm), t, Spacer(1, 2 * mm)]


def bloque_tabla(head, rows, widths, alto=None, centrar=None):
    centrar = centrar or []
    anchos = [ANCHO_UTIL * w for w in widths]
    data = [[Paragraph(inline(h), S['th']) for h in head]]
    for r in rows:
        fila = []
        for j, c in enumerate(r):
            estilo = S['td_c'] if j in centrar else S['td']
            fila.append(Paragraph(inline(c), estilo) if c else Paragraph('',
                                                                        estilo))
        data.append(fila)
    kw = {'colWidths': anchos}
    if alto:
        kw['rowHeights'] = [None] + [alto * mm] * len(rows)
    t = Table(data, repeatRows=1, **kw)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BORDO),
        ('GRID', (0, 0), (-1, -1), 0.5, GRIS_LINEA),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white,
                                              colors.HexColor('#fafafa')]),
    ]))
    return [t, Spacer(1, 4 * mm)]


def bloque_respuesta(texto):
    filas = [[Paragraph('CLAVE DE CORRECCION', S['resp_t'])],
             [Paragraph(inline(texto), S['resp'])]]
    t = Table(filas, colWidths=[ANCHO_UTIL])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), VERDE_BG),
        ('LINEBEFORE', (0, 0), (0, -1), 2.5, VERDE),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 1),
        ('TOPPADDING', (0, -1), (-1, -1), 2),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 7),
    ]))
    return [t, Spacer(1, 3 * mm)]


class Doc(BaseDocTemplate):
    def __init__(self, path, meta, sufijo):
        BaseDocTemplate.__init__(self, path, pagesize=A4,
                                 leftMargin=MARGEN, rightMargin=MARGEN,
                                 topMargin=MARGEN + 8 * mm,
                                 bottomMargin=MARGEN + 4 * mm,
                                 title=meta['titulo'] + sufijo,
                                 author='UTN FRM - Programacion 3')
        self.meta, self.sufijo = meta, sufijo
        frame = Frame(MARGEN, MARGEN + 10 * mm, ANCHO_UTIL,
                      A4[1] - 2 * MARGEN - 16 * mm, id='cuerpo',
                      leftPadding=0, rightPadding=0,
                      topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id='std', frames=[frame],
                                            onPage=self._decorar)])

    def _decorar(self, c, doc):
        c.saveState()
        y = A4[1] - MARGEN - 2 * mm
        c.setFont('Helvetica-Bold', 7)
        c.setFillColor(BORDO)
        c.drawString(MARGEN, y, 'TECNICATURA UNIVERSITARIA EN PROGRAMACION')
        c.setFont('Helvetica', 7)
        c.setFillColor(GRIS_SUAVE)
        c.drawRightString(A4[0] - MARGEN, y, self.meta['header_der'])
        c.setStrokeColor(BORDO)
        c.setLineWidth(0.8)
        c.line(MARGEN, y - 3 * mm, A4[0] - MARGEN, y - 3 * mm)
        c.setStrokeColor(GRIS_LINEA)
        c.setLineWidth(0.5)
        c.line(MARGEN, MARGEN + 8 * mm, A4[0] - MARGEN, MARGEN + 8 * mm)
        c.setFont('Helvetica', 7)
        c.setFillColor(GRIS_SUAVE)
        c.drawString(MARGEN, MARGEN + 4 * mm, self.meta['pie'] + self.sufijo)
        c.drawRightString(A4[0] - MARGEN, MARGEN + 4 * mm,
                          'Pagina %d' % c.getPageNumber())
        c.restoreState()


def portada(meta, con_clave):
    sub = meta['subtitulo']
    if con_clave:
        sub += '  -  CLAVE DE CORRECCION DOCENTE'
    els = [Paragraph(meta['eyebrow'], S['eyebrow']), Spacer(1, 2 * mm),
           Paragraph(meta['titulo'], S['titulo']), Spacer(1, 1.5 * mm),
           Paragraph(sub, S['subtitulo']),
           Spacer(1, 4 * mm), Regla(), Spacer(1, 4 * mm)]
    filas = [[Paragraph(k, S['meta_k']), Paragraph(inline(v), S['meta_v'])]
             for k, v in meta['ficha']]
    t = Table(filas, colWidths=[ANCHO_UTIL * 0.20, ANCHO_UTIL * 0.80])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LINEBELOW', (0, 0), (-1, -2), 0.4, colors.HexColor('#e4e4e7')),
    ]))
    els += [t, Spacer(1, 5 * mm)]
    return els


def componer(meta, contenido, con_clave):
    els = portada(meta, con_clave)
    for tipo, dato in contenido:
        if tipo == 'parte':
            els += banda_parte(dato[0], dato[1])
        elif tipo == 'sub':
            els += [Spacer(1, 2 * mm), Paragraph(inline(dato), S['sub']),
                    Spacer(1, 2 * mm)]
        elif tipo == 'p':
            els += [Paragraph(inline(dato), S['p']), Spacer(1, 2.5 * mm)]
        elif tipo == 'code':
            els += bloque_code(dato)
        elif tipo == 'nota':
            els += bloque_nota(dato[0], dato[1], dato[2])
        elif tipo == 'item':
            bloque = bloque_item(dato['num'], dato['texto'], dato.get('pts'))
            if con_clave:
                bloque += bloque_respuesta(dato['resp'])
            elif dato.get('lineas'):
                bloque += [LineasEscritura(dato['lineas']), Spacer(1, 2 * mm)]
            els += [KeepTogether(bloque)]
        elif tipo == 'tabla':
            filas = dato['rows_clave'] if con_clave else dato['rows']
            alto = None if con_clave else dato.get('alto')
            els += bloque_tabla(dato['head'], filas, dato['widths'], alto,
                                dato.get('centrar'))
        elif tipo == 'lineas':
            if not con_clave:
                els += [LineasEscritura(dato), Spacer(1, 2 * mm)]
        elif tipo == 'salto':
            # En la clave no hay nada que completar a mano: compactar.
            if not con_clave:
                els += [PageBreak()]
        elif tipo == 'espacio':
            els += [Spacer(1, dato * mm)]
        else:
            raise ValueError('tipo desconocido: %s' % tipo)
    return els


def revisar_winansi(mod):
    malos = {}
    for nombre in ('META', 'CONTENIDO'):
        texto = repr(getattr(mod, nombre))
        for ch in texto:
            if ord(ch) > 127:
                if ch.encode('cp1252', 'ignore') == b'':
                    malos[ch] = malos.get(ch, 0) + 1
    if malos:
        det = ', '.join('%r (U+%04X) x%d' % (c, ord(c), n)
                        for c, n in malos.items())
        raise SystemExit('ABORTADO: caracteres fuera de WinAnsi -> %s\n'
                         'reportlab los dibuja vacios y sin avisar.' % det)


def main():
    if len(sys.argv) < 2:
        raise SystemExit('uso: generar-taller.py <modulo_de_contenido>')
    mod = importlib.import_module(sys.argv[1])
    revisar_winansi(mod)
    meta = mod.META
    for con_clave, sufijo, salida in (
            (False, '', meta['salida']),
            (True, ' - Respuestas', meta['salida_clave'])):
        doc = Doc(salida, meta, sufijo)
        doc.build(componer(meta, mod.CONTENIDO, con_clave))
        print('OK ->', salida)


if __name__ == '__main__':
    main()
