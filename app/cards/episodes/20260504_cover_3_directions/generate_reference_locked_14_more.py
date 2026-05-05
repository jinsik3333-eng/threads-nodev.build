from __future__ import annotations

import base64
import json
import sys
import time
import importlib.util
from pathlib import Path

HERMES = Path('/Users/jinsik/.hermes/hermes-agent')
sys.path.insert(0, str(HERMES))

_plugin_path = HERMES / 'plugins' / 'image_gen' / 'openai-codex' / '__init__.py'
_spec = importlib.util.spec_from_file_location('openai_codex_image_plugin', _plugin_path)
_mod = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_mod)
_build_codex_client = _mod._build_codex_client
from agent.image_gen_provider import save_b64_image  # type: ignore

REF = Path('/Users/jinsik/.hermes/cache/images/openai_codex_gpt-image-2-high_20260504_132632_dc987e9e.png')
OUT_DIR = Path('/Users/jinsik/Desktop/Workspace/01_project_threads/app/cards/episodes/20260504_cover_3_directions/character_reference_locked_20')
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Copy/manifest existing 6 first in final naming convention is handled by contact sheet script.
BASE_PROMPT = """
You are generating a reference-locked character asset for @nodev.builder.
Use the attached reference image as the strict identity reference.
Create the EXACT SAME cute 3D mascot character, not a similar new character.

Identity lock:
- identical rounded face shape and cheek volume
- identical large round black horn-rimmed glasses, same size and position
- identical low black knit beanie, not taller, not pointier
- identical short wavy bangs under the beanie, same amount of exposed hair, same direction
- identical oversized dark charcoal hoodie silhouette
- identical cute 2.8-to-3-heads-tall body proportion
- identical rounded hand size and limb proportion
- clean-shaven face: NO beard, NO mustache, NO stubble, NO facial hair
- not adult man, not developer bro, not hipster, not realistic human

Do not change the head-to-body ratio. Do not make the face slimmer. Do not make the legs longer. Do not make the glasses smaller. Do not change the hairline. Do not make the beanie taller.

Style:
- premium soft 3D mascot, warm cream studio background
- text-free, no readable letters, no logo
- simple muted teal / warm neutral props only
- clean hands, no distorted fingers
""".strip()

POSES = [
    (7, "07_error_surprise", "Pose: surprised by a small error warning icon, gentle confused expression, full body, one hand raised slightly, abstract warning shapes only."),
    (8, "08_workflow_fix", "Pose: adjusting abstract workflow node blocks with both hands, focused but cute expression, same body scale as reference."),
    (9, "09_qa_inspect", "Pose: holding a magnifying glass to inspect abstract UI cards, QA/checking mood, keep face and glasses identical."),
    (10, "10_success_check", "Pose: holding a blank checkmark board with simple check icon only, completed/success expression, full body."),
    (11, "11_thumbsup", "Pose: cheerful thumbs up beside a blank finished app window made of abstract blocks, no readable text."),
    (12, "12_tool_adjust", "Pose: holding a small rounded wrench, adjusting simple automation blocks, friendly maker expression, no complex tiny fingers."),
    (13, "13_idea_bulb", "Pose: holding a soft glowing light bulb icon, excited but gentle expression, keep the same 2.8-heads-tall proportion, do not make body thinner."),
    (14, "14_learning_manual", "Pose: reading a small manual notebook with abstract diagrams only, calm learning mood, same face and low beanie."),
    (15, "15_checklist_guide", "Pose: standing beside a blank checklist with three icon bullets, explaining the order with open palm, full body scale same as reference."),
    (16, "16_small_win", "Pose: celebrating a small win with tiny confetti shapes, holding a finished cube/app block, joyful restrained expression."),
    (17, "17_flowchart_draw", "Pose: drawing a simple flowchart in the air with a stylus, abstract connected dots only, no readable text."),
    (18, "18_mobile_result", "Pose: holding a phone mockup with abstract UI blocks, showing mobile automation result, friendly proud expression."),
    (19, "19_question_help", "Pose: helpful guide answering a question, one hand open, small empty question bubble with no text, reassuring expression."),
    (20, "20_confident_soft", "Pose: soft confident standing pose with hands relaxed near chest, not arms crossed, trust/authority but still cute and youthful, blank dashboard blocks behind."),
]


def ref_data_url() -> str:
    return 'data:image/png;base64,' + base64.b64encode(REF.read_bytes()).decode('ascii')


def collect_image_b64(client, prompt: str) -> str | None:
    image_b64 = None
    with client.responses.stream(
        model='gpt-5.4',
        store=False,
        instructions='You must use the image_generation tool. Preserve the attached reference character identity strictly; change only pose and props.',
        input=[{
            'type': 'message',
            'role': 'user',
            'content': [
                {'type': 'input_text', 'text': prompt},
                {'type': 'input_image', 'image_url': ref_data_url()},
            ],
        }],
        tools=[{
            'type': 'image_generation',
            'model': 'gpt-image-2',
            'size': '1024x1024',
            'quality': 'high',
            'output_format': 'png',
            'background': 'opaque',
            'partial_images': 1,
        }],
        tool_choice={'type': 'allowed_tools', 'mode': 'required', 'tools': [{'type': 'image_generation'}]},
    ) as stream:
        for event in stream:
            et = getattr(event, 'type', '')
            if et == 'response.output_item.done':
                item = getattr(event, 'item', None)
                if getattr(item, 'type', None) == 'image_generation_call':
                    result = getattr(item, 'result', None)
                    if isinstance(result, str) and result:
                        image_b64 = result
            elif et == 'response.image_generation_call.partial_image':
                partial = getattr(event, 'partial_image_b64', None)
                if isinstance(partial, str) and partial:
                    image_b64 = partial
        final = stream.get_final_response()
    for item in getattr(final, 'output', None) or []:
        if getattr(item, 'type', None) == 'image_generation_call':
            result = getattr(item, 'result', None)
            if isinstance(result, str) and result:
                image_b64 = result
    return image_b64


def main():
    client = _build_codex_client()
    if not client:
        raise SystemExit('NO_CLIENT')
    manifest = []
    for no, slug, pose in POSES:
        out_path = OUT_DIR / f'nodev_builder_ref_locked_{no:02d}_{slug}.png'
        if out_path.exists() and out_path.stat().st_size > 1000:
            print(f'SKIP existing {no} {slug}', flush=True)
            manifest.append({'no': no, 'slug': slug, 'file': str(out_path), 'cache': None, 'pose': pose})
            continue
        prompt = BASE_PROMPT + '\n\n' + pose
        print(f'GENERATE {no} {slug}', flush=True)
        last_err = None
        b64 = None
        for attempt in range(1, 4):
            try:
                b64 = collect_image_b64(client, prompt)
                if b64:
                    break
                last_err = RuntimeError('empty image result')
            except Exception as exc:
                last_err = exc
                print(f'RETRY {no} {slug} attempt={attempt} error={type(exc).__name__}: {str(exc)[:180]}', flush=True)
                time.sleep(4 * attempt)
        if not b64:
            raise RuntimeError(f'No image result for {slug}: {last_err}')
        cache_path = Path(save_b64_image(b64, prefix=f'nodev_ref_locked_{no:02d}_{slug}'))
        out_path.write_bytes(cache_path.read_bytes())
        manifest.append({'no': no, 'slug': slug, 'file': str(out_path), 'cache': str(cache_path), 'pose': pose})
        print(str(out_path), flush=True)
    (OUT_DIR / 'manifest_07_20.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print('DONE')
    print(str(OUT_DIR))

if __name__ == '__main__':
    main()
