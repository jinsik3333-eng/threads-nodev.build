from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import zipfile, math, random

W, H = 1080, 1350
ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'output'
OUT.mkdir(parents=True, exist_ok=True)

FONT_DIRS = [Path('/Users/jinsik/Library/Fonts'), Path('/System/Library/Fonts'), Path('/Library/Fonts')]
def find_font(names):
    for d in FONT_DIRS:
        for n in names:
            hits = list(d.glob(n))
            if hits:
                return str(hits[0])
    return '/System/Library/Fonts/AppleSDGothicNeo.ttc'

FONT_BOLD = find_font(['SUIT-Heavy*.otf','SUIT-ExtraBold*.otf','Pretendard-ExtraBold*.otf','Pretendard-Bold*.otf'])
FONT_SEMI = find_font(['SUIT-SemiBold*.otf','Pretendard-SemiBold*.otf','Pretendard-Medium*.otf'])

def font(path, size):
    return ImageFont.truetype(path, size)

C = {
    'bg': (247, 242, 233), 'paper': (255, 252, 244), 'ink': (31, 38, 49),
    'muted': (96, 102, 111), 'blue': (73, 143, 203), 'dark': (29, 39, 51),
    'line': (222, 214, 201), 'blue2': (224, 239, 249)
}

slides = [
    dict(no='01', kicker='CONTENT SYSTEM', title=['콘텐츠 30일치', 'Claude가 짜줌'], accent=[0], body='아이디어 하나를 한 달치 발행 재료로 바꾸는 방법', note='무료 프롬프트 키트 → 프로필 링크', layout='cover'),
    dict(no='02', kicker='PROBLEM', title=['매일 새로 생각하면', '계정은 멈춥니다'], accent=[1], body='문제는 아이디어 부족이 아니라, 발행 구조가 없다는 것.', chips=['빈 캘린더','밀린 초안','반복 고민'], layout='editorial'),
    dict(no='03', kicker='TURN', title=['더 짜지 말고', '쪼개세요'], accent=[1], body='하나의 주제를 훅, 캡션, 카드, 캘린더 단위로 나눕니다.', chips=['HOOK','CAPTION','CALENDAR'], layout='split'),
    dict(no='04', kicker='PROMPT', title=['결과물 형식까지', '먼저 요청하세요'], accent=[0], body='“좋은 아이디어 줘”보다 “30일 일정표로 쪼개줘”가 더 명확합니다.', chips=['주제 1개','포맷 5개','30일 일정표'], layout='prompt'),
    dict(no='05', kicker='OUTPUT', title=['아이디어만 말고', '바로 올릴 재료'], accent=[1], body='훅, 카드 흐름, 캡션, CTA까지 한 번에 묶어둡니다.', chips=['CAROUSEL','REELS','CAPTION'], layout='board'),
    dict(no='06', kicker='FREE KIT', title=['복붙용 키트는', '프로필 링크에'], accent=[0], body='프롬프트 · 예시 입력값 · 검수 체크리스트를 바로 복사해 쓸 수 있게 정리했어요.', note='프로필 링크 눌러 무료 키트 받기 →', layout='cta'),
]

def rounded(draw, box, r, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def shadow_panel(img, box, r=36, fill=(255,252,244,246)):
    layer = Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(layer)
    x1,y1,x2,y2=box
    rounded(d,(x1+10,y1+14,x2+10,y2+14),r,(74,64,45,25))
    layer = layer.filter(ImageFilter.GaussianBlur(8)); img.alpha_composite(layer)
    d=ImageDraw.Draw(img)
    rounded(d,box,r,fill,outline=(238,231,218,220),width=2)

def base_bg(seed=0):
    random.seed(seed)
    img = Image.new('RGBA',(W,H),C['bg']+(255,)); px=img.load()
    for y in range(H):
        for x in range(W):
            cool = 24 if (x > W*0.56 and y < H*0.58) else 0
            warm = int(9*math.sin((x+y)/230))
            px[x,y]=(min(255,C['bg'][0]+warm), min(255,C['bg'][1]+warm+cool//4), min(255,C['bg'][2]+warm+cool),255)
    d=ImageDraw.Draw(img)
    for x in range(70,W,70): d.line((x,0,x,H), fill=(255,255,255,24), width=1)
    for y in range(80,H,80): d.line((0,y,W,y), fill=(255,255,255,18), width=1)
    for _ in range(4):
        cx=random.randint(-100,W+80); cy=random.randint(-80,H+80); rr=random.randint(150,290)
        d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr), fill=(210,230,245,28))
    return img

def header(d, no):
    d.text((W//2,68),'@nodev.builder',font=font(FONT_SEMI,28),fill=(80,86,94),anchor='mm')
    d.text((W-92,68),no,font=font(FONT_BOLD,28),fill=(74,80,89),anchor='mm')

def text_wrap(draw, text, f, maxw):
    out=[]; cur=''
    for word in text.split(' '):
        test=(cur+' '+word).strip()
        if draw.textlength(test,font=f) <= maxw:
            cur=test
        else:
            if cur: out.append(cur)
            cur=word
    if cur: out.append(cur)
    return out

def draw_title(d, lines, x, y, accent=None, size=98, align='left'):
    yy=y; accent=accent or []
    for i,line in enumerate(lines):
        s=size if len(line)<=9 else size-8
        f=font(FONT_BOLD,s); fill=C['blue'] if i in accent else C['ink']
        d.text((x,yy),line,font=f,fill=fill,anchor='lt' if align=='left' else 'mt')
        yy += s + 16
    return yy

def body(d, text, x, y, w=760, size=34, align='left'):
    f=font(FONT_SEMI,size); yy=y
    for line in text_wrap(d,text,f,w):
        if align == 'center': d.text((x+w/2,yy),line,font=f,fill=C['muted'],anchor='mt')
        else: d.text((x,yy),line,font=f,fill=C['muted'])
        yy += size + 18
    return yy

def kicker(d, text, x, y, center=False):
    f=font(FONT_BOLD,25); bw=d.textlength(text,font=f)+34
    xx=x-bw/2 if center else x
    rounded(d,(xx,y,xx+bw,y+43),22,(255,255,255,230),outline=(227,219,205,210))
    d.text((xx+17,y+10),text,font=f,fill=C['blue'])

def chips(d, arr, x, y):
    f=font(FONT_BOLD,27); xx=x
    for c in arr:
        bw=d.textlength(c,font=f)+42
        rounded(d,(xx,y,xx+bw,y+54),27,(255,255,255,238),outline=(225,217,204,230))
        d.text((xx+21,y+14),c,font=f,fill=C['dark'])
        xx += bw + 14

def note_pill(d, text, x, y, center=False):
    f=font(FONT_BOLD,31); bw=d.textlength(text,font=f)+62
    xx=x-bw/2 if center else x
    rounded(d,(xx,y,xx+bw,y+72),36,C['dark']+(246,))
    d.text((xx+31,y+20),text,font=f,fill=(255,255,255))

def mini_cards(d, x, y, scale=1.0):
    # 장식이 아니라 메시지 보조용. 요소 수를 줄여 난잡함을 막는다.
    items=[('HOOK','첫 문장'),('CARD','6장 흐름'),('CTA','다음 행동')]
    for i,(a,b) in enumerate(items):
        xx=x+(i%2)*235*scale; yy=y+(i//2)*150*scale
        rounded(d,(xx,yy,xx+208*scale,yy+120*scale),26,(255,255,255,224),outline=(224,216,202,230))
        d.text((xx+22*scale,yy+19*scale),a,font=font(FONT_BOLD,int(25*scale)),fill=C['blue'])
        d.text((xx+22*scale,yy+62*scale),b,font=font(FONT_SEMI,int(25*scale)),fill=C['ink'])

def calendar(d, x, y):
    rounded(d,(x,y,x+420,y+330),34,(255,255,255,220),outline=(225,217,203,230),width=2)
    d.text((x+34,y+30),'30 DAY PLAN',font=font(FONT_BOLD,30),fill=C['blue'])
    for r in range(4):
        for c in range(5):
            xx=x+35+c*72; yy=y+88+r*50
            fill=(229,240,248,230) if (r+c)%3==0 else (242,236,226,220)
            rounded(d,(xx,yy,xx+48,yy+32),12,fill)

def one_to_thirty(d, x, y):
    d.ellipse((x,y,x+300,y+300), fill=(226,240,250,190), outline=(203,225,241,210), width=2)
    d.text((x+150,y+98),'1',font=font(FONT_BOLD,88),fill=C['ink'],anchor='mm')
    d.text((x+150,y+154),'→',font=font(FONT_BOLD,48),fill=C['blue'],anchor='mm')
    d.text((x+150,y+222),'30',font=font(FONT_BOLD,92),fill=C['blue'],anchor='mm')

def output_stack(d, x, y):
    items=[('01','훅'),('02','카드 흐름'),('03','캡션 + CTA')]
    for i,(n,t) in enumerate(items):
        yy=y+i*94
        rounded(d,(x,yy,x+650,yy+72),24,(255,255,255,230),outline=(224,216,202,230))
        d.text((x+28,yy+19),n,font=font(FONT_BOLD,26),fill=C['blue'])
        d.text((x+92,yy+17),t,font=font(FONT_BOLD,31),fill=C['ink'])

def make(slide, idx):
    img=base_bg(idx); d=ImageDraw.Draw(img); header(d,slide['no']); layout=slide['layout']
    if layout=='cover':
        shadow_panel(img,(70,150,880,705),42); d=ImageDraw.Draw(img)
        kicker(d,slide['kicker'],112,198); yy=draw_title(d,slide['title'],112,278,slide['accent'],104)
        body(d,slide['body'],112,yy+28,620,35); mini_cards(d,620,775,0.95); calendar(d,85,820); note_pill(d,slide['note'],82,1190)
    elif layout=='editorial':
        shadow_panel(img,(74,175,1006,705),42); d=ImageDraw.Draw(img)
        kicker(d,slide['kicker'],118,225); yy=draw_title(d,slide['title'],118,310,slide['accent'],96)
        by=body(d,slide['body'],118,yy+26,760,34); chips(d,slide['chips'],118,by+32); calendar(d,610,780)
    elif layout=='split':
        shadow_panel(img,(72,150,650,690),42); d=ImageDraw.Draw(img)
        kicker(d,slide['kicker'],118,205); yy=draw_title(d,slide['title'],118,292,slide['accent'],106)
        by=body(d,slide['body'],118,yy+26,460,34); chips(d,slide['chips'],118,by+32); one_to_thirty(d,710,295)
        d.line((160,850,920,850),fill=(198,211,222,160),width=3); d.text((540,895),'아이디어 하나 → 여러 발행물',font=font(FONT_BOLD,38),fill=C['blue'],anchor='mm')
    elif layout=='prompt':
        shadow_panel(img,(78,160,1002,715),42); d=ImageDraw.Draw(img)
        kicker(d,slide['kicker'],124,215); yy=draw_title(d,slide['title'],124,300,slide['accent'],92)
        by=body(d,slide['body'],124,yy+24,770,33); chips(d,slide['chips'],124,by+32)
        shadow_panel(img,(116,825,964,1118),34,(255,255,255,220)); d=ImageDraw.Draw(img)
        d.text((156,870),'Claude에게 이렇게 요청',font=font(FONT_BOLD,35),fill=C['ink'])
        d.text((156,940),'“이 주제를 30일 일정표로 쪼개줘.”',font=font(FONT_BOLD,42),fill=C['blue'])
        d.text((156,1020),'포맷 · 훅 · 캡션 · CTA까지 포함해서',font=font(FONT_SEMI,30),fill=C['muted'])
    elif layout=='board':
        shadow_panel(img,(80,170,1000,720),42); d=ImageDraw.Draw(img)
        kicker(d,slide['kicker'],126,225); yy=draw_title(d,slide['title'],126,310,slide['accent'],98)
        by=body(d,slide['body'],126,yy+26,760,34); chips(d,slide['chips'],126,by+32); output_stack(d,215,835)
    elif layout=='cta':
        shadow_panel(img,(120,210,960,800),50); d=ImageDraw.Draw(img)
        kicker(d,slide['kicker'],540,272,True); yy=draw_title(d,slide['title'],540,370,slide['accent'],98,'center')
        body(d,slide['body'],190,yy+30,700,34,'center'); mini_cards(d,300,865,0.9); note_pill(d,slide['note'],540,1058,True)
    return img.convert('RGB')

paths=[]
for i,sl in enumerate(slides,1):
    p=OUT/f'card-{i:02d}.png'; make(sl,i).save(p,quality=95); paths.append(p)
thumbs=[]
for p in paths:
    im=Image.open(p); im.thumbnail((270,338)); thumbs.append(im.copy())
sheet=Image.new('RGB',(270*3+40,338*2+30),(246,242,235))
for i,im in enumerate(thumbs): sheet.paste(im,(10+(i%3)*280,10+(i//3)*348))
sheet.save(OUT/'contact-sheet.png',quality=95)
(ROOT/'storyboard.md').write_text('# 두 번째 게시글 readable v2\n\n얼굴 가림/AI 모델컷/난잡한 이미지 주도 문제를 제거한 버전. 인물 이미지는 제외하고, 짐코딩식 가독성/정보 위계를 우선한다.\n')
(ROOT/'post.md').write_text('# 두 번째 게시글 — 콘텐츠 30일치 Claude가 짜줌 readable v2\n\n## 업로드 파일\n- output/card-01.png ~ output/card-06.png\n\n## 캡션 초안\n콘텐츠를 매일 새로 생각하면 금방 멈춥니다.\n\n문제는 아이디어가 없는 게 아니라, 하나의 아이디어를 발행 가능한 형태로 쪼개는 구조가 없다는 것에 가깝습니다.\n\n저는 Claude에게 이렇게 시킵니다.\n\n“좋은 아이디어 줘”가 아니라, “이 주제를 30일 콘텐츠 일정표로 쪼개줘.”\n\n그러면 하나의 주제가 훅, 카드 흐름, 캡션, CTA, 발행 일정으로 나뉩니다.\n\n복붙해서 써볼 수 있는 프롬프트 키트는 프로필 링크에 열어둘게요.\n')
zip_path=OUT/'second-post-content-30-readable-v2.zip'
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for p in paths: z.write(p,p.name)
    z.write(OUT/'contact-sheet.png','contact-sheet.png'); z.write(ROOT/'storyboard.md','storyboard.md'); z.write(ROOT/'post.md','post.md')
print(OUT); print(zip_path)
