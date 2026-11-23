#!/usr/bin/env node
/*
  taste-skill audit-slop.mjs - Dedicated Anti-AI-Slop Governance and Visual Scanner.
  Node 22+, zero external dependencies.

  Usage:
    node scripts/audit-slop.mjs <file | folder> [--kind <kind>] [--report] [--json] [--strict]
*/
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf('--' + k); return i < 0 ? d : (args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : true); };

const TARGET = args.find(a => !a.startsWith('--')) || process.cwd();
const KIND = String(opt('kind', 'general')).toLowerCase();
const AS_JSON = args.includes('--json');
const WRITE_REPORT = args.includes('--report');
const STRICT = args.includes('--strict');

const SLOP_PATTERNS = [
  {
    id: 'glassmorphism-excess',
    name: 'Unnecessary Glassmorphism',
    regex: /(backdrop-filter|backdrop-blur|rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*0\.[0-3]\))/gi,
    severity: 'MEDIUM',
    recommendation: 'Replace translucent glass panels with clear, high-contrast solid surface tokens.',
    action: 'REDUCE',
    reason: 'Improves accessibility contrast, readability, and eliminates generic AI aesthetic.'
  },
  {
    id: 'purple-gradient-cliche',
    name: 'Generic Purple/Blue AI Gradient',
    regex: /(linear-gradient\(.*(#8b5cf6|#a855f7|#6366f1|#3b82f6|violet|purple).*#ec4899|from-purple|to-indigo|from-violet)/gi,
    severity: KIND === 'software' || KIND === 'tech' ? 'LOW' : 'HIGH',
    recommendation: 'Replace generic AI purple/blue gradient with domain-appropriate brand tokens.',
    action: KIND === 'software' ? 'JUSTIFIED' : 'REMOVE',
    reason: 'Generic purple gradient signals templated, synthetic AI site.'
  },
  {
    id: 'floating-background-blob',
    name: 'Artificial Background Blobs',
    regex: /(blur-3xl|filter:\s*blur\((\d{2,3})px\)|rounded-full\s+absolute\s+(bg-gradient|bg-purple|bg-blue))/gi,
    severity: 'HIGH',
    recommendation: 'Remove drifting background color blobs.',
    action: 'REMOVE',
    reason: 'Creates visual noise, distracts from content hierarchy, and hurts GPU rasterization.'
  },
  {
    id: 'excessive-border-radius',
    name: 'Oversized Rounded Borders on Cards',
    regex: /(rounded-3xl|rounded-\[3\dpx\]|border-radius:\s*(3\d|4\d|[5-9]\d)px)/gi,
    severity: 'MEDIUM',
    recommendation: 'Use controlled radii (4px, 8px, or 12px) that match typography scale.',
    action: 'REDUCE',
    reason: 'Excessive border radius eats card content padding and creates toy-like appearance.'
  },
  {
    id: 'glow-effects',
    name: 'Unnecessary Glow and Heavy Shadows',
    regex: /(box-shadow:\s*0\s+0\s+(3\d|4\d|[5-9]\d)px|shadow-2xl|drop-shadow-\[.*\])/gi,
    severity: 'MEDIUM',
    recommendation: 'Use subtle 1px border or crisp 1px-2px elevation shadow.',
    action: 'REMOVE',
    reason: 'Heavy glow effects obscure text boundaries and look dated.'
  },
  {
    id: 'marketing-buzzwords-pill',
    name: 'Filler Marketing Badge / Pill',
    regex: /(✨|🚀|⚡|Next-Gen|Revolutionary|The Future of|All-in-one platform)/gi,
    severity: 'MEDIUM',
    recommendation: 'State plain, direct product capabilities without superlative filler words.',
    action: 'REMOVE',
    reason: 'Empty buzzwords erode credibility.'
  }
];

function scanFiles(targetPath) {
  const files = [];
  const stat = fs.statSync(targetPath);
  if (stat.isFile()) {
    files.push(targetPath);
  } else if (stat.isDirectory()) {
    const walk = dir => {
      for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
        if (e.name.startsWith('.') || e.name === 'node_modules') continue;
        const p = path.join(dir, e.name);
        if (e.isDirectory()) walk(p);
        else if (/\.(html|css|js|jsx|ts|tsx|vue|svelte)$/i.test(e.name)) files.push(p);
      }
    };
    walk(targetPath);
  }
  return files;
}

const files = scanFiles(TARGET);
const findings = [];

for (const file of files) {
  const content = fs.readFileSync(file, 'utf8');
  for (const pat of SLOP_PATTERNS) {
    const matches = content.match(pat.regex);
    if (matches && matches.length > 0) {
      findings.push({
        file: path.relative(process.cwd(), file),
        patternId: pat.id,
        name: pat.name,
        severity: pat.severity,
        count: matches.length,
        recommendation: pat.recommendation,
        action: pat.action,
        reason: pat.reason
      });
    }
  }
}

if (WRITE_REPORT) {
  const repDir = path.join(process.cwd(), '.taste-skill', 'reports');
  fs.mkdirSync(repDir, { recursive: true });
  const repPath = path.join(repDir, 'anti-slop-audit.md');
  const md = `# Anti-AI-Slop Governance Audit Report
Target: \`${TARGET}\`
Files Scanned: ${files.length}
Findings Detected: ${findings.length}
Date: ${new Date().toISOString()}

${findings.length === 0 ? '### Result: PASS — Clean Interface (No Slop Patterns Detected)' : findings.map(f => `
### Pattern: ${f.name}
* **Severity:** ${f.severity}
* **File:** \`${f.file}\` (${f.count} occurrence(s))
* **Action:** \`${f.action}\`
* **Recommendation:** ${f.recommendation}
* **Reason:** ${f.reason}
`).join('\n---\n')}
`;
  fs.writeFileSync(repPath, md, 'utf8');
  if (!AS_JSON) console.log(`Wrote anti-slop audit report to ${repPath}`);
}

if (AS_JSON) {
  console.log(JSON.stringify({ filesScanned: files.length, findingsCount: findings.length, findings }, null, 2));
} else {
  console.log(`Anti-Slop Audit: Scanned ${files.length} file(s). Found ${findings.length} issue(s).`);
  for (const f of findings) {
    console.log(`  [${f.severity}] ${f.name} in ${f.file} (${f.count}x) -> Action: ${f.action}`);
  }
}

if (STRICT && findings.some(f => f.severity === 'HIGH')) {
  process.exit(1);
}
