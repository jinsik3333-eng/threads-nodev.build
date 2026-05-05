const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const outdir = __dirname + '/output';
fs.mkdirSync(outdir, { recursive: true });

const slides = [
  {
    kicker: 'CLAUDE CODE STARTER',
    title: ['비개발자가', 'Claude Code를', '처음 켤 때'],
    accent: '처음 켤 때',
    body: '코딩 공부보다 먼저 필요한 건\n“내 일을 어떻게 맡길지” 감을 잡는 것입니다.',
    tag: '1~3편만 먼저 보면 됩니다'
  },
  {
    kicker: 'WHY PEOPLE STOP',
    title: ['막히는 지점은', '코딩이 아니라', '첫 화면입니다'],
    accent: '첫 화면입니다',
    body: '터미널, 폴더, 설치 화면.\n처음엔 이게 맞는지 아닌지부터 불안합니다.',
    tag: '그래서 화면 감각부터'
  },
  {
    kicker: 'STEP 01',
    title: ['1편', '화면 감각', '익히기'],
    accent: '화면 감각',
    body: 'Claude Code를 쓰기 전,\n계정·화면·폴더 구조를 먼저 익힙니다.',
    tag: '처음 보는 화면이 덜 무서워짐'
  },
  {
    kicker: 'STEP 02',
    title: ['2편', '설치에서', '막히지 않기'],
    accent: '설치에서',
    body: '명령어를 외우는 게 아니라,\n“성공 화면”과 “오류 화면” 기준으로 따라갑니다.',
    tag: '터미널이 처음이어도 가능'
  },
  {
    kicker: 'STEP 03',
    title: ['3편', '첫 프로젝트', '만들기'],
    accent: '첫 프로젝트',
    body: '거창한 앱이 아니어도 됩니다.\n회의록 정리, 파일 정리, 콘텐츠 초안부터 시작합니다.',
    tag: '내 폴더에서 결과물 하나 만들기'
  },
  {
    kicker: 'GET THE GUIDE',
    title: ['댓글에', '“시작”', '남겨주세요'],
    accent: '“시작”',
    body: '비개발자용 Claude Code 1~3편 링크를\nDM으로 보내드릴게요.',
    tag: '@nodev.builder'
  }
];

const esc = (s='') => String(s).replace(/[&<>\"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const bodyHtml = (text) => esc(text).split('\n').join('<br>');

function slideHtml(s, idx) {
  const title = s.title.map(line => {
    const cls = line === s.accent ? 'accent' : '';
    return `<span class="${cls}">${esc(line)}</span>`;
  }).join('');

  const isLast = idx === slides.length;
  return `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Pret;src:url('file:///Users/jinsik/Library/Fonts/Pretendard-Regular.otf');font-weight:400}
@font-face{font-family:Pret;src:url('file:///Users/jinsik/Library/Fonts/Pretendard-Medium.otf');font-weight:500}
@font-face{font-family:Pret;src:url('file:///Users/jinsik/Library/Fonts/Pretendard-SemiBold.otf');font-weight:650}
@font-face{font-family:Pret;src:url('file:///Users/jinsik/Library/Fonts/Pretendard-Bold.otf');font-weight:700}
*{box-sizing:border-box} html,body{margin:0;background:#e9dfd2}.card{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Pret,-apple-system,BlinkMacSystemFont,sans-serif;color:#1d1712;background:${isLast ? '#17120f' : '#f1e7d9'};} 
.card:before{content:"";position:absolute;inset:-120px;background:${isLast ? 'radial-gradient(circle at 72% 16%,rgba(219,255,102,.16),transparent 26%),radial-gradient(circle at 18% 86%,rgba(176,220,255,.12),transparent 30%)' : 'radial-gradient(circle at 78% 15%,#d6eef2 0,#f1e7d9 30%,transparent 52%),radial-gradient(circle at 5% 90%,#e0cdb7 0,transparent 38%)'};}
.noise{position:absolute;inset:0;opacity:.055;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.7' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='180' height='180' filter='url(%23n)' opacity='.55'/%3E%3C/svg%3E")}
.brand{position:absolute;top:58px;left:50%;transform:translateX(-50%);font-size:23px;font-weight:650;letter-spacing:.16em;color:${isLast ? 'rgba(255,255,255,.78)' : 'rgba(29,23,18,.55)'};white-space:nowrap}.page{position:absolute;top:60px;right:58px;font-size:23px;font-weight:650;color:${isLast ? 'rgba(255,255,255,.46)' : 'rgba(29,23,18,.38)'};letter-spacing:.04em}.kicker{position:absolute;left:64px;top:166px;font-size:23px;font-weight:650;letter-spacing:.14em;color:${isLast ? 'rgba(219,255,102,.72)' : 'rgba(124,91,54,.68)'};}
.title{position:absolute;left:58px;right:58px;top:245px;font-weight:700;letter-spacing:-.072em;line-height:.98;font-size:${isLast ? '104px' : '96px'};color:${isLast ? '#fffaf2' : '#201812'};word-break:keep-all}.title span{display:block}.title .accent{color:${isLast ? '#d9ff66' : '#7b5b35'}}
.body{position:absolute;left:66px;right:90px;top:${isLast ? '590px' : '600px'};font-size:38px;font-weight:500;letter-spacing:-.055em;line-height:1.32;color:${isLast ? 'rgba(255,250,242,.72)' : 'rgba(32,24,18,.62)'};word-break:keep-all}.panel{position:absolute;left:64px;right:64px;bottom:116px;height:${isLast ? '310px' : '330px'};border-radius:36px;background:${isLast ? 'rgba(255,255,255,.08)' : 'rgba(255,255,255,.52)'};border:1px solid ${isLast ? 'rgba(255,255,255,.15)' : 'rgba(32,24,18,.10)'};box-shadow:0 28px 90px rgba(80,54,30,.14);padding:36px 40px;}
.tag{display:inline-flex;border-radius:999px;padding:18px 26px;background:${isLast ? '#d9ff66' : '#211914'};color:${isLast ? '#17120f' : '#fffaf2'};font-size:28px;font-weight:700;letter-spacing:-.03em}.small{position:absolute;left:40px;right:40px;bottom:38px;font-size:29px;font-weight:500;line-height:1.34;letter-spacing:-.045em;color:${isLast ? 'rgba(255,255,255,.62)' : 'rgba(32,24,18,.58)'};word-break:keep-all}.line{position:absolute;left:40px;right:40px;top:112px;height:1px;background:${isLast ? 'rgba(255,255,255,.14)' : 'rgba(32,24,18,.10)'}}
.indexbig{position:absolute;right:60px;bottom:74px;font-family:Arial,sans-serif;font-weight:900;font-size:168px;line-height:.8;letter-spacing:-.1em;color:${isLast ? 'rgba(255,255,255,.045)' : 'rgba(32,24,18,.045)'}}
</style></head><body><div class="card"><div class="noise"></div><div class="brand">NODEV BUILDER</div><div class="page">${String(idx).padStart(2,'0')} / ${String(slides.length).padStart(2,'0')}</div><div class="kicker">${esc(s.kicker)}</div><div class="title">${title}</div><div class="body">${bodyHtml(s.body)}</div><div class="panel"><div class="tag">${esc(s.tag)}</div><div class="line"></div><div class="small">${isLast ? '처음부터 9편을 다 보지 말고, 1~3편만 먼저 따라오면 됩니다.' : '비개발자 기준으로 필요한 순서만 추렸습니다. 저장해두고 천천히 따라오세요.'}</div></div><div class="indexbig">${String(idx).padStart(2,'0')}</div></div></body></html>`;
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  for (let i=0; i<slides.length; i++) {
    const htmlPath = path.join(outdir, `card-${String(i+1).padStart(2,'0')}.html`);
    fs.writeFileSync(htmlPath, slideHtml(slides[i], i+1));
    await page.goto('file://' + htmlPath, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(outdir, `card-${String(i+1).padStart(2,'0')}.png`), fullPage: false });
  }
  const sheetHtml = `<!doctype html><html><head><meta charset="utf-8"><style>*{box-sizing:border-box}body{margin:0;background:#ded4c8}.sheet{width:2160px;height:4050px;padding:44px;display:grid;grid-template-columns:repeat(2,1fr);gap:36px}.slot{position:relative;border-radius:24px;overflow:hidden;box-shadow:0 22px 60px rgba(0,0,0,.18);background:#111}.slot img{width:100%;height:100%;object-fit:cover}.lab{position:absolute;left:20px;top:20px;background:rgba(255,255,255,.92);border-radius:999px;padding:8px 13px;font:800 18px Arial;color:#111}</style></head><body><div class="sheet">${slides.map((_,i)=>`<div class="slot"><img src="file://${outdir}/card-${String(i+1).padStart(2,'0')}.png"><div class="lab">${String(i+1).padStart(2,'0')}</div></div>`).join('')}</div></body></html>`;
  const sheetPath = path.join(outdir, 'contact-sheet.html');
  fs.writeFileSync(sheetPath, sheetHtml);
  const sheet = await browser.newPage({ viewport: { width:2160, height:4050 }, deviceScaleFactor:1 });
  await sheet.goto('file://' + sheetPath, { waitUntil:'networkidle' });
  await sheet.screenshot({ path: path.join(outdir, 'contact-sheet.png'), fullPage:false });
  await browser.close();
  console.log(outdir);
})();
