#!/usr/bin/env node
/*
  taste-skill instruction-audit.mjs - Discovers and audits project-level instruction files.
  Node 22+, zero external dependencies.

  Usage:
    node scripts/instruction-audit.mjs [--cwd <dir>] [--report] [--json] [--strict]
*/
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf('--' + k); return i < 0 ? d : (args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : true); };

const CWD = path.resolve(opt('cwd', process.cwd()));
const AS_JSON = args.includes('--json');
const WRITE_REPORT = args.includes('--report');
const STRICT = args.includes('--strict');

const CANDIDATE_FILES = [
  'AGENTS.md',
  'CLAUDE.md',
  'GEMINI.md',
  '.cursorrules',
  '.github/copilot-instructions.md',
  'PROJECT.md',
  'DESIGN.md',
  'DESIGN-SYSTEM.md',
  'STYLEGUIDE.md',
  'README.md',
  'package.json'
];

function discoverInstructions(startDir) {
  const discovered = [];
  let current = startDir;
  const root = path.parse(current).root;

  while (current) {
    for (const rel of CANDIDATE_FILES) {
      const full = path.join(current, rel);
      if (fs.existsSync(full) && fs.statSync(full).isFile()) {
        discovered.push({
          rel: path.relative(startDir, full) || rel,
          full,
          level: current === startDir ? 'local' : 'inherited'
        });
      }
    }
    // Check .cursor/rules directory if present
    const cursorRules = path.join(current, '.cursor', 'rules');
    if (fs.existsSync(cursorRules) && fs.statSync(cursorRules).isDirectory()) {
      for (const f of fs.readdirSync(cursorRules)) {
        if (/\.(md|mdc)$/i.test(f)) {
          const full = path.join(cursorRules, f);
          discovered.push({
            rel: path.relative(startDir, full),
            full,
            level: current === startDir ? 'local' : 'inherited'
          });
        }
      }
    }

    if (current === root) break;
    current = path.dirname(current);
  }

  return discovered;
}

function analyzeInstructions(discovered) {
  const rules = [];
  const conflicts = [];
  const constraints = [];

  for (const item of discovered) {
    try {
      const content = fs.readFileSync(item.full, 'utf8');
      if (/dark\s*mode\s*only/i.test(content) && /light\s*mode\s*only/i.test(content)) {
        conflicts.push({ file: item.rel, issue: 'Conflicting light/dark mode directives' });
      }
      if (/tailwind/i.test(content)) {
        constraints.push({ file: item.rel, constraint: 'Project utilizes Tailwind CSS' });
      }
      if (/no\s*animation/i.test(content) || /prefers-reduced-motion/i.test(content)) {
        constraints.push({ file: item.rel, constraint: 'Strict motion reduction mandated' });
      }
    } catch {
      // skip unreadable files
    }
  }

  return { discovered, rules, conflicts, constraints };
}

const audit = analyzeInstructions(discoverInstructions(CWD));

if (WRITE_REPORT) {
  const reportDir = path.join(CWD, '.taste-skill', 'reports');
  fs.mkdirSync(reportDir, { recursive: true });
  const reportPath = path.join(reportDir, 'instruction-audit.md');
  const md = `# Instruction Audit Report
Generated: ${new Date().toISOString()}
Target Directory: \`${CWD}\`

## Discovered Instruction Files (${audit.discovered.length})
${audit.discovered.length ? audit.discovered.map(d => `- **${d.rel}** (${d.level})`).join('\n') : '_No instruction files discovered._'}

## Identified Constraints (${audit.constraints.length})
${audit.constraints.length ? audit.constraints.map(c => `- **${c.constraint}** (source: \`${c.file}\`)`).join('\n') : '_No explicit technical constraints detected._'}

## Detected Conflicts (${audit.conflicts.length})
${audit.conflicts.length ? audit.conflicts.map(c => `- ⚠️ **${c.issue}** in \`${c.file}\``).join('\n') : '_No conflicting instructions detected._'}

## Precedence Enforcement
1. Explicit human user prompt
2. Project instruction files (${audit.discovered.filter(d => d.level === 'local').map(d => d.rel).join(', ') || 'none'})
3. Inherited instruction files (${audit.discovered.filter(d => d.level === 'inherited').map(d => d.rel).join(', ') || 'none'})
4. Taste Skill design defaults
`;
  fs.writeFileSync(reportPath, md, 'utf8');
  if (!AS_JSON) console.log(`Wrote report to ${reportPath}`);
}

if (AS_JSON) {
  console.log(JSON.stringify(audit, null, 2));
} else {
  console.log(`Discovered ${audit.discovered.length} instruction file(s).`);
  for (const d of audit.discovered) {
    console.log(`  - [${d.level}] ${d.rel}`);
  }
  if (audit.conflicts.length) {
    console.log(`WARN: ${audit.conflicts.length} instruction conflict(s) detected.`);
  }
}

if (STRICT && audit.conflicts.length > 0) {
  process.exit(1);
}
