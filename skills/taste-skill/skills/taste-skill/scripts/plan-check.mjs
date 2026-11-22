#!/usr/bin/env node
/*
  taste-skill plan-check.mjs - Pre-build design gate validator.
  Node 22+, zero external dependencies.

  Usage:
    node scripts/plan-check.mjs [--plan <path>] [--level <1-5>] [--strict] [--json]
*/
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf('--' + k); return i < 0 ? d : (args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : true); };

const PLAN_PATH = path.resolve(opt('plan', path.join(process.cwd(), '.taste-skill', 'design-plan.md')));
const AS_JSON = args.includes('--json');
const STRICT = args.includes('--strict');

const FULL_SECTIONS = [
  'Product understanding',
  'User and business context',
  'Existing application audit',
  'Instruction audit summary',
  'Existing design-system analysis',
  'Identified UI problems',
  'Anti-slop findings',
  'Proposed visual direction',
  'Color strategy',
  'Typography strategy',
  'Spacing strategy',
  'Component strategy',
  'Layout strategy',
  'Responsive strategy',
  'Interaction strategy',
  'Animation strategy',
  'Accessibility requirements',
  'Performance requirements',
  'Components to preserve',
  'Components to modify',
  'Components to remove',
  'Components to introduce',
  'Implementation sequence',
  'Validation strategy',
  'Risks and assumptions'
];

const LIGHTWEIGHT_SECTIONS = [
  'Task scope',
  'Problem description',
  'Proposed change',
  'Accessibility check',
  'Verification'
];

function checkPlan(filePath) {
  if (!fs.existsSync(filePath)) {
    return {
      state: 'GATE: PLAN_REQUIRED',
      valid: false,
      level: 0,
      missing: ['File does not exist: ' + filePath],
      warnings: []
    };
  }

  const content = fs.readFileSync(filePath, 'utf8');
  const levelMatch = content.match(/LEVEL\s*([1-5])/i);
  const level = levelMatch ? parseInt(levelMatch[1], 10) : 3;

  const requiredSections = (level <= 2) ? LIGHTWEIGHT_SECTIONS : FULL_SECTIONS;
  const missing = [];
  const empty = [];

  for (const s of requiredSections) {
    const re = new RegExp(`(^|\\n)#{1,4}\\s*.*${s.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&')}`, 'i');
    if (!re.test(content)) {
      missing.push(s);
    }
  }

  if (content.length < (level <= 2 ? 150 : 800)) {
    empty.push(`Plan content is too brief (${content.length} characters) for Level ${level}`);
  }

  const approvalNeeded = /requires?\s*approval|breaking\s*change|destructive/i.test(content) && !/approved\s*by/i.test(content);

  let state = 'GATE: READY';
  if (missing.length > 0 || empty.length > 0) {
    state = 'GATE: PLAN_INVALID';
  } else if (approvalNeeded) {
    state = 'GATE: APPROVAL_REQUIRED';
  }

  return {
    state,
    valid: state === 'GATE: READY',
    level,
    missing,
    empty,
    approvalNeeded,
    sectionsChecked: requiredSections.length
  };
}

const result = checkPlan(PLAN_PATH);

if (AS_JSON) {
  console.log(JSON.stringify(result, null, 2));
} else {
  console.log(`Plan Check: ${PLAN_PATH}`);
  console.log(`State: ${result.state}`);
  console.log(`Task Level: LEVEL ${result.level} (${result.level <= 2 ? 'Lightweight' : 'Full 25-Point Plan'})`);
  if (result.missing.length) {
    console.log(`Missing required sections (${result.missing.length}):`);
    for (const m of result.missing) console.log(`  - ${m}`);
  }
  if (result.empty.length) {
    for (const e of result.empty) console.log(`  - WARN: ${e}`);
  }
  if (result.approvalNeeded) {
    console.log('  - NOTICE: Human approval required for material scope changes before implementation.');
  }
}

if (!result.valid && STRICT) {
  process.exit(1);
}
