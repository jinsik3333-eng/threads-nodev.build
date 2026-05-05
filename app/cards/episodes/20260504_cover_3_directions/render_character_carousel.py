from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import textwrap, json

W, H = 1080, 1350
OUT = Path('/Users/jinsik/Desktop/Workspace/01_project_threads/app/cards/episodes/20260504_cover_3_directions/character_carousel')
OUT.mkdir(parents=True, exist_ok=True)
FONT_DIR = Path('/Users/jinsik/Library/Fonts')
P = {
    'pret_r': str(FONT_DIR / 'Pretendard-Regular.otf'),
    'pret_m': str(FONT_DIR / 'Pretendard-Medium.otf'),
    'pret_sb': str(FONT_DIR / 'Pretendard-SemiBold.otf'),
    'pret_b': str(FONT_DIR / 'Pretendard-Bold.otf'),
    'suit_m': str(FONT_DIR / 'SUIT-Medium.otf'),
    'suit_sb': str(FONT_DIR / 'SUIT-SemiBold.otf'),
    'suit_b': str(FONT_DIR / 'SUIT-Bold.otf'),
    'suit_eb': str(FONT_DIR / 'SUIT-ExtraBold.otf'),
    'ibm_m': str(FONT_DIR / 'IBMPlexSansKR-Medium.otf'),
}
IMG_CHAR = '/Users/jinsik/.hermes/cache/images/openai_codex_gpt-image-2-high_20260504_132632_dc987e9e.png'
IMG_DOG = '/Users/jinsik/.hermes/cache/images/openai_codex_gpt-image-2-high_20260504_171356_b1d4a69a.png'
CHAR_SET = Path('/Users/jinsik/Desktop/Workspace/01_project_threads/app/cards/episodes/20260504_cover_3_directions/character_reference_locked_20')
IMG_THINKING = str(CHAR_SET / 'nodev_builder_ref_locked_03_03_thinking_stuck.png')
IMG_FLOW = str(CHAR_SET / 'nodev_builder_ref_locked_17_17_flowchart_draw.png')
IMG_STEPS = str(CHAR_SET / 'nodev_builder_ref_locked_05_05_three_steps.png')

INK = (35, 30, 26)
INK2 = (70, 58, 49)
MUTED = (118, 100, 86)
CREAM = (246, 238, 226)
PAPER = (255, 250, 241)
TEAL = (30, 103, 90)
TEAL2 = (184, 218, 204)
ORANGE = (151, 82, 45)
LINE = (35, 30, 26, 42)
DARK = (31, 35, 34)

slides = [
    {
        'no': '01 / 06', 'role': 'IDENTITY',
        'title': ['코딩 몰라도', '내 업무 시스템은', '직접 만듭니다'],
        'accent_line': 2,
        'subtitle': '비개발자를 위한 AI 작업 시스템',
        'badge': '전체 가이드 무료 공개'
    },
    {
        'no': '02 / 06', 'role': '막히는 지점',
        'title': ['아이디어는 있는데,', '만들다가 막히나요?'],
        'body': '회의록 정리기, 파일 정리 자동화, 콘텐츠 캘린더.\n생각은 있는데 늘 첫 화면에서 멈춥니다.',
        'quote': '문제는 의지가 아니라\n시작 순서가 없다는 것.'
    },
    {
        'no': '03 / 06', 'role': '생각 바꾸기',
        'title': ['개발자가 되는 게', '목표는', '아닙니다'],
        'body': '필요한 건 코딩 지식보다 먼저\nAI에게 일을 맡길 수 있는 설계도입니다.',
        'keys': ['목표', '자료', '조건', '확인 기준']
    },
    {
        'no': '04 / 06', 'role': '제작 기록',
        'title': ['만드는 과정을', '그대로', '보여드립니다'],
        'items': ['처음 막힌 화면', '잘못 나온 결과', '수정 프롬프트', '완성된 흐름'],
        'body': '잘 된 결과만 모으지 않고, 막히고 고치는 과정까지 기록합니다.'
    },
    {
        'no': '05 / 06', 'role': '입문 순서',
        'title': ['처음이라면', '이 3단계부터'],
        'steps': [('01', '화면 감각 잡기'), ('02', '도구 설치 따라하기'), ('03', '첫 프로젝트 만들기')],
        'body': '전체 가이드는 공개해두었습니다.\n처음에는 볼 순서만 잡아도 충분합니다.'
    },
    {
        'no': '06 / 06', 'role': '댓글 키워드',
        'title': ['처음 시작할 때', '순서가 필요하면', '“시작”'],
        'body': '댓글에 “시작”을 남기면\n입문 3단계 순서를 DM으로 보내드립니다.',
        'footer': '@nodev.builder · 비개발자를 위한 AI 작업 시스템'
    },
]

def font(path, size):
    return ImageFont.truetype(path, size)

def text_size(d, s, f):
    b = d.textbbox((0,0), s, font=f)
    return b[2]-b[0], b[3]-b[1]

def header(d, no, fill=INK):
    f = font(P['ibm_m'], 25)
    d.text((W//2, 64), '@nodev.builder', font=f, fill=fill, anchor='mm')
    d.text((W-78, 64), no, font=f, fill=fill, anchor='rm')

def rounded(d, box, r=34, fill=PAPER, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def pill(d, xy, label, fill, txt, outline=None, fs=26, px=24, py=12):
    f = font(P['pret_sb'], fs)
    x,y = xy
    b = d.textbbox((0,0), label, font=f)
    ww = b[2]-b[0] + px*2
    hh = b[3]-b[1] + py*2
    d.rounded_rectangle((x,y,x+ww,y+hh), radius=hh//2, fill=fill, outline=outline, width=1)
    d.text((x+ww/2, y+hh/2+1), label, font=f, fill=txt, anchor='mm')
    return (x,y,x+ww,y+hh)

def title_block(d, lines, x=78, y=204, sizes=None, accent_idx=None, accent=TEAL, dark=INK, leading=1.05):
    if sizes is None: sizes = [82]*len(lines)
    cy = y
    for i, line in enumerate(lines):
        sz = sizes[i] if i < len(sizes) else sizes[-1]
        f = font(P['suit_eb'], sz)
        fill = accent if accent_idx == i else dark
        d.text((x, cy), line, font=f, fill=fill)
        cy += int(sz * leading)
    return cy

def draw_wrapped(d, xy, text, f, fill, max_chars=22, spacing=9):
    lines = []
    for para in text.split('\n'):
        if len(para) <= max_chars:
            lines.append(para)
        else:
            lines += textwrap.wrap(para, width=max_chars, break_long_words=False)
    d.multiline_text(xy, '\n'.join(lines), font=f, fill=fill, spacing=spacing)


def centered_multiline(d, box, text, f, fill, spacing=10):
    x1, y1, x2, y2 = box
    lines = text.split('\n')
    heights = []
    widths = []
    for line in lines:
        b = d.textbbox((0, 0), line, font=f)
        widths.append(b[2] - b[0])
        heights.append(b[3] - b[1])
    total_h = sum(heights) + spacing * (len(lines) - 1)
    y = y1 + ((y2 - y1) - total_h) / 2
    for line, h in zip(lines, heights):
        d.text(((x1 + x2) / 2, y), line, font=f, fill=fill, anchor='ma')
        y += h + spacing

def char_image():
    im = Image.open(IMG_CHAR).convert('RGBA')
    return im


def dog_image():
    return Image.open(IMG_DOG).convert('RGBA')


def paste_small_dog(base, xy=(760, 910), size=250, opacity=245):
    im = dog_image()
    iw, ih = im.size
    # Crop the dog/right-side companion area with enough beige around it so it blends naturally.
    crop = im.crop((int(iw*0.42), int(ih*0.20), int(iw*0.98), int(ih*0.92)))
    scale = size / crop.height
    crop = crop.resize((int(crop.width*scale), size), Image.LANCZOS)
    if opacity < 255:
        alpha = crop.getchannel('A').point(lambda p: int(p*opacity/255))
        crop.putalpha(alpha)
    # subtle grounding shadow so it doesn't feel like a pasted sticker
    dd = ImageDraw.Draw(base)
    x, y = xy
    sw = max(90, int(crop.width * 0.62))
    dd.ellipse((x + 18, y + size - 34, x + 18 + sw, y + size - 10), fill=(70, 55, 40, 26))
    base.alpha_composite(crop, xy)


def draw_soft_3d_props(d, variant='teal'):
    # Soft 3D-like props: shaded capsules/spheres instead of flat background circles or square blocks.
    if variant == 'dark':
        d.rounded_rectangle((700,130,1100,235), radius=52, fill=(42,108,94,64))
        d.rounded_rectangle((-80,1038,350,1160), radius=58, fill=(139,78,46,56))
        d.ellipse((872,320,940,388), fill=(238,202,145,42))
        d.ellipse((930,365,982,417), fill=(220,238,229,34))
        return
    d.rounded_rectangle((760,118,1120,220), radius=54, fill=(220,234,226,132))
    d.rounded_rectangle((816,248,1004,324), radius=38, fill=(190,220,207,92))
    d.ellipse((910,352,982,424), fill=(238,202,145,82))
    d.ellipse((972,396,1020,444), fill=(30,103,90,42))
    d.rounded_rectangle((-96,1054,320,1164), radius=56, fill=(240,224,206,116))

def paste_cover_char(base):
    im = char_image()
    # fit height, focus on right character from generated portrait
    iw, ih = im.size
    scale = H / ih
    nw, nh = int(iw*scale), H
    im = im.resize((nw, nh), Image.LANCZOS)
    # portrait image is 1024x1536 -> 900x1350, paste right aligned
    base.alpha_composite(im, (W-nw, 0))
    wash = Image.new('RGBA', (W,H), (0,0,0,0))
    pix = wash.load()
    for y in range(H):
        for x in range(W):
            t = min(1, x/690)
            a = int(230*(1-t))
            pix[x,y] = (248,241,229,a)
    base.alpha_composite(wash)

def paste_small_char(base, xy=(740,870), size=260, opacity=255):
    im = char_image()
    # crop lower/right character area loosely
    iw, ih = im.size
    crop = im.crop((int(iw*0.28), int(ih*0.18), iw, int(ih*0.98)))
    scale = size / crop.height
    crop = crop.resize((int(crop.width*scale), size), Image.LANCZOS)
    if opacity < 255:
        alpha = crop.getchannel('A').point(lambda p: int(p*opacity/255))
        crop.putalpha(alpha)
    base.alpha_composite(crop, xy)


def paste_asset_char(base, path, xy, size=230, opacity=255, crop_pad=78):
    """Paste a reference-locked character asset as a quiet scene element.

    The asset backgrounds are close to the card background, so avoid another
    outlined box/sticker and use only a soft grounding shadow.
    """
    im = Image.open(path).convert('RGBA')
    iw, ih = im.size
    crop = im.crop((crop_pad, crop_pad, iw - crop_pad, ih - crop_pad))
    scale = size / crop.height
    crop = crop.resize((int(crop.width * scale), size), Image.LANCZOS)
    if opacity < 255:
        alpha = crop.getchannel('A').point(lambda p: int(p * opacity / 255))
        crop.putalpha(alpha)
    d = ImageDraw.Draw(base)
    x, y = xy
    d.ellipse((x + 28, y + size - 30, x + crop.width - 28, y + size - 6), fill=(70, 55, 40, 22))
    base.alpha_composite(crop, xy)


def new_base(dark=False):
    # Keep inner-slide backgrounds clean for now: no circles, long pills, or decorative props.
    if dark:
        return Image.new('RGBA', (W,H), (32,36,35,255))
    return Image.new('RGBA', (W,H), CREAM+(255,))

def slide1(s):
    base = new_base()
    paste_cover_char(base)
    d = ImageDraw.Draw(base)
    header(d, s['no'])
    pill(d, (78,132), s['badge'], (30,103,90,232), (255,255,248), fs=30)
    title_block(d, s['title'], 78, 270, [86,76,86], accent_idx=2)
    draw_wrapped(d, (82,650), s['subtitle']+'\n무료 가이드와 제작 과정을 함께 공개합니다.', font(P['pret_m'],36), INK2, 24, 13)
    pill(d, (82,1060), '입문 3단계 안내', (35,30,26), (255,250,241), fs=31, px=28, py=14)
    return base

def slide2(s):
    base = new_base(); d = ImageDraw.Draw(base); header(d, s['no'])
    pill(d, (78,132), s['role'], (35,30,26), (255,250,241), fs=31, px=28, py=14)
    title_block(d, s['title'], 78, 230, [76,90], accent_idx=1, accent=ORANGE)
    draw_wrapped(d, (82,500), s['body'], font(P['pret_m'],37), INK2, 24, 14)
    # idea cards — no confusing connector lines; three examples sit as separate symptoms
    labels = ['회의록\n정리기', '파일 정리\n자동화', '콘텐츠\n캘린더']
    xs = [86, 386, 686]
    for i, lab in enumerate(labels):
        rounded(d, (xs[i], 730, xs[i]+240, 880), r=36, fill=(255,250,241,235), outline=None)
        d.text((xs[i]+120,805), lab, font=font(P['pret_sb'],35), fill=INK, anchor='mm', align='center', spacing=8)
    # Put the conclusion directly under the examples — no unclear middle label/connector.
    rounded(d, (230,960,850,1134), r=46, fill=(31, 76, 67), outline=None)
    d.text((540,1047), s['quote'], font=font(P['pret_b'],43), fill=(255,250,241), anchor='mm', align='center', spacing=13)
    return base

def slide3(s):
    base = new_base(); d=ImageDraw.Draw(base); header(d,s['no'])
    pill(d,(78,132),s['role'],(35,30,26),(255,250,241),fs=31,px=28,py=14)
    title_block(d,s['title'],78,220,[74,98,98],accent_idx=2,accent=TEAL)
    draw_wrapped(d,(82,570),s['body'],font(P['pret_m'],34),INK2,23,13)
    rounded(d,(86,760,994,1110),r=44,fill=(255,250,241,235),outline=None)
    d.text((135,820),'AI에게 맡기기 전 정리할 4가지',font=font(P['pret_sb'],34),fill=INK)
    x0,y0=135,900
    for i,k in enumerate(s['keys']):
        x=x0+(i%2)*410; y=y0+(i//2)*104
        rounded(d,(x,y,x+330,y+66),r=26,fill=(230,242,236) if i%2==0 else (245,232,216),outline=None)
        d.text((x+34,y+33),k,font=font(P['suit_b'],31),fill=TEAL if i%2==0 else ORANGE,anchor='lm')
    d.text((135,1182),'코드를 외우는 대신, 일을 설명하는 방법을 배웁니다.',font=font(P['pret_m'],30),fill=MUTED)
    return base

def slide4(s):
    base = new_base(); d=ImageDraw.Draw(base); header(d,s['no'])
    pill(d,(78,132),s['role'],(35,30,26),(255,250,241),fs=31,px=28,py=14)
    title_block(d,s['title'],78,210,[76,98,98],accent_idx=1,accent=TEAL)
    draw_wrapped(d,(82,560),s['body'],font(P['pret_m'],35),INK2,25,14)
    x=94; y=725
    for i,item in enumerate(s['items']):
        yy=y+i*120
        d.ellipse((104,yy+22,152,yy+70),fill=TEAL if i==3 else (255,250,241),outline=None,width=0)
        rounded(d,(180,yy,930,yy+92),r=30,fill=(255,250,241,235),outline=None)
        d.text((226,yy+46),item,font=font(P['pret_sb'],39),fill=INK,anchor='lm')
        d.text((880,yy+46),f'0{i+1}',font=font(P['ibm_m'],30),fill=(30,103,90,180),anchor='rm')
    return base

def slide5(s):
    base = new_base(); d=ImageDraw.Draw(base); header(d,s['no'])
    pill(d,(78,132),s['role'],(35,30,26),(255,250,241),fs=31,px=28,py=14)
    title_block(d,s['title'],78,230,[80,92],accent_idx=1,accent=ORANGE)
    draw_wrapped(d,(82,485),s['body'],font(P['pret_m'],34),INK2,23,13)
    y=670
    for i,(num,txt) in enumerate(s['steps']):
        yy=y+i*142
        rounded(d,(86,yy,994,yy+104),r=34,fill=(255,250,241,235),outline=None)
        d.text((138,yy+52),num,font=font(P['ibm_m'],34),fill=TEAL,anchor='lm')
        d.text((238,yy+52),txt,font=font(P['suit_b'],42),fill=INK,anchor='lm')
        # No connector lines: each step is a clean stacked card.
    rounded(d,(86,1134,994,1224),r=30,fill=(31, 76, 67),outline=None)
    d.text((540,1179),'전부 보려 하지 말고, 먼저 시작 순서부터 잡으세요.',font=font(P['pret_sb'],32),fill=(255,250,241),anchor='mm')
    return base

def slide6(s):
    base = new_base(dark=True); d=ImageDraw.Draw(base); header(d,s['no'],fill=(248,241,229))
    # dark background motifs are drawn in new_base(); avoid extra circles here.
    pill(d,(78,132),s['role'],(255,250,241),(35,30,26),fs=31,px=28,py=14)
    title_block(d,s['title'],78,246,[78,78,112],accent_idx=2,accent=(235,190,120),dark=(255,250,241))
    # Keep CTA page clean: no cropped mascot inside the content area.
    info_box = (78, 640, 1002, 850)
    rounded(d,info_box,r=44,fill=(255,250,241),outline=None)
    centered_multiline(d, info_box, s['body'], font(P['pret_sb'],44), INK, spacing=17)
    cta_box = (122, 925, 958, 1096)
    rounded(d,cta_box,r=44,fill=(30,103,90),outline=None)
    d.text((540,972),'댓글 키워드',font=font(P['pret_m'],32),fill=(220,238,229),anchor='mm')
    d.text((540,1040),'시작',font=font(P['suit_eb'],72),fill=(255,250,241),anchor='mm')
    d.text((540,1140),s['footer'],font=font(P['pret_m'],30),fill=(255,250,241,220),anchor='mm')
    return base

renderers = [slide1, slide2, slide3, slide4, slide5, slide6]
files=[]
for i, s in enumerate(slides):
    im = renderers[i](s).convert('RGB')
    path = OUT / f'card-{i+1:02d}.png'
    im.save(path, quality=95)
    assert im.size == (W,H)
    files.append(path)

# contact sheet 3x2
thumb_w, thumb_h = 260, 325
sheet = Image.new('RGB',(thumb_w*3+80, thumb_h*2+110),(248,246,242))
d = ImageDraw.Draw(sheet)
for idx, p in enumerate(files):
    im = Image.open(p).convert('RGB').resize((thumb_w,thumb_h),Image.LANCZOS)
    x = 25 + (idx%3)*(thumb_w+15)
    y = 25 + (idx//3)*(thumb_h+40)
    sheet.paste(im,(x,y))
    d.text((x+thumb_w/2,y+thumb_h+20),f'{idx+1:02d}',font=font(P['pret_sb'],22),fill=INK,anchor='mm')
sheet.save(OUT/'contact-sheet.png',quality=95)

with open(OUT/'card_script.json','w',encoding='utf-8') as f:
    json.dump(slides, f, ensure_ascii=False, indent=2)

for p in files+[OUT/'contact-sheet.png', OUT/'card_script.json']:
    print(p)
