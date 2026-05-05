from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import zipfile

ROOT = Path('/Users/jinsik/Desktop/Workspace/01_project_threads')
OUT = ROOT/'app/cards/episodes/20260504_second_post_content_30_campaign_ref/output'
OUT.mkdir(parents=True, exist_ok=True)
W,H = 1080,1350
CREAM=(247,244,236)
SAGE=(148,151,115)
SAGE2=(168,171,136)
BROWN=(50,28,27)
BLACK=(9,10,13)
WHITE=(255,255,255)
CYAN=(35,225,235)
MUTED=(100,98,88)
LIME=(214,222,178)
FONT_DIR=Path('/Users/jinsik/Library/Fonts')
SUIT_H=str(FONT_DIR/'SUIT-Heavy.otf')
SUIT_EB=str(FONT_DIR/'SUIT-ExtraBold.otf')
SUIT_B=str(FONT_DIR/'SUIT-Bold.otf')
SUIT_SB=str(FONT_DIR/'SUIT-SemiBold.otf')
SUIT_M=str(FONT_DIR/'SUIT-Medium.otf')
SERIF='/System/Library/Fonts/Supplemental/Georgia Italic.ttf'
SERIF_B='/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf'
MONO='/System/Library/Fonts/Menlo.ttc'
COVER_IMG=Path('/Users/jinsik/.hermes/cache/images/openai_codex_gpt-image-2-high_20260504_002542_609421fa.png')
MOOD_IMG=Path('/Users/jinsik/.hermes/cache/images/openai_codex_gpt-image-2-high_20260504_002650_10bcf489.png')

def font(path, size): return ImageFont.truetype(path, size)
def cover_crop(img, size=(W,H)):
    img=img.convert('RGB'); sw,sh=img.size; tw,th=size
    scale=max(tw/sw, th/sh); nw,nh=int(sw*scale),int(sh*scale)
    img=img.resize((nw,nh), Image.LANCZOS)
    left=(nw-tw)//2; top=(nh-th)//2
    return img.crop((left,top,left+tw,top+th))
def text_w(d, text, fnt): return d.textbbox((0,0), text, font=fnt)[2]
def text_h(d, text, fnt):
    bb=d.textbbox((0,0), text, font=fnt); return bb[3]-bb[1]
def logo(d, fill=None):
    fill = fill or BROWN
    d.text((W//2,44), 'NODEV\nBUILDER', font=font(SUIT_H,26), fill=fill, anchor='ma', align='center', spacing=-5)
def page(d, n, total=6, dark=False):
    bg=(72,72,72,180) if not dark else (24,24,27,210)
    x,y=955,48
    d.rounded_rectangle((x,y,x+88,y+52), radius=26, fill=bg)
    d.text((x+44,y+26), f'{n}/{total}', font=font(SUIT_SB,23), fill=WHITE, anchor='mm')
def pill(d, xy, txt, bg, fg, size=29, pad=22):
    x,y=xy; f=font(SUIT_B,size); tw=text_w(d,txt,f); th=text_h(d,txt,f)
    d.rounded_rectangle((x,y,x+tw+pad*2,y+th+20), radius=(th+20)//2, fill=bg)
    d.text((x+pad,y+9), txt, font=f, fill=fg)
    return x+tw+pad*2
def rounded_shadow(base, box, radius=18, fill=WHITE, shadow=(0,0,0,45), offset=(0,8), blur=16):
    layer=Image.new('RGBA',(W,H),(0,0,0,0)); sd=ImageDraw.Draw(layer)
    x1,y1,x2,y2=box; ox,oy=offset
    sd.rounded_rectangle((x1+ox,y1+oy,x2+ox,y2+oy), radius=radius, fill=shadow)
    layer=layer.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(layer)
    d=ImageDraw.Draw(base)
    d.rounded_rectangle(box, radius=radius, fill=fill)
    return d
def mock_window(d, box, title='Claude', fill=(255,255,255), dark=False):
    x1,y1,x2,y2=box
    d.rounded_rectangle(box, radius=18, fill=fill)
    bar=(236,236,232) if not dark else (36,36,38)
    d.rounded_rectangle((x1,y1,x2,y1+44), radius=18, fill=bar)
    d.rectangle((x1,y1+25,x2,y1+44), fill=bar)
    for i,c in enumerate([(238,90,85),(245,190,75),(95,190,95)]):
        d.ellipse((x1+18+i*23,y1+16,x1+29+i*23,y1+27), fill=c)
    d.text((x1+92,y1+13), title, font=font(SUIT_SB,18), fill=(80,76,68) if not dark else (215,215,210))

def slide1():
    img=cover_crop(Image.open(COVER_IMG)).convert('RGBA')
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
    od.rectangle((0,590,W,H), fill=(0,0,0,95)); od.rectangle((0,0,W,210), fill=(0,0,0,30))
    img.alpha_composite(ov); d=ImageDraw.Draw(img); logo(d, WHITE)
    d.text((62,625),'콘텐츠',font=font(SUIT_H,106),fill=WHITE)
    d.text((62,738),'30일치',font=font(SUIT_H,128),fill=WHITE)
    d.text((62,882),'Claude가',font=font(SUIT_H,112),fill=WHITE)
    d.text((62,1002),'짜줌',font=font(SUIT_H,132),fill=WHITE)
    pill(d,(62,1185),'copy-ready workflow →',bg=(122,119,82,230),fg=WHITE,size=30)
    return img

def slide2():
    im=Image.new('RGBA',(W,H),SAGE2); d=ImageDraw.Draw(im); logo(d, WHITE); page(d,2)
    x,y=78,135; items=['아이디어','훅','카드 흐름','캡션','CTA']
    for i,it in enumerate(items):
        d.rounded_rectangle((x,y+i*58,x+300,y+42+i*58), radius=8, fill=(65,43,40))
        d.rounded_rectangle((x+12,y+9+i*58,x+34,y+31+i*58), radius=4, fill=CREAM)
        d.line((x+17,y+20+i*58,x+23,y+26+i*58,x+31,y+14+i*58), fill=BROWN, width=3)
        d.text((x+52,y+9+i*58), it, font=font(SUIT_B,25), fill=WHITE)
    mood=cover_crop(Image.open(MOOD_IMG), (420,340)).resize((410,330)).convert('RGBA')
    im.alpha_composite(mood,(585,152)); d.rounded_rectangle((585,152,995,482), radius=18, outline=(255,255,255,120), width=3)
    rounded_shadow(im,(420,420,932,665),18,fill=(250,249,244,245),shadow=(0,0,0,35),blur=12)
    d=ImageDraw.Draw(im); d.text((450,450),'Prompt',font=font(SUIT_EB,20),fill=BROWN)
    small='이 주제를 30일 콘텐츠 일정표로 쪼개줘.\n훅, 카드 흐름, 캡션, CTA까지 포함해줘.'
    d.multiline_text((450,488),small,font=font(SUIT_M,24),fill=(54,48,42),spacing=10)
    d.rectangle((0,760,W,H), fill=CREAM)
    d.text((78,830),'아이디어 하나를',font=font(SUIT_H,70),fill=BROWN)
    d.text((78,908),'5가지 포맷으로',font=font(SUIT_H,70),fill=BROWN)
    d.text((78,1010),'쪼갭니다',font=font(SUIT_H,78),fill=BROWN)
    d.multiline_text((78,1138),'매일 새로 고민하는 게 아니라,\n훅, 카드 흐름, 캡션, CTA, 일정으로 나눠줍니다.',font=font(SUIT_SB,36),fill=BROWN,spacing=8)
    pill(d,(760,1225),'SWIPE',bg=(121,116,78),fg=WHITE,size=25)
    return im

def slide3():
    im=Image.new('RGBA',(W,H),SAGE); d=ImageDraw.Draw(im); logo(d, WHITE); page(d,3)
    pill(d,((W-230)//2,410),'Post Ideas',bg=(196,202,168),fg=WHITE,size=32)
    lines=['새 글을 더','짜내지 말고,','쪼개세요']; y=520
    for i,l in enumerate(lines):
        f=font(SUIT_H,78 if i<2 else 92); tw=text_w(d,l,f); color=WHITE if i<2 else BROWN
        d.text(((W-tw)//2,y),l,font=f,fill=color); y += 86
    sub='아이디어 1개를 주면\nClaude가 한 달치 구조로 나눕니다.\n막막한 건 소재가 아니라 발행 단위예요.'
    d.multiline_text((W//2,835),sub,font=font(SUIT_SB,36),fill=WHITE,anchor='ma',align='center',spacing=11)
    d.arc((815,1100,980,1260),200,300,fill=CREAM,width=3); d.line((945,1205,980,1250,925,1240),fill=CREAM,width=3)
    return im

def slide4():
    im=Image.new('RGBA',(W,H),SAGE2); d=ImageDraw.Draw(im); logo(d, WHITE); page(d,4)
    d.text((120,215),'The Prompt',font=font(SERIF,31),fill=CREAM)
    rounded_shadow(im,(92,260,490,330),10,fill=(250,248,244,245),shadow=(0,0,0,25),blur=8)
    d=ImageDraw.Draw(im);    d.text((120,282),'“콘텐츠 자동화”를 30일 일정표로',font=font(MONO,24),fill=BROWN)
    mock_window(d,(578,205,968,510),'Example Brief',fill=(252,251,247))
    d.text((610,278),'WHAT I WANT',font=font(SUIT_EB,20),fill=BROWN)
    for i,t in enumerate(['타깃: 비개발자','결과물: 카드뉴스 6장','포함: 훅 / 캡션 / CTA','톤: 쉽게, 실무적으로']):
        d.text((610,320+i*38),'✓ '+t,font=font(SUIT_M,22),fill=(64,57,49))
    d.text((108,635),'The Result',font=font(SERIF,31),fill=CREAM)
    mock_window(d,(92,690,530,860),'Output',fill=(37,37,39),dark=True)
    d.multiline_text((125,755),'DAY 01  문제 제기\nDAY 02  전환 문장\nDAY 03  프롬프트 예시\nDAY 04  결과물 구조',font=font(MONO,21),fill=(230,230,220),spacing=10)
    d.rectangle((0,940,W,H),fill=CREAM)
    d.text((78,1008),'브랜드 목소리는',font=font(SUIT_H,70),fill=BROWN)
    d.text((78,1084),'먼저 고정하세요',font=font(SUIT_H,70),fill=BROWN)
    d.multiline_text((78,1192),'주제만 던지면 매번 다른 말투가 나옵니다.\n타깃, 톤, 금지어, CTA를 먼저 정해두면 결과가 훨씬 안정적이에요.',font=font(SUIT_SB,32),fill=BROWN,spacing=8)
    return im

def slide5():
    im=Image.new('RGBA',(W,H),CREAM); d=ImageDraw.Draw(im); logo(d, BROWN); page(d,5)
    x0,y0=80,155; card_w,card_h=260,210
    labels=[('Claude','아이디어 분해'),('Notion','일정표 정리'),('Canva','카드 초안'),('Instagram','발행/저장')]
    for idx,(name,desc) in enumerate(labels):
        col=idx%2; row=idx//2; x=x0+col*360; y=y0+row*255
        rounded_shadow(im,(x,y,x+card_w,y+card_h),22,fill=(255,255,255),shadow=(0,0,0,28),blur=12); d=ImageDraw.Draw(im)
        d.ellipse((x+26,y+26,x+78,y+78),fill=(118,109,75)); d.text((x+52,y+52),str(idx+1),font=font(SUIT_H,24),fill=WHITE,anchor='mm')
        d.text((x+28,y+102),name,font=font(SUIT_H,34),fill=BROWN); d.text((x+28,y+150),desc,font=font(SUIT_SB,25),fill=MUTED)
    d.line((360,260,430,260),fill=(76,58,43),width=5); d.polygon([(430,260),(410,248),(410,272)],fill=(76,58,43))
    d.line((230,395,230,440),fill=(76,58,43),width=5); d.polygon([(230,440),(218,420),(242,420)],fill=(76,58,43))
    d.line((590,395,590,440),fill=(76,58,43),width=5); d.polygon([(590,440),(578,420),(602,420)],fill=(76,58,43))
    d.text((70,750),'한 번 돌리면',font=font(SUIT_H,84),fill=BROWN)
    d.text((70,845),'한 달 캘린더가',font=font(SUIT_H,84),fill=BROWN)
    d.text((70,940),'나옵니다',font=font(SUIT_H,84),fill=BROWN)
    d.text((705,1022),'workflow',font=font(SERIF_B,54),fill=(95,66,53))
    d.multiline_text((70,1130),'매번 처음부터 쓰는 게 아니라,\n하나의 흐름을 반복 가능한 작업판으로 만듭니다.',font=font(SUIT_SB,34),fill=BROWN,spacing=9)
    return im

def slide6():
    im=Image.new('RGBA',(W,H),BROWN); d=ImageDraw.Draw(im); logo(d, WHITE); page(d,6,dark=True)
    d.text((W//2,265),'FREE KIT',font=font(SUIT_EB,28),fill=LIME,anchor='mm')
    d.text((W//2,380),'복붙용 키트는',font=font(SUIT_H,72),fill=WHITE,anchor='mm')
    d.text((W//2,468),'프로필 링크에',font=font(SUIT_H,84),fill=WHITE,anchor='mm')
    d.text((W//2,570),'콘텐츠 30일치 프롬프트, 예시 입력값,\n검수 체크리스트까지 한 번에 정리했습니다.',font=font(SUIT_SB,32),fill=(235,230,220),anchor='ma',align='center',spacing=10)
    rounded_shadow(im,(150,720,930,990),24,fill=CREAM,shadow=(0,0,0,80),blur=20); d=ImageDraw.Draw(im)
    d.text((205,780),'30-day content prompt kit',font=font(SUIT_EB,40),fill=BROWN)
    d.text((205,850),'콘텐츠 캘린더를 바로 뽑는 복붙용 워크플로우',font=font(SUIT_M,30),fill=MUTED)
    pill(d,(205,910),'PROFILE LINK →',bg=(123,105,72),fg=WHITE,size=32)
    d.rounded_rectangle((148,1080,932,1177),radius=24,fill=WHITE)
    d.ellipse((176,1104,224,1152),fill=CYAN)
    d.text((246,1101),'@nodev.builder',font=font(SUIT_EB,33),fill=BROWN)
    d.text((246,1139),'비개발자를 위한 AI 작업 시스템',font=font(SUIT_M,24),fill=MUTED)
    d.rounded_rectangle((730,1102,905,1157),radius=17,fill=(82,95,236))
    d.text((817,1130),'Follow',font=font(SUIT_B,25),fill=WHITE,anchor='mm')
    d.text((W//2,1225),'저장해두고, 콘텐츠 막힐 때 그대로 돌려보세요.',font=font(SUIT_SB,28),fill=(235,230,220),anchor='mm')
    return im

slides=[slide1(),slide2(),slide3(),slide4(),slide5(),slide6()]
paths=[]
for i,im in enumerate(slides,1):
    p=OUT/f'card-{i:02d}.png'; im.convert('RGB').save(p, quality=95); paths.append(p)
thumbs=[Image.open(p).resize((270,338),Image.LANCZOS) for p in paths]
sheet=Image.new('RGB',(270*3+28*4,338*2+28*3),(24,24,24))
for idx,t in enumerate(thumbs):
    x=28+(idx%3)*(270+28); y=28+(idx//3)*(338+28); sheet.paste(t,(x,y))
sheet.save(OUT/'contact-sheet.png',quality=95)
post='''# 콘텐츠 30일치 Claude가 짜줌 — campaign reference version

## Upload files
card-01.png ~ card-06.png

## Caption draft
콘텐츠를 매일 새로 생각하면 금방 멈춥니다.

문제는 아이디어가 없는 게 아니라,
하나의 아이디어를 발행 가능한 형태로 쪼개는 구조가 없다는 것에 가깝습니다.

Claude에게 “좋은 아이디어 줘”가 아니라,
“이 주제를 30일 콘텐츠 일정표로 쪼개줘”라고 시켜보세요.

훅, 카드 흐름, 캡션, CTA, 발행 일정으로 나뉩니다.

복붙해서 써볼 수 있는 프롬프트 키트는 프로필 링크에 정리해뒀습니다.

저장해두고 콘텐츠 막힐 때 한 번 돌려보세요.
'''
(OUT.parent/'post.md').write_text(post, encoding='utf-8')
story='''# Storyboard

Reference-led campaign direction based on actual provided images from @adrianabubori / @mobileeditingclub, with final dark CTA inspired by Instagram closing slides.

1. Cover: premium human/editorial campaign, huge Korean+Claude headline.
2. Repurpose board: idea -> formats, top collage + bottom editorial text block.
3. Quiet statement slide: sage background, centered big message.
4. Prompt/result board: prompt, brief, output UI + bottom headline.
5. Workflow board: Claude -> Notion -> Canva -> Instagram.
6. Dark CTA: profile link resource kit + follow bar.
'''
(OUT.parent/'storyboard.md').write_text(story, encoding='utf-8')
zip_path=OUT/'second-post-content-30-campaign-ref.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in paths+[OUT/'contact-sheet.png',OUT.parent/'post.md',OUT.parent/'storyboard.md']:
        z.write(p, p.name)
print('created', OUT/'contact-sheet.png')
print('zip', zip_path, zip_path.stat().st_size)
