const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');

const projectRoot = '/Users/jinsik/Desktop/Workspace/01_project_threads';
const fontDir = '/Users/jinsik/Library/Fonts';
const scriptPath = process.argv[2]
  ? path.resolve(process.cwd(), process.argv[2])
  : path.join(projectRoot, 'app/cards/episodes/20260502_card_script_pipeline_sample/card_script.json');

if (!fs.existsSync(scriptPath)) {
  console.error(`Missing card_script: ${scriptPath}`);
  process.exit(1);
}

const validator = path.join(projectRoot, 'app/cards/templates/validate-card-script.mjs');
execFileSync('node', [validator, scriptPath], { stdio: 'inherit', cwd: projectRoot });

const cardScript = JSON.parse(fs.readFileSync(scriptPath, 'utf8'));
const episodeDir = path.dirname(scriptPath);
const outdir = path.join(episodeDir, 'output');
fs.mkdirSync(outdir, { recursive: true });

const assets = {
  cover: 'file:///Users/jinsik/.hermes/cache/images/openai_codex_gpt-image-2-high_20260501_190324_36fe5098.png',
  mood: 'file:///Users/jinsik/.hermes/cache/images/openai_codex_gpt-image-2-high_20260501_221725_b2a88e60.png',
  desk: 'file:///Users/jinsik/.hermes/cache/images/openai_codex_gpt-image-2-high_20260501_221857_2d6746b7.png'
};

const esc = (value = '') => String(value)
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;');

const lineBreaks = (lines = []) => lines.map(esc).join('<br>');
const brand = esc(cardScript.brand?.account_name || 'NODEV BUILDER');
const minPx = Math.max(22, Number(cardScript.font_policy?.min_readable_px || 22));

const css = `
@font-face{font-family:SUITLocal;font-weight:800;src:url('file://${fontDir}/SUIT-ExtraBold.otf')}
@font-face{font-family:SUITLocal;font-weight:600;src:url('file://${fontDir}/SUIT-SemiBold.otf')}
@font-face{font-family:IBMPlexKRLocal;font-weight:700;src:url('file://${fontDir}/IBMPlexSansKR-Bold.otf')}
@font-face{font-family:IBMPlexKRLocal;font-weight:500;src:url('file://${fontDir}/IBMPlexSansKR-Regular.otf')}
*{box-sizing:border-box}html,body{margin:0;background:#111}.card{position:relative;width:1080px;height:1350px;overflow:hidden;background:#111;color:#fff;font-family:SUITLocal,-apple-system,BlinkMacSystemFont,sans-serif}.bg{position:absolute;inset:0;background-size:cover;background-position:center}.shade{position:absolute;inset:0}.brand{position:absolute;top:58px;left:50%;transform:translateX(-50%);z-index:20;font:700 22px IBMPlexKRLocal,Arial;letter-spacing:.18em;color:rgba(255,255,255,.92);white-space:nowrap}.brand.dark{color:#17120e}.page{position:absolute;top:60px;right:58px;z-index:20;font:700 22px IBMPlexKRLocal,Arial;letter-spacing:.04em;color:rgba(255,255,255,.72)}.page.dark{color:rgba(0,0,0,.46)}.title{font-family:SUITLocal,Arial,sans-serif;font-weight:800;letter-spacing:-.078em;line-height:.93;word-break:keep-all}.accent{color:#D9FF56}.serif{font-family:Georgia,'Times New Roman',serif;font-style:italic;font-weight:500;letter-spacing:-.06em}.mono{font-family:Menlo,Consolas,'SF Mono',monospace;letter-spacing:-.035em}.pill{position:absolute;border-radius:999px;padding:15px 25px 14px;background:#fff;color:#111;font:700 ${minPx}px IBMPlexKRLocal,Arial;letter-spacing:.025em}.glass{background:rgba(255,255,255,.22);border:1px solid rgba(255,255,255,.38);backdrop-filter:blur(18px);box-shadow:0 18px 60px rgba(0,0,0,.16)}.cream{background:#f3e7d8;color:#15110d}.support{font:600 31px/1.24 SUITLocal;letter-spacing:-.055em;color:rgba(0,0,0,.62);word-break:keep-all}.window{position:absolute;border-radius:34px;overflow:hidden;background:rgba(255,255,255,.88);border:1px solid rgba(0,0,0,.10);box-shadow:0 28px 90px rgba(80,54,30,.18);color:#15110d}.bar{height:62px;display:flex;align-items:center;padding:0 24px;font:700 22px IBMPlexKRLocal;color:rgba(0,0,0,.45);border-bottom:1px solid rgba(0,0,0,.10)}.dot{display:inline-block;width:13px;height:13px;border-radius:50%;background:rgba(0,0,0,.20);margin-right:8px}.ui-card{background:rgba(255,255,255,.88);border:1px solid rgba(0,0,0,.09);border-radius:28px;padding:28px 30px;box-shadow:0 18px 60px rgba(80,54,30,.13);color:#15110d}.mini-label{font:700 ${minPx}px IBMPlexKRLocal;letter-spacing:.12em;color:rgba(0,0,0,.46);text-transform:uppercase}.mini-title{margin-top:12px;font:800 42px/.96 SUITLocal;letter-spacing:-.065em;color:#15110d}.mini-copy{margin-top:14px;font:600 25px/1.22 SUITLocal;letter-spacing:-.052em;color:rgba(0,0,0,.58);word-break:keep-all}.asset{position:absolute;background:rgba(255,255,255,.88);border:1px solid rgba(0,0,0,.09);border-radius:28px;padding:26px 28px;box-shadow:0 20px 70px rgba(0,0,0,.14);color:#15110d}.frame-card{background:#fff;border:1px solid rgba(0,0,0,.10);border-radius:24px;padding:22px;color:#15110d}.frame-num{font:800 22px IBMPlexKRLocal;letter-spacing:.1em;color:#8aa114}.frame-title{margin-top:12px;font:800 31px/.98 SUITLocal;letter-spacing:-.06em}.frame-copy{margin-top:10px;font:600 22px/1.24 SUITLocal;letter-spacing:-.04em;color:rgba(0,0,0,.56)}
`;

const html = (body) => `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${body}</body></html>`;
const brandNode = (dark = false) => `<div class="brand${dark ? ' dark' : ''}">${brand}</div>`;
const pageNode = (i, dark = false) => `<div class="page${dark ? ' dark' : ''}">${String(i).padStart(2, '0')} / ${String(cardScript.slides.length).padStart(2, '0')}</div>`;

function renderSlide(slide, index) {
  switch (slide.template_id) {
    case 'T01_CAMPAIGN_HERO': return renderT01(slide, index);
    case 'T11_FULL_IMAGE_BREAKER': return renderT11(slide, index);
    case 'T03_SKILL_OUTPUT_MOCKUP': return renderT03(slide, index);
    case 'T07_ASSET_LIBRARY': return renderT07(slide, index);
    case 'T06_STORYBOARD_PREVIEW': return renderT06(slide, index);
    case 'T08_FINAL_COMMENT_CTA': return renderT08(slide, index);
    default:
      throw new Error(`Unsupported template_id in renderer v1: ${slide.template_id}`);
  }
}

function renderT01(slide, index) {
  const first = esc(slide.headline?.[0] || '콘텐츠 30일치').replace('30일치', '<span class="accent">30일치</span>');
  const second = esc(slide.headline?.[1] || 'Claude가 짜줌').replace('Claude', '<span style="font-family:Arial;font-weight:900;letter-spacing:-.08em">Claude</span>');
  return html(`<div class="card">
    <div class="bg" style="background-image:url('${assets.cover}')"></div>
    <div class="shade" style="background:linear-gradient(180deg,rgba(0,0,0,.02),rgba(0,0,0,.02) 38%,rgba(0,0,0,.70))"></div>
    ${brandNode(false)}
    <div class="glass" style="position:absolute;right:36px;top:126px;width:350px;border-radius:24px;padding:22px 24px">
      <b style="font:700 22px IBMPlexKRLocal;letter-spacing:.10em;color:rgba(255,255,255,.88)">CLAUDE PROMPT</b>
      <p class="mono" style="margin:10px 0 0;font-size:${minPx}px;line-height:1.28;color:rgba(255,255,255,.92)">1 idea → 30 days<br>hooks · slides · captions</p>
    </div>
    <div class="title" style="position:absolute;left:58px;right:58px;bottom:160px;font-size:100px;text-shadow:0 12px 42px rgba(0,0,0,.32)"><span style="display:block">${first}</span><span style="display:block">${second}</span></div>
    <div class="pill" style="right:58px;bottom:104px">COPY THE PROMPT →</div>
  </div>`);
}

function renderT11(slide, index) {
  return html(`<div class="card">
    <div class="bg" style="background-image:url('${assets.mood}');filter:saturate(1.03)"></div>
    <div class="shade" style="background:linear-gradient(180deg,rgba(0,0,0,.18),rgba(0,0,0,.04) 44%,rgba(0,0,0,.54))"></div>
    ${brandNode(false)}${pageNode(index, false)}
    <div class="title" style="position:absolute;left:58px;right:58px;bottom:258px;font-size:94px;text-shadow:0 14px 46px rgba(0,0,0,.36)">${lineBreaks(slide.headline)}</div>
    <div style="position:absolute;left:64px;right:120px;bottom:164px;font:600 32px/1.24 SUITLocal;letter-spacing:-.055em;color:rgba(255,255,255,.84);word-break:keep-all">Claude에게 바로 묻기 전에, 콘텐츠의 방향과 기준을 먼저 고정한다.</div>
    <div class="pill" style="left:64px;bottom:80px">MOOD → DIRECTION</div>
  </div>`);
}

function renderT03(slide, index) {
  return html(`<div class="card cream">
    <div style="position:absolute;inset:0;background:linear-gradient(180deg,#f5eadc 0%,#f2e3d2 47%,#15110d 47%,#15110d 100%)"></div>
    ${brandNode(true)}${pageNode(index, true)}
    <div class="title" style="position:absolute;left:58px;top:142px;font-size:88px;color:#15110d;width:920px">${lineBreaks(slide.headline)}</div>
    <div class="support" style="position:absolute;left:64px;top:340px;width:760px">${esc(slide.support_copy)}</div>
    <div class="window" style="left:64px;right:64px;top:488px;height:294px;background:#fff">
      <div class="bar"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span style="margin-left:14px">claude.ai / setup</span></div>
      <div class="mono" style="padding:30px 34px;font-size:29px;line-height:1.35;color:rgba(0,0,0,.74)"><span style="color:#7c9b18">/campaign-builder</span><br>목표 · 타깃 · 톤 · 금지사항을 먼저 고정</div>
    </div>
    <div style="position:absolute;left:64px;right:64px;bottom:158px;display:grid;grid-template-columns:1fr 1fr;gap:22px;align-items:start">
      <div class="ui-card" style="height:258px;padding:28px 32px"><div class="mini-label">BRAND CONTEXT</div><div class="mini-title">타깃 설정</div><div class="mini-copy">누구에게, 어떤 상황에서 말할지 입력</div></div>
      <div class="ui-card" style="height:258px;padding:28px 32px"><div class="mini-label">OUTPUT FORMAT</div><div class="mini-title">출력 형식</div><div class="mini-copy">훅 · 슬라이드 · 캡션 · CTA까지 지정</div></div>
    </div>
  </div>`);
}

function renderT07(slide, index) {
  const items = [
    ['01 HOOKS', '10 angles', 'pain · desire · twist'],
    ['02 CAROUSEL', '6 frames', 'Cover → Save'],
    ['03 CAPTION', '3 tones', 'short · deep · light'],
    ['04 CALENDAR', '30 days', 'feed · reels · story']
  ];
  return html(`<div class="card cream">
    <div style="position:absolute;inset:0;background:radial-gradient(circle at 78% 20%,#d7f7ff 0,#f4eadb 30%,#ead8c3 100%)"></div>
    ${brandNode(true)}${pageNode(index, true)}
    <div class="title" style="position:absolute;left:58px;top:146px;font-size:92px;color:#15110d">${lineBreaks(slide.headline)}</div>
    <div class="support" style="position:absolute;left:64px;top:392px;width:760px">훅, 캡션, 비주얼, 캘린더가 한 세트로 나와야 바로 쓸 수 있다.</div>
    <div style="position:absolute;left:64px;right:64px;top:526px;display:grid;grid-template-columns:1fr 1fr;gap:24px">
      ${items.map(([label, title, copy]) => `<div class="ui-card" style="height:250px"><div class="mini-label">${label}</div><div class="mini-title" style="font-size:46px">${title}</div><div class="mini-copy">${copy}</div></div>`).join('')}
    </div>
    <div style="position:absolute;right:72px;bottom:100px;font:900 80px/.86 Arial;color:rgba(0,0,0,.105);letter-spacing:-.09em">ASSET<br>LIBRARY</div>
  </div>`);
}

function renderT06(slide, index) {
  const frames = [
    ['01', 'Hook', '결과 약속'],
    ['02', 'Bridge', '문제 연결'],
    ['03', 'Prompt', '조건 입력'],
    ['04', 'Assets', '소재 정리'],
    ['05', 'Flow', '순서 배열'],
    ['06', 'CTA', '댓글 행동']
  ];
  return html(`<div class="card cream">
    <div style="position:absolute;inset:0;background:linear-gradient(135deg,#f6ecdd 0%,#e8d4bd 52%,#d8f4fb 100%)"></div>
    ${brandNode(true)}${pageNode(index, true)}
    <div class="title" style="position:absolute;left:58px;top:142px;font-size:88px;color:#15110d;width:920px">${lineBreaks(slide.headline)}</div>
    <div class="support" style="position:absolute;left:64px;top:342px;width:800px">6단계만 채우면 카드뉴스 초안 완성.</div>
    <div style="position:absolute;right:70px;top:326px;font:900 108px/.82 Arial;color:rgba(0,0,0,.035);letter-spacing:-.09em">STORY<br>BOARD</div>
    <div style="position:absolute;left:64px;right:64px;top:510px;height:652px;border-radius:34px;background:rgba(255,255,255,.72);border:1px solid rgba(0,0,0,.10);box-shadow:0 28px 90px rgba(80,54,30,.16);padding:34px">
      <div class="mini-label">STORYBOARD PREVIEW</div>
      <div style="margin-top:24px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px">
        ${frames.map(([num, title, copy]) => `<div class="frame-card" style="height:238px"><div class="frame-num">${num}</div><div class="frame-title">${title}</div><div class="frame-copy">${copy}</div></div>`).join('')}
      </div>
    </div>
    <div class="pill" style="right:58px;bottom:72px;background:#15110d;color:#fff">6-STEP WORKFLOW →</div>
  </div>`);
}

function renderT08(slide, index) {
  const support = esc(slide.support_copy || '콘텐츠 캘린더 프롬프트 템플릿을 DM으로 보내드릴게요.');
  return html(`<div class="card">
    <div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 18%,rgba(217,255,86,.18),transparent 26%),linear-gradient(135deg,#11100f,#221813 58%,#0c0c0c)"></div>
    ${brandNode(false)}${pageNode(index, false)}
    <div style="position:absolute;left:60px;right:60px;top:150px;text-align:center">
      <div style="font:700 23px IBMPlexKRLocal;letter-spacing:.15em;color:rgba(255,255,255,.56)">FREE TEMPLATE</div>
      <div class="title" style="margin-top:30px;font-size:92px;line-height:.94;text-shadow:0 12px 44px rgba(0,0,0,.28)">댓글에 <span class="accent">“30일치”</span><br>남기면</div>
      <div style="margin:30px auto 0;width:780px;font:600 38px/1.30 SUITLocal;white-space:normal;letter-spacing:-.058em;color:rgba(255,255,255,.76)">콘텐츠 캘린더 프롬프트 템플릿을 DM으로 보내드릴게요.</div>
    </div>
    <div style="position:absolute;left:50%;top:680px;transform:translateX(-50%);border-radius:999px;background:#D9FF56;color:#111;padding:22px 34px;font:800 32px IBMPlexKRLocal;letter-spacing:.01em;box-shadow:0 22px 70px rgba(217,255,86,.16);white-space:nowrap">댓글에 “30일치” 남기기</div>
    <div style="position:absolute;left:118px;right:118px;top:800px;height:172px;border-top:1px solid rgba(255,255,255,.18);border-bottom:1px solid rgba(255,255,255,.18);display:grid;grid-template-columns:1fr 1fr 1fr;align-items:center;text-align:center">
      ${['Prompt', 'Calendar', 'Workflow'].map((x, i) => `<div><div style="font:700 22px IBMPlexKRLocal;letter-spacing:.13em;color:rgba(255,255,255,.42)">0${i + 1}</div><div style="margin-top:10px;font:800 33px SUITLocal;letter-spacing:-.055em;color:white">${x}</div></div>`).join('')}
    </div>
    <div class="glass" style="position:absolute;left:84px;right:84px;bottom:112px;border-radius:999px;padding:24px 32px;display:flex;justify-content:space-between;align-items:center;gap:22px">
      <div style="font:800 31px SUITLocal;letter-spacing:-.055em;color:white;white-space:nowrap">@nodev.builder</div>
      <div style="font:700 24px SUITLocal;letter-spacing:-.035em;color:rgba(255,255,255,.58);white-space:nowrap">AI 워크플로우 더 보려면 팔로우 →</div>
    </div>
  </div>`);
}

(async () => {
  const htmlFiles = [];
  cardScript.slides.forEach((slide, index) => {
    const file = path.join(outdir, `card-${String(index + 1).padStart(2, '0')}.html`);
    fs.writeFileSync(file, renderSlide(slide, index + 1));
    htmlFiles.push(file);
  });

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: cardScript.format.width, height: cardScript.format.height }, deviceScaleFactor: 1 });
  for (let i = 0; i < htmlFiles.length; i += 1) {
    const name = `card-${String(i + 1).padStart(2, '0')}`;
    await page.goto('file://' + htmlFiles[i], { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(outdir, `${name}.png`), fullPage: false });
  }

  const contactCss = `*{box-sizing:border-box}html,body{margin:0;background:#e8dfd2}.sheet{width:2160px;height:4050px;background:#e8dfd2;padding:44px;display:grid;grid-template-columns:repeat(2,1fr);gap:36px}.slot{position:relative;background:#111;border-radius:24px;overflow:hidden;box-shadow:0 22px 60px rgba(0,0,0,.18)}.slot img{width:100%;height:100%;object-fit:cover}.lab{position:absolute;left:20px;top:20px;background:rgba(255,255,255,.92);color:#111;border-radius:999px;padding:8px 13px;font:800 18px Arial}`;
  fs.writeFileSync(path.join(outdir, 'contact-sheet.html'), `<!doctype html><html><head><meta charset="utf-8"><style>${contactCss}</style></head><body><div class="sheet">${cardScript.slides.map((_, i) => `<div class="slot"><img src="file://${outdir}/card-${String(i + 1).padStart(2, '0')}.png"><div class="lab">${String(i + 1).padStart(2, '0')}</div></div>`).join('')}</div></body></html>`);
  const contact = await browser.newPage({ viewport: { width: 2160, height: 4050 }, deviceScaleFactor: 1 });
  await contact.goto('file://' + path.join(outdir, 'contact-sheet.html'), { waitUntil: 'networkidle' });
  await contact.screenshot({ path: path.join(outdir, 'contact-sheet.png'), fullPage: false });
  await browser.close();

  const qaReport = [
    '# QA Report — card_script renderer v1',
    '',
    `- script: ${scriptPath}`,
    `- output: ${outdir}`,
    `- slides: ${cardScript.slides.length}`,
    `- min readable px: ${minPx}`,
    '',
    '## Slide contract check',
    '',
    ...cardScript.slides.map((s) => [
      `### ${s.slide_id} — ${s.template_id}`,
      `- role: ${s.role}`,
      `- message: ${s.message}`,
      `- image_role: ${s.image_role}`,
      `- element jobs: ${s.elements.map((e) => `${e.id}:${e.job}`).join(', ')}`,
      `- qa_rules: ${s.qa_rules.join(', ')}`,
      ''
    ].join('\n')),
    '## Renderer v1 notes',
    '',
    '- T03 bottom output cards are top-aligned.',
    '- T06 uses Storyboard Preview, not a tool network.',
    '- T08 has no meaningless bright preview box; resource is explicit in text/list.',
    '- Vision QA should still inspect contact sheet plus risk cards 03/05/06 individually.'
  ].join('\n');
  fs.writeFileSync(path.join(outdir, 'qa-report.md'), qaReport);

  console.log(`Rendered ${cardScript.slides.length} cards to ${outdir}`);
})();
