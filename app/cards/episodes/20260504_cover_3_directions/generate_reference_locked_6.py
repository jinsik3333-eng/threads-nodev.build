from __future__ import annotations

import base64
import json
import sys
from pathlib import Path
from datetime import datetime

HERMES = Path('/Users/jinsik/.hermes/hermes-agent')
sys.path.insert(0, str(HERMES))

import importlib.util

_plugin_path = HERMES / 'plugins' / 'image_gen' / 'openai-codex' / '__init__.py'
_spec = importlib.util.spec_from_file_location('openai_codex_image_plugin', _plugin_path)
_mod = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_mod)
_build_codex_client = _mod._build_codex_client

from agent.image_gen_provider import save_b64_image  # type: ignore

REF = Path('/Users/jinsik/.hermes/cache/images/openai_codex_gpt-image-2-high_20260504_132632_dc987e9e.png')
OUT_DIR = Path('/Users/jinsik/Desktop/Workspace/01_project_threads/app/cards/episodes/20260504_cover_3_directions/character_reference_locked_6')
OUT_DIR.mkdir(parents=True, exist_ok=True)

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
    ("01_waving", "Pose: friendly representative waving hello, relaxed smile, full body, useful for cover/profile intro."),
    ("02_tablet_explain", "Pose: holding a tablet with abstract workflow nodes, explaining with one open palm."),
    ("03_thinking_stuck", "Pose: gentle thinking / stuck expression, one hand near chin, blank abstract problem screen beside the character."),
    ("04_laptop_work", "Pose: working on a laptop, focused but cute expression, abstract UI blocks behind with no text."),
    ("05_three_steps", "Pose: presenting three blank rounded step cards, guide/explainer gesture."),
    ("06_cta_point", "Pose: pointing to an empty speech bubble or blank CTA panel, friendly guide expression."),
]


def ref_data_url() -> str:
    data = base64.b64encode(REF.read_bytes()).decode('ascii')
    return f'data:image/png;base64,{data}'


def collect_image_b64(client, prompt: str) -> str | None:
    image_b64 = None
    with client.responses.stream(
        model='gpt-5.4',
        store=False,
        instructions='You must use the image_generation tool to create a new image. Preserve the attached reference character identity strictly.',
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
        tool_choice={
            'type': 'allowed_tools',
            'mode': 'required',
            'tools': [{'type': 'image_generation'}],
        },
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
    import time
    for idx, (slug, pose) in enumerate(POSES, 1):
        prompt = BASE_PROMPT + "\n\n" + pose
        out_path = OUT_DIR / f'nodev_builder_ref_locked_{idx:02d}_{slug}.png'
        if out_path.exists() and out_path.stat().st_size > 1000:
            print(f'SKIP existing {idx} {slug}', flush=True)
            manifest.append({'no': idx, 'slug': slug, 'file': str(out_path), 'cache': None, 'pose': pose})
            continue
        print(f'GENERATE {idx} {slug}', flush=True)
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
                print(f'RETRY {idx} {slug} attempt={attempt} error={type(exc).__name__}: {str(exc)[:160]}', flush=True)
                time.sleep(3 * attempt)
        if not b64:
            raise RuntimeError(f'No image result for {slug}: {last_err}')
        cache_path = Path(save_b64_image(b64, prefix=f'nodev_ref_locked_{idx:02d}_{slug}'))
        out_path.write_bytes(cache_path.read_bytes())
        manifest.append({'no': idx, 'slug': slug, 'file': str(out_path), 'cache': str(cache_path), 'pose': pose})
        print(str(out_path), flush=True)
    (OUT_DIR / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print('DONE')
    print(str(OUT_DIR))

if __name__ == '__main__':
    main()
