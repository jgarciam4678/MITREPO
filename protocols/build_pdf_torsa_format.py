import markdown,re,base64,subprocess,io
import pymupdf as fitz
from playwright.sync_api import sync_playwright
B='/tmp/claude-0/-home-user-MITREPO/480f8cc2-2a03-53c8-b6fb-fe6a4dde86fd/scratchpad/build/'
SRC='/home/user/MITREPO/protocols/EN-CMS-PROC-PRUEBAS-L8_pdf.md'
OUT='/home/user/MITREPO/protocols/EN-CMS-PROC-PRUEBAS-L8_v1.0.pdf'
CHROME='/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
DOC='EN-CMS-PROC-PRUEBAS-L8'; VER='1.0'
def b64(p,mime='image/png'): return f'data:{mime};base64,'+base64.b64encode(open(p,'rb').read()).decode()
def font(w): return b64(B+f'fonts/rhd-latin-{w}.woff2','font/woff2')
md=open(SRC).read()
main,annex_tail=md.split('## ANNEX A to G: TEST LAYOUTS')
_,after=annex_tail.split('## ANNEX H: TEST RECORD FORMAT')
annexH,rest=after.split('*****',1)
annexH='## ANNEX H: TEST RECORD FORMAT'+annexH; rest='*****'+rest
ext=['tables','sane_lists']; H=lambda s: markdown.markdown(s,extensions=ext)
figs=[('A','Scenario L1: Straight trajectory','Figure 1: Scenario L1 – Controlled straight approach'),
('B','Scenario L2: Controlled reversing','Figure 2: Scenario L2 – Reversing trajectory toward an obstacle'),
('C','Scenario L5: Parallel trajectories in opposite directions','Figure 3: Scenario L5 – Parallel trajectories in opposite directions'),
('D','Scenario T4: Perpendicular intersection','Figure 4: Scenario T4 – Perpendicular crossing between vehicles'),
('E','Scenario C1: Head-on curve','Figure 5: Scenario C1 – Head-on encounter in a curve'),
('F','Scenario R2: Cleaning flow','Figure 6: Scenario R2 – Operational cleaning flow'),
('G','Scenario O1: Truck approaching a safety berm (optional V2O)','Figure 7: Scenario O1 – Truck approaching a safety berm')]
figcap={f[0]:f[2] for f in figs}
def inlinefig(h):
    return re.sub(r'<p>\{\{FIG:([A-G])\}\}</p>',lambda m:f'<div class="inl"><img src="{b64(B+"figcrop_"+m.group(1)+".png")}"/><p class="cap">{figcap[m.group(1)]}</p></div>',h)
def fixh3(h):
    h=re.sub(r'<h3>(\d+\.\d+)\s',r'<h3>\1. ',h); return h
annex_html='<div class="pb"><h2>ANNEXES</h2><p>The following annexes complement this protocol with reference operational diagrams, test layouts and the record format used during field execution.</p></div>'
for L,t,c in figs:
    mh='170mm' if L in 'ABCG' else '120mm'
    annex_html+=f'<div class="pb fig"><h3>{L}.&nbsp;&nbsp;{t.upper()}</h3><img src="{b64(B+"figcrop_"+L+".png")}" style="max-height:{mh};max-width:150mm"/><p class="cap">{c}</p></div>'
annex_html+='<div class="pb">'+H(annexH).replace('<h2>','<h3>').replace('</h2>','</h3>')+'</div>'
rev_idx=H(rest).index('<h2>8. REVISION CONTROL</h2>')
body_main=fixh3(inlinefig(H(main)))
body_rest=H(rest)[rev_idx:].replace('<td>2026-10-20</td>','<td style="white-space:nowrap">2026-10-20</td>')
inner=body_main+annex_html+'<div class="pb">'+fixh3(body_rest)+'</div>'
css=f'''
@font-face{{font-family:RHD;font-weight:300;src:url({font(300)}) format("woff2")}}
@font-face{{font-family:RHD;font-weight:400;src:url({font(400)}) format("woff2")}}
@font-face{{font-family:RHD;font-weight:700;src:url({font(700)}) format("woff2")}}
@page{{size:A4}}
html,body{{margin:0;padding:0}}
body{{font-family:RHD,"DejaVu Sans",sans-serif;font-weight:300;font-size:10.5pt;line-height:1.4;color:#000}}
strong,b{{font-weight:700}}
h2,h3{{page-break-after:avoid;break-after:avoid}}
h2{{font-weight:700;font-size:20pt;text-align:right;margin:0 0 6pt;color:#000}}
h3{{font-weight:700;font-size:14pt;text-align:right;margin:16pt 0 8pt;text-transform:uppercase;color:#000}}
p{{margin:5pt 0;text-align:justify}}
table{{border-collapse:collapse;width:100%;margin:8pt 0 12pt;font-size:8.6pt;font-weight:400}}
tr{{page-break-inside:avoid}}
th,td{{border:0.6pt solid #9a9a9a;padding:3pt 5pt;vertical-align:top;text-align:left;font-weight:400}}
th{{background:#051c2c;color:#fff;font-weight:700}}
th strong{{color:#fff}}
td strong{{font-weight:700}}
blockquote{{margin:8pt 0;padding:3pt 10pt;border-left:3pt solid #d40019;background:#f5f5f5}}
blockquote p{{margin:2pt 0;text-align:left}}
hr{{border:0;margin:6pt 0}}
ul{{margin:4pt 0 4pt 16pt;padding:0}} li{{margin:2pt 0}}
.pb{{page-break-before:always}}
.fig{{text-align:center}}.fig h3{{text-align:right}}
.cap{{text-align:center;font-size:8.5pt;color:#555}}
.inl{{text-align:center;page-break-inside:avoid;margin:6pt 0 12pt}}.inl img{{max-height:46mm;max-width:70mm}}
.toc div{{display:flex;margin:5pt 0;font-size:10.5pt}}.toc .l1{{font-weight:700;margin-top:9pt}}.toc .l2{{padding-left:20pt}}
.toc span.t{{flex:1;border-bottom:1px dotted #777;margin:0 4px 3px}}
'''
# headings for TOC
toc_items=[]
for m in re.finditer(r'<h([23])>(.*?)</h\1>',inner):
    lv=int(m.group(1)); t=re.sub(r'<[^>]+>','',m.group(2)).replace('&nbsp;',' ').strip()
    if lv==3 and re.match(r'^[A-H]\.',t): continue
    toc_items.append((lv-1,t))
toc_items=[(l,t) for l,t in toc_items]
def doc(toc_pages=None):
    toc=''
    if toc_pages is not None:
        toc='<div><h2>INDEX</h2><div class="toc">'+''.join(f'<div class="l{l}"><span>{t}</span><span class="t"></span><span>{toc_pages.get(t,"")}</span></div>' for l,t in toc_items)+'</div></div>'
    return f'<html><head><meta charset="utf-8"><style>{css}</style></head><body>{toc}<div class="pb">{inner}</div></body></html>'
M={'top':'27.2mm','bottom':'28mm','left':'20.1mm','right':'19.4mm'}
def render(html,path):
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path=CHROME); pg=b.new_page(); pg.set_content(html); pg.wait_for_timeout(400)
        pg.pdf(path=path,format='A4',print_background=True,margin=M); b.close()
render(doc({}),B+'tw1.pdf')
d1=fitz.open(B+'tw1.pdf'); pages={}; start=2
for pn in range(1,len(d1)):  # skip TOC page 0
    txt=d1[pn].get_text()
    for l,t in toc_items:
        if t not in pages and re.search(r'^\s*'+re.escape(t)+r'\s*$',txt,re.M|re.I): pages[t]=pn+2   # +1 for cover, +1 for 1-based
render(doc(pages),B+'tw.pdf')
# --- assemble with overlays
body=fitz.open(B+'tw.pdf'); out=fitz.open(); N=len(body)+1
W,Hh=595.2,841.92
F={w:B+f'fonts/rhd-{w}.ttf' for w in (300,400,700)}
def addfonts(pg):
    pg.insert_font(fontname='rl',fontfile=F[300]); pg.insert_font(fontname='rb',fontfile=F[700]); pg.insert_font(fontname='rr',fontfile=F[400])
def rtext(pg,x,y,text,size,font,color):
    w=fitz.get_text_length(text,fontname=font,fontsize=size) if font in ('helv',) else fitz.Font(fontfile=F[{'rl':300,'rr':400,'rb':700}[font]]).text_length(text,fontsize=size)
    pg.insert_text((x-w,y),text,fontname=font,fontsize=size,color=color)
GREY=(0.463,0.443,0.443); NAVY=(5/255,28/255,44/255)
# cover
cv=out.new_page(width=W,height=Hh); addfonts(cv)
rtext(cv,539,374,'CMS L8 TEST',48,'rb',(0,0,0)); rtext(cv,539,433,'PROTOCOL',48,'rb',(0,0,0))
cv.draw_line((177,450),(537,450),color=(0,0,0),width=1.6)
cv.insert_image(fitz.Rect(293.7,458.2,537.6,514.8),filename=B+'tw/cover_logo.png')
rtext(cv,539,540,f'{DOC} · Version {VER}',9,'rl',GREY); rtext(cv,539,552,'20 October 2026',9,'rl',GREY)
out.insert_pdf(body)
for i in range(1,len(out)):
    pg=out[i]; addfonts(pg)
    pg.insert_image(fitz.Rect(0.3,302.2,532.1,840.8),filename=B+'tw/watermark.png',overlay=False)
    pg.insert_image(fitz.Rect(56.7,28.7,178.5,57.0),filename=B+'tw/header_logo.png')
    for y,t in ((37.5,'TORSA Worldwide S.L.'),(47.5,'C/Severo Ochoa, 19 – Parque Tecnológico de Andalucía'),(57,'29590 Málaga, España')): rtext(pg,539,y,t,7.9,'rl',GREY)
    pg.insert_text((57,788),'Documento:',fontname='rl',fontsize=7.9,color=GREY); pg.insert_text((57,797),DOC,fontname='rl',fontsize=7.9,color=GREY)
    pg.insert_text((340,788),'Versión:',fontname='rl',fontsize=7.9,color=GREY); pg.insert_text((340,797),VER,fontname='rl',fontsize=7.9,color=GREY)
    pg.insert_text((416,793),f'Página {i+1} de {N}',fontname='rl',fontsize=7.9,color=GREY)
out.save(OUT,garbage=3,deflate=True); print(pages,N)
