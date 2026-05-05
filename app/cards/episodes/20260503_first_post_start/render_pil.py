from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import random, math

OUT = Path(__file__).parent / 'output'
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1080, 1350
FONT = Path('/Users/jinsik/Library/Fonts')
REG = str(FONT/'Pretendard-Regular.otf')
MED = str(FONT/'Pretendard-Medium.otf')
SB = str(FONT/'Pretendard-SemiBold.otf')
BD = str(FONT/'Pretendard-Bold.otf')

slides = [
    dict(kicker='CLAUDE CODE STARTER', title=['비개발자가','Claude Code를','처음 켤 때'], accent='처음 켤 때', body=['코딩 공부보다 먼저 필요한 건','“내 일을 어떻게 맡길지” 감을 잡는 것입니다.'], tag='1~3편만 먼저 보면 됩니다'),
    dict(kicker='WHY PEOPLE STOP', title=['막히는 지점은','코딩이 아니라','첫 화면입니다'], accent='첫 화면입니다', body=['터미널, 폴더, 설치 화면.','처음엔 이게 맞는지 아닌지부터 불안합니다.'], tag='그래서 화면 감각부터'),
    dict(kicker='STEP 01', title=['1편','화면 감각','익히기'], accent='화면 감각', body=['Claude Code를 쓰기 전,','계정·화면·폴더 구조를 먼저 익힙니다.'], tag='처음 보는 화면이 덜 무서워짐'),
    dict(kicker='STEP 02', title=['2편','설치에서','막히지 않기'], accent='설치에서', body=['명령어를 외우는 게 아니라,','“성공 화면”과 “오류 화면” 기준으로 따라갑니다.'], tag='터미널이 처음이어도 가능'),
    dict(kicker='STEP 03', title=['3편','첫 프로젝트','만들기'], accent='첫 프로젝트', body=['거창한 앱이 아니어도 됩니다.','회의록 정리, 파일 정리,','콘텐츠 초안부터 시작합니다.'], tag='내 폴더에서 결과물 하나 만들기'),
    dict(kicker='GET THE GUIDE', title=['“시작” 댓글','남기면','DM으로'], accent='“시작” 댓글', body=['비개발자용 Claude Code 1~3편 링크를','DM으로 보내드릴게요.'], tag='@nodev.builder'),
]

def font(size, weight='reg'):
    mp = {'reg':REG, 'med':MED, 'sb':SB, 'bd':BD}
    return ImageFont.truetype(mp[weight], size)

def hex_to_rgb(h):
    h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))

def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))

def gradient_bg(dark=False):
    img = Image.new('RGB',(W,H))
    pix=img.load()
    c1=hex_to_rgb('#17120f' if dark else '#f3e8da')
    c2=hex_to_rgb('#241812' if dark else '#e8d4bd')
    c3=hex_to_rgb('#0d0d0d' if dark else '#d7eef3')
    for y in range(H):
        for x in range(W):
            t=(x/W*.35 + y/H*.65)
            base=lerp(c1,c2,t)
            # soft blue/green blob top-right
            dx=(x-820)/430; dy=(y-190)/350
            blob=max(0,1-(dx*dx+dy*dy))
            col=lerp(base,c3,blob*0.45)
            if dark:
                dx2=(x-220)/360; dy2=(y-1110)/390
                blob2=max(0,1-(dx2*dx2+dy2*dy2))
                col=lerp(col,hex_to_rgb('#273232'),blob2*0.25)
            pix[x,y]=col
    return img

def add_noise(img, amount=10):
    random.seed(7)
    noise = Image.new('L', img.size)
    p=noise.load()
    for y in range(H):
        for x in range(W):
            p[x,y]=random.randint(128-amount,128+amount)
    noise=noise.filter(ImageFilter.GaussianBlur(0.35))
    overlay=Image.new('RGB', img.size, (128,128,128))
    return Image.blend(img, Image.merge('RGB',(noise,noise,noise)), 0.035)

def text(draw, xy, content, fnt, fill, spacing=0):
    draw.text(xy, content, font=fnt, fill=fill, spacing=spacing)

def rounded(draw, box, r, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def draw_slide(s, idx):
    dark = idx == 6
    img = add_noise(gradient_bg(dark))
    d = ImageDraw.Draw(img, 'RGBA')
    fg = (255,250,242,255) if dark else (32,24,18,255)
    muted = (255,255,255,125) if dark else (32,24,18,110)
    accent = (217,255,102,255) if dark else (123,91,53,255)

    # header
    brand = 'NODEV BUILDER'
    bf = font(23,'sb')
    bbox=d.textbbox((0,0),brand,font=bf)
    d.text(((W-(bbox[2]-bbox[0]))/2,58),brand,font=bf,fill=(255,255,255,200) if dark else (29,23,18,140))
    d.text((910,60),f'{idx:02d} / 06',font=bf,fill=(255,255,255,115) if dark else (29,23,18,95))

    d.text((64,166),s['kicker'],font=font(23,'sb'),fill=(217,255,102,185) if dark else (124,91,54,175))

    # title
    y=245
    title_font=font(96 if not dark else 104,'bd')
    for line in s['title']:
        fill = accent if line == s['accent'] else fg
        d.text((58,y),line,font=title_font,fill=fill)
        y += 98 if not dark else 106

    # body
    y = 600 if not dark else 590
    body_font = font(38,'med')
    for line in s['body']:
        d.text((66,y),line,font=body_font,fill=(255,250,242,184) if dark else (32,24,18,158))
        y += 52

    # bottom panel
    panel=(64,904 if not dark else 924,1016,1234)
    rounded(d,panel,36,(255,255,255,132) if not dark else (255,255,255,20),(32,24,18,26) if not dark else (255,255,255,38),1)
    # subtle shadow handled by no shadow (PIL). tag
    tag_font=font(28,'bd')
    tb=d.textbbox((0,0),s['tag'],font=tag_font)
    tag_w=tb[2]-tb[0]+52; tag_h=64
    tag_box=(104,panel[1]+36,104+tag_w,panel[1]+36+tag_h)
    rounded(d,tag_box,32,(217,255,102,255) if dark else (33,25,20,255))
    d.text((130,panel[1]+52),s['tag'],font=tag_font,fill=(23,18,15,255) if dark else (255,250,242,255))
    d.line((104,panel[1]+112,976,panel[1]+112),fill=(255,255,255,35) if dark else (32,24,18,28),width=1)
    smalls = [
        '처음엔 전체를 다 보려 하지 말고,\n1~3편만 먼저 보면 됩니다.',
        '코딩 지식보다 먼저,\n내 화면이 맞는지 확인하는 게 중요합니다.',
        '계정, 폴더, 화면 위치부터\n천천히 익히면 됩니다.',
        '명령어를 외우기보다,\n성공 화면과 오류 화면을 기준으로 봅니다.',
        '회의록 정리, 파일 정리,\n콘텐츠 초안부터 시작해도 충분합니다.',
        '전체 가이드를 한 번에 보려 하지 말고,\n먼저 1~3편만 따라오면 됩니다.'
    ]
    small = smalls[idx-1]
    sy=panel[1]+154
    sf=font(29,'med')
    for line in small.split('\n'):
        d.text((104,sy),line,font=sf,fill=(255,255,255,158) if dark else (32,24,18,145))
        sy += 42

    # 큰 장식 번호는 제거: 상단 우측 페이지 번호만 사용해 템플릿 느낌을 줄인다.
    return img

paths=[]
for i,s in enumerate(slides,1):
    img=draw_slide(s,i)
    p=OUT/f'card-{i:02d}.png'
    img.save(p, quality=95)
    paths.append(p)

# contact sheet 2 x 3
sheet=Image.new('RGB',(2160,4050),hex_to_rgb('#ded4c8'))
for i,p in enumerate(paths):
    im=Image.open(p).resize((1018,1272),Image.Resampling.LANCZOS)
    x=44+(i%2)*(1018+36)
    y=44+(i//2)*(1272+36)
    mask=Image.new('L',im.size,0); md=ImageDraw.Draw(mask); md.rounded_rectangle((0,0,1018,1272),radius=24,fill=255)
    sheet.paste(im,(x,y),mask)
    lab=ImageDraw.Draw(sheet,'RGBA')
    lab.rounded_rectangle((x+20,y+20,x+76,y+54),radius=17,fill=(255,255,255,235))
    lab.text((x+35,y+27),f'{i+1:02d}',font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',18),fill=(17,17,17,255))
sheet.save(OUT/'contact-sheet.png',quality=95)
print(OUT)
