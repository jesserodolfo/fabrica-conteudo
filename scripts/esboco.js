/* Desenhos rabiscados (estilo Excalidraw) com rough.js. Usado por render_esboco.py.
   Lê window.ESB = {cor, slide:{type,...}} e desenha dentro de #d. */
(function(){
const NS='http://www.w3.org/2000/svg';
const INK='#111', GR='#8a8a8a', HI='#ffd54a', HIL='#ffe27a';
async function main(){
  const E=window.ESB, RED=E.cor, REDL='#f4a7a1';
  await Promise.all(['700 30px Kalam','400 30px Kalam'].map(f=>document.fonts.load(f)));
  const host=document.getElementById('d'); const r=host.getBoundingClientRect();
  let W=Math.round(r.width), H=Math.round(r.height)-26;
  const svg=document.createElementNS(NS,'svg'); svg.setAttribute('width',W); svg.setAttribute('height',H); svg.setAttribute('viewBox',`0 0 ${W} ${H}`); svg.style.display='block'; svg.style.overflow='visible';
  host.appendChild(svg);
  const rc=rough.svg(svg); let seed=11;
  const cv=document.createElement('canvas').getContext('2d');
  let layer=svg; const add=n=>{layer.appendChild(n);return n};
  const base=o=>Object.assign({roughness:1.5,bowing:1.4,strokeWidth:3.4,stroke:INK,seed:(seed+=17)},o||{});
  const fillo=(c,o)=>Object.assign({fill:c,fillStyle:'hachure',hachureGap:12,fillWeight:2,hachureAngle:-41},o||{});
  function box(x,y,w,h,o){o=o||{};add(rc.rectangle(x,y,w,h,base(Object.assign({strokeLineDash:o.dash?[14,10]:undefined},o.fill?fillo(o.fill,o.fo):{},{stroke:o.c||INK,strokeWidth:o.sw||3.4}))))}
  function ell(cx,cy,w,h,o){o=o||{};add(rc.ellipse(cx,cy,w,h,base(Object.assign({strokeLineDash:o.dash?[14,10]:undefined},o.fill?fillo(o.fill,o.fo):{},{stroke:o.c||INK,strokeWidth:o.sw||3.4,roughness:o.r||1.5}))))}
  function line(a,b,c,d,o){o=o||{};add(rc.line(a,b,c,d,base({stroke:o.c||INK,strokeWidth:o.sw||3.2,strokeLineDash:o.dash?[14,11]:undefined,roughness:o.r||1.6})))}
  function lp(pts,o){o=o||{};add(rc.linearPath(pts,base({stroke:o.c||INK,strokeWidth:o.sw||3.4,roughness:o.r||1.4})))}
  function arrow(x1,y1,x2,y2,o){o=o||{};const dx=x2-x1,dy=y2-y1,L=Math.hypot(dx,dy)||1,nx=-dy/L,ny=dx/L,b=(o.bend==null?0.07:o.bend)*L;
    const mx=(x1+x2)/2+nx*b,my=(y1+y2)/2+ny*b;
    add(rc.curve([[x1,y1],[mx,my],[x2,y2]],base({stroke:o.c||INK,strokeWidth:o.sw||3.4,roughness:1.2})));
    const a=Math.atan2(y2-my,x2-mx),hl=o.hl||24;
    [0.5,-0.5].forEach(s=>line(x2,y2,x2-hl*Math.cos(a+s),y2-hl*Math.sin(a+s),{c:o.c,sw:o.sw||3.4,r:0.9}));}
  function meas(s,size,wt){cv.font=`${wt||700} ${size}px Kalam`;return cv.measureText(s).width}
  function fit(s,maxW,size,wt){while(size>20&&meas(s,size,wt)>maxW)size-=1;return size}
  function txt(x,y,s,o){o=o||{};const t=document.createElementNS(NS,'text');t.setAttribute('x',x);t.setAttribute('y',y);
    t.setAttribute('font-family',o.ff||'Kalam, sans-serif');t.setAttribute('font-size',o.size||32);t.setAttribute('font-weight',o.wt||700);
    t.setAttribute('fill',o.c||INK);t.setAttribute('text-anchor',o.a||'start');t.setAttribute('dominant-baseline','central');
    if(o.rot)t.setAttribute('transform',`rotate(${o.rot} ${x} ${y})`);t.style.whiteSpace='pre';t.setAttribute('xml:space','preserve');t.textContent=s;add(t);return t}
  function ctr(x,y,w,h,s,o){o=o||{};const sz=fit(s,w-(o.pad==null?28:o.pad),o.size||32,o.wt||700);txt(x+w/2,y+h/2+2,s,Object.assign({},o,{size:sz,a:'middle'}))}
  function wrap(s,maxW,size,wt){const ws=s.split(' ');const L=[];let c='';ws.forEach(w=>{const t=c?c+' '+w:w;if(meas(t,size,wt)>maxW&&c){L.push(c);c=w}else c=t});if(c)L.push(c);return L}
  function check(x,y,c){lp([[x,y+2],[x+13,y+17],[x+36,y-18]],{c:c||INK,sw:6,r:1})}
  function xmark(cx,cy,s,c,sw){line(cx-s,cy-s,cx+s,cy+s,{c,sw:sw||6,r:1.2});line(cx+s,cy-s,cx-s,cy+s,{c,sw:sw||6,r:1.2})}
  function under(x,y,w,c){line(x,y,x+w,y+3,{c:c||RED,sw:3.4,r:1.3});line(x+4,y+9,x+w-6,y+7,{c:c||RED,sw:2.6,r:1.3})}
  function gtxt(s,x,y,sz){txt(x,y,s,{size:sz||24,wt:400,c:GR})}

  const D=E.slide, T={};
  if(D.panel){const P={r:['#ffd9d5',RED],g:['#c9f0cf','#1f7a3a'],k:['#f1f1f1',INK]}[D.panel];
    box(2,2,W-4,H-4,{c:P[1],sw:4.4,fill:P[0],fo:{fillStyle:'solid'}});
    const gg=document.createElementNS(NS,'g'); gg.setAttribute('transform','translate(34,34)'); svg.appendChild(gg); layer=gg; W-=68; H-=68;}

  /* 1. o que falam x o que funciona */
  T.falam=()=>{
    const HH=D.robo?H-250:H; const mid=W/2, top=64, n=Math.max(D.left.length,D.right.length), step=(HH-top-10)/n;
    if(D.robo){robo(mid-62,HH+78,124);} if(D.ex)gtxt(D.ex,0,H-8,26);
    txt(mid/2,24,D.lt,{size:34,c:RED,a:'middle'}); under(mid/2-meas(D.lt,34)/2,42,meas(D.lt,34),RED);
    txt(mid+mid/2,24,D.rt,{size:34,a:'middle'}); under(mid+mid/2-meas(D.rt,34)/2,42,meas(D.rt,34),INK);
    line(mid,0,mid,HH-6,{dash:true,c:'#777',sw:3});
    D.left.forEach((s,i)=>{const cy=top+step*i+step/2, w=Math.min(330,mid-70), cx=(i%2?mid/2+34:mid/2-34);
      const h=Math.min(96,step-16); ell(cx,cy,w,h,{c:RED,fill:i%2?null:REDL,fo:{hachureGap:13,fillWeight:1.6}}); ctr(cx-w/2,cy-h/2,w,h,s,{c:RED,size:36,pad:56});});
    D.right.forEach((s,i)=>{const y=top+step*i+(step-Math.min(100,step-16))/2, h=Math.min(100,step-16), x=mid+30, w=W-x;
      box(x,y,w,h,{fill:i===0?HI:null,fo:{hachureGap:13,fillWeight:1.8}}); if(D.nonum)check(x+14,y+h/2+4);else txt(x+18,y+h/2+2,(i+1)+'.',{size:34,c:RED}); const sz=fit(s,w-84,34,700); txt(x+62,y+h/2+2,s,{size:sz});});
    arrow(mid-36,HH*0.5+2,mid+40,HH*0.5+2,{c:INK,bend:-0.14,sw:3.8});
  };

  /* 2. errado x certo */
  T.errado=()=>{
    const mid=W/2, top=64, gap=46, n=D.right.length, h=Math.min(124,(H-top-gap*(n-1))/n), colW=mid-44;
    txt(mid/2,24,D.lt,{size:32,c:RED,a:'middle'}); under(mid/2-meas(D.lt,32)/2,42,meas(D.lt,32),RED);
    txt(mid+mid/2,24,D.rt,{size:32,a:'middle'}); under(mid+mid/2-meas(D.rt,32)/2,42,meas(D.rt,32),INK);
    line(mid,0,mid,H,{dash:true,c:'#777',sw:3});
    D.left.forEach((s,i)=>{const y=top+i*(h+gap), last=i===D.left.length-1;
      box(0,y,colW,h,{c:RED,fill:last?REDL:null,fo:{hachureGap:12,fillWeight:1.6}}); ctr(0,y,colW,h,s,{c:RED,size:38});
      if(!last)arrow(colW/2,y+h+4,colW/2+4,y+h+gap-5,{c:RED,sw:3.6,hl:20});
      else {xmark(colW-10,y+h/2,26,RED,7);} });
    D.right.forEach((s,i)=>{const y=top+i*(h+gap), x=mid+44, last=i===n-1;
      box(x,y,colW,h,{fill:(i===0||last)?HI:null,fo:{hachureGap:13,fillWeight:1.8}}); ctr(x,y,colW,h,s,{size:38});
      if(!last)arrow(x+colW/2,y+h+4,x+colW/2-4,y+h+gap-5,{sw:3.6,hl:20});
      else check(x+colW-52,y+h/2,RED);});
  };

  /* 3. tabela */
  T.tabela=()=>{
    const cw=[W*0.32,W*0.21,W*0.47], hh=70, rh=Math.min(138,(H-hh-130)/3), th=hh+rh*3, y0=(H-th-100)/2<0?0:Math.max(0,(H-th-110)/2);
    box(0,y0,W,th,{sw:3.6});
    let x=0; cw.forEach((w,i)=>{if(i>0)line(x,y0+4,x,y0+th-4,{c:'#555',sw:2.6,r:1.3}); x+=w});
    line(6,y0+hh,W-6,y0+hh,{c:'#555',sw:2.8});
    for(let r=1;r<3;r++)line(6,y0+hh+rh*r,W-6,y0+hh+rh*r+2,{c:'#999',sw:2.4});
    x=0; D.head.forEach((h,i)=>{txt(x+18,y0+hh/2+2,h,{size:32,wt:700,c:i===2?RED:GR});x+=cw[i]});
    D.rows.forEach((row,r)=>{x=0;row.forEach((c,i)=>{const cy=y0+hh+rh*r+rh/2+2;const sz=fit(c,cw[i]-30,i===0?38:36,i===1?400:700);txt(x+18,cy,c,{size:sz,c:i===2?RED:INK,wt:i===1?400:700});x+=cw[i]})});
    const cx=cw[0]+cw[1];
    box(cx+3,y0+hh+4,cw[2]-8,rh*3-8,{c:RED,dash:true,sw:3.2});
    const ay=y0+th+16;
    txt(W-cw[2]/2,ay+54,D.note,{size:38,c:RED,a:'middle'});
    arrow(W-cw[2]/2+60,ay+34,W-cw[2]/2+80,y0+th+4,{c:RED,bend:-0.15,hl:20});
    gtxt(D.ex,0,ay+54,28);
  };

  /* 4. dor vaga -> processo concreto */
  T.riscada=()=>{
    const b1=120, pitch=104, lh=D.lines.length*pitch+70, gap=56, tot=b1+gap+lh, y0=Math.max(0,(H-tot-30)/2);
    box(0,y0,W,b1,{c:RED,dash:true}); txt(22,y0+26,D.l1,{size:30,c:RED,wt:700});
    const s=D.strike, sz=fit(s,W-60,44,400), w=meas(s,sz,400), sx=(W-w)/2;
    txt(W/2,y0+b1/2+16,s,{size:sz,wt:400,c:GR,a:'middle'});
    lp([[sx-8,y0+b1/2+22],[sx+w*0.3,y0+b1/2+8],[sx+w*0.55,y0+b1/2+26],[sx+w,y0+b1/2+10]],{c:RED,sw:5,r:1.6});
    const ay=y0+b1+6; arrow(W/2,ay,W/2+6,ay+gap-8,{sw:4,hl:22,bend:0.1});
    const y2=y0+b1+gap; box(0,y2,W,lh,{fill:HIL,fo:{hachureGap:15,fillWeight:1.5},sw:3.8});
    txt(22,y2+28,D.l2,{size:30,c:INK});
    D.lines.forEach((runs,li)=>{let x=24;const ty=y2+88+li*pitch;
      runs.forEach(r=>{const wt=700,sz=42;txt(x,ty,r.t,{size:sz,wt});const w=meas(r.t,sz,wt);
        if(r.u){const uw=meas(r.t.trim(),sz,wt);under(x+(r.t.startsWith(' ')?meas(' ',sz,wt):0),ty+26,uw,RED);txt(x+(r.t.startsWith(' ')?meas(' ',sz,wt):0)+uw/2,ty+58,r.u,{size:28,c:RED,wt:400,a:'middle'});}
        x+=w});});
    gtxt(D.ex,0,y2+lh+22,24);
  };

  /* 5. piramide sintoma/problema/causa */
  T.piramide=()=>{
    const hs=[118,118,176], gap=40, tot=hs[0]+hs[1]+hs[2]+gap*2, ws=[W*0.60,W*0.80,W], y0=Math.max(0,(H-tot)/2);
    let y=y0; D.items.forEach((it,i)=>{const w=ws[i],x=(W-w)/2,h=hs[i],last=i===2,c=last?INK:RED;
      box(x,y,w,h,{c:last?INK:RED,fill:last?HI:null,fo:{hachureGap:13,fillWeight:2},sw:last?4.2:3.4});
      txt(x+22,y+30,it.k.toUpperCase(),{size:30,c:RED,wt:700});
      if(last){const L=wrap(it.t,w-48,38,700);L.slice(0,2).forEach((l,j)=>txt(x+22,y+86+j*50,l,{size:38}));}
      else txt(x+22,y+82,it.t,{size:fit(it.t,w-44,38,700),c:INK});
      if(i<2)arrow(W/2+(i?30:-30),y+h+4,W/2+(i?34:-26),y+h+gap-3,{c:i===1?INK:RED,hl:18,sw:3.4});
      y+=h+gap;});
    txt(0,y0+56,D.tag,{size:34,c:GR,wt:400,rot:-6});
  };

  /* 6. grade de 7 opcoes */
  T.grade=()=>{
    const cols=2, gx=26, n=D.items.length, rows=Math.ceil(n/2), gy=18, h=Math.min(140,(H-gy*(rows-1))/rows), w=(W-gx)/2;
    D.items.forEach((it,i)=>{let r=Math.floor(i/2),c=i%2,x=c*(w+gx),ww=w;
      if(i===n-1&&n%2){x=0;ww=W;r=rows-1;c=0}
      const y=r*(h+gy);
      if(it.k==='agente'){box(x,y,ww,h,{c:RED,fill:REDL,fo:{hachureGap:11,fillWeight:2},sw:4});ctr(x+40,y,ww-40,h,it.t,{c:RED,size:40});xmark(x+36,y+h/2,14,RED,6);}
      else if(it.k==='destaque'){box(x,y,ww,h,{fill:HI,fo:{hachureGap:11,fillWeight:2},sw:4});check(x+14,y+h/2+4);ctr(x+60,y,ww-60,h,it.t,{size:38,pad:50});}
      else if(it.k==='skip'){box(x,y,ww,h,{dash:true,c:'#666'});ctr(x,y,ww,h,it.t,{c:'#555',size:38});}
      else{box(x,y,ww,h);check(x+14,y+h/2+4);ctr(x+60,y,ww-60,h,it.t,{size:36,pad:50});}
    });
  };

  /* 7. matriz impacto x facilidade */
  T.matriz=()=>{
    const ox=46, oy=H-62, pw=W-ox-6, ph=oy-12;
    arrow(ox,oy,ox+pw,oy+2,{bend:0.01,sw:3.6}); arrow(ox,oy,ox+2,10,{bend:0.01,sw:3.6});
    txt(ox+10,oy+34,D.x+' →',{size:32,wt:700,c:GR});
    txt(14,oy/2,'impacto →',{size:30,wt:700,c:GR,a:'middle',rot:-90});
    const pos=[[0.76,0.2],[0.45,0.5],[0.2,0.8]], bw=320, bh=Math.min(120,ph*0.28);
    const pts=[D.pts[0],D.pts[1],D.pts[2]];
    pts.forEach((p,i)=>{const cx=ox+pos[i][0]*pw+(i===0?-6:0), cy=12+pos[i][1]*ph*0.92+bh*0.05;
      const k=i===0;
      ell(cx,cy,bw,bh,{fill:k?HI:null,fo:{hachureGap:13,fillWeight:1.8},dash:i===2,c:i===2?'#666':INK,sw:k?4.2:3.4});
      txt(cx,cy-18,p.t,{size:36,a:'middle',c:i===2?'#666':INK});
      txt(cx,cy+22,p.s,{size:28,a:'middle',wt:400,c:k?INK:GR});
      pos[i].cx=cx;pos[i].cy=cy;});
    arrow(pos[2].cx+100,pos[2].cy-bh/2-4,pos[1].cx-100,pos[1].cy+bh/2+6,{c:RED,bend:-0.12,hl:20});
    arrow(pos[1].cx+110,pos[1].cy-bh/2+8,pos[0].cx-120,pos[0].cy+bh/2-4,{c:RED,bend:-0.12,hl:20});
    txt(W,oy+34,D.ex,{size:26,wt:400,c:GR,a:'end'});
  };

  /* 8. escada de 4 degraus */
  T.escada=()=>{
    const n=D.steps.length, g=14, w=(W-g*(n-1))/n, hmin=150, hmax=H-8;
    D.steps.forEach((s,i)=>{const h=hmin+(hmax-hmin)*i/(n-1), x=i*(w+g), y=H-h, last=i===n-1;
      box(x,y,w,h,{fill:last?HI:null,fo:{hachureGap:13,fillWeight:1.8},sw:last?4.2:3.4});
      ell(x+36,y+38,52,52,{c:RED,sw:3.2,r:1.1}); txt(x+36,y+40,String(i+1),{size:30,a:'middle',c:RED});
      s.forEach((l,j)=>txt(x+w/2,y+(s.length>1?96:96)+j*36,l,{size:fit(l,w-20,31,700),a:'middle'}));
    });
    const dl=hmax-hmin, x4=3*(w+g);
    arrow(30,H-hmin-dl/3-70,x4-20,H-hmin-dl*0.95,{c:RED,bend:-0.06,sw:3.8});
  };

  /* 9. lista numerada de 4 etapas */
  T.lista=()=>{
    const n=D.items.length, gap=24, h=(H-gap*(n-1))/n;
    D.items.forEach((it,i)=>{const y=i*(h+gap), last=i===n-1;
      box(0,y,W,h,{fill:last?HIL:null,fo:{hachureGap:15,fillWeight:1.5},sw:3.6});
      if(D.chk){check(30,y+h/2+2,RED);}else{ell(52,y+h/2,58,58,{c:RED,sw:3.4,r:1.1}); txt(52,y+h/2+3,String(i+1),{size:34,a:'middle',c:RED});}
      if(it.d){txt(104,y+h*0.36,it.t,{size:fit(it.t,W-130,36,700)});
      txt(104,y+h*0.72,it.d,{size:fit(it.d,W-130,28,400),wt:400,c:'#555'});}else txt(104,y+h/2+2,it.t,{size:fit(it.t,W-130,42,700)});
      if(i<n-1&&!D.chk)arrow(W/2+(i%2?-20:20),y+h+2,W/2+(i%2?-16:24),y+h+gap-2,{c:RED,hl:14,sw:3,bend:0.2});
    });
  };

  /* 10A. escada resumo + CTA */
  T.cta=()=>{
    const ctaH=Math.min(200,H*0.36), sh=H-ctaH-26, n=D.steps.length, rh=Math.min(58,(sh-(n-1)*8)/n), off=Math.min(54,(W-420)/(n-1));
    D.steps.forEach((s,i)=>{const lv=n-1-i;const y=lv*(rh+8), x=i*off, w=W-(n-1)*off-30, last=i===n-1;
      box(x,y,w,rh,{fill:last?HI:null,fo:{hachureGap:12,fillWeight:1.8},sw:last?4:3.2});
      txt(x+16,y+rh/2+2,(i+1)+'.',{size:30,c:RED}); txt(x+62,y+rh/2+2,s,{size:fit(s,w-90,32,700)});});
    const by=H-ctaH, bh=Math.round(ctaH*0.56);
    box(0,by,W,bh,{fill:HIL,fo:{hachureGap:15,fillWeight:1.5},sw:3.8});
    const pre=D.cta.replace(D.kw,''), sz=46; txt(24,by+bh*0.36,pre,{size:sz});
    const px=24+meas(pre,sz,700)+(D.kwgap||0); txt(px,by+bh*0.36+1,D.kw,{size:sz-4,ff:'Archivo, sans-serif',wt:900,c:RED});
    const kwid=(()=>{cv.font='900 '+(sz-4)+'px Archivo';return cv.measureText(D.kw).width})(); ell(px+kwid/2,by+bh*0.36+2,kwid+(D.kwpad||30),bh*0.5,{c:RED,sw:3.2,r:1.2});
    txt(24,by+bh*0.78,D.sub,{size:fit(D.sub,W-48,28,400),wt:400,c:'#333'});
    const bw=Math.min(W,meas(D.btn,32,700)+70), bx=W-bw, byy=by+bh+16;
    box(bx,byy,bw,ctaH-bh-16,{c:RED,fill:REDL,fo:{hachureGap:12,fillWeight:1.8},sw:3.8}); ctr(bx,byy,bw,ctaH-bh-16,D.btn,{size:32,c:INK});
    arrow(bx-70,byy+(ctaH-bh-16)/2,bx-8,byy+(ctaH-bh-16)/2,{c:RED,bend:-0.15,hl:18});
  };

  /* 10B. antes ou depois + comentario */
  T.comentario=()=>{
    const mid=W/2, eh=Math.min(200,H*0.30), cy=eh/2+6, ew=mid-44;
    ell(mid/2,cy,ew,eh,{c:RED,fill:REDL,fo:{hachureGap:12,fillWeight:1.6}}); txt(mid/2,cy+2,D.a,{size:54,c:RED,a:'middle'});
    ell(mid+mid/2,cy,ew,eh,{fill:HI,fo:{hachureGap:12,fillWeight:1.8},sw:4}); txt(mid+mid/2,cy+2,D.b,{size:54,a:'middle'});
    line(mid,4,mid,eh+8,{dash:true,c:'#777',sw:3});
    const ch=Math.min(250,H-eh-120), y=H-ch; box(0,y,W,ch,{sw:3.8});
    ell(66,y+ch*0.32,66,66,{c:'#777',fill:'#ccc',fo:{hachureGap:9,fillWeight:1.4},sw:3});
    txt(122,y+ch*0.30,D.name,{size:34}); txt(122+meas(D.name,34)+16,y+ch*0.30+2,D.when,{size:28,wt:400,c:GR});
    const tx=D.text, sz=fit(tx,W-60,46,700); txt(28,y+ch*0.70,tx,{size:sz});
    const cx=28+meas(tx,sz,700)+10; if(cx<W-20)line(cx,y+ch*0.70-22,cx+2,y+ch*0.70+22,{c:RED,sw:4,r:0.8});
    arrow(mid/2,eh+8,mid/2+30,y-10,{c:RED,bend:0.1,hl:20});arrow(mid+mid/2,eh+8,mid+mid/2-30,y-10,{c:INK,bend:-0.1,hl:20});
  };


  /* robozinho original (cabeca quadrada, antena, olhos, sorriso) */
  function robo(x,y,s){
    const hw=s, hh=s*0.8;
    line(x+hw/2,y,x+hw/2+3,y-s*0.22,{sw:3.4}); ell(x+hw/2+3,y-s*0.28,s*0.14,s*0.14,{c:RED,fill:RED,fo:{hachureGap:5,fillWeight:2},sw:3});
    box(x,y,hw,hh,{fill:HIL,fo:{hachureGap:12,fillWeight:1.4},sw:3.8});
    box(x-s*0.07,y+hh*0.35,s*0.07,hh*0.3,{sw:3}); box(x+hw,y+hh*0.35,s*0.07,hh*0.3,{sw:3});
    ell(x+hw*0.30,y+hh*0.36,s*0.17,s*0.17,{c:RED,fill:RED,fo:{hachureGap:4,fillWeight:2},sw:3,r:1});
    ell(x+hw*0.70,y+hh*0.36,s*0.17,s*0.17,{c:RED,fill:RED,fo:{hachureGap:4,fillWeight:2},sw:3,r:1});
    lp([[x+hw*0.28,y+hh*0.66],[x+hw*0.40,y+hh*0.80],[x+hw*0.60,y+hh*0.80],[x+hw*0.72,y+hh*0.66]],{c:INK,sw:3.6,r:1});
    box(x+hw*0.25,y+hh+8,hw*0.5,s*0.22,{sw:3.4});
  }
  function stamp(x,y,s,rot){const sz=30,w=meas(s,sz,700)+36; const g=document.createElementNS(NS,'g');
    box(x-w/2,y-26,w,52,{c:RED,sw:3.2,dash:true}); txt(x,y+2,s,{size:sz,c:RED,a:'middle'});}

  /* NOVO robo: so o robozinho, centralizado, com frase opcional */
  T.robo=()=>{const s=Math.min(260,H*0.4);robo(W/2-s/2,H/2-s/2,s);if(D.t)txt(W/2,H-30,D.t,{size:34,a:'middle'});};

  /* NOVO grafico: barras simples a mao */
  T.grafico=()=>{
    const n=D.bars.length, ox=10, oy=H-120, ph=oy-110, pw=W-ox-10, g=40, bw=(pw-g*(n+1))/n, mx=Math.max(...D.bars.map(b=>b.v),1);
    arrow(ox,oy,ox+pw,oy+2,{bend:0.01,sw:3.6});
    D.bars.forEach((b,i)=>{const x=ox+g+i*(bw+g), h=b.v>0?ph*b.v/mx:0;
      if(b.v>0)box(x,oy-h,bw,h,{c:RED,fill:REDL,fo:{hachureGap:12,fillWeight:2},sw:3.8});
      else check(x+bw/2-18,oy-34,INK);
      txt(x+bw/2,oy-h-(b.v>0?34:84),b.val,{size:40,a:'middle',c:b.v>0?RED:INK});
      txt(x+bw/2,oy+44,b.l,{size:34,a:'middle',wt:400,c:'#555'});});
    stamp(W-130,40,D.ex||'EXEMPLO'); gtxt('erros por semana',0,24,28);
  };

  /* NOVO fluxo: pasta com 2 caixas que viram o PDF */
  T.fluxo=()=>{
    const fh=H*0.46, fy=20, tab=64;
    box(0,fy+tab-8,W,fh,{c:'#666',dash:true,sw:3.4}); lp([[0,fy+tab-8],[0,fy],[W*0.34,fy],[W*0.38,fy+tab-8]],{c:'#666',sw:3.4});
    txt(18,fy+tab/2-4,D.pasta,{size:30,c:'#555',wt:400});
    const bw=(W-3*40)/2, bh=fh-110, by=fy+tab+34;
    D.fontes.forEach((f,i)=>{const x=40+i*(bw+40); box(x,by,bw,bh,{}); ctr(x,by,bw,bh,f,{size:40});});
    const py=by+bh+(fh-bh-34-tab)+110, ph=H-py-40;
    D.fontes.forEach((f,i)=>{const x=40+i*(bw+40)+bw/2; arrow(x,by+bh+34,W/2+(i?30:-30),py-6,{c:RED,bend:i?-0.08:0.08,sw:3.8,hl:22});});
    const pw=W*0.62; box((W-pw)/2,py,pw,Math.min(ph,150),{fill:HI,fo:{hachureGap:12,fillWeight:1.8},sw:4.2}); ctr((W-pw)/2,py,pw,Math.min(ph,150),D.saida,{size:44});
    if(D.ex)gtxt(D.ex,0,H-6,26);
  };

  /* NOVO skill: caixa SKILL com linhas curtas + robo */
  T.skill=()=>{
    const bw=W*0.70, n=D.lines.length, hh=84, lh=(H-hh-40)/n>96?96:(H-hh-40)/n, bh=hh+lh*n+24, y0=Math.max(0,(H-bh)/2);
    box(0,y0,bw,bh,{sw:4}); box(0,y0,bw,hh,{fill:HI,fo:{hachureGap:12,fillWeight:1.8},sw:4});
    txt(24,y0+hh/2+2,D.t,{size:44,c:INK}); 
    D.lines.forEach((l,i)=>{const y=y0+hh+14+lh*i+lh/2; ell(46,y,40,40,{c:RED,sw:3,r:1}); txt(46,y+2,String(i+1),{size:26,a:'middle',c:RED}); txt(86,y+2,l,{size:fit(l,bw-110,36,700)});});
    const rs=Math.min(190,W-bw-60); robo(bw+(W-bw)/2-rs/2,y0+bh-rs*0.8-rs*0.22-30,rs);
    arrow(bw+(W-bw)/2-rs*0.2,y0+bh-rs*1.35,bw+10,y0+bh*0.55,{c:RED,bend:0.2,hl:18,sw:3.4});
  };

  /* NOVO alertas: 3 itens com triangulo de aviso */
  T.alertas=()=>{
    const n=D.items.length, gap=30, h=Math.min(190,(H-gap*(n-1)-40)/n), y0=Math.max(0,(H-n*h-gap*(n-1)-40)/2);
    D.items.forEach((t,i)=>{const y=y0+i*(h+gap); box(0,y,W,h,{sw:3.6,fill:i===0?HIL:null,fo:{hachureGap:15,fillWeight:1.5}});
      const cx=70,cy=y+h/2; lp([[cx-38,cy+30],[cx,cy-36],[cx+38,cy+30],[cx-38,cy+30]],{c:RED,sw:4.2,r:1}); txt(cx,cy+8,'!',{size:42,a:'middle',c:RED});
      txt(140,cy+2,t,{size:fit(t,W-170,44,700)});});
    if(D.ex)gtxt(D.ex,0,H-6,26);
  };

  /* NOVO linha: linha do tempo com 3 pontos */
  T.linha=()=>{
    const y=H*0.42, x0=60, x1=W-60;
    arrow(x0-20,y,x1+20,y+2,{bend:0.01,sw:4.2,hl:28});
    D.pts.forEach((p,i)=>{const x=x0+(x1-x0)*i/(D.pts.length-1), last=i===D.pts.length-1;
      ell(x,y,last?60:48,last?60:48,{c:last?INK:RED,fill:last?HI:null,fo:{fillStyle:'solid'},sw:4.4,r:0.8});
      txt(x,y-96,p.t,{size:46,a:'middle'}); if(p.h)txt(x,y+84,p.h,{size:44,a:'middle',c:RED});});
    if(D.nota)txt(W/2,H-50,D.nota,{size:30,a:'middle',wt:400,c:'#555'});
  };

  /* NOVO numeros: 3 numeros grandes + selo EXEMPLO */
  T.numeros=()=>{
    const n=D.items.length, gap=30, h=Math.min(200,(H-gap*(n-1)-90)/n), y0=70;
    D.items.forEach((it,i)=>{const y=y0+i*(h+gap), last=i===n-1;
      box(0,y,W,h,{sw:last?4.2:3.6,fill:last?HI:null,fo:{hachureGap:13,fillWeight:1.8}});
      txt(30,y+h/2+2,it.l,{size:48,wt:700,c:last?INK:'#444'});
      txt(W-30,y+h/2+2,it.v,{size:60,a:'end',c:last?INK:RED});});
    stamp(W-130,32,D.ex||'EXEMPLO');
  };


  /* NOVO capa: 2 cards antes x agora, cada um com relogio desenhado */
  function relogio(cx,cy,R,hh,mm,c,o){o=o||{};
    ell(cx,cy,R*2,R*2,{c:c,sw:6,r:0.9,fill:'#fff',fo:{fillStyle:'solid'}});
    for(let i=0;i<12;i++){const a=i*Math.PI/6, big=i%3===0, r1=R*(big?0.74:0.83), r2=R*0.92;
      line(cx+r1*Math.sin(a),cy-r1*Math.cos(a),cx+r2*Math.sin(a),cy-r2*Math.cos(a),{c:INK,sw:big?5:3,r:0.4});}
    const ma=mm*Math.PI/30, ha=(hh%12+mm/60)*Math.PI/6;
    line(cx,cy,cx+R*0.52*Math.sin(ha),cy-R*0.52*Math.cos(ha),{c:INK,sw:9,r:0.3});
    line(cx,cy,cx+R*0.78*Math.sin(ma),cy-R*0.78*Math.cos(ma),{c:INK,sw:6,r:0.3});
    ell(cx,cy,R*0.13,R*0.13,{c:c,fill:c,fo:{fillStyle:'solid'},sw:3,r:0.4});}
  T.capa=()=>{
    const g=36, cw=(W-g)/2, ch=H-4, R=Math.min(cw*0.26,118);
    D.cards.forEach((k,i)=>{const x=i*(cw+g), c=i?'#1f7a3a':RED, cx=x+cw/2;
      box(x,2,cw,ch,{c:c,sw:4.4,fill:i?'#c9f0cf':'#ffb8b2',fo:{fillStyle:'solid'}});
      txt(cx,52,k.lbl,{size:44,c:c,a:'middle'});
      relogio(cx,104+R+8,R,k.h,k.m,c);
      const y2=104+R*2+80;
      txt(cx,y2,k.big,{size:fit(k.big,cw-40,76,700),c:c,a:'middle'});
      txt(cx,y2+66,k.l1,{size:fit(k.l1,cw-40,38,700),a:'middle'});
      txt(cx,y2+66+78,k.l2,{size:fit(k.l2,cw-40,38,700),c:c,a:'middle',wt:400});});
  };

  (T[D.type]||(()=>{}))();
  window.__ready=true;
}
main().catch(e=>{window.__err=String(e);window.__ready=true});
})();
