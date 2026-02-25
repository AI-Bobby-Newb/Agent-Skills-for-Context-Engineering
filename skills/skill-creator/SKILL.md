---
name: skill-creator
description: Use this skill when the user asks to create a new skill, update an existing skill, design skill metadata, structure SKILL.md content, or package reusable references/scripts/assets for a skill.
---

# Skill Creator

This skill provides a practical workflow for creating high-quality Codex/agent skills with minimal context overhead.

## When to Activate

Activate this skill when:
- A user asks to create a new skill
- A user asks to revise or improve an existing skill
- The task involves writing `SKILL.md` frontmatter (`name`, `description`)
- The task requires deciding what should live in `SKILL.md` vs `references/` vs `scripts/` vs `assets/`
- The user wants better trigger wording so a skill activates reliably

## Core Concepts

### 1) Progressive disclosure

Keep `SKILL.md` focused on the activation criteria and core workflow. Move detailed references to `references/` so they are loaded only when needed.

### 2) Metadata quality drives activation

The `name` and `description` fields are the routing layer. Good descriptions include concrete user intents and domain keywords.

### 3) Match guidance strictness to task fragility

- High freedom: principles and heuristics
- Medium freedom: preferred patterns and examples
- Low freedom: scripts with explicit steps and parameters

### 4) Bundle deterministic helpers

If the same complex logic is repeated, place it in `scripts/` and call the script instead of rewriting logic in every task.

## Creation Workflow

1. **Define scope**
   - Capture what outcomes the skill should enable
   - Identify primary triggers and exclusions
2. **Choose structure**
   - Put essential workflow in `SKILL.md`
   - Put heavy domain docs in `references/`
   - Put repeatable execution logic in `scripts/`
   - Put output resources/templates in `assets/`
3. **Write frontmatter first**
   - `name`: lowercase, digits, hyphens only
   - `description`: include clear “when to use” language and intent keywords
4. **Draft SKILL.md body**
   - Start with activation cues and concise workflow
   - Add decision rules and failure handling
   - Link reference files directly (one level deep)
5. **Validate quality**
   - Ensure no duplicate content between `SKILL.md` and references
   - Ensure body stays compact and actionable
   - Ensure examples reflect realistic user requests

For a copy/paste-ready quality gate, see [skill-review-checklist.md](./references/skill-review-checklist.md).

## Guidelines

1. Keep `SKILL.md` concise; avoid long conceptual essays.
2. Prefer concrete trigger phrases over abstract descriptions.
3. Avoid auxiliary docs like `README.md` inside skills unless explicitly required.
4. Use one-step reference navigation (link files directly from `SKILL.md`).
5. Include at least one realistic input/output style example.

## Example

**Input request:** "Create a skill that helps me evaluate agent responses with rubrics and pairwise comparison."

**Expected skill-creator behavior:**
- Propose a skill name like `response-evaluation`
- Draft frontmatter with activation keywords (rubric, pairwise, scoring)
- Create `SKILL.md` workflow for rubric design, scoring, and comparison
- Move metric catalogs into `references/metrics.md`
- Optionally add `scripts/score_parser.py` if deterministic parsing is needed

## Integration

- context-fundamentals — informs context-budget decisions
- context-compression — helps keep skills compact and high-signal
- tool-design — useful when a skill requires custom tool patterns
- project-development — useful for end-to-end workflow design

## References

- [Skill review checklist](./references/skill-review-checklist.md) — quality gate before publishing/updating a skill

---

## Skill Metadata

**Created**: 2026-02-25
**Last Updated**: 2026-02-25
**Author**: Agent Skills for Context Engineering Contributors
**Version**: 1.0.0
