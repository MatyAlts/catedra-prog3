import sys, re
from html.parser import HTMLParser

WPM = 165

class Diapo(HTMLParser):
    """Cuenta las palabras narrables de un bloque .diapo: excluye num, titulo-diapo y nota."""
    def __init__(self):
        super().__init__(); self.skip=0; self.buf=[]; self.stack=[]
    def handle_starttag(self, tag, attrs):
        c = dict(attrs).get('class','').split()
        sk = tag=='div' and any(x in c for x in ('num','titulo-diapo','nota','cierre'))
        self.stack.append(sk)
        if sk: self.skip += 1
    def handle_endtag(self, tag):
        if self.stack:
            if self.stack.pop(): self.skip -= 1
    def handle_data(self, d):
        if not self.skip: self.buf.append(d)
    def words(self):
        return len(' '.join(self.buf).split())

def mmss(seg):
    seg = round(seg)
    return f"{seg//60}:{seg%60:02d}"

def procesar(path):
    src = open(path, encoding='utf-8').read()
    partes = src.split('<div class="diapo">')
    out = [partes[0]]
    t = 0.0
    total_pal = 0
    for bloque in partes[1:]:
        p = Diapo(); p.feed('<div class="diapo">' + bloque)
        w = p.words(); total_pal += w
        dur = w / WPM * 60
        ini, fin = mmss(t), mmss(t + dur)
        bloque = re.sub(r'<small>[^<]*</small>', f'<small>{ini}</small>', bloque, count=1)
        bloque = re.sub(r'<span class="tc">[^<]*</span>',
                        f'<span class="tc">{ini} – {fin}</span>', bloque, count=1)
        out.append(bloque)
        t += dur
    src = '<div class="diapo">'.join(out)
    open(path, 'w', encoding='utf-8').write(src)
    print(f"{path}: {total_pal} palabras · {mmss(t)} a {WPM} p/min")

for f in sys.argv[1:]:
    procesar(f)
