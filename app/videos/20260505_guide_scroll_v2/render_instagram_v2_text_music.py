from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, subprocess, shutil, wave, struct, random

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "app/videos/20260505_guide_scroll/nodev-guide-real-scroll-instagram-9x16-no-caption.mp4"
OUTDIR = ROOT / "app/videos/20260505_guide_scroll_v2"
FRAMES = OUTDIR / "frames_overlay"
QA = OUTDIR / "qa"
OUTDIR.mkdir(parents=True, exist_ok=True)
QA.mkdir(parents=True, exist_ok=True)

FONT_DIR = Path.home() / "Library/Fonts"
FONT_BOLD = str(FONT_DIR / "SUIT-ExtraBold.otf")
FONT_SEMI = str(FONT_DIR / "SUIT-SemiBold.otf")
FONT_MED = str(FONT_DIR / "Pretendard-Medium.otf")

W, H = 1080, 1920
FPS = 30
DUR = 11.5

# 레퍼런스 적용: 실제 화면은 주인공으로 두고, 텍스트는 짧은 훅/판단 포인트만.
CAPTIONS = [
    # 레퍼런스 반영: 마케팅 카피보다 실제 가이드 기능을 말하는 정보형 문구.
    (0.45, 2.05, "처음 설치 기준", "화면 기준부터 보면 됩니다", "실제 화면"),
    (4.70, 6.25, "오류 예시 포함", "막히는 지점도 같이 봅니다", "가이드"),
    (9.45, 11.20, "댓글에 ‘시작’", "입문 순서 보내드릴게요", "키워드"),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def ease_out_back(x):
    x=max(0,min(1,x)); c1=1.70158; c3=c1+1
    return 1+c3*(x-1)**3+c1*(x-1)**2


def ease(x):
    x=max(0,min(1,x)); return 0.5-0.5*math.cos(math.pi*x)


def active_caption(t):
    for c in CAPTIONS:
        if c[0] <= t <= c[1]:
            return c
    return None


def rounded_text_box(base, title, sub, tag, progress, out_progress):
    layer = Image.new('RGBA', (W,H), (0,0,0,0))
    d = ImageDraw.Draw(layer)

    # 최종 업로드용: 가이드 글자 위에 얹지 않고, 상단 editorial safe band 안에만 텍스트 배치.
    alpha = int(255 * min(ease(progress*1.35), ease(out_progress*1.35)))
    if alpha <= 0:
        return base

    f_tag = font(FONT_SEMI, 20)
    f_title = font(FONT_BOLD, 54)
    f_sub = font(FONT_MED, 27)

    # full-width soft band: 배경 텍스트와 오버레이가 충돌하지 않도록 상단을 정리
    band_h = 405
    d.rectangle((0,0,W,band_h), fill=(252,250,246,int(232*alpha/255)))
    for yy in range(band_h, band_h+120):
        a = int(232 * (1-(yy-band_h)/120) * alpha/255)
        d.line((0,yy,W,yy), fill=(252,250,246,a))

    x0 = 86
    y = 166
    tag_text = tag
    gb = d.textbbox((0,0), tag_text, font=f_tag)
    d.rounded_rectangle((x0,y,x0+(gb[2]-gb[0])+30,y+34), radius=17, fill=(99,102,241,int(220*alpha/255)))
    d.text((x0+15,y+7), tag_text, font=f_tag, fill=(255,255,255,alpha))

    title_fill = (24,24,38,alpha)
    if '시작' in title:
        title_fill = (31,55,45,alpha)
    d.text((x0,y+52), title, font=f_title, fill=title_fill)
    d.text((x0+2,y+108), sub, font=f_sub, fill=(72,72,94,alpha))

    # 아주 얇은 구분선만 추가해서 광고 배너 느낌을 줄임
    d.line((86, band_h-18, W-86, band_h-18), fill=(222,218,235,int(115*alpha/255)), width=1)

    out = base.convert('RGBA')
    out.alpha_composite(layer)
    return out.convert('RGB')


def layout_for_reels(im):
    # 텍스트와 실제 가이드가 충돌하지 않도록 상단 카피 영역과 스크롤 화면 영역을 분리.
    canvas = Image.new('RGB', (W,H), (252,250,246))
    guide = im.resize((W, 1420), Image.Resampling.LANCZOS)
    canvas.paste(guide, (0, 430))
    # 하단 인스타 UI 영역으로 갈수록 살짝 밝게 처리
    layer = Image.new('RGBA', (W,H), (0,0,0,0))
    d = ImageDraw.Draw(layer)
    for yy in range(1720,H):
        a = int(130*((yy-1720)/(H-1720)))
        d.line((0,yy,W,yy), fill=(252,250,246,a))
    out = canvas.convert('RGBA'); out.alpha_composite(layer)
    return out.convert('RGB')


def add_safe_frame(base):
    # 레이아웃 분리 후에는 과한 그라데이션을 넣지 않음.
    return base


def synth_music(path, duration=DUR, sr=44100):
    # 저작권 이슈 없는 자체 생성 lo-fi soft beat. 업로드 시 인스타에서 유행음원으로 교체해도 됨.
    random.seed(7)
    bpm = 92
    beat = 60/bpm
    chords = [
        [261.63, 329.63, 392.00, 493.88],  # Cmaj7 느낌
        [220.00, 261.63, 329.63, 392.00],
        [293.66, 349.23, 440.00, 523.25],
        [196.00, 246.94, 293.66, 392.00],
    ]
    n = int(duration*sr)
    samples=[]
    prev=0.0
    for i in range(n):
        t=i/sr
        bar=int(t/(beat*4))
        local=t%(beat*4)
        chord=chords[bar%len(chords)]
        # soft pad
        pad=0
        for f in chord:
            pad += math.sin(2*math.pi*f*t) * 0.045
            pad += math.sin(2*math.pi*(f*2.003)*t) * 0.010
        pad *= 0.55 + 0.45*math.sin(math.pi*min(1, local/(beat*4)))
        # bass
        bass_f=chord[0]/2
        bass=math.sin(2*math.pi*bass_f*t)*0.055
        # kick/snare/hat envelopes
        pos=t%beat
        step=int(t/(beat/2))
        kick=0
        if pos < 0.11 and (int(t/beat)%4 in [0,2]):
            kick=math.sin(2*math.pi*(72-32*pos/0.11)*t)*math.exp(-pos*32)*0.34
        snare=0
        if pos < 0.09 and (int(t/beat)%4 in [1,3]):
            noise=(random.random()*2-1)
            snare=noise*math.exp(-pos*38)*0.10
        hat=0
        hpos=t%(beat/2)
        if hpos < 0.035:
            hat=(random.random()*2-1)*math.exp(-hpos*90)*0.035
        # tiny pluck on caption changes
        pluck=0
        for st,_,_,_,_ in CAPTIONS:
            dt=t-st
            if 0 <= dt < 0.18:
                pluck += math.sin(2*math.pi*880*t)*math.exp(-dt*22)*0.045
        val=pad+bass+kick+snare+hat+pluck
        # soft saturation + low pass-ish smoothing
        val=math.tanh(val*1.25)*0.82
        val=prev*0.08+val*0.92; prev=val
        samples.append(val)
    with wave.open(str(path),'w') as wv:
        wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(sr)
        for v in samples:
            iv=max(-32767,min(32767,int(v*32767)))
            wv.writeframes(struct.pack('<hh',iv,iv))


def render():
    if FRAMES.exists(): shutil.rmtree(FRAMES)
    FRAMES.mkdir(parents=True)
    # extract base frames
    subprocess.run(['ffmpeg','-y','-i',str(BASE),'-vf',f'fps={FPS}',str(FRAMES/'base_%04d.png')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    paths=sorted(FRAMES.glob('base_*.png'))
    for idx,p in enumerate(paths):
        t=idx/FPS
        im=Image.open(p).convert('RGB').resize((W,H), Image.Resampling.LANCZOS)
        im=layout_for_reels(im)
        im=add_safe_frame(im)
        cap=active_caption(t)
        if cap:
            st,en,title,sub,tag=cap
            prog=(t-st)/0.38
            outp=(en-t)/0.34
            im=rounded_text_box(im,title,sub,tag,prog,outp)
        im.save(FRAMES/f'frame_{idx:04d}.jpg', quality=94, optimize=True)
        p.unlink(missing_ok=True)
    music=OUTDIR/'nodev-soft-scroll-beat.wav'
    synth_music(music)
    output=OUTDIR/'nodev-guide-scroll-instagram-v8-final-layout-text-music.mp4'
    subprocess.run([
        'ffmpeg','-y','-framerate',str(FPS),'-i',str(FRAMES/'frame_%04d.jpg'),'-i',str(music),
        '-shortest','-vf','scale=in_range=pc:out_range=tv,format=yuv420p',
        '-c:v','libx264','-crf','20','-profile:v','high','-c:a','aac','-b:a','128k','-movflags','+faststart',str(output)
    ], check=True)
    # QA sheet + single frames
    times=[0.8,2.8,5.1,7.8,10.2]
    imgs=[]
    for i,t in enumerate(times):
        q=QA/f'v2_{i:02d}.jpg'
        subprocess.run(['ffmpeg','-y','-ss',str(t),'-i',str(output),'-frames:v','1',str(q)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        im=Image.open(q).convert('RGB'); r=240/im.width; im=im.resize((240,int(im.height*r)), Image.Resampling.LANCZOS); imgs.append(im)
    sheet=Image.new('RGB',(sum(i.width for i in imgs),max(i.height for i in imgs)),(245,245,250))
    x=0
    for im in imgs:
        sheet.paste(im,(x,0)); x+=im.width
    sheet.save(QA/'instagram-v8-final-layout-text-music-midpoints.jpg', quality=92)
    print(output, output.stat().st_size)
    print(music, music.stat().st_size)
    print(QA/'instagram-v7-editorial-band-music-midpoints.jpg')

if __name__=='__main__':
    render()
