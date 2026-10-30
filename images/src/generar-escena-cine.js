// Generador de escena cinematográfica: proyección 3D simple + postproceso SVG
const fs = require('fs');
const OUT = process.argv[2];
const W = 1920, H = 1080, BAR = 138;

// ---------- utilidades vectoriales ----------
const sub = (a, b) => [a[0]-b[0], a[1]-b[1], a[2]-b[2]];
const add = (a, b) => [a[0]+b[0], a[1]+b[1], a[2]+b[2]];
const mul = (a, s) => [a[0]*s, a[1]*s, a[2]*s];
const dot = (a, b) => a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
const cross = (a, b) => [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]];
const norm = a => mul(a, 1/Math.hypot(...a));
const lerp3 = (a, b, t) => add(a, mul(sub(b, a), t));

// ---------- cámara ----------
const eye = [-7.5, 1.1, 15.5], target = [6.8, 4.4, 0.0];
const F = 1250, CX = W/2, CY = H/2 + 40;
const fw = norm(sub(target, eye));
const rt = norm(cross(fw, [0,1,0]));
const up = cross(rt, fw);
function P(p) {
  const d = sub(p, eye);
  const z = dot(d, fw);
  return [CX + F*dot(d, rt)/z, CY - F*dot(d, up)/z, z];
}
const pts = arr => arr.map(p => { const q = P(p); return q[0].toFixed(1)+','+q[1].toFixed(1); }).join(' ');

// ---------- iluminación (sol bajo, a contraluz) ----------
const L = norm([0.75, 0.32, -0.6]);
function shade(base, n, opts = {}) {
  const sun = Math.max(0, dot(n, L));
  const sky = 0.5 + 0.5*n[1];
  const bounce = Math.max(0, -n[1]);
  const c = [0,1,2].map(i => {
    const amb = [0.40, 0.42, 0.46][i]*sky*0.85;
    const bnc = [0.62, 0.42, 0.24][i]*(bounce*0.6 + (1-Math.abs(n[1]))*0.38);
    const sn  = [1.25, 0.88, 0.55][i]*sun*1.25;
    return base[i]*(amb + bnc + sn + (opts.emit||0));
  });
  return c.map(v => Math.round(255*Math.min(1, Math.pow(Math.max(0, v), 1/1.9))));
}
const rgb = c => `rgb(${c[0]},${c[1]},${c[2]})`;

const YEL = [0.98, 0.66, 0.05], DARK = [0.16, 0.15, 0.14], STEEL = [0.45, 0.45, 0.46], TIRE = [0.07, 0.07, 0.075];

let gradId = 0; const defs = [];
function facePoly(vs, base, opts = {}) {
  const c = vs.reduce((a, v) => add(a, v), [0,0,0]).map(x => x/vs.length);
  let n = norm(cross(sub(vs[1], vs[0]), sub(vs[2], vs[0])));
  if (opts.center && dot(n, sub(c, opts.center)) < 0) n = mul(n, -1);
  if (dot(n, sub(eye, c)) <= 0) return '';
  const col = shade(base, n, opts);
  const id = 'g' + (gradId++);
  const hi = col.map(v => Math.min(255, Math.round(v*1.08))), lo = col.map(v => Math.round(v*(opts.ao ?? 0.72)));
  defs.push(`<linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${rgb(hi)}"/><stop offset="1" stop-color="${rgb(lo)}"/></linearGradient>`);
  return `<polygon points="${pts(vs)}" fill="url(#${id})" stroke="${rgb(lo)}" stroke-width="0.8" stroke-linejoin="round"/>`;
}
function box(x0,x1,y0,y1,z0,z1,base,opts={}) {
  const v = (x,y,z) => [x,y,z];
  const center = [(x0+x1)/2,(y0+y1)/2,(z0+z1)/2];
  const fs_ = [
    [v(x0,y0,z1),v(x1,y0,z1),v(x1,y1,z1),v(x0,y1,z1)],
    [v(x0,y0,z0),v(x0,y1,z0),v(x1,y1,z0),v(x1,y0,z0)],
    [v(x0,y0,z0),v(x0,y0,z1),v(x0,y1,z1),v(x0,y1,z0)],
    [v(x1,y0,z0),v(x1,y1,z0),v(x1,y1,z1),v(x1,y0,z1)],
    [v(x0,y1,z0),v(x0,y1,z1),v(x1,y1,z1),v(x1,y1,z0)],
    [v(x0,y0,z0),v(x1,y0,z0),v(x1,y0,z1),v(x0,y0,z1)],
  ];
  return fs_.map(f => facePoly(f, base, {...opts, center})).join('');
}
function prism(profile, z0, z1, base, opts={}) {
  const cx = profile.reduce((a,p)=>a+p[0],0)/profile.length, cy = profile.reduce((a,p)=>a+p[1],0)/profile.length;
  const center = [cx, cy, (z0+z1)/2];
  let s = '';
  s += facePoly(profile.map(p => [p[0],p[1],z0]), base, {...opts, center});
  for (let i = 0; i < profile.length; i++) {
    const a = profile[i], b = profile[(i+1)%profile.length];
    s += facePoly([[a[0],a[1],z0],[b[0],b[1],z0],[b[0],b[1],z1],[a[0],a[1],z1]], base, {...opts, center});
  }
  s += facePoly(profile.map(p => [p[0],p[1],z1]), base, {...opts, center});
  return s;
}
function line3(a, b, stroke, w, extra='') {
  const p = P(a), q = P(b);
  return `<line x1="${p[0].toFixed(1)}" y1="${p[1].toFixed(1)}" x2="${q[0].toFixed(1)}" y2="${q[1].toFixed(1)}" stroke="${stroke}" stroke-width="${w}" stroke-linecap="round" ${extra}/>`;
}
const circle3 = (c, r, zf, n=56) => Array.from({length:n}, (_, i) => { const t = i/n*2*Math.PI; return [c[0]+r*Math.cos(t), c[1]+r*Math.sin(t), zf]; });
function hull(points) {
  const p = points.slice().sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
  const cr = (o,a,b)=>(a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0]);
  const lo=[], hi=[];
  for (const q of p){ while(lo.length>=2&&cr(lo[lo.length-2],lo[lo.length-1],q)<=0) lo.pop(); lo.push(q); }
  for (const q of p.reverse()){ while(hi.length>=2&&cr(hi[hi.length-2],hi[hi.length-1],q)<=0) hi.pop(); hi.push(q); }
  return lo.slice(0,-1).concat(hi.slice(0,-1));
}
const poly2 = arr => arr.map(q => q[0].toFixed(1)+','+q[1].toFixed(1)).join(' ');

function wheel(cx, cz, side, r=2.05, w=1.55) {
  // side: +1 = cara exterior hacia +z
  const zo = cz + side*w/2, zi = cz - side*w/2, cy = r;
  const outer = circle3([cx,cy], r, zo), inner = circle3([cx,cy], r, zi);
  const all = outer.concat(inner).map(P);
  let s = `<polygon points="${poly2(hull(all))}" fill="#1c1a18"/>`;
  // tacos de la banda de rodadura (chevron)
  for (let i = 0; i < 36; i++) {
    const t = i/36*2*Math.PI, t2 = t + 0.09;
    const nrm = [Math.cos(t), Math.sin(t), 0];
    const pt = (tt, zz) => [cx+r*1.01*Math.cos(tt), cy+r*1.01*Math.sin(tt), zz];
    if (dot(nrm, sub(eye, pt(t, cz))) <= 0) continue;
    s += line3(pt(t, zo), pt(t2, cz+side*0.05), '#0b0a09', 6) + line3(pt(t+0.045, zi), pt(t2+0.045, cz-side*0.05), '#0b0a09', 6);
  }
  const visibleOuter = dot([0,0,side], sub(eye, [cx,cy,zo])) > 0;
  if (visibleOuter) {
    const op = outer.map(P);
    s += `<polygon points="${poly2(op)}" fill="url(#sidewall)"/>`;
    const rimP = circle3([cx,cy], r*0.56, zo+side*0.02).map(P);
    s += `<polygon points="${poly2(rimP)}" fill="url(#rim)" stroke="#5a3d05" stroke-width="2"/>`;
    const hubP = circle3([cx,cy], r*0.22, zo+side*0.12).map(P);
    s += `<polygon points="${poly2(hubP)}" fill="#3a3632" stroke="#1d1b19" stroke-width="2"/>`;
    for (let i = 0; i < 12; i++) {
      const t = i/12*2*Math.PI; const q = P([cx+r*0.38*Math.cos(t), cy+r*0.38*Math.sin(t), zo+side*0.05]);
      s += `<circle cx="${q[0].toFixed(1)}" cy="${q[1].toFixed(1)}" r="4" fill="#2b2620"/>`;
    }
    // barro en el flanco
    s += `<polygon points="${poly2(op)}" fill="url(#mud)" opacity="0.85"/>`;
  }
  return s;
}

// ---------- construir el camión ----------
let truck = '';
// ruedas lado lejano
truck += wheel(10.6, -4.05, -1) + wheel(10.6, -2.45, -1) + wheel(3.0, -4.05, -1);
// chasis
truck += box(0.8, 13.2, 1.5, 2.9, -2.2, 2.2, DARK);
truck += box(5, 12.5, 0.9, 1.6, -1.2, 1.2, DARK);
// tolva (prisma con perfil lateral)
const bedProf = [[4.1,3.0],[13.8,4.1],[15.3,4.9],[15.0,7.3],[4.1,8.0]];
truck += prism(bedProf, -4.9, 4.9, YEL, {ao: 0.6});
// carga de mineral asomando
const load = [];
for (let i = 0; i <= 28; i++) { const x = 4.4 + i*(10.4/28); const ytop = 8.0 - (x-4.1)*(0.7/10.9); load.push([x, ytop + 0.25 + 0.6*Math.sin(Math.PI*(i/28)) + 0.12*Math.sin(i*2.3)]); }
const loadPts = load.map(([x,y]) => P([x,y,4.3]));
const loadBase = [P([14.8,7.35,4.3]), P([4.3,7.98,4.3])];
truck += `<polygon points="${poly2(loadPts.concat(loadBase))}" fill="url(#ore)"/>`;
// nervaduras laterales de la tolva
for (const x of [6.4, 8.8, 11.2, 13.4]) {
  const yb = 3.0 + (x-4.1)*(1.1/9.7), yt = 8.0 - (x-4.1)*(0.7/10.9);
  truck += box(x-0.18, x+0.18, yb+0.1, yt-0.05, 4.9, 5.15, YEL, {ao:0.55});
}
truck += box(4.1, 15.1, 7.6, 7.95, 4.9, 5.2, YEL); // borde superior
// visera sobre la cabina
truck += box(0.1, 4.2, 7.65, 8.05, -4.9, 4.9, YEL, {ao:0.6});
// cilindro de volteo
truck += line3([6.2,2.3,4.0],[7.0,4.0,4.0], '#6c6c6c', 22) + line3([6.2,2.3,4.0],[6.6,3.1,4.0], '#b8b8b8', 11);
// ruedas traseras lado cercano
truck += wheel(10.6, 2.45, 1) + wheel(10.6, 4.05, 1);
// módulo del radiador y motor
truck += box(0.25, 3.8, 1.3, 4.6, -1.7, 1.7, YEL, {ao:0.6});
// rejilla
for (let i = 0; i <= 9; i++) {
  const z = -1.45 + i*0.32;
  truck += line3([0.24, 1.6, z], [0.24, 4.3, z], '#2a2216', 3.2);
}
truck += line3([0.24,1.6,-1.45],[0.24,1.6,1.43],'#2a2216',3) + line3([0.24,4.3,-1.45],[0.24,4.3,1.43],'#2a2216',3);
// plataforma
truck += box(0.0, 5.3, 4.6, 4.95, -4.9, 4.9, YEL, {ao:0.55});
// barandas
for (const z of [-4.8, -2.4, 0, 2.4, 4.8]) truck += line3([0.05,4.95,z],[0.05,6.0,z], '#e9b21e', 4);
truck += line3([0.05,6.0,-4.8],[0.05,6.0,4.8], '#ffd25a', 4) + line3([0.05,5.5,-4.8],[0.05,5.5,4.8], '#e9b21e', 3);
truck += line3([0.05,6.0,4.8],[4.0,6.0,4.8], '#ffd25a', 4) + line3([0.05,5.5,4.8],[4.0,5.5,4.8], '#e9b21e', 3);
// cabina (lado cercano)
truck += box(0.9, 3.7, 4.95, 7.5, 1.3, 4.1, YEL, {ao:0.7});
// parachoques
truck += box(-0.2, 0.5, 1.0, 1.9, -3.2, 3.2, [0.25,0.24,0.22]);
// faros
const lights = [[-0.05, 4.45, 3.6], [-0.05, 4.45, 3.0], [-0.05, 4.45, -3.0], [-0.05, 4.45, -3.6], [-0.22, 1.5, 2.6], [-0.22, 1.5, -2.6]];
// escalera diagonal
truck += line3([-1.6,0.6,4.3],[0.1,4.6,4.3],'#3b3b3b',6) + line3([-1.6,0.6,3.6],[0.1,4.6,3.6],'#3b3b3b',6);
for (let i = 1; i < 9; i++) { const t = i/9; truck += line3(lerp3([-1.6,0.6,4.3],[0.1,4.6,4.3],t), lerp3([-1.6,0.6,3.6],[0.1,4.6,3.6],t), '#5a5a5a', 4); }
// rueda delantera cercana
truck += wheel(3.0, 4.05, 1);

// ventana frontal de la cabina (parabrisas)
const ws = [[0.88,5.3,1.5],[0.88,5.3,3.9],[0.88,7.25,3.9],[0.88,7.25,1.5]];
const wsP = ws.map(P);
const wsMinX = Math.min(...wsP.map(p=>p[0])), wsMaxX = Math.max(...wsP.map(p=>p[0]));
const wsMinY = Math.min(...wsP.map(p=>p[1])), wsMaxY = Math.max(...wsP.map(p=>p[1]));
const wcx = (wsMinX+wsMaxX)/2, wh = wsMaxY - wsMinY;
// ventana lateral (deja entrar contraluz)
const sideWin = [[1.1,5.5,4.11],[3.4,5.5,4.11],[3.4,7.25,4.11],[1.1,7.25,4.11]];

// número de flota en la tolva
function affine(o, ux, vy) {
  const O = P(o), U = P(ux), V = P(vy);
  return `matrix(${(U[0]-O[0]).toFixed(3)},${(U[1]-O[1]).toFixed(3)},${(V[0]-O[0]).toFixed(3)},${(V[1]-O[1]).toFixed(3)},${O[0].toFixed(2)},${O[1].toFixed(2)})`;
}
const decal = `<g transform="${affine([9.3,6.6,4.92],[10.3,6.6,4.92],[9.3,5.6,4.92])}">
  <text x="0" y="0" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="2.1" fill="#1a1612" opacity="0.88" text-anchor="middle">10</text></g>`;

// sombra proyectada (el sol está detrás: la sombra viene hacia la cámara)
const shadowSrc = [];
for (const x of [-0.2, 5.3, 15.3]) for (const y of [0.1, 4.9, 8.0]) for (const z of [-4.9, 4.9]) shadowSrc.push([x,y,z]);
const shadowPts = hull(shadowSrc.map(p => { const g = sub(p, mul(L, p[1]/L[1])); return P([g[0], 0, g[2]]); }));

// polvo y luces
const sunXY = [1590, 300];

// ---------- jugador en la cabina ----------
const s = wh/178; // escala del dibujo del jugador
const player = `
<g clip-path="url(#wsclip)">
  <rect x="${wsMinX-5}" y="${wsMinY-5}" width="${wsMaxX-wsMinX+10}" height="${wh+10}" fill="url(#cabin)"/>
  <g transform="translate(${wcx-6*s} ${wsMinY+30*s}) scale(${s})">
    <!-- luz trasera que entra por la ventana lateral -->
    <ellipse cx="30" cy="40" rx="70" ry="60" fill="url(#cabglow)"/>
    <!-- torso / camiseta -->
    <path d="M-52 150 L-48 92 Q-40 70 -14 64 L14 64 Q40 70 48 92 L52 150 Z" fill="url(#jersey)"/>
    <g opacity="0.92">
      <path d="M-30 150 L-28 70 L-16 66 L-16 150 Z" fill="#a3161a"/>
      <path d="M-4 150 L-4 64 L8 64 L8 150 Z" fill="#a3161a"/>
      <path d="M20 150 L20 66 L32 70 L32 150 Z" fill="#a3161a"/>
    </g>
    <path d="M-52 150 L-48 92 Q-40 70 -14 64 L14 64 Q40 70 48 92 L52 150 Z" fill="url(#torsoShade)"/>
    <!-- cuello en V -->
    <path d="M-12 64 L0 82 L12 64" fill="none" stroke="#1d1d1d" stroke-width="4"/>
    <!-- brazalete -->
    <path d="M-50 100 L-36 96 L-35 108 L-50 112 Z" fill="#f2c500"/>
    <!-- cuello -->
    <path d="M-9 50 L9 50 L11 66 L0 74 L-11 66 Z" fill="#7a4a2e"/>
    <!-- cabeza -->
    <ellipse cx="0" cy="30" rx="21" ry="26" fill="url(#skin)"/>
    <ellipse cx="-21" cy="32" rx="4" ry="7" fill="#8a5636"/>
    <ellipse cx="21" cy="32" rx="4" ry="7" fill="#b07148"/>
    <!-- pelo -->
    <path d="M-22 26 Q-25 2 0 0 Q25 2 22 26 Q20 12 8 12 Q-6 8 -22 26 Z" fill="#1a110b"/>
    <path d="M-21 18 Q0 8 21 18" stroke="#f4f1ea" stroke-width="4" fill="none"/>
    <!-- rasgos -->
    <path d="M-12 26 L-4 25 M4 25 L12 26" stroke="#2a1a10" stroke-width="2.5" stroke-linecap="round"/>
    <ellipse cx="-8" cy="31" rx="2.6" ry="2" fill="#120b07"/>
    <ellipse cx="8" cy="31" rx="2.6" ry="2" fill="#120b07"/>
    <path d="M0 33 L-2 41 L2 42" stroke="#6e3f24" stroke-width="2" fill="none"/>
    <path d="M-7 47 Q0 50 7 47" stroke="#4e2a18" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <path d="M-17 40 Q0 62 17 40 Q12 52 0 54 Q-12 52 -17 40 Z" fill="#2a1a10" opacity="0.55"/>
    <!-- luz de borde (rim light) en el contorno derecho -->
    <path d="M14 8 Q24 18 21 40 Q18 52 8 56" stroke="#ffcf7a" stroke-width="3" fill="none" opacity="0.9"/>
    <path d="M40 74 Q50 86 52 130" stroke="#ffd08a" stroke-width="4" fill="none" opacity="0.8"/>
    <!-- brazos y volante -->
    <path d="M-44 96 Q-56 120 -30 128" stroke="#e9e6e0" stroke-width="15" fill="none" stroke-linecap="round"/>
    <path d="M44 96 Q56 120 30 128" stroke="#d8d3cb" stroke-width="15" fill="none" stroke-linecap="round"/>
    <ellipse cx="0" cy="134" rx="46" ry="12" fill="none" stroke="#151515" stroke-width="7"/>
    <ellipse cx="-30" cy="128" rx="7" ry="6" fill="#7a4a2e"/>
    <ellipse cx="30" cy="128" rx="7" ry="6" fill="#8d5737"/>
  </g>
  <!-- tablero -->
  <rect x="${wsMinX-5}" y="${wsMaxY-14*s}" width="${wsMaxX-wsMinX+10}" height="${20*s}" fill="#121110"/>
  <!-- reflejos en el vidrio -->
  <polygon points="${poly2(wsP)}" fill="url(#glassRefl)"/>
  <path d="M${wsMinX} ${wsMinY+wh*0.15} L${wsMinX+wh*0.6} ${wsMinY} L${wsMinX+wh*0.8} ${wsMinY} L${wsMinX} ${wsMinY+wh*0.45} Z" fill="#fff" opacity="0.12"/>
</g>
<polygon points="${poly2(wsP)}" fill="none" stroke="#1a1712" stroke-width="5" stroke-linejoin="round"/>
<line x1="${(wsP[0][0]+wsP[1][0])/2}" y1="${(wsP[0][1]+wsP[1][1])/2}" x2="${(wsP[2][0]+wsP[3][0])/2}" y2="${(wsP[2][1]+wsP[3][1])/2}" stroke="#1a1712" stroke-width="0"/>`;

const sideWinP = sideWin.map(P);

// balón en primer plano (desenfocado)
const ballC = [330, 868];
const ballR = 58;

// luces de faros
const lightSvg = lights.map(l => { const q = P(l); const r = F*0.17/q[2]; return `<circle cx="${q[0].toFixed(1)}" cy="${q[1].toFixed(1)}" r="${r.toFixed(1)}" fill="#fffbe8"/>`; }).join('');
const lightGlow = lights.map(l => { const q = P(l); const r = F*1.3/q[2]; return `<circle cx="${q[0].toFixed(1)}" cy="${q[1].toFixed(1)}" r="${r.toFixed(1)}" fill="url(#lampGlow)"/>`; }).join('');

// borde iluminado (rim light) a lo largo de siluetas superiores
const rim = [
  line3([4.1,8.02,4.95],[15.0,7.36,4.95],'#ffdf9a',3.5),
  line3([15.0,7.36,4.95],[15.3,4.9,4.95],'#ffcf7a',4),
  line3([0.1,8.07,4.9],[4.2,8.07,4.9],'#ffdf9a',3),
  line3([0.9,7.52,4.1],[3.7,7.52,4.1],'#ffd890',2.5),
  line3([3.7,7.5,4.1],[3.7,4.95,4.1],'#ffc870',3),
].join('');

const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
  ${defs.join('\n  ')}
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#2b4c62"/>
    <stop offset="0.2" stop-color="#6f8086"/>
    <stop offset="0.4" stop-color="#d4955c"/>
    <stop offset="0.55" stop-color="#ffcf8a"/>
    <stop offset="1" stop-color="#ffd59a"/>
  </linearGradient>
  <radialGradient id="sunGlow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#fffbe8" stop-opacity="1"/>
    <stop offset="0.08" stop-color="#fff0c0" stop-opacity="1"/>
    <stop offset="0.25" stop-color="#ffc56b" stop-opacity="0.55"/>
    <stop offset="0.6" stop-color="#ff9a3c" stop-opacity="0.18"/>
    <stop offset="1" stop-color="#ff8a30" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="lampGlow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#fff7d6" stop-opacity="0.95"/>
    <stop offset="0.2" stop-color="#ffe7a8" stop-opacity="0.35"/>
    <stop offset="1" stop-color="#ffd27a" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#b98652"/>
    <stop offset="0.25" stop-color="#8e6239"/>
    <stop offset="1" stop-color="#3e2a1b"/>
  </linearGradient>
  <radialGradient id="sidewall" cx="0.45" cy="0.45" r="0.6">
    <stop offset="0.5" stop-color="#262321"/>
    <stop offset="1" stop-color="#0d0c0b"/>
  </radialGradient>
  <radialGradient id="rim" cx="0.6" cy="0.35" r="0.7">
    <stop offset="0" stop-color="#d9a12a"/>
    <stop offset="1" stop-color="#6b4807"/>
  </radialGradient>
  <linearGradient id="mud" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0.35" stop-color="#6b4a2c" stop-opacity="0"/>
    <stop offset="1" stop-color="#6b4a2c" stop-opacity="0.9"/>
  </linearGradient>
  <linearGradient id="ore" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#8a6a52"/>
    <stop offset="1" stop-color="#3b2c22"/>
  </linearGradient>
  <linearGradient id="cabin" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#14161a"/>
    <stop offset="1" stop-color="#3a3026"/>
  </linearGradient>
  <radialGradient id="cabglow" cx="0.7" cy="0.4" r="0.6">
    <stop offset="0" stop-color="#ffb35c" stop-opacity="0.55"/>
    <stop offset="1" stop-color="#ffb35c" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="jersey" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#cfcac2"/>
    <stop offset="1" stop-color="#f3eee6"/>
  </linearGradient>
  <linearGradient id="torsoShade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#000" stop-opacity="0.45"/>
    <stop offset="0.6" stop-color="#000" stop-opacity="0.1"/>
    <stop offset="1" stop-color="#000" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="skin" cx="0.65" cy="0.4" r="0.7">
    <stop offset="0" stop-color="#b47a50"/>
    <stop offset="1" stop-color="#6e4129"/>
  </radialGradient>
  <linearGradient id="glassRefl" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#9fc4d8" stop-opacity="0.35"/>
    <stop offset="0.5" stop-color="#9fc4d8" stop-opacity="0.05"/>
    <stop offset="1" stop-color="#ffb46a" stop-opacity="0.18"/>
  </linearGradient>
  <radialGradient id="vignette" cx="0.5" cy="0.5" r="0.75">
    <stop offset="0.5" stop-color="#000" stop-opacity="0"/>
    <stop offset="1" stop-color="#000" stop-opacity="0.6"/>
  </radialGradient>
  <radialGradient id="dustMask" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#fff" stop-opacity="1"/>
    <stop offset="0.6" stop-color="#fff" stop-opacity="0.6"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="gradeWarm" x1="1" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ff9a3a"/>
    <stop offset="1" stop-color="#1c4a5c"/>
  </linearGradient>
  <radialGradient id="ballShade" cx="0.7" cy="0.3" r="0.8">
    <stop offset="0" stop-color="#f4efe6"/>
    <stop offset="0.6" stop-color="#9b958c"/>
    <stop offset="1" stop-color="#3b3631"/>
  </radialGradient>
  <linearGradient id="sideGlass" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#2a2a2c"/><stop offset="0.55" stop-color="#5b4a3a"/><stop offset="1" stop-color="#ffb764"/>
  </linearGradient>
  <clipPath id="wsclip"><polygon points="${poly2(wsP)}"/></clipPath>
  <clipPath id="frame"><rect x="0" y="${BAR}" width="${W}" height="${H-2*BAR}"/></clipPath>

  <filter id="dust" x="-20%" y="-20%" width="140%" height="140%">
    <feTurbulence type="fractalNoise" baseFrequency="0.0045 0.009" numOctaves="5" seed="7" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.93  0 0 0 0 0.68  0 0 0 0 0.42  0 0 0 2.2 -0.85" result="c"/>
    <feComposite in="c" in2="SourceGraphic" operator="in"/>
    <feGaussianBlur stdDeviation="3"/>
  </filter>
  <filter id="dustFine" x="-20%" y="-20%" width="140%" height="140%">
    <feTurbulence type="fractalNoise" baseFrequency="0.012 0.02" numOctaves="4" seed="21" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 0.78  0 0 0 0 0.5  0 0 0 2.6 -1.1" result="c"/>
    <feComposite in="c" in2="SourceGraphic" operator="in"/>
    <feGaussianBlur stdDeviation="1.5"/>
  </filter>
  <filter id="dirt" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="3" seed="4" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.35  0 0 0 0 0.24  0 0 0 0 0.14  0 0 0 1.6 -0.55" result="c"/>
    <feComposite in="c" in2="SourceGraphic" operator="in" result="d"/>
    <feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="d"/></feMerge>
  </filter>
  <filter id="groundTex" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.004 0.03" numOctaves="5" seed="11" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.2  0 0 0 0 0.13  0 0 0 0 0.07  0 0 0 1.5 -0.4" result="c"/>
    <feComposite in="c" in2="SourceGraphic" operator="in"/>
  </filter>
  <filter id="bgBlur"><feGaussianBlur stdDeviation="3.5"/></filter>
  <filter id="fgBlur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7"/></filter>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="22"/></filter>
  <filter id="soft2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
  <filter id="rimGlow" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="5" stitchTiles="stitch"/>
    <feColorMatrix type="saturate" values="0"/>
  </filter>
</defs>

<rect width="${W}" height="${H}" fill="#000"/>
<g clip-path="url(#frame)">
  <!-- cielo -->
  <rect width="${W}" height="${H}" fill="url(#sky)"/>
  <circle cx="${sunXY[0]}" cy="${sunXY[1]}" r="520" fill="url(#sunGlow)"/>

  <!-- paredes del rajo, lejanas y desenfocadas -->
  <g filter="url(#bgBlur)">
    <path d="M0 470 L180 450 L340 470 L520 440 L700 462 L880 430 L1080 455 L1300 425 L1500 450 L1700 432 L1920 448 L1920 700 L0 700 Z" fill="#a8774f" opacity="0.75"/>
    <path d="M0 520 L1920 500 L1920 700 L0 700 Z" fill="#96673f" opacity="0.85"/>
    <path d="M0 565 L1920 548 L1920 700 L0 700 Z" fill="#87582f" opacity="0.9"/>
    <g stroke="#c99a6a" stroke-width="3" opacity="0.6">
      <line x1="0" y1="520" x2="1920" y2="500"/><line x1="0" y1="565" x2="1920" y2="548"/>
    </g>
    <!-- camión lejano -->
    <g transform="translate(330 520) scale(0.22)" fill="#2c2018">
      <rect x="0" y="0" width="200" height="70"/><rect x="-60" y="30" width="70" height="50"/>
      <circle cx="20" cy="95" r="30"/><circle cx="170" cy="95" r="30"/>
    </g>
  </g>
  <!-- bruma atmosférica -->
  <rect x="0" y="420" width="${W}" height="220" fill="#f6c084" opacity="0.5" filter="url(#soft)"/>

  <!-- suelo -->
  <path d="M0 600 L${W} 585 L${W} ${H} L0 ${H} Z" fill="url(#ground)"/>
  <path d="M0 600 L${W} 585 L${W} ${H} L0 ${H} Z" fill="#000" filter="url(#groundTex)" opacity="0.9"/>
  <!-- huellas de neumáticos -->
  <g stroke="#2f2015" stroke-width="10" opacity="0.35" fill="none">
    <path d="M-200 1000 Q500 760 1500 610"/><path d="M80 1080 Q700 780 1650 612"/>
    <path d="M-300 900 Q300 720 1200 615"/>
  </g>
  <!-- sombra del camión -->
  <polygon points="${poly2(shadowPts)}" fill="#120a05" opacity="0.6" filter="url(#soft2)"/>

  <!-- polvo detrás del camión (contraluz) -->
  <ellipse cx="1650" cy="560" rx="520" ry="230" fill="url(#dustMask)" filter="url(#dust)" opacity="0.95"/>

  <!-- CAMIÓN -->
  <g>${truck}</g>
  ${decal}
  <polygon points="${poly2(sideWinP)}" fill="url(#sideGlass)" stroke="#1a1712" stroke-width="4"/>
  ${player}
  <g filter="url(#rimGlow)">${rim}</g>
  ${lightGlow}
  ${lightSvg}

  <!-- polvo levantado por las ruedas -->
  <ellipse cx="1430" cy="770" rx="420" ry="130" fill="url(#dustMask)" filter="url(#dust)" opacity="0.85"/>
  <ellipse cx="700" cy="880" rx="520" ry="120" fill="url(#dustMask)" filter="url(#dustFine)" opacity="0.55"/>

  <!-- rayos de sol -->
  <g opacity="0.22" filter="url(#soft)" style="mix-blend-mode:screen">
    <polygon points="${sunXY[0]},${sunXY[1]} 900,950 1150,950" fill="#ffd79a"/>
    <polygon points="${sunXY[0]},${sunXY[1]} 1400,950 1560,950" fill="#ffd79a"/>
    <polygon points="${sunXY[0]},${sunXY[1]} 1850,950 1920,860" fill="#ffd79a"/>
  </g>

  <!-- balón en primer plano, desenfocado -->
  <g filter="url(#fgBlur)">
    <ellipse cx="${ballC[0]+ballR*0.2}" cy="${ballC[1]+ballR*0.95}" rx="${ballR*1.3}" ry="${ballR*0.25}" fill="#000" opacity="0.5"/>
    <circle cx="${ballC[0]}" cy="${ballC[1]}" r="${ballR}" fill="url(#ballShade)"/>
    <g transform="translate(${ballC[0]} ${ballC[1]}) scale(${ballR/38})" fill="#16130f" opacity="0.85">
      <polygon points="2,-10 13,-2 9,12 -5,12 -9,-2"/>
      <polygon points="-34,-14 -26,-24 -18,-12 -24,0"/>
      <polygon points="30,-20 36,-6 26,0 22,-12"/>
      <polygon points="18,28 26,20 32,26 24,34"/>
      <polygon points="-22,24 -10,30 -14,36 -24,32"/>
    </g>
    <path d="M${ballC[0]+ballR*0.3} ${ballC[1]-ballR*0.95} A${ballR} ${ballR} 0 0 1 ${ballC[0]+ballR*0.98} ${ballC[1]+ballR*0.1}" stroke="#ffd59a" stroke-width="${ballR*0.12}" fill="none"/>
  </g>

  <!-- bloom del sol por encima de todo -->
  <circle cx="${sunXY[0]}" cy="${sunXY[1]}" r="160" fill="url(#sunGlow)" style="mix-blend-mode:screen" opacity="0.9"/>
  <!-- destellos de lente -->
  <g style="mix-blend-mode:screen" opacity="0.5">
    <circle cx="${sunXY[0] - 420}" cy="${sunXY[1] + 190}" r="38" fill="#ffb060" opacity="0.35" filter="url(#soft2)"/>
    <circle cx="${sunXY[0] - 760}" cy="${sunXY[1] + 340}" r="18" fill="#9fd0ff" opacity="0.5" filter="url(#soft2)"/>
    <circle cx="${sunXY[0] - 1040}" cy="${sunXY[1] + 465}" r="62" fill="#ff9a50" opacity="0.18" filter="url(#soft2)"/>
    <rect x="0" y="${sunXY[1]-2}" width="${W}" height="4" fill="#ffd9a0" opacity="0.35" filter="url(#soft2)"/>
  </g>

  <!-- etalonaje (teal & orange) -->
  <rect width="${W}" height="${H}" fill="url(#gradeWarm)" opacity="0.28" style="mix-blend-mode:soft-light"/>
  <rect width="${W}" height="${H}" fill="#1b3644" opacity="0.07" style="mix-blend-mode:multiply"/>
  <rect width="${W}" height="${H}" fill="url(#vignette)"/>
  <!-- grano de película -->
  <rect width="${W}" height="${H}" filter="url(#grain)" opacity="0.13" style="mix-blend-mode:overlay"/>
</g>
</svg>`;
fs.writeFileSync(OUT, svg);
console.log('windshield', wsMinX|0, wsMinY|0, wsMaxX|0, wsMaxY|0, 'ball', ballC.map(v=>v|0), ballR|0);
