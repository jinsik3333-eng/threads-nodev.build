from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import random

OUT = Path(__file__).parent / 'output'
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1080, 1350
FONT = Path('/Users/jinsik/Library/Fonts')
REG = str(FONT/'Pretendard-Regular.otf')
MED = str(FONT/'Pretendard-Medium.otf')
SB = str(FONT/'Pretendard-SemiBold.otf')
BD = str(FONT/'Pretendard-Bold.otf')
EB = str(FONT/'Pretendard-ExtraBold.otf')

slides = [
    dict(kicker='FREE GUIDE', title=['코딩 몰라도','내 일은','직접 만들 수 있습니다'], accent='직접 만들 수 있습니다', body=['전체 가이드 무료 공개','비개발자를 위한 AI 작업 시스템'], tag='@nodev.builder', mode='cover'),
    dict(kicker='BEFORE', title=['아이디어는 있는데','구현에서','멈춘 적 있나요'], accent='구현에서', body=['회의록 정리기, 파일 정리 자동화,','콘텐츠 캘린더 같은 것들.'], tag='문제는 아이디어가 아니라 실행 순서였습니다', mode='list', chips=['회의록 정리기','파일 정리 자동화','콘텐츠 캘린더']),
    dict(kicker='REFRAME', title=['개발자가 되는 게','목표는','아닙니다'], accent='아닙니다', body=['목표, 자료, 조건, 확인 기준을 정리해','AI에게 일을 맡기는 법을 익히는 것.'], tag='코딩 강의보다 작업 지시서에 가깝습니다', mode='formula'),
    dict(kicker='WHAT WE SHOW', title=['이 계정에서는','만드는 과정을','그대로 보여드립니다'], accent='그대로 보여드립니다', body=['처음 막힌 화면, 잘못 나온 결과,','수정하는 프롬프트까지 기록합니다.'], tag='실전 기록으로 따라오는 AI 작업 시스템', mode='roadmap', chips=['Claude Code 시작하기','첫 프로젝트 만들기','업무별 워크스페이스','반복 업무 자동화']),
    dict(kicker='OPEN GUIDE', title=['전체 가이드는','공개해두었습니다'], accent='공개해두었습니다', body=['다만 처음이라면 전부 보지 말고,','입문 3단계만 먼저 따라오세요.'], tag='화면 감각 → 설치 → 첫 프로젝트', mode='steps'),
    dict(kicker='START HERE', title=['처음 시작하는','순서가 필요하면','“시작”'], accent='“시작”', body=['댓글에 “시작”이라고 남겨주세요.','입문 3단계부터 볼 순서를 DM으로 안내드릴게요.'], tag='전체 목차는 프로필 링크에도 열어두었습니다', mode='cta'),
]

def font(size, weight='reg'):
    return ImageFont.truetype({'reg':REG,'med':MED,'sb':SB,'bd':BD,'eb':EB}[weight], size)

def rgb(h):
    h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))

def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))

def bg(dark=False):
    img=Image.new('RGB',(W,H))
    pix=img.load()
    c1=rgb('#f5ecdf') if not dark else rgb('#14110f')
    c2=rgb('#e8d6c0') if not dark else rgb('#251912')
    c3=rgb('#d9eef2') if not dark else rgb('#33403c')
    for y in range(H):
        for x in range(W):
            t=(x/W*.28+y/H*.72)
            col=lerp(c1,c2,t)
            dx=(x-830)/480; dy=(y-160)/380
            blob=max(0,1-(dx*dx+dy*dy))
            col=lerp(col,c3,blob*(.45 if not dark else .22))
            dx2=(x-120)/420; dy2=(y-1180)/360
            blob2=max(0,1-(dx2*dx2+dy2*dy2))
            if blob2: col=lerp(col, rgb('#efe1cf') if not dark else rgb('#1a2422'), blob2*.24)
            pix[x,y]=col
    return img

def noise(img):
    random.seed(11)
    n=Image.new('L',img.size)
    p=n.load()
    for y in range(H):
        for x in range(W): p[x,y]=random.randint(116,140)
    return Image.blend(img, Image.merge('RGB',(n,n,n)), .028)

def rounded(d, box, r, fill, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def draw_text_lines(d, x, y, lines, fnt, fills, leading):
    for line in lines:
        fill = fills(line) if callable(fills) else fills
        d.text((x,y), line, font=fnt, fill=fill)
        y += leading
    return y

def draw_chip(d, x, y, text, dark=False, filled=False):
    f=font(27,'sb')
    b=d.textbbox((0,0),text,font=f)
    w=b[2]-b[0]+42; h=58
    rounded(d,(x,y,x+w,y+h),29,(217,255,102,255) if filled else ((255,255,255,25) if dark else (255,255,255,128)),(255,255,255,42) if dark else (32,24,18,26),1)
    d.text((x+21,y+14),text,font=f,fill=(18,16,13,255) if filled else ((255,250,242,210) if dark else (32,24,18,200)))
    return w

def draw_ui_panel(d, s, idx, dark):
    if s['mode']=='cover':
        # 첫 페이지는 카드 박스를 제거하고, 얇은 구분선 + 서명형 설명만 둔다.
        d.line((104,930,976,930),fill=(32,24,18,34),width=1)
        d.text((104,982),'무료 가이드와 실제 제작 과정을 함께 공개합니다.',font=font(32,'med'),fill=(32,24,18,152))
        d.text((104,1054),'@nodev.builder',font=font(31,'sb'),fill=(32,24,18,185))
        return
    panel_y=860
    rounded(d,(64,panel_y,1016,1236),38,(255,255,255,24) if dark else (255,255,255,132),(255,255,255,40) if dark else (32,24,18,26),1)
    if s['mode']=='list':
        y=908
        for chip in s['chips']:
            draw_chip(d,104,y,chip,dark=False)
            y+=74
    elif s['mode']=='formula':
        items=[('목표','무엇을 만들지'),('자료','무엇을 읽힐지'),('기준','언제 끝났는지')]
        x=104
        for i,(a,b) in enumerate(items):
            rounded(d,(x,912,x+260,1098),30,(255,255,255,112),(32,24,18,24),1)
            d.text((x+28,946),a,font=font(38,'bd'),fill=(32,24,18,230))
            d.text((x+28,1006),b,font=font(25,'med'),fill=(32,24,18,132))
            x+=296
    elif s['mode']=='roadmap':
        y=884
        for i,chip in enumerate(s['chips']):
            d.text((104,y+8),f'{i+1:02d}',font=font(23,'bd'),fill=(123,91,53,142))
            d.text((170,y),chip,font=font(32,'sb'),fill=(32,24,18,220))
            y+=64
        d.line((104,1148,976,1148),fill=(32,24,18,30),width=1)
    elif s['mode']=='steps':
        steps=[('01','화면 감각'),('02','설치'),('03','첫 프로젝트')]
        x=104
        for num,label in steps:
            rounded(d,(x,914,x+250,1102),30,(33,25,20,255),None,1)
            d.text((x+28,946),num,font=font(25,'bd'),fill=(217,255,102,230))
            d.text((x+28,1004),label,font=font(34,'bd'),fill=(255,250,242,255))
            x+=288
    elif s['mode']=='cta':
        draw_chip(d,104,916,'댓글 키워드: 시작',dark=True,filled=True)
        d.line((104,1010,976,1010),fill=(255,255,255,42),width=1)
        d.text((104,1052),'처음 볼 순서를 정리해서 DM으로 안내드립니다.',font=font(30,'med'),fill=(255,255,255,158))
    else:
        draw_chip(d,104,930,s['tag'],dark=dark,filled=dark)

    # panel bottom tag
    if s['mode'] not in ['cta']:
        y=1180 if s['mode']=='roadmap' else 1155
        d.text((104,y),s['tag'],font=font(27 if s['mode']=='roadmap' else 29,'sb'),fill=(255,255,255,160) if dark else (32,24,18,142))

def draw_slide(s, idx):
    dark = s['mode']=='cta'
    img=noise(bg(dark))
    d=ImageDraw.Draw(img,'RGBA')
    fg=(255,250,242,255) if dark else (30,23,18,255)
    muted=(255,255,255,150) if dark else (30,23,18,135)
    accent=(217,255,102,255) if dark else (116,82,45,255)

    # header
    brand='NODEV BUILDER'
    bf=font(22,'sb'); bw=d.textbbox((0,0),brand,font=bf)[2]
    d.text(((W-bw)/2,58),brand,font=bf,fill=(255,255,255,195) if dark else (30,23,18,138))
    d.text((910,60),f'{idx:02d} / 06',font=bf,fill=(255,255,255,105) if dark else (30,23,18,92))
    d.text((64,166),s['kicker'],font=font(23,'sb'),fill=(217,255,102,190) if dark else (124,91,54,175))

    # title
    size = 94
    if idx==1: size=92
    if idx==4: size=88
    if idx==6: size=91
    tf=font(size,'eb')
    y=245
    for line in s['title']:
        d.text((58,y),line,font=tf,fill=accent if line==s['accent'] else fg)
        y += int(size*1.04)

    # body
    yf=590 if idx != 6 else 660
    for bi, line in enumerate(s['body']):
        if idx == 1 and bi == 0:
            d.text((66,yf),line,font=font(45,'sb'),fill=accent)
            yf += 58
        else:
            d.text((66,yf),line,font=font(37 if idx!=6 else 35,'med'),fill=muted)
            yf += 52

    draw_ui_panel(d,s,idx,dark)
    return img

paths=[]
for i,s in enumerate(slides,1):
    im=draw_slide(s,i)
    p=OUT/f'card-{i:02d}.png'
    im.save(p,quality=95)
    paths.append(p)

sheet=Image.new('RGB',(2160,4050),rgb('#ded4c8'))
for i,p in enumerate(paths):
    im=Image.open(p).resize((1018,1272),Image.Resampling.LANCZOS)
    x=44+(i%2)*(1018+36); y=44+(i//2)*(1272+36)
    mask=Image.new('L',im.size,0); md=ImageDraw.Draw(mask); md.rounded_rectangle((0,0,1018,1272),radius=24,fill=255)
    sheet.paste(im,(x,y),mask)
sheet.save(OUT/'contact-sheet.png',quality=95)
print(OUT)
