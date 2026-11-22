#!/usr/bin/env node
/*
  tests/test-governance.mjs - Automated test suite for Taste Skill v2.6.0 Governance Engines.
  Node 22+, zero external dependencies. Tests instruction-audit.mjs, audit-slop.mjs, and plan-check.mjs.
*/
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SCRIPTS = path.join(ROOT, 'skills', 'taste-skill', 'scripts');

let passed = 0;
let failed = 0;

function assert(condition, message) {
  if (condition) {
    console.log(`  ✓ PASS: ${message}`);
    passed++;
  } else {
    console.error(`  ✗ FAIL: ${message}`);
    failed++;
  }
}

console.log('Running Taste Skill Governance & Anti-Slop Test Suite...\n');

// -------------------------------------------------------------
// Test 1: Instruction Discovery Engine
// -------------------------------------------------------------
console.log('[Test Suite 1: instruction-audit.mjs]');
const tmp1 = fs.mkdtempSync(path.join(os.tmpdir(), 'taste-test-instruct-'));
try {
  fs.writeFileSync(path.join(tmp1, 'AGENTS.md'), '# Agent Operating Rules\nStrict dark mode only.\n');
  fs.writeFileSync(path.join(tmp1, 'README.md'), '# Project README\n');
  const sub = path.join(tmp1, 'packages', 'web');
  fs.mkdirSync(sub, { recursive: true });
  fs.writeFileSync(path.join(sub, '.cursorrules'), 'Use Tailwind CSS conventions.\n');

  const out = execFileSync(process.execPath, [
    path.join(SCRIPTS, 'instruction-audit.mjs'),
    '--cwd', sub,
    '--json'
  ], { encoding: 'utf8' });

  const data = JSON.parse(out);
  assert(data.discovered.length >= 3, `Discovered ${data.discovered.length} files (expected >= 3)`);
  assert(data.discovered.some(d => d.rel.includes('.cursorrules') && d.level === 'local'), 'Identified local .cursorrules');
  assert(data.discovered.some(d => d.rel.includes('AGENTS.md') && d.level === 'inherited'), 'Identified inherited AGENTS.md');
  assert(data.constraints.some(c => c.constraint.includes('Tailwind')), 'Extracted Tailwind constraint from rules');
} finally {
  fs.rmSync(tmp1, { recursive: true, force: true });
}

// -------------------------------------------------------------
// Test 2: Anti-AI-Slop Governance Engine
// -------------------------------------------------------------
console.log('\n[Test Suite 2: audit-slop.mjs]');
const tmp2 = fs.mkdtempSync(path.join(os.tmpdir(), 'taste-test-slop-'));
try {
  const badHtml = `
    <!DOCTYPE html>
    <html>
      <head><style>
        .card { backdrop-filter: blur(20px); background: rgba(255,255,255,0.1); border-radius: 40px; box-shadow: 0 0 50px rgba(0,0,0,0.5); }
        .hero { background: linear-gradient(to right, #8b5cf6, #ec4899); }
        .blob { filter: blur(60px); border-radius: 9999px; }
      </style></head>
      <body>
        <div class="blob"></div>
        <span class="pill">✨ The Future of Next-Gen AI</span>
        <div class="card"><h1>Hero</h1></div>
      </body>
    </html>
  `;
  const htmlFile = path.join(tmp2, 'sloppy.html');
  fs.writeFileSync(htmlFile, badHtml, 'utf8');

  const out = execFileSync(process.execPath, [
    path.join(SCRIPTS, 'audit-slop.mjs'),
    htmlFile,
    '--json'
  ], { encoding: 'utf8' });

  const data = JSON.parse(out);
  assert(data.findingsCount >= 4, `Detected ${data.findingsCount} visual slop patterns (expected >= 4)`);
  assert(data.findings.some(f => f.patternId === 'glassmorphism-excess'), 'Flagged excessive glassmorphism');
  assert(data.findings.some(f => f.patternId === 'purple-gradient-cliche'), 'Flagged generic purple/blue AI gradient');
  assert(data.findings.some(f => f.patternId === 'floating-background-blob'), 'Flagged artificial background blur blobs');
  assert(data.findings.some(f => f.patternId === 'marketing-buzzwords-pill'), 'Flagged meaningless buzzword marketing pill');
} finally {
  fs.rmSync(tmp2, { recursive: true, force: true });
}

// -------------------------------------------------------------
// Test 3: Pre-Build Design Gate Validator
// -------------------------------------------------------------
console.log('\n[Test Suite 3: plan-check.mjs]');
const tmp3 = fs.mkdtempSync(path.join(os.tmpdir(), 'taste-test-plan-'));
try {
  const planDir = path.join(tmp3, '.taste-skill');
  fs.mkdirSync(planDir, { recursive: true });
  const planFile = path.join(planDir, 'design-plan.md');

  // Test 3A: Missing plan -> GATE: PLAN_REQUIRED
  const outMissing = execFileSync(process.execPath, [
    path.join(SCRIPTS, 'plan-check.mjs'),
    '--plan', planFile,
    '--json'
  ], { encoding: 'utf8' });
  const dataMissing = JSON.parse(outMissing);
  assert(dataMissing.state === 'GATE: PLAN_REQUIRED', 'Uncreated plan halts at GATE: PLAN_REQUIRED');

  // Test 3B: Level 1 Lightweight Plan
  const l1Plan = `
# Design Plan
LEVEL 1 — MICRO FIX

## Task scope
Fix button contrast ratio on landing page navbar.

## Problem description
The sign-in button uses gray text on white background (contrast 2.8:1).

## Proposed change
- MODIFY: Change navbar button text color token to var(--ink) achieving 7.1:1 contrast.
- PRESERVE: Existing button padding, font size, and hover animation.

## Accessibility check
Verified WCAG AA 4.5:1 ratio met. Focus ring preserved.

## Verification
Run consistency.mjs --quick and verify button-contrast passes.
  `;
  fs.writeFileSync(planFile, l1Plan, 'utf8');

  const outL1 = execFileSync(process.execPath, [
    path.join(SCRIPTS, 'plan-check.mjs'),
    '--plan', planFile,
    '--json'
  ], { encoding: 'utf8' });
  const dataL1 = JSON.parse(outL1);
  assert(dataL1.state === 'GATE: READY', 'Level 1 lightweight plan passes and achieves GATE: READY');

  // Test 3C: Level 3 Plan without required sections -> GATE: PLAN_INVALID
  const incompleteL3Plan = `
# Design Plan
LEVEL 3 — PAGE REDESIGN
## Product understanding
Enterprise analytics dashboard.
  `;
  fs.writeFileSync(planFile, incompleteL3Plan, 'utf8');

  const outL3Bad = execFileSync(process.execPath, [
    path.join(SCRIPTS, 'plan-check.mjs'),
    '--plan', planFile,
    '--json'
  ], { encoding: 'utf8' });
  const dataL3Bad = JSON.parse(outL3Bad);
  assert(dataL3Bad.state === 'GATE: PLAN_INVALID', 'Incomplete Level 3 plan rejected with GATE: PLAN_INVALID');
  assert(dataL3Bad.missing.length > 15, `Identified ${dataL3Bad.missing.length} missing required sections`);
} finally {
  fs.rmSync(tmp3, { recursive: true, force: true });
}

// -------------------------------------------------------------
// Summary
// -------------------------------------------------------------
console.log('\n====================================');
console.log(`Results: ${passed} passed, ${failed} failed.`);
console.log('====================================');

if (failed > 0) {
  process.exit(1);
} else {
  console.log('All governance tests passed cleanly!');
}
