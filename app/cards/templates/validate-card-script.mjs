#!/usr/bin/env node
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const root = path.resolve(__dirname);
const registryPath = path.join(root, 'template-registry.json');
const scriptPath = process.argv[2]
  ? path.resolve(process.argv[2])
  : path.resolve(process.cwd(), 'card_script.json');

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exitCode = 1;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

const registry = readJson(registryPath);
const script = readJson(scriptPath);
const templateIds = new Set(registry.templates.map(t => t.id));
const allowedImageRoles = new Set(['none', 'desire_hook', 'proof', 'transition', 'comparison', 'detail_check', 'asset_mockup', 'mood_bridge']);
const allowedJobs = new Set(['brand_identification', 'hook_message', 'story_progression', 'proof_result', 'content_preview', 'instruction', 'comparison_basis', 'cta_action', 'visual_rhythm_break', 'decoration_only']);

if (script.format?.width !== 1080 || script.format?.height !== 1350) fail('format must be 1080x1350');
if (script.format?.platform !== 'instagram-carousel') fail('platform must be instagram-carousel');
if (script.brand?.account_position !== 'top-center') fail('brand.account_position must be top-center');
if (script.brand?.required_on_all_slides !== true) fail('brand.required_on_all_slides must be true');
if ((script.font_policy?.min_readable_px ?? 0) < 22) fail('font_policy.min_readable_px must be >= 22');
if (!Array.isArray(script.slides) || script.slides.length === 0) fail('slides must be a non-empty array');

const seenSlideIds = new Set();
for (const slide of script.slides || []) {
  const prefix = `slide ${slide.slide_id || '(missing)'}`;
  if (!/^\d{2}$/.test(slide.slide_id || '')) fail(`${prefix}: slide_id must be 2 digits`);
  if (seenSlideIds.has(slide.slide_id)) fail(`${prefix}: duplicate slide_id`);
  seenSlideIds.add(slide.slide_id);

  if (!slide.role) fail(`${prefix}: role is required`);
  if (!templateIds.has(slide.template_id)) fail(`${prefix}: unknown template_id ${slide.template_id}`);
  if (!slide.message || slide.message.length < 5) fail(`${prefix}: message is too short`);
  if (!Array.isArray(slide.headline) || slide.headline.length < 1 || slide.headline.length > 4) fail(`${prefix}: headline must be 1-4 lines`);
  if (!allowedImageRoles.has(slide.image_role)) fail(`${prefix}: invalid image_role ${slide.image_role}`);
  if (!slide.visual_direction) fail(`${prefix}: visual_direction is required`);

  if (!Array.isArray(slide.elements) || slide.elements.length === 0) fail(`${prefix}: elements must be non-empty`);
  const hasBrand = slide.elements.some(e => e.job === 'brand_identification' && e.content === script.brand.account_name);
  if (script.brand.required_on_all_slides && !hasBrand) fail(`${prefix}: missing brand element ${script.brand.account_name}`);

  if (slide.image_role !== 'none') {
    const hasImageLike = slide.elements.some(e => ['image', 'mockup'].includes(e.type));
    if (!hasImageLike) fail(`${prefix}: image_role is ${slide.image_role} but no image/mockup element exists`);
  }

  for (const el of slide.elements) {
    const ep = `${prefix} element ${el.id || '(missing)'}`;
    if (!el.id) fail(`${ep}: id is required`);
    if (!el.type) fail(`${ep}: type is required`);
    if (!allowedJobs.has(el.job)) fail(`${ep}: invalid job ${el.job}`);
    if (typeof el.content !== 'string') fail(`${ep}: content must be string`);
    if (!Number.isInteger(el.priority) || el.priority < 1 || el.priority > 5) fail(`${ep}: priority must be 1-5`);
    if (typeof el.must_be_readable !== 'boolean') fail(`${ep}: must_be_readable must be boolean`);
    if (el.job !== 'decoration_only' && !el.notes) fail(`${ep}: notes required for non-decoration elements`);
  }

  if (slide.slide_id === '05') {
    const combined = `${slide.headline.join(' ')} ${slide.support_copy} ${slide.elements.map(e => e.content).join(' ')}`;
    const toolNames = ['Claude', 'Notion', 'Canva', 'Instagram'];
    const toolCount = toolNames.filter(t => combined.includes(t)).length;
    if (slide.template_id === 'T06_STORYBOARD_PREVIEW' && toolCount >= 3) {
      fail(`${prefix}: storyboard slide looks like a tool network`);
    }
  }
}

if (!process.exitCode) {
  console.log(`PASS: ${scriptPath}`);
  console.log(`slides: ${script.slides.length}`);
  console.log(`templates used: ${[...new Set(script.slides.map(s => s.template_id))].join(', ')}`);
}
