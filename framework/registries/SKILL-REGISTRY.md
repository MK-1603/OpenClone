# OpenClone Skill Registry
**Canonical Registry of Verified Engineering, Design & Security Skills**  
*OpenClone Global Standards | Managed by `src/openclone/skills/engine.py`*

---

## 1. Registered Skills Master Index

| Skill ID | Display Name | Version | Category | Precedence | Location | Pre-Build Gate | Finish Gate | Maturity Status |
|---|---|---|---|:---:|---|---|---|:---:|
| `saas-security-baseline` | **SaaS Security Baseline Skill** | `v1.0.0` | `security` | 5 | [`docs/security/saas-security-baseline.md`](file:///docs/security/saas-security-baseline.md) | Security scan / RLS check | 19-Point Checklist Pass | `VERIFIED_IMPLEMENTED` |
| `taste-skill` | **Taste Skill** | `v2.6.0` | `design` | 10 | [`skills/taste-skill`](file:///skills/taste-skill) | `plan-check.mjs` (`GATE: READY`) | `gate.mjs` (`GATE: PASS`) | `VERIFIED_IMPLEMENTED` |
| `strix-pentest-adapter` | **Strix Dynamic Pentest Adapter** | `v1.0.0` | `security` | 15 | [`docs/integrations/strix-dynamic-testing.md`](file:///docs/integrations/strix-dynamic-testing.md) | Written Target Authorization | Retest Finding Closure | `SPECIFIED & BOUNDED` |
| `typography-standards` | **Typography Standards Skill** | `v1.0.0` | `design` | 20 | [`domains/05/HUMAN-CRAFTED-DESIGN-SYSTEM.md`](file:///domains/05-UX-UI-ENGINEERING/HUMAN-CRAFTED-DESIGN-SYSTEM.md) | Type Scale Validation | Optical Contrast / Line-length | `VERIFIED_IMPLEMENTED` |
| `backend-architecture` | **Backend System Architecture Skill** | `v1.0.0` | `backend` | 20 | [`docs/knowledge/backend-system-design-catalogue.md`](file:///docs/knowledge/backend-system-design-catalogue.md) | Migration Rollback Check | Transaction / Contract Test | `VERIFIED_DOCUMENTED` |
| `ai-context-engineering` | **AI & Context Engineering Skill** | `v1.0.0` | `ai` | 20 | [`docs/knowledge/ai-engineering-catalogue.md`](file:///docs/knowledge/ai-engineering-catalogue.md) | Schema Output Validation | Token Budget / Rate Limit | `VERIFIED_DOCUMENTED` |
| `motion-design` | **Motion & Animation Skill** | `v1.0.0` | `design` | 25 | [`docs/knowledge/motion-and-animation.md`](file:///docs/knowledge/motion-and-animation.md) | Compositor Property Check | `prefers-reduced-motion` | `VERIFIED_IMPLEMENTED` |

---

## 2. Design-Skill Precedence Hierarchy

To prevent conflicting visual directions when multiple design skills match:
1. **Product Brief & Constraints (`PROJECT.md`)**: Human owner requirements are authoritative.
2. **Design-System Extraction (`design-md-chrome`)**: Extract tokens from existing brand assets.
3. **Art Direction & Anti-Slop (`taste-skill`)**: Establishes purpose, visual density, and eliminates clichés.
4. **Component Primitives (`shadcn/ui`, `frontend-design`)**: Accessible UI component assemblies.
5. **Typography Standards (`typography-standards`)**: Proportional scales, fluid clamp, line-length constraints.
6. **Design Critique & QA (`impeccable`, `hallmark`)**: Pre-release inspection and defect scoring.
7. **Accessibility Verification (`a11y`)**: WCAG 2.2 AA contrast, keyboard navigation, and reduced-motion checks.

---

## 3. Skill Diagnostics CLI

Inspect discovered skills and test task selection:
```bash
# List all registered skills
python tools/skill_engine.py list

# Select skills for a task
python tools/skill_engine.py select --task "Build accessible login form with auth" --task-id "AUTH-01"

# Generate markdown selection report
python tools/skill_engine.py select --task "Build SaaS analytics dashboard" --report

# Verify all skill paths and manifests
python tools/skill_engine.py verify
```
