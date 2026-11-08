from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys
B="/System/Library/Fonts/Supplemental/Arial Bold.ttf"; R="/System/Library/Fonts/Supplemental/Arial.ttf"
RED=(229,57,47); BLK=(17,17,17); GR=(90,90,90)
cards=[("01","ECONOMIA","Pix tem falha parcial e afeta clientes de vários bancos","06.11.2026","O Povo / Mix Vale"),
("02","CRIPTO","Nubank e Mercado Pago travam saque e depósito de cripto","06.11.2026","Bloomberg Línea / O Tempo"),
("03","CRIPTO","Binance tem roubo estimado em US$ 6,3 bilhões e promete cobrir clientes","29.10.2026","AP / The National"),
("04","MUNDO","Banco francês perde cerca de 100 milhões de euros em ataque hacker","04.11.2026","AFP / Jovem Pan"),
("05a","MUNDO","Comissão Europeia orienta população a se preparar para as primeiras 72 h de crise","03.11.2026","Comissão Europeia"),
("05b","BRASIL","Defesa Civil orienta kit de água e comida para 72 horas","06.11.2026","Defesa Civil Nacional / Metrópoles")]
def wrap(d,t,f,w):
    out=[];l=""
    for p in t.split():
        if d.textlength((l+" "+p).strip(),font=f)<=w: l=(l+" "+p).strip()
        else: out.append(l); l=p
    out.append(l); return out
W=1000; M=40; CW=W-2*M; P=36
for n,ed,ti,da,fo in cards:
    d0=ImageDraw.Draw(Image.new("RGB",(10,10)))
    ft=ImageFont.truetype(B,68); fb=ImageFont.truetype(B,40); fs=ImageFont.truetype(R,34)
    lines=wrap(d0,ti,ft,CW-2*P)
    bandh=84; th=len(lines)*80; H=bandh+P+th+P+70+P//2
    img=Image.new("RGBA",(W,H+2*M+20),(0,0,0,0))
    sh=Image.new("RGBA",img.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([M,M+14,M+CW,M+14+H],14,fill=(0,0,0,130))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    card=Image.new("RGBA",(CW,H),(255,255,255,255)); c=ImageDraw.Draw(card)
    c.rectangle([0,0,CW,bandh],fill=RED)
    c.text((P,bandh/2),ed,font=fb,fill="white",anchor="lm")
    c.text((CW-P,bandh/2),da,font=fb,fill="white",anchor="rm")
    y=bandh+P
    for l in lines: c.text((P,y),l,font=ft,fill=BLK); y+=80
    c.line([P,y+P//2,CW-P,y+P//2],fill=(220,220,220),width=2)
    c.text((P,y+P//2+22),"Fonte: "+fo,font=fs,fill=GR)
    mask=Image.new("L",(CW,H),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,CW,H],14,fill=255)
    img.paste(card,(M,M),mask)
    img.save(f"posts/2026-11-08-reel-noticias/telas/card-{n}.png"); print(n,img.size,len(lines))
