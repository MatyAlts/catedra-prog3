import sys, re
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack=[]
        self.videos=[]   # (titulo, palabras_total, palabras_cortables, n_ejemplos, [(diapo,pal)])
        self.cur=None
        self.buf=[]
        self.mode=None   # 'diapo'
        self.skip=0
        self.cortable=0
        self.cortbuf=None
        self.ej=0
        self.diapos=[]
    def cls(self,attrs):
        d=dict(attrs); return d.get('class','')
    def handle_starttag(self,tag,attrs):
        c=self.cls(attrs)
        if tag=='div' and 'video' in c.split():
            self.cur={'pal':0,'cort':0,'ej':0,'diapos':[]}
        elif tag=='div' and 'diapo' in c.split():
            self.mode='diapo'; self.buf=[]
        elif tag=='div' and 'num' in c.split():
            self.skip+=1
        elif tag=='div' and 'titulo-diapo' in c.split():
            self.skip+=1
        elif tag=='div' and 'nota' in c.split():
            self.skip+=1
        elif tag=='div' and 'ej' in c.split():
            if self.cur: self.cur['ej']+=1
        elif 'cortable' in c.split():
            self.cortbuf=[]
        self.stack.append((tag,c))
    def handle_endtag(self,tag):
        if not self.stack: return
        t,c=self.stack.pop()
        if t=='div' and 'diapo' in c.split():
            w=len(' '.join(self.buf).split())
            if self.cur:
                self.cur['pal']+=w; self.cur['diapos'].append(w)
            self.mode=None
        elif t=='div' and ('num' in c.split() or 'titulo-diapo' in c.split() or 'nota' in c.split()):
            self.skip-=1
        elif t=='div' and 'video' in c.split():
            self.videos.append(self.cur); self.cur=None
        elif 'cortable' in c.split() and self.cortbuf is not None:
            if self.cur: self.cur['cort']+=len(' '.join(self.cortbuf).split())
            self.cortbuf=None
    def handle_data(self,d):
        if self.skip: return
        if self.cortbuf is not None: self.cortbuf.append(d)
        if self.mode=='diapo': self.buf.append(d)

src=open(sys.argv[1],encoding='utf-8').read()
p=P(); p.feed(src)
tot=totc=tote=0
def mmss(w,wpm): 
    s=round(w/wpm*60); return f"{s//60}:{s%60:02d}"
for i,v in enumerate(p.videos,1):
    tot+=v['pal']; totc+=v['cort']; tote+=v['ej']
    print(f"Video {i}: {v['pal']} pal | tijeras {v['cort']} | ejemplos {v['ej']} | 165={mmss(v['pal'],165)} sin-tijeras={mmss(v['pal']-v['cort'],165)} | 145={mmss(v['pal'],145)}")
    print("   por diapo:", v['diapos'])
print(f"TOTAL: {tot} pal | tijeras {totc} | ejemplos {tote} | 165={mmss(tot,165)} sin-tijeras={mmss(tot-totc,165)} | 145={mmss(tot,145)}")
