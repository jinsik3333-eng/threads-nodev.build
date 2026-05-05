from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import textwrap, zipfile, os, math

ROOT = Path('/Users/jinsik/Desktop/Workspace/01_project_threads/app/cards/episodes/20260504_second_post_content_30_image2')
OUT = ROOT / 'output'
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1350
FONT_DIR = Path('/Users/jinsik/Library/Fonts')
FONT_HEAVY = str(FONT_DIR / 'SUIT-Heavy.otf')
FONT_BOLD = str(FONT_DIR / 'SUIT-Bold.otf')
FONT_SEMI = str(FONT_DIR / 'SUIT-SemiBold.otf')
FONT_MED = str(FONT_DIR / 'SUIT-Medium.otf')
FONT_REG = str(FONT_DIR / 'SUIT-Regular.otf')

COLORS = {
    'ink': (34, 45, 58),
    'ink2': (55, 67, 82),
    'blue': (79, 151, 211),
    'deepblue': (28, 72, 116),
    'cream': (252, 249, 240),
    'white': (255, 255, 255),
    'muted': (116, 127, 139),
    'dark': (18, 23, 31),
}

slides = [
    {
        'idx': '01',
        'img': '/Users/jinsik/.hermes/cache/images/openai_codex_gpt-image-2-high_20260503_195936_ac832bf6.png',
        'centering': (0.56, 0.46),
        'overlay': 'left_light',
        'kicker': 'CONTENT SYSTEM',
        'title': ['콘텐츠 30일치', 'Claude가 짜줌'],
        'accent_lines': [0],
        'support': '아이디어 하나를 한 달치 발행 재료로 바꾸는 방법',
        'pill': '무료 프롬프트 키트 → 프로필 링크',
        'pos': 'left',
    },
    {
        'idx': '02',
        'img': '/Users/jinsik/.hermes/cache/images/openai_codex_gpt-image-2-high_20260503_200029_94ec6b4d.png',
        'centering': (0.48, 0.42),
        'overlay': 'top_light',
        'kicker': 'PROBLEM',
        'title': ['매일 새로 생각하면', '계정은 멈춥니다'],
        'accent_lines': [1],
        'support': '문제는 아이디어 부족이 아니라, 발행 구조가 없다는 것.',
        'labels': ['빈 캘린더', '밀린 초안', '반복되는 고민'],
        'pos': 'top',
    },
    {
        'idx': '03',
        'img': '/Users/jinsik/.hermes/cache/images/openai_codex_gpt-image-2-high_20260503_194118_e0d7a8b6.png',
        'centering': (0.51, 0.50),
        'overlay': 'top_light',
        'kicker': 'TURN',
        'title': ['더 짜지 말고', '쪼개세요'],
        'accent_lines': [1],
        'support': '하나의 주제를 훅, 캡션, 카드, 캘린더 단위로 나눕니다.',
        'labels': ['HOOKS', 'CAPTIONS', 'CALENDAR'],
        'pos': 'top',
    },
    {
        'idx': '04',
        'img': '/Users/jinsik/.hermes/cache/images/openai_codex_gpt-image-2-high_20260503_194215_309f0cf8.png',
        'centering': (0.48, 0.47),
        'overlay': 'left_light',
        'kicker': 'CLAUDE OUTPUT',
        'title': ['결과물 형식까지', '먼저 요청하세요'],
        'accent_lines': [0],
        'support': '“좋은 아이디어 줘”보다 “30일 일정표로 쪼개줘”가 더 명확합니다.',
        'labels': ['주제 1개', '포맷 5개', '30일 일정표'],
        'pos': 'left',
    },
    {
        'idx': '05',
        'img': '/Users/jinsik/.hermes/cache/images/openai_codex_gpt-image-2-high_20260503_194327_c049bd20.png',
        'centering': (0.48, 0.52),
        'overlay': 'top_light',
        'kicker': 'ASSET BOARD',
        'title': ['아이디어만 말고', '바로 올릴 재료'],
        'accent_lines': [1],
        'support': '훅, 카드 흐름, 캡션, CTA까지 한 번에 묶어둡니다.',
        'labels': ['CAROUSEL', 'REELS', 'CAPTION'],
        'pos': 'top',
    },
    {
        'idx': '06',
        'img': '/Users/jinsik/.hermes/cache/images/openai_codex_gpt-image-2-high_20260503_200126_100e242d.png',
        'centering': (0.50, 0.50),
        'overlay': 'center_clean',
        'kicker': 'FREE KIT',
        'title': ['복붙용 키트는', '프로필 링크에'],
        'accent_lines': [0],
        'support': '프롬프트 · 예시 입력값 · 검수 체크리스트를 바로 복사해 쓸 수 있게 정리했어요.',
        'pill': '프로필 링크 눌러 무료 키트 받기 →',
        'pos': 'center',
    },
]


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_image(path, centering):
    img = Image.open(path).convert('RGB')
    return ImageOps_fit(img, (W, H), centering=centering)


def ImageOps_fit(img, size, centering=(0.5,0.5)):
    # custom cover crop to avoid importing extra ambiguity
    sw, sh = img.size
    tw, th = size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    cx = int((nw - tw) * centering[0]) if nw > tw else 0
    cy = int((nh - th) * centering[1]) if nh > th else 0
    return img.crop((cx, cy, cx + tw, cy + th))


def rounded_rect(draw, xy, r, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def add_gradient(base, mode):
    overlay = Image.new('RGBA', (W, H), (0,0,0,0))
    px = overlay.load()
    # 더 강한 텍스트 포커스: 배경은 살리되, 글자가 올라가는 영역은 Gymcoding식으로 조용하게 눌러준다.
    if mode == 'left_light':
        for x in range(W):
            a = int(max(0, 250 * (1 - x / 760)))
            for y in range(H):
                px[x,y] = (252,249,240,a)
    elif mode == 'top_light':
        for y in range(H):
            a = int(max(0, 255 * (1 - y / 700)))
            for x in range(W):
                px[x,y] = (252,249,240,a)
    elif mode == 'center_clean':
        for y in range(H):
            for x in range(W):
                dx = abs(x - W/2)/(W/2)
                dy = abs(y - H/2)/(H/2)
                a = int(max(0, 230 * (1 - max(dx*0.95, dy*0.9))))
                px[x,y] = (252,249,240,a)
    return Image.alpha_composite(base.convert('RGBA'), overlay)


def add_focus_panel(base, xy, radius=42):
    # SaaS 박스가 아니라 텍스트 집중용 종이 레이어. 배경과 글자를 분리한다.
    x1, y1, x2, y2 = xy
    shadow = Image.new('RGBA', (W, H), (0,0,0,0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((x1+8, y1+12, x2+8, y2+12), radius=radius, fill=(45,54,66,26))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    panel = Image.new('RGBA', (W, H), (0,0,0,0))
    pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle(xy, radius=radius, fill=(252,249,240,226), outline=(255,255,255,150), width=2)
    return Image.alpha_composite(Image.alpha_composite(base, shadow), panel)


def draw_tracking(draw, xy, text, fnt, fill, tracking=2):
    x, y = xy
    for ch in text:
        draw.text((x,y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


def multiline_title(draw, lines, x, y, accent_lines=None, align='left', max_width=760, base_size=94):
    accent_lines = accent_lines or []
    cur = y
    for i, line in enumerate(lines):
        size = base_size
        # 긴 한글은 줄 수를 줄인 대신 모바일에서 읽히도록 과하게 줄이지 않는다.
        if len(line) >= 10: size = int(base_size * 0.82)
        elif len(line) >= 8: size = int(base_size * 0.90)
        fnt = font(FONT_HEAVY, size)
        fill = COLORS['blue'] if i in accent_lines else COLORS['ink']
        bbox = draw.textbbox((0,0), line, font=fnt)
        tw = bbox[2]-bbox[0]
        xx = x if align == 'left' else (W - tw)//2
        draw.text((xx, cur), line, font=fnt, fill=fill)
        cur += int(size * 1.12)
    return cur


def draw_support(draw, text, x, y, width=660, size=34, align='left'):
    fnt = font(FONT_SEMI, size)
    lines = []
    cur = ''
    for word in text.split(' '):
        test = (cur + ' ' + word).strip()
        if draw.textlength(test, font=fnt) > width and cur:
            lines.append(cur)
            cur = word
        else:
            cur = test
    if cur: lines.append(cur)
    for line in lines[:2]:
        tw = draw.textlength(line, font=fnt)
        xx = x if align == 'left' else (W - tw)//2
        draw.text((xx, y), line, font=fnt, fill=COLORS['ink2'])
        y += int(size * 1.5)
    return y


def draw_header(draw, idx, dark=False):
    c = (255,255,255,235) if dark else (42,55,70,215)
    f1 = font(FONT_BOLD, 24)
    f2 = font(FONT_MED, 23)
    label = '@nodev.builder'
    tw = draw.textlength(label, font=f1)
    draw.text(((W-tw)/2, 54), label, font=f1, fill=c)
    draw.text((W-94, 54), idx, font=f2, fill=c)


def draw_kicker(draw, text, x, y, center=False):
    f = font(FONT_BOLD, 22)
    pad_x, pad_y = 18, 10
    tw = draw.textlength(text, font=f)
    box_w = int(tw + pad_x*2)
    xx = int((W-box_w)/2) if center else x
    rounded_rect(draw, (xx, y, xx+box_w, y+44), 22, (255,255,255,185), outline=(255,255,255,80))
    draw.text((xx+pad_x, y+10), text, font=f, fill=COLORS['deepblue'])
    return xx + box_w


def draw_labels(draw, labels, x, y, center=False):
    f = font(FONT_BOLD, 28)
    widths = [int(draw.textlength(t, font=f)+42) for t in labels]
    total = sum(widths) + 14*(len(labels)-1)
    xx = int((W-total)/2) if center else x
    for t, bw in zip(labels, widths):
        rounded_rect(draw, (xx, y, xx+bw, y+56), 28, (255,255,255,220), outline=(255,255,255,150))
        draw.text((xx+21, y+14), t, font=f, fill=COLORS['deepblue'])
        xx += bw + 14


def draw_pill(draw, text, x, y, center=False, dark=False):
    f = font(FONT_BOLD, 33)
    tw = draw.textlength(text, font=f)
    bw = int(tw + 68)
    xx = int((W-bw)/2) if center else x
    fill = (34,45,58,242) if not dark else (255,255,255,235)
    txt = (255,255,255,250) if not dark else COLORS['dark']
    rounded_rect(draw, (xx, y, xx+bw, y+78), 39, fill)
    draw.text((xx+34, y+22), text, font=f, fill=txt)


def make_slide(s):
    img = fit_image(s['img'], s['centering'])
    base = add_gradient(img, s['overlay'])

    # 텍스트 집중 레이아웃: 배경 이미지는 무드, 메시지는 독립된 읽기 영역.
    if s['pos'] == 'left':
        base = add_focus_panel(base, (56, 128, 760, 760), radius=44)
    elif s['pos'] == 'top':
        base = add_focus_panel(base, (54, 124, 1006, 600), radius=44)
    else:
        base = add_focus_panel(base, (132, 170, 948, 790), radius=50)

    draw = ImageDraw.Draw(base)
    draw_header(draw, s['idx'])

    if s['pos'] == 'left':
        x, y = 94, 166
        draw_kicker(draw, s['kicker'], x, y)
        end = multiline_title(draw, s['title'], x, y+76, s.get('accent_lines'), 'left', base_size=104)
        sy = draw_support(draw, s['support'], x, end+28, width=590, size=34)
        if 'labels' in s:
            draw_labels(draw, s['labels'], x, sy+28)
        if 'pill' in s:
            draw_pill(draw, s['pill'], x, H-158)
    elif s['pos'] == 'top':
        x, y = 90, 160
        draw_kicker(draw, s['kicker'], x, y)
        end = multiline_title(draw, s['title'], x, y+72, s.get('accent_lines'), 'left', base_size=92)
        sy = draw_support(draw, s['support'], x, end+22, width=780, size=33)
        if 'labels' in s:
            draw_labels(draw, s['labels'], x, sy+24)
    else:
        draw_kicker(draw, s['kicker'], 0, 218, center=True)
        end = multiline_title(draw, s['title'], W//2, 326, s.get('accent_lines'), 'center', base_size=94)
        draw_support(draw, s['support'], 190, end+30, width=700, size=33, align='center')
        draw_pill(draw, s['pill'], 0, H-296, center=True)
    return base.convert('RGB')


pngs = []
for s in slides:
    slide = make_slide(s)
    out = OUT / f"card-{s['idx']}.png"
    slide.save(out, quality=95)
    pngs.append(out)

# contact sheet 3x2
thumb_w, thumb_h = 360, 450
sheet = Image.new('RGB', (thumb_w*3, thumb_h*2), (244,241,232))
for i, p in enumerate(pngs):
    im = Image.open(p).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    sheet.paste(im, ((i%3)*thumb_w, (i//3)*thumb_h))
sheet.save(OUT / 'contact-sheet.png', quality=95)

# zip
zip_path = OUT / 'second-post-content-30-image2.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in pngs:
        z.write(p, arcname=p.name)
    z.write(OUT / 'contact-sheet.png', arcname='contact-sheet.png')
    if (ROOT / 'storyboard.md').exists():
        z.write(ROOT / 'storyboard.md', arcname='storyboard.md')
    if (ROOT / 'post.md').exists():
        z.write(ROOT / 'post.md', arcname='post.md')
print(OUT)
print(zip_path)
