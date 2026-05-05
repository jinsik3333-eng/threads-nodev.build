from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json

OUT_DIR = Path('/Users/jinsik/Desktop/Workspace/01_project_threads/app/cards/episodes/20260504_cover_3_directions/character_reference_locked_6')
manifest = json.loads((OUT_DIR / 'manifest.json').read_text())
labels = {
    '01_waving':'대표 인사',
    '02_tablet_explain':'태블릿 설명',
    '03_thinking_stuck':'고민/막힘',
    '04_laptop_work':'노트북 작업',
    '05_three_steps':'3단계 안내',
    '06_cta_point':'CTA 포인트',
}
thumb = 320
label_h = 62
gap = 24
margin = 34
cols = 3
rows = 2
W = margin*2 + cols*thumb + (cols-1)*gap
H = margin*2 + 74 + rows*(thumb+label_h) + (rows-1)*gap
sheet = Image.new('RGB', (W,H), (246,239,225))
d = ImageDraw.Draw(sheet)
try:
    font_title = ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', 30)
    font = ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', 23)
    font_small = ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', 16)
except:
    font_title = font = font_small = None

d.text((margin, 24), '기준 이미지 입력 기반 캐릭터 일관성 테스트 6컷', fill=(34,32,28), font=font_title)
d.text((margin, 58), '원본 귀여운 캐릭터를 input_image로 넣고 생성', fill=(105,99,88), font=font_small)
for idx,item in enumerate(manifest):
    r = idx // cols
    c = idx % cols
    x = margin + c*(thumb+gap)
    y = 98 + r*(thumb+label_h+gap)
    img = Image.open(item['file']).convert('RGB')
    img.thumbnail((thumb,thumb), Image.LANCZOS)
    bg = Image.new('RGB',(thumb,thumb),(250,247,239))
    bg.paste(img, ((thumb-img.width)//2,(thumb-img.height)//2))
    sheet.paste(bg,(x,y))
    d.rounded_rectangle((x,y,x+thumb,y+thumb), radius=20, outline=(222,211,192), width=2)
    slug=item['slug']
    d.text((x+10,y+thumb+9), f"{item['no']:02d}. {labels.get(slug, slug)}", fill=(42,39,34), font=font)
    d.text((x+10,y+thumb+37), slug, fill=(112,104,92), font=font_small)

sheet_path = OUT_DIR / 'contact-sheet-ref-locked-6.png'
sheet.save(sheet_path, quality=95)
print(sheet_path)
