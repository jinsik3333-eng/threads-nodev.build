from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W, H = 1080, 1350
OUT = Path('/Users/jinsik/Desktop/Workspace/01_project_threads/app/cards/episodes/20260504_cover_3_directions')
FONT_DIR = Path('/Users/jinsik/Library/Fonts')
P = {
    'pret_r': str(FONT_DIR / 'Pretendard-Regular.otf'),
    'pret_m': str(FONT_DIR / 'Pretendard-Medium.otf'),
    'pret_sb': str(FONT_DIR / 'Pretendard-SemiBold.otf'),
    'suit_sb': str(FONT_DIR / 'SUIT-SemiBold.otf'),
    'suit_b': str(FONT_DIR / 'SUIT-Bold.otf'),
    'suit_eb': str(FONT_DIR / 'SUIT-ExtraBold.otf'),
    'ibm_m': str(FONT_DIR / 'IBMPlexSansKR-Medium.otf'),
}
IMG_WORK = '/Users/jinsik/.hermes/cache/images/openai_codex_gpt-image-2-high_20260501_143518_1b6bc06d.png'
IMG_CHAR = '/Users/jinsik/.hermes/cache/images/openai_codex_gpt-image-2-high_20260504_121608_3d9a8c95.png'


def font(path, size):
    return ImageFont.truetype(path, size)


def cover_crop(path, focus=(0.5, 0.5)):
    im = Image.open(path).convert('RGB')
    iw, ih = im.size
    scale = max(W / iw, H / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    fx, fy = focus
    x = max(0, min(int((nw - W) * fx), nw - W))
    y = max(0, min(int((nh - H) * fy), nh - H))
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


def multiline(d, xy, s, f, fill, spacing=8, align='left'):
    d.multiline_text(xy, s, font=f, fill=fill, spacing=spacing, align=align)


def pill(d, xy, label, fill, txt, outline=None, fs=24):
    f = font(P['ibm_m'], fs)
    x, y = xy
    pad_x, pad_y = 22, 11
    bbox = d.textbbox((0, 0), label, font=f)
    ww, hh = bbox[2] - bbox[0] + pad_x * 2, bbox[3] - bbox[1] + pad_y * 2
    d.rounded_rectangle((x, y, x + ww, y + hh), radius=hh // 2, fill=fill, outline=outline, width=1)
    d.text((x + ww / 2, y + hh / 2 + 1), label, font=f, fill=txt, anchor='mm')


def header(d, fill):
    f = font(P['ibm_m'], 25)
    d.text((W // 2, 64), '@nodev.builder', font=f, fill=fill, anchor='mm')
    d.text((W - 84, 64), '01 / 06', font=f, fill=fill, anchor='rm')

# D: A+B hybrid — real workspace, B-ish typography power
base = cover_crop(IMG_WORK, focus=(0.43, 0.52))
base.alpha_composite(gradient((W, H), (245, 238, 226, 185), (245, 238, 226, 25)))
base.alpha_composite(gradient((W, H), (242, 232, 216, 220), (242, 232, 216, 5), horizontal=True))
# subtle bottom depth
base.alpha_composite(gradient((W, H), (0, 0, 0, 0), (64, 48, 35, 50)))
d = ImageDraw.Draw(base)
header(d, (43, 35, 29, 220))
pill(d, (80, 134), '전체 가이드 무료 공개', (43, 35, 29, 20), (43, 35, 29, 230), (43, 35, 29, 70), 23)
# title block with B font feel
x, y = 82, 300
f = font(P['suit_eb'], 76)
d.text((x, y), '코딩 없이도', font=f, fill=(31, 27, 23, 248))
y += 96
d.text((x, y), '내 업무 시스템은', font=f, fill=(31, 27, 23, 248))
y += 96
d.text((x, y), '직접 설계할 수 있습니다', font=font(P['suit_eb'], 62), fill=(126, 70, 42, 255))
multiline(d, (86, 684), '비개발자를 위한 AI 작업 시스템', font(P['pret_m'], 36), (77, 65, 55, 238), spacing=8)
d.line((86, 1008, 518, 1008), fill=(52, 42, 34, 100), width=2)
multiline(d, (86, 1044), 'AI에게 업무를 맡기는 구조를\n처음부터 함께 만듭니다.', font(P['pret_m'], 38), (43, 35, 29, 238), spacing=14)
base.convert('RGB').save(OUT / 'cover-d-ab-hybrid.png', quality=95)

# E: B character mascot direction
base = cover_crop(IMG_CHAR, focus=(0.50, 0.48))
# left readability wash, keep character right clear
base.alpha_composite(gradient((W, H), (248, 241, 229, 205), (248, 241, 229, 0), horizontal=True))
base.alpha_composite(gradient((W, H), (255, 255, 255, 32), (83, 68, 54, 42)))
d = ImageDraw.Draw(base)
header(d, (43, 35, 29, 220))
pill(d, (78, 132), 'NODEV BUILDER', (43, 35, 29, 22), (43, 35, 29, 230), (43, 35, 29, 70), 24)
# more compact B-style title, avoid covering character
x, y = 78, 270
f1 = font(P['suit_eb'], 86)
d.text((x, y), '코딩 몰라도', font=f1, fill=(32, 28, 24, 250))
y += 108
d.text((x, y), '내 업무 시스템은', font=font(P['suit_eb'], 76), fill=(32, 28, 24, 250))
y += 100
d.text((x, y), '직접 만듭니다', font=f1, fill=(28, 95, 84, 255))
multiline(d, (82, 648), 'AI에게 일을 맡기는 흐름을\n캐릭터로 쉽게 풀어드립니다.', font(P['pret_m'], 36), (73, 62, 53, 238), spacing=13)
pill(d, (82, 1088), '전체 가이드 무료 공개', (28, 95, 84, 238), (255, 255, 250, 245), None, 30)
multiline(d, (84, 1238), 'E. Character mascot / friendly builder', font(P['ibm_m'], 20), (86, 72, 60, 180))
base.convert('RGB').save(OUT / 'cover-e-character-builder.png', quality=95)

# Contact sheet for developed 2 variants
files = ['cover-d-ab-hybrid.png', 'cover-e-character-builder.png']
sheet = Image.new('RGB', (900, 620), (248, 246, 242))
d = ImageDraw.Draw(sheet)
labels = ['D. A+B Hybrid', 'E. B Character']
for i, f in enumerate(files):
    im = Image.open(OUT / f).convert('RGB').resize((420, 525), Image.LANCZOS)
    x = 30 + i * 450
    sheet.paste(im, (x, 0))
    d.text((x + 210, 570), labels[i], font=font(P['pret_sb'], 28), fill=(35, 29, 24), anchor='mm')
sheet.save(OUT / 'cover-developed-contact-sheet.png', quality=95)

for f in files + ['cover-developed-contact-sheet.png']:
    print(OUT / f)
