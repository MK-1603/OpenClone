#!/usr/bin/env python3
"""OpenClone repository quality gate. Validates structure, names, schemas, fixtures and internal Markdown links."""
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
errors = []; warnings = []

required = [
    'README.md',
    'PROJECT.md',
    'AGENTS.md',
    'LICENSE',
    'NOTICE',
    'VERSION',
    'docs/legal/LICENSE-DECISION.md',
    'framework/templates/PROJECT.template.md',
    'framework/templates/AGENTS.template.md',
    'project/PROJECT.md.template',
    'project/AGENTS.md.template',
    'framework/workflows/WF-013-PROJECT-DEFINITION-ASSESSMENT-AND-IMPLEMENTATION-PLANNING.md',
    'tools/openclone_runtime/project.py',
    'tools/openclone_runtime/templates/PROJECT.md.template.md',
    'docs/concepts/OPENCLONE-MISSION-AND-SCOPE.md',
    'framework/domains/00-GOVERNANCE/OPENCLONE-RULEBOOK.md',
    'framework/modes/MODE-1-PROBLEM-DISCOVERY.md',
    'framework/modes/MODE-2-NEW-PROJECT.md',
    'framework/modes/MODE-3-EXISTING-PROJECT.md',
    'framework/prompts/MASTER-ENTRY-PROMPT.md',
    'framework/reference-projects/DEVTRACK/README.md',
    'docs/guides/RELEASE-READINESS.md',
    'docs/guides/project-lifecycle/PROJECT-AND-AGENT-FILES.md',
    'framework/rules/RULE-PRECEDENCE-AND-CONFLICT-RESOLUTION.md',
    'global/core/OPENCLONE-GLOBAL.md',
]

for rel in required:
    if not (ROOT / rel).is_file():
        errors.append(f'Missing required file: {rel}')

# Domains in framework/domains
domain_dirs = sorted([p.name for p in (ROOT / 'framework/domains').iterdir() if p.is_dir() and re.match(r'^\d\d-', p.name)])
if len(domain_dirs) != 31:
    errors.append(f'Expected 31 domains in framework/domains/; found {len(domain_dirs)}')

root_numbered = [p.name for p in ROOT.iterdir() if p.is_dir() and re.match(r'^\d\d-', p.name)]
if root_numbered:
    errors.append(f'Numbered domains must live in framework/domains/, found at root: {root_numbered}')

engines = sorted((ROOT / 'framework/engines').glob('E-*.md'))
schemas = sorted((ROOT / 'framework/schemas').glob('*.schema.json'))

if len(engines) != 56:
    errors.append(f'Expected 56 engine specs in framework/engines/; found {len(engines)}')

ids = []
for p in engines:
    m = re.match(r'E-(\d{3})-', p.name)
    if not m:
        errors.append(f'Invalid engine filename: {p.relative_to(ROOT)}')
    else:
        ids.append(int(m.group(1)))
    if '## Engine-specific execution contract' not in p.read_text(encoding='utf-8'):
        errors.append(f'Missing engine-specific contract: {p.name}')

if sorted(ids) != list(range(1, 57)):
    errors.append('Engine IDs must be exactly E-001 through E-056')

if len(schemas) < 8:
    errors.append(f'Expected at least 8 schemas in framework/schemas/; found {len(schemas)}')

for p in schemas:
    try:
        data = json.loads(p.read_text(encoding='utf-8'))
        if data.get('$schema') != 'https://json-schema.org/draft/2020-12/schema':
            errors.append(f'{p.name}: incorrect JSON Schema draft')
    except Exception as e:
        errors.append(f'{p.name}: invalid JSON: {e}')

fixtures = list((ROOT / 'tests/fixtures').glob('*.json'))
for p in fixtures:
    try:
        json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:
        errors.append(f'{p.relative_to(ROOT)}: invalid JSON: {e}')

# Validate all SVG assets parse as valid XML
import xml.etree.ElementTree as ET
for svg_p in ROOT.rglob('*.svg'):
    if any(part.startswith('.') for part in svg_p.parts):
        continue
    try:
        rt = ET.parse(svg_p).getroot().tag
        if not rt.endswith('svg'):
            errors.append(f'{svg_p.relative_to(ROOT)}: root tag is not svg')
    except Exception as e:
        errors.append(f'{svg_p.relative_to(ROOT)}: invalid SVG XML: {e}')

# Every major directory has README.md
for d in [p for p in ROOT.iterdir() if p.is_dir() and not p.name.startswith('.')]:
    if any(d.iterdir()) and not (d / 'README.md').is_file():
        warnings.append(f'Major directory has no README.md: {d.name}')

# Internal markdown links (ignore anchors-only, external URLs, templates)
for md in ROOT.rglob('*.md'):
    if any(part.startswith('.') for part in md.parts):
        continue
    try:
        txt = md.read_text(encoding='utf-8')
    except Exception:
        continue
    for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', txt):
        t_clean = target.split('#', 1)[0].strip()
        if not t_clean or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', t_clean) or t_clean.startswith('#') or '{{' in t_clean or t_clean.startswith('file://'):
            continue
        resolved = (md.parent / t_clean).resolve()
        if not resolved.exists():
            errors.append(f'Broken Markdown link in {md.relative_to(ROOT)}: {target}')

# Version check
ver = (ROOT / 'VERSION').read_text().strip()
if json.loads((ROOT / 'openclone.manifest.json').read_text())['version'] != ver:
    errors.append('openclone.manifest.json version differs from VERSION')
if f'Version: {ver}' not in (ROOT / 'PROJECT.md').read_text() and f'{ver}' not in (ROOT / 'PROJECT.md').read_text():
    errors.append('PROJECT.md version differs from VERSION')
if ver not in (ROOT / 'README.md').read_text():
    errors.append('README.md does not mention the current VERSION')

lock = ROOT / 'security/scanners.lock.json'
if not lock.is_file():
    errors.append('missing security/scanners.lock.json')
else:
    for e in json.loads(lock.read_text())['entries']:
        if not re.fullmatch(r'[0-9a-f]{40}', e.get('pinned_ref') or ''):
            errors.append(f"scanner lock entry {e.get('id')} is not pinned to a 40-char commit SHA")

for rel in ('openclone.py', 'docs/guides/RULES-AND-ENFORCEMENT.md', 'security/policies/release-gate.json', 'adapters/COMPATIBILITY.md', 'adapters/CONFORMANCE.md', 'framework/memory/README.md', 'examples/demo.sh', 'docs/demo/TRANSCRIPT.md'):
    if not (ROOT / rel).is_file():
        errors.append(f'missing required file: {rel}')

# JSON Schema validation
try:
    import jsonschema
    for p in schemas:
        jsonschema.Draft202012Validator.check_schema(json.loads(p.read_text(encoding='utf-8')))
    mapping = {'work-unit.valid.json': 'work-unit.schema.json', 'completion-report.valid.json': 'completion-report.schema.json'}
    for fixture, schema in mapping.items():
        fp = ROOT / 'tests/fixtures' / fixture
        if fp.exists():
            jsonschema.validate(json.loads(fp.read_text()), json.loads((ROOT / 'framework/schemas' / schema).read_text()))
    print('PASS: JSON Schema meta-validation and mapped fixture conformance.')
except ImportError:
    warnings.append('Install requirements-dev.txt for JSON Schema meta-validation and fixture conformance.')
except Exception as e:
    errors.append(f'JSON Schema validation: {e}')

if warnings:
    print('WARN:')
    for w in warnings:
        print(' - ' + w)

if errors:
    print('FAIL:')
    for e in errors:
        print(' - ' + e)
    sys.exit(1)

print(f'PASS: {len(engines)} uniquely numbered engine specifications with specific contracts in framework/engines.')
print(f'PASS: {len(schemas)} JSON Schema files; {len(fixtures)} JSON fixtures parse in framework/schemas.')
print('PASS: required project definition, agent instructions, reusable templates, license, governance and release-readiness documents present.')
print(f'PASS: version {ver} consistent; scanner lock fully pinned; hardening artefacts present.')
print('PASS: All internal Markdown links verified valid.')
