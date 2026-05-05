from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math, os, subprocess, shutil

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "app/videos/20260505_guide_intro"
FRAMES = OUT / "frames"
OUT.mkdir(parents=True, exist_ok=True)

FONT_DIR = Path.home() / "Library/Fonts"
FONT_BOLD = str(FONT_DIR / "SUIT-ExtraBold.otf")
FONT_SEMI = str(FONT_DIR / "SUIT-SemiBold.otf")
FONT_MED = str(FONT_DIR / "Pretendard-Medium.otf")
FONT_REG = str(FONT_DIR / "Pretendard-Regular.otf")

CARD_DIR = ROOT / "app/cards/episodes/20260504_cover_3_directions/character_carousel"
SCREEN_DIR = ROOT / "guides/assets/screens"
ASSETS = {
    "card1": CARD_DIR / "card-01.png",
    "card2": CARD_DIR / "card-02.png",
    "card3": CARD_DIR / "card-03.png",
    "card5": CARD_DIR / "card-05.png",
    "card6": CARD_DIR / "card-06.png",
    "terminal": SCREEN_DIR / "real-terminal-success.png",
    "cursor": SCREEN_DIR / "real-cursor-project.png",
}

COLORS = {
    "cream": (245, 238, 221),
    "paper": (255, 251, 242),
    "ink": (29, 43, 39),
    "green": (39, 72, 58),
    "brown": (150, 87, 50),
    "muted": (113, 104, 89),
    "line": (223, 211, 188),
    "blue": (208, 228, 238),
}

FPS = 24
SCENES = [
    {"dur": 2.2, "kind": "card", "asset": "card2", "eyebrow": "실제 화면 가이드", "title": ["아이디어는 있는데", "첫 화면에서 멈춘다면"], "sub": "문제는 의지가 아니라 시작 순서입니다"},
    {"dur": 2.4, "kind": "screen", "asset": "terminal", "eyebrow": "STEP 01", "title": ["검은 화면도", "성공 기준부터 보면 됩니다"], "sub": "답변이 보이면 일단 준비 완료"},
    {"dur": 2.4, "kind": "screen", "asset": "cursor", "eyebrow": "STEP 02", "title": ["왼쪽은 파일", "아래는 AI에게 시키는 창"], "sub": "결과는 새 문서로 남습니다"},
    {"dur": 2.3, "kind": "card", "asset": "card5", "eyebrow": "처음이라면", "title": ["입문 3단계만", "먼저 따라오세요"], "sub": "화면 감각 → 설치 → 첫 프로젝트"},
    {"dur": 2.2, "kind": "card", "asset": "card6", "eyebrow": "무료 가이드", "title": ["댓글에 ‘시작’", "순서 보내드릴게요"], "sub": "@nodev.builder"},
]


def font(path, size):
    return ImageFont.truetype(path, size)


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * max(0, min(1, t)))


def cover_resize(img, size, zoom=1.0, x_bias=0.5, y_bias=0.5):
    W, H = size
    iw, ih = img.size
    scale = max(W / iw, H / ih) * zoom
    nw, nh = int(iw * scale), int(ih * scale)
    im = img.resize((nw, nh), Image.Resampling.LANCZOS)
    x = int((nw - W) * x_bias)
    y = int((nh - H) * y_bias)
    return im.crop((x, y, x + W, y + H))


def contain_resize(img, max_size):
    W, H = max_size
    im = img.copy()
    im.thumbnail((W, H), Image.Resampling.LANCZOS)
    return im


def rounded_rect(draw, xy, r, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def draw_text_lines(draw, xy, lines, fnt, fill, spacing=10, anchor=None, align="left", stroke_width=0, stroke_fill=None):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill, anchor=anchor, align=align, stroke_width=stroke_width, stroke_fill=stroke_fill)
        bbox = draw.textbbox((x, y), line, font=fnt, stroke_width=stroke_width)
        y += (bbox[3] - bbox[1]) + spacing
    return y


def text_w(draw, text, fnt):
    b = draw.textbbox((0,0), text, font=fnt)
    return b[2]-b[0]


def make_bg(size):
    W,H = size
    base = Image.new('RGB', size, COLORS['cream'])
    d = ImageDraw.Draw(base)
    # soft editorial blobs
    d.ellipse((-W*0.20, H*0.08, W*0.46, H*0.52), fill=(238,226,203))
    d.ellipse((W*0.62, -H*0.08, W*1.18, H*0.35), fill=(227,239,239))
    d.ellipse((W*0.68, H*0.67, W*1.12, H*1.10), fill=(235,222,207))
    return base.filter(ImageFilter.GaussianBlur(0.2))


def add_chrome(canvas, platform):
    W,H = canvas.size
    d = ImageDraw.Draw(canvas)
    f_small = font(FONT_SEMI, 24 if W < H else 22)
    d.text((W//2, 42 if W < H else 34), "@nodev.builder", font=f_small, fill=COLORS['green'], anchor="mm")
    return canvas


def paste_shadow(base, im, xy, radius=28, shadow=(0,0,0,52)):
    x,y = xy
    W,H = im.size
    sh = Image.new('RGBA', (W+radius*2, H+radius*2), (0,0,0,0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle((radius, radius, radius+W, radius+H), radius=34, fill=shadow)
    sh = sh.filter(ImageFilter.GaussianBlur(radius/2))
    base.alpha_composite(sh, (x-radius, y-radius+8))
    base.alpha_composite(im, (x,y))


def rounded_image(img, radius=32, outline=True):
    im = img.convert('RGBA')
    mask = Image.new('L', im.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0,0,im.size[0],im.size[1]), radius=radius, fill=255)
    out = Image.new('RGBA', im.size, (0,0,0,0))
    out.alpha_composite(im, (0,0))
    out.putalpha(mask)
    if outline:
        layer = Image.new('RGBA', im.size, (0,0,0,0))
        ld = ImageDraw.Draw(layer)
        ld.rounded_rectangle((1,1,im.size[0]-2,im.size[1]-2), radius=radius, outline=(225,214,195,255), width=2)
        out.alpha_composite(layer)
    return out


def render_frame(size, scene, progress, platform):
    W,H = size
    portrait = H > W
    canvas = make_bg(size).convert('RGBA')
    add_chrome(canvas, platform)
    d = ImageDraw.Draw(canvas)

    f_eye = font(FONT_SEMI, 25 if portrait else 23)
    f_title = font(FONT_BOLD, 70 if portrait else 58)
    f_sub = font(FONT_MED, 32 if portrait else 29)
    f_note = font(FONT_REG, 22 if portrait else 20)

    p = ease(progress)
    img = Image.open(ASSETS[scene['asset']]).convert('RGB')

    if scene['kind'] == 'card':
        if portrait:
            # Keep the original carousel art fully inside the frame.
            # Cropping the card makes Korean headlines look broken in Reels previews.
            d.text((70, 112), scene['eyebrow'], font=f_eye, fill=COLORS['brown'])
            draw_text_lines(d, (70, 162), scene['title'], f_title, COLORS['ink'], spacing=6)
            card_max_h = 890 if scene['asset'] != 'card6' else 820
            card = contain_resize(img, (W-130, card_max_h))
            if p > 0:
                zw, zh = int(card.size[0]*(1+0.018*p)), int(card.size[1]*(1+0.018*p))
                card = card.resize((zw, zh), Image.Resampling.LANCZOS)
            card = rounded_image(card, 34)
            x = (W-card.size[0])//2
            y = 500 if scene['asset'] != 'card6' else 520
            paste_shadow(canvas, card, (x,y), radius=28)
            rounded_rect(d, (70, H-250, W-70, H-150), 30, COLORS['green'])
            d.text((104, H-200), scene['sub'], font=f_sub, fill=(255,250,240), anchor="lm")
            d.text((70, H-104), "짧게 보고, 필요한 순서만 따라오면 됩니다", font=f_note, fill=COLORS['muted'])
        else:
            # left card, right message
            card = contain_resize(img, (560, 700))
            card = rounded_image(card, 34)
            x = 78
            y = (H-card.size[1])//2 + 18
            paste_shadow(canvas, card, (x,y), radius=30)
            tx = 700
            d.text((tx, 138), scene['eyebrow'], font=f_eye, fill=COLORS['brown'])
            draw_text_lines(d, (tx, 190), scene['title'], f_title, COLORS['ink'], spacing=8)
            rounded_rect(d, (tx, 455, W-74, 540), 28, COLORS['green'])
            d.text((tx+34, 497), scene['sub'], font=f_sub, fill=(255,250,240), anchor="lm")
            d.text((tx, 612), "실제 가이드 화면을 짧게 보여주는 소개 영상", font=f_note, fill=COLORS['muted'])
    else:
        if portrait:
            # screen mockup centered, text top/bottom
            d.text((70, 110), scene['eyebrow'], font=f_eye, fill=COLORS['brown'])
            draw_text_lines(d, (70, 160), scene['title'], f_title, COLORS['ink'], spacing=6)
            screen = contain_resize(img, (W-100, 610))
            screen = rounded_image(screen, 34)
            x = (W-screen.size[0])//2
            y = 560 if H >= 1920 else 500
            # Ken Burns slight scale by resizing contained image
            if p > 0:
                zw, zh = int(screen.size[0]*(1+0.025*p)), int(screen.size[1]*(1+0.025*p))
                screen = screen.resize((zw, zh), Image.Resampling.LANCZOS)
                x = (W-zw)//2
            paste_shadow(canvas, screen, (x,y), radius=28)
            rounded_rect(d, (70, H-250, W-70, H-150), 30, COLORS['green'])
            d.text((104, H-200), scene['sub'], font=f_sub, fill=(255,250,240), anchor="lm")
            d.text((70, H-104), "비개발자도 ‘내 화면이 맞는지’ 먼저 확인할 수 있게", font=f_note, fill=COLORS['muted'])
        else:
            screen = contain_resize(img, (690, 500))
            screen = rounded_image(screen, 34)
            x = 74
            y = (H-screen.size[1])//2 + 18
            paste_shadow(canvas, screen, (x,y), radius=30)
            tx = 830
            d.text((tx, 130), scene['eyebrow'], font=f_eye, fill=COLORS['brown'])
            draw_text_lines(d, (tx, 184), scene['title'], f_title, COLORS['ink'], spacing=8)
            rounded_rect(d, (tx, 472, W-76, 558), 28, COLORS['green'])
            d.text((tx+34, 515), scene['sub'], font=f_sub, fill=(255,250,240), anchor="lm")
            d.text((tx, 626), "화면 예시 → 따라할 순서 → 댓글 CTA", font=f_note, fill=COLORS['muted'])

    # subtle progress bar
    d = ImageDraw.Draw(canvas)
    total = sum(s['dur'] for s in SCENES)
    # caller passes scene-only progress; global bar added outside in generator using monkey attr? skip per-scene bar.
    return canvas.convert('RGB')


def build(platform, size, outfile):
    frame_dir = FRAMES / platform
    if frame_dir.exists():
        shutil.rmtree(frame_dir)
    frame_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for scene in SCENES:
        frames = int(scene['dur'] * FPS)
        for i in range(frames):
            im = render_frame(size, scene, i / max(1, frames-1), platform)
            # global fade in/out per scene
            if i < 5:
                alpha = i/5
                bg = make_bg(size)
                im = Image.blend(bg, im, alpha)
            if i > frames-7:
                alpha = (frames-1-i)/6
                bg = make_bg(size)
                im = Image.blend(bg, im, max(0, alpha))
            im.save(frame_dir / f"frame_{n:05d}.jpg", quality=93, optimize=True)
            n += 1
    cmd = [
        "ffmpeg", "-y", "-framerate", str(FPS), "-i", str(frame_dir / "frame_%05d.jpg"),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-shortest", "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-r", str(FPS), "-movflags", "+faststart", "-c:a", "aac", "-b:a", "96k",
        str(outfile)
    ]
    subprocess.run(cmd, check=True)
    return n

if __name__ == "__main__":
    vertical = OUT / "nodev-guide-intro-instagram-9x16.mp4"
    landscape = OUT / "nodev-guide-intro-threads-16x9.mp4"
    print("rendering vertical...")
    nv = build("instagram", (1080, 1920), vertical)
    print("rendering landscape...")
    nl = build("threads", (1280, 720), landscape)
    for f in [vertical, landscape]:
        print(f, f.stat().st_size)
