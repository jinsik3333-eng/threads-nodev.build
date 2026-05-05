from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, shutil

BASE = Path('/Users/jinsik/Desktop/Workspace/01_project_threads/app/cards/episodes/20260504_cover_3_directions')
SRC6 = BASE / 'character_reference_locked_6'
OUT = BASE / 'character_reference_locked_20'
OUT.mkdir(parents=True, exist_ok=True)

items = [
(1,'01_waving','대표 인사', SRC6/'nodev_builder_ref_locked_01_01_waving.png'),
(2,'02_tablet_explain','태블릿 설명', SRC6/'nodev_builder_ref_locked_02_02_tablet_explain.png'),
(3,'03_thinking_stuck','고민/막힘', SRC6/'nodev_builder_ref_locked_03_03_thinking_stuck.png'),
(4,'04_laptop_work','노트북 작업', SRC6/'nodev_builder_ref_locked_04_04_laptop_work.png'),
(5,'05_three_steps','3단계 안내', SRC6/'nodev_builder_ref_locked_05_05_three_steps.png'),
(6,'06_cta_point','CTA 포인트', SRC6/'nodev_builder_ref_locked_06_06_cta_point.png'),
(7,'07_error_surprise','오류/당황', OUT/'nodev_builder_ref_locked_07_07_error_surprise.png'),
(8,'08_workflow_fix','흐름 수정', OUT/'nodev_builder_ref_locked_08_08_workflow_fix.png'),
(9,'09_qa_inspect','QA/검수', OUT/'nodev_builder_ref_locked_09_09_qa_inspect.png'),
(10,'10_success_check','체크/완료', OUT/'nodev_builder_ref_locked_10_10_success_check.png'),
(11,'11_thumbsup','잘 됨/엄지', OUT/'nodev_builder_ref_locked_11_11_thumbsup.png'),
(12,'12_tool_adjust','도구로 조정', OUT/'nodev_builder_ref_locked_12_12_tool_adjust.png'),
(13,'13_idea_bulb','아이디어', OUT/'nodev_builder_ref_locked_13_13_idea_bulb.png'),
(14,'14_learning_manual','학습/매뉴얼', OUT/'nodev_builder_ref_locked_14_14_learning_manual.png'),
(15,'15_checklist_guide','체크리스트 안내', OUT/'nodev_builder_ref_locked_15_15_checklist_guide.png'),
(16,'16_small_win','작은 성취', OUT/'nodev_builder_ref_locked_16_16_small_win.png'),
(17,'17_flowchart_draw','흐름도 그리기', OUT/'nodev_builder_ref_locked_17_17_flowchart_draw.png'),
(18,'18_mobile_result','모바일 결과', OUT/'nodev_builder_ref_locked_18_18_mobile_result.png'),
(19,'19_question_help','질문/도움', OUT/'nodev_builder_ref_locked_19_19_question_help.png'),
(20,'20_confident_soft','신뢰/자신감', OUT/'nodev_builder_ref_locked_20_20_confident_soft.png'),
]
manifest=[]
for no, slug, label, src in items:
    final = OUT / f'nodev_builder_ref_locked_{no:02d}_{slug}.png'
    if src != final:
        shutil.copy2(src, final)
    manifest.append({'no':no,'slug':slug,'label':label,'file':str(final)})

thumb=260; label_h=58; gap=18; margin=28; cols=5; rows=4
W=margin*2+cols*thumb+(cols-1)*gap
H=margin*2+76+rows*(thumb+label_h)+(rows-1)*gap
sheet=Image.new('RGB',(W,H),(246,239,225))
d=ImageDraw.Draw(sheet)
try:
    font_title=ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc',30)
    font=ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc',20)
    font_small=ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc',15)
except:
    font_title=font=font_small=None

d.text((margin,20),'@nodev.builder 기준 이미지 입력 기반 캐릭터 20종',fill=(34,32,28),font=font_title)
d.text((margin,56),'원본 귀여운 캐릭터를 input_image로 고정해 포즈/상황만 확장',fill=(105,99,88),font=font_small)
for idx,item in enumerate(manifest):
    r=idx//cols; c=idx%cols
    x=margin+c*(thumb+gap); y=92+r*(thumb+label_h+gap)
    img=Image.open(item['file']).convert('RGB')
    img.thumbnail((thumb,thumb), Image.LANCZOS)
    bg=Image.new('RGB',(thumb,thumb),(250,247,239))
    bg.paste(img,((thumb-img.width)//2,(thumb-img.height)//2))
    sheet.paste(bg,(x,y))
    d.rounded_rectangle((x,y,x+thumb,y+thumb),radius=18,outline=(222,211,192),width=2)
    d.text((x+8,y+thumb+8),f"{item['no']:02d}. {item['label']}",fill=(45,43,38),font=font)
    d.text((x+8,y+thumb+34),item['slug'],fill=(105,99,88),font=font_small)

sheet_path=OUT/'contact-sheet-ref-locked-20.png'
sheet.save(sheet_path,quality=95)
(OUT/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
readme=['# @nodev.builder reference-locked character set 20','',f'Contact sheet: `{sheet_path}`','']
for item in manifest:
    readme.append(f"{item['no']:02d}. {item['label']} — `{Path(item['file']).name}`")
(OUT/'README.md').write_text('\n'.join(readme))
print(sheet_path)
print(OUT)
