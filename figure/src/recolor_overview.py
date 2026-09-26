#!/usr/bin/env python3
"""Recolour the author's overview SVG into the paper's muted palette (paper_style.py).
Each saturated colour family is mapped in OKLCH to its semantic target (teacher F -> Original steel blue,
student G -> SOMA sage-teal, trainable parts -> muted violet, rollback -> brick); lightness structure
(tints, outlines) is preserved, chroma is capped, and text becomes near-black."""
import re, math
def srgb2lin(c): return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def lin2srgb(x): x=max(0,min(1,x)); return 12.92*x if x<=0.0031308 else 1.055*x**(1/2.4)-0.055
def hex2oklch(h):
    r,g,b=[srgb2lin(int(h[i:i+2],16)/255) for i in (1,3,5)]
    l=0.4122214708*r+0.5363325363*g+0.0514459929*b; m=0.2119034982*r+0.6806995451*g+0.1073969566*b; s=0.0883024619*r+0.2817188376*g+0.6299787005*b
    l,m,s=[x**(1/3) for x in (l,m,s)]
    L=0.2104542553*l+0.7936177850*m-0.0040720468*s; a=1.9779984951*l-2.4285922050*m+0.4505937099*s; bb=0.0259040371*l+0.7827717662*m-0.8086757660*s
    return L, math.hypot(a,bb), math.degrees(math.atan2(bb,a))%360
def oklch2hex(L,C,h):
    a=C*math.cos(math.radians(h)); b=C*math.sin(math.radians(h))
    l_=L+0.3963377774*a+0.2158037573*b; m_=L-0.1055613458*a-0.0638541728*b; s_=L-0.0894841775*a-1.2914855480*b
    l,m,s=l_**3,m_**3,s_**3
    r=4.0767416621*l-3.3077115913*m+0.2309699292*s; g=-1.2684380046*l+2.6097574011*m-0.3413193965*s; bb=-0.0041960863*l-0.7034186147*m+1.7076147010*s
    return '#%02x%02x%02x'%tuple(round(lin2srgb(v)*255) for v in (r,g,bb))
# family: (hue range test on sRGB-HLS hue & saturation) -> (source main colour, target colour)
import colorsys
def hls(h):
    r,g,b=[int(h[i:i+2],16)/255 for i in (1,3,5)]; H,L,S=colorsys.rgb_to_hls(r,g,b); return H*360,L,S
FAM={'teacher':('#f59a00','#5a76a0'), 'student':('#00809a','#4e9588'), 'trainable':('#8000ff','#7f74ae'), 'rollback':('#ff2822','#b25e59')}
def family(c):
    H,L,S=hls(c)
    if S<0.05 or L>0.985: return None
    if c in ('#061139',): return 'text'
    if c in ('#e62b15','#bc3017'): return 'teacher'   # 'Cached teacher replies' / 'Teacher serves' labels
    if (H<=12 or H>=350) and S>0.6: return 'rollback'
    if 25<=H<=50: return 'teacher'
    if 180<=H<=199 and S>=0.55: return 'student'
    if 204<=H<=210 and S>=0.8: return 'student'
    if 255<=H<=290 and S>=0.6: return 'trainable'
    return None
def remap(c):
    f=family(c)
    if f is None: return c
    if f=='text': return '#1f1f1f'
    src,tgt=FAM[f]
    L0,C0,h0=hex2oklch(c); Ls,Cs,hs=hex2oklch(src); Lt,Ct,ht=hex2oklch(tgt)
    w=1.0 if L0<=Ls+0.08 else max(0.0,(0.985-L0)/(0.985-(Ls+0.08)))   # tints keep their lightness
    L=L0+(Lt-Ls)*w
    C=min(Ct*1.15, Ct*C0/Cs) if Cs>0 else Ct
    return oklch2hex(L,C,ht)
s=open('soma_overview_cropped.svg').read()
cols=sorted(set(m.lower() for m in re.findall(r'#[0-9a-fA-F]{6}\b', s)))
mapping={c:remap(c) for c in cols}
changed={c:v for c,v in mapping.items() if c!=v}
out=re.sub(r'#[0-9a-fA-F]{6}\b', lambda m: mapping[m.group(0).lower()], s)
open('soma_overview_muted.svg','w').write(out)
print('recoloured', len(changed), 'of', len(cols), 'colours; e.g.', list(changed.items())[:8])
