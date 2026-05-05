from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os, shutil, subprocess, time, urllib.parse, socket

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "app/videos/20260505_guide_scroll"
FRAMES = OUT / "frames"
QA = OUT / "qa"
OUT.mkdir(parents=True, exist_ok=True)
QA.mkdir(parents=True, exist_ok=True)

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FPS_CAPTURE = 10
FPS_OUT = 30

FONT_DIR = Path.home() / "Library/Fonts"
FONT_SEMI = str(FONT_DIR / "SUIT-SemiBold.otf")
FONT_BOLD = str(FONT_DIR / "SUIT-ExtraBold.otf")
FONT_REG = str(FONT_DIR / "Pretendard-Regular.otf")


def find_free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def start_server():
    port = find_free_port()
    p = subprocess.Popen(
        ["python3", "-m", "http.server", str(port), "--bind", "127.0.0.1"],
        cwd=str(ROOT), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    time.sleep(0.8)
    return p, port


def make_wrapper():
    html = r'''<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#fafafa;font-family:-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo',sans-serif}
iframe{position:fixed;inset:0;width:100vw;height:100vh;border:0;background:#fff}
.scroll-hint{position:fixed;right:18px;bottom:18px;padding:8px 12px;border-radius:999px;background:rgba(26,26,46,.68);color:white;font-size:13px;font-weight:700;letter-spacing:-.02em;backdrop-filter:blur(8px);z-index:9999}
</style></head><body>
<iframe id="page"></iframe><div class="scroll-hint" id="hint">가이드 미리보기</div>
<script>
const q = new URLSearchParams(location.search);
const src = q.get('src') || '/guides/guide-02-claude-code-install.html';
const y = Number(q.get('y') || 0);
const hint = q.get('hint') || '가이드 미리보기';
document.getElementById('hint').textContent = hint;
const f = document.getElementById('page');
f.src = src;
f.addEventListener('load', () => {
  setTimeout(() => {
    try {
      const w = f.contentWindow;
      w.document.documentElement.style.scrollBehavior = 'auto';
      w.scrollTo(0, y);
      const nav = w.document.querySelector('.step-nav,.top-nav');
      if(nav){ nav.style.position = 'sticky'; nav.style.top = '0px'; }
      w.document.body.style.cursor='default';
    } catch(e) {}
  }, 80);
});
</script></body></html>'''
    (OUT / "scroll_wrapper.html").write_text(html, encoding="utf-8")


def smooth_path(max_y, seconds, fps, bounce=True):
    n = int(seconds * fps)
    vals = []
    for i in range(n):
        t = i / max(1, n-1)
        if bounce:
            # 0 -> 72% -> 58% -> 100%, like a human checking and continuing
            if t < 0.56:
                u = t / 0.56
                y = max_y * 0.72 * (0.5 - 0.5 * math.cos(math.pi * u))
            elif t < 0.72:
                u = (t - 0.56) / 0.16
                y = max_y * (0.72 - 0.14 * (0.5 - 0.5 * math.cos(math.pi * u)))
            else:
                u = (t - 0.72) / 0.28
                y = max_y * (0.58 + 0.42 * (0.5 - 0.5 * math.cos(math.pi * u)))
        else:
            y = max_y * (0.5 - 0.5 * math.cos(math.pi * t))
        vals.append(int(y))
    return vals


def chrome_screenshot(url, size, out_path):
    w, h = size
    user_dir = OUT / "chrome-profile"
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        "--disable-extensions",
        f"--user-data-dir={user_dir}",
        f"--window-size={w},{h}",
        "--force-device-scale-factor=1",
        "--hide-scrollbars",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=900",
        f"--screenshot={out_path}",
        url,
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def load_font(path, size):
    return ImageFont.truetype(path, size)


def add_subtle_caption(im, text, mode):
    # Not a designed AI poster: just a tiny screen-recording style label.
    if not text:
        return im
    W, H = im.size
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    d = ImageDraw.Draw(layer)
    fs = 34 if mode == 'vertical' else 24
    f = load_font(FONT_SEMI, fs)
    pad_x, pad_y = (30, 16) if mode == 'vertical' else (22, 12)
    bbox = d.textbbox((0,0), text, font=f)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    x = (W - tw) // 2
    y = H - th - (92 if mode == 'vertical' else 38)
    d.rounded_rectangle((x-pad_x, y-pad_y, x+tw+pad_x, y+th+pad_y), radius=28, fill=(20,22,32,150))
    d.text((x, y), text, font=f, fill=(255,255,255,245))
    out = im.convert('RGBA')
    out.alpha_composite(layer)
    return out.convert('RGB')


def build_frames(port, name, src, viewport, max_scroll, seconds, hint, caption, mode):
    frame_dir = FRAMES / name
    if frame_dir.exists():
        shutil.rmtree(frame_dir)
    frame_dir.mkdir(parents=True, exist_ok=True)
    ys = smooth_path(max_scroll, seconds, FPS_CAPTURE, bounce=True)
    wrapper = f"http://127.0.0.1:{port}/app/videos/20260505_guide_scroll/scroll_wrapper.html"
    for i, y in enumerate(ys):
        url = wrapper + "?" + urllib.parse.urlencode({"src": src, "y": y, "hint": hint})
        shot = frame_dir / f"raw_{i:04d}.png"
        chrome_screenshot(url, viewport, shot)
        im = Image.open(shot).convert('RGB')
        im = add_subtle_caption(im, caption, mode)
        im.save(frame_dir / f"frame_{i:04d}.jpg", quality=94, optimize=True)
        shot.unlink(missing_ok=True)
    return frame_dir, len(ys)


def encode(frame_dir, output, input_fps=FPS_CAPTURE, out_fps=FPS_OUT):
    cmd = [
        "ffmpeg", "-y", "-framerate", str(input_fps), "-i", str(frame_dir / "frame_%04d.jpg"),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-shortest", "-vf", f"fps={out_fps},scale=in_range=pc:out_range=tv,format=yuv420p",
        "-c:v", "libx264", "-crf", "20", "-profile:v", "high",
        "-movflags", "+faststart", "-c:a", "aac", "-b:a", "96k", str(output)
    ]
    subprocess.run(cmd, check=True)


def make_qa(video, out_img, times, thumb_w):
    tmp = QA / (out_img.stem + "_frames")
    if tmp.exists(): shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    imgs=[]
    for idx, t in enumerate(times):
        p = tmp / f"{idx:02d}.jpg"
        subprocess.run(["ffmpeg","-y","-ss",str(t),"-i",str(video),"-frames:v","1",str(p)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        im = Image.open(p).convert('RGB')
        ratio = thumb_w / im.width
        im = im.resize((thumb_w, int(im.height*ratio)), Image.Resampling.LANCZOS)
        imgs.append(im)
    sheet = Image.new('RGB', (sum(i.width for i in imgs), max(i.height for i in imgs)), (245,245,250))
    x=0
    for im in imgs:
        sheet.paste(im, (x,0)); x += im.width
    sheet.save(out_img, quality=92)


def main():
    if not Path(CHROME).exists():
        raise SystemExit("Chrome not found")
    make_wrapper()
    server, port = start_server()
    try:
        # 실제 가이드 상세 페이지를 그대로 스크롤. 세로는 모바일 화면으로 꽉 채움.
        vertical_dir, _ = build_frames(
            port=port,
            name="instagram_mobile_scroll",
            src="/guides/guide-02-claude-code-install.html",
            viewport=(1080,1920),
            max_scroll=5200,
            seconds=11.5,
            hint="실제 가이드 화면",
            caption="가이드는 이런 식으로 따라오면 됩니다",
            mode="vertical",
        )
        vertical = OUT / "nodev-guide-scroll-instagram-9x16.mp4"
        encode(vertical_dir, vertical)

        # Threads는 데스크톱 가이드가 실제로 위아래로 움직이는 화면 녹화 느낌.
        horizontal_dir, _ = build_frames(
            port=port,
            name="threads_desktop_scroll",
            src="/guides/index.html",
            viewport=(1280,720),
            max_scroll=2400,
            seconds=11.5,
            hint="가이드 페이지 스크롤",
            caption="처음엔 1~3편만 보면 됩니다",
            mode="horizontal",
        )
        horizontal = OUT / "nodev-guide-scroll-threads-16x9.mp4"
        encode(horizontal_dir, horizontal)

        make_qa(vertical, QA / "instagram-scroll-midpoints.jpg", [0.8,2.8,5.2,7.8,10.3], 240)
        make_qa(horizontal, QA / "threads-scroll-midpoints.jpg", [0.8,2.8,5.2,7.8,10.3], 300)
        for f in [vertical, horizontal, QA/"instagram-scroll-midpoints.jpg", QA/"threads-scroll-midpoints.jpg"]:
            print(f, f.stat().st_size)
    finally:
        server.terminate()
        try: server.wait(timeout=2)
        except subprocess.TimeoutExpired: server.kill()

if __name__ == "__main__":
    main()
