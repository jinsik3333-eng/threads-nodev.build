from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W, H = 1080, 1350
OUT = Path('/Users/jinsik/Desktop/Workspace/01_project_threads/app/cards/episodes/20260504_cover_3_directions')
OUT.mkdir(parents=True, exist_ok=True)
FONT_DIR = Path('/Users/jinsik/Library/Fonts')
P = {
    'pret_r': str(FONT_DIR / 'Pretendard-Regular.otf'),
    'pret_m': str(FONT_DIR / 'Pretendard-Medium.otf'),
    'pret_sb': str(FONT_DIR / 'Pretendard-SemiBold.otf'),
    'pret_b': str(FONT_DIR / 'Pretendard-Bold.otf'),
    'suit_r': str(FONT_DIR / 'SUIT-Regular.otf'),
    'suit_sb': str(FONT_DIR / 'SUIT-SemiBold.otf'),
    'suit_b': str(FONT_DIR / 'SUIT-Bold.otf'),
    'suit_eb': str(FONT_DIR / 'SUIT-ExtraBold.otf'),
    'ibm_m': str(FONT_DIR / 'IBMPlexSansKR-Medium.otf'),
}
IMG = {
    'workspace': '/Users/jinsik/.hermes/cache/images/openai_codex_gpt-image-2-high_20260501_143518_1b6bc06d.png',
    'campaign': '/Users/jinsik/.hermes/cache/images/openai_codex_gpt-image-2-high_20260503_200828_30bcb5b3.png',
    'dark': '/Users/jinsik/.hermes/cache/images/openai_codex_gpt-image-2-high_20260501_151743_d4c9e435.png',
}


def font(path, size):
    return ImageFont.truetype(path, size)


def cover_crop(path, focus=(0.5, 0.5)):
    im = Image.open(path).convert('RGB')
    iw, ih = im.size
    scale = max(W / iw, H / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    fx, fy = focus
    x = int((nw - W) * fx)
    y = int((nh - H) * fy)
    return im.crop((x, y, x + W, y + H)).convert('RGBA')


def gradient(size, top, bottom, horizontal=False):
    w, h = size
    img = Image.new('RGBA', size)
    pix = img.load()
    for y in range(h):
        for x in range(w):
            t = (x / (w - 1)) if horizontal else (y / (h - 1))
            pix[x, y] = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(4))
    return img


def rounded(draw, xy, r, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def multiline(draw, xy, s, f, fill, spacing=8, align='left'):
    draw.multiline_text(xy, s, font=f, fill=fill, spacing=spacing, align=align)


def draw_header(d, fill, page='01 / 06', brand='@nodev.builder'):
    f = font(P['ibm_m'], 25)
    d.text((W // 2, 64), brand, font=f, fill=fill, anchor='mm')
    d.text((W - 84, 64), page, font=f, fill=fill, anchor='rm')


def draw_pill(d, xy, label, fill, txt, outline=None, fs=24):
    f = font(P['ibm_m'], fs)
    x, y = xy
    pad_x, pad_y = 22, 11
    bbox = d.textbbox((0, 0), label, font=f)
    ww = bbox[2] - bbox[0] + pad_x * 2
    hh = bbox[3] - bbox[1] + pad_y * 2
    rounded(d, (x, y, x + ww, y + hh), hh // 2, fill, outline, 1)
    d.text((x + ww / 2, y + hh / 2 + 1), label, font=f, fill=txt, anchor='mm')
    return (x, y, x + ww, y + hh)


# A. Warm Editorial / workspace
base = cover_crop(IMG['workspace'], focus=(0.43, 0.52))
base.alpha_composite(gradient((W, H), (248, 241, 231, 135), (248, 241, 231, 20)))
base.alpha_composite(gradient((W, H), (247, 239, 226, 205), (247, 239, 226, 15), horizontal=True))
d = ImageDraw.Draw(base)
draw_header(d, (48, 39, 32, 220))
draw_pill(d, (82, 140), '전체 가이드 무료 공개', (48, 39, 32, 18), (48, 39, 32, 220), (48, 39, 32, 70), 23)
d.line((84, 242, 440, 242), fill=(48, 39, 32, 85), width=2)
multiline(d, (84, 310), '코딩 몰라도\n내 업무 시스템은\n직접 만들 수 있습니다', font(P['pret_sb'], 74), (35, 29, 24, 245), spacing=18)
multiline(d, (88, 704), '비개발자를 위한 AI 작업 시스템', font(P['pret_r'], 32), (81, 70, 61, 235), spacing=8)
d.line((88, 1042, 430, 1042), fill=(65, 53, 43, 95), width=2)
multiline(d, (88, 1072), '무료 가이드와 제작 과정을\n함께 공개합니다.', font(P['pret_m'], 32), (48, 39, 32, 230), spacing=11)
multiline(d, (88, 1212), 'A. Warm Editorial / workspace', font(P['ibm_m'], 21), (88, 76, 65, 190))
base.convert('RGB').save(OUT / 'cover-a-warm-editorial.png', quality=95)

# B. Premium Campaign / 3D no-code scene
base = cover_crop(IMG['campaign'], focus=(0.5, 0.5))
base.alpha_composite(gradient((W, H), (18, 36, 44, 30), (18, 36, 44, 135)))
base.alpha_composite(gradient((W, H), (20, 38, 45, 145), (20, 38, 45, 0), horizontal=True))
d = ImageDraw.Draw(base)
draw_header(d, (255, 255, 255, 230))
draw_pill(d, (78, 132), 'FREE GUIDE', (255, 255, 255, 34), (255, 255, 255, 235), (255, 255, 255, 90), 24)
f_big = font(P['suit_eb'], 78)
x, y = 78, 702
d.text((x, y), '코딩 몰라도', font=f_big, fill=(255, 255, 255, 245))
y += 100
d.text((x, y), '내 업무 시스템은', font=f_big, fill=(255, 255, 255, 245))
y += 100
d.text((x, y), '직접 만듭니다', font=f_big, fill=(210, 238, 183, 255))
multiline(d, (82, 1036), '아이디어를 실제 업무 도구로 바꾸는\n제작 과정을 공개합니다.', font(P['suit_sb'], 35), (255, 255, 255, 230), spacing=11)
draw_pill(d, (82, 1180), '전체 가이드 무료 공개', (255, 255, 255, 220), (23, 46, 52, 245), None, 27)
multiline(d, (82, 1274), 'B. Premium Campaign / no-code system', font(P['ibm_m'], 20), (255, 255, 255, 185))
base.convert('RGB').save(OUT / 'cover-b-premium-campaign.png', quality=95)

# C. Dark Briefing / system dashboard
base = cover_crop(IMG['dark'], focus=(0.52, 0.5))
base.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, 80)))
base.alpha_composite(gradient((W, H), (0, 0, 0, 45), (0, 0, 0, 190)))
base.alpha_composite(gradient((W, H), (0, 0, 0, 180), (0, 0, 0, 30), horizontal=True))
d = ImageDraw.Draw(base)
draw_header(d, (239, 236, 226, 225))
draw_pill(d, (76, 136), '비개발자를 위한 AI 작업 시스템', (237, 234, 226, 20), (237, 234, 226, 230), (237, 234, 226, 70), 23)
d.rounded_rectangle((78, 304, 88, 575), radius=5, fill=(122, 209, 213, 230))
multiline(d, (116, 292), '코딩 몰라도\n내 업무 시스템은\n직접 만들 수 있습니다', font(P['pret_b'], 70), (245, 242, 232, 248), spacing=20)
multiline(d, (84, 814), 'Claude에게 업무를 맡기는 구조를\n처음부터 함께 만듭니다.', font(P['pret_m'], 36), (237, 234, 226, 232), spacing=13)
d.line((84, 1004, 560, 1004), fill=(237, 234, 226, 80), width=2)
multiline(d, (84, 1044), '비개발자를 위한 AI 작업 시스템 가이드\n전체 가이드와 제작 과정을 공개합니다.', font(P['pret_r'], 31), (206, 200, 188, 230), spacing=11)
multiline(d, (84, 1244), 'C. Dark Briefing / system builder', font(P['ibm_m'], 20), (237, 234, 226, 165))
base.convert('RGB').save(OUT / 'cover-c-dark-briefing.png', quality=95)

# Contact sheet
files = ['cover-a-warm-editorial.png', 'cover-b-premium-campaign.png', 'cover-c-dark-briefing.png']
thumbs = []
for f in files:
    im = Image.open(OUT / f).convert('RGB').resize((360, 450), Image.LANCZOS)
    thumbs.append(im)
sheet = Image.new('RGB', (1080, 510), (248, 246, 242))
d = ImageDraw.Draw(sheet)
labels = ['A Warm Editorial', 'B Premium Campaign', 'C Dark Briefing']
for i, im in enumerate(thumbs):
    x = i * 360
    sheet.paste(im, (x, 0))
    d.rectangle((x, 450, x + 360, 510), fill=(248, 246, 242))
    d.text((x + 180, 482), labels[i], font=font(P['pret_sb'], 24), fill=(35, 29, 24), anchor='mm')
sheet.save(OUT / 'cover-contact-sheet.png', quality=95)

(OUT / 'cover-evaluation.md').write_text(
    '# Cover 3 directions evaluation draft\n\n'
    '- A Warm Editorial: 23번 워크스페이스 이미지. 첫 게시글 정체성 선언용으로 가장 안전.\n'
    '- B Premium Campaign: 07번 3D 캠페인 이미지. 산뜻하고 브랜드형이나 앱 광고 느낌이 강할 수 있음.\n'
    '- C Dark Briefing: 21번 다크 시스템 이미지. 전문적이고 강하지만 첫 게시글로는 다소 무거울 수 있음.\n',
    encoding='utf-8'
)

for f in files + ['cover-contact-sheet.png', 'cover-evaluation.md']:
    print(OUT / f)
