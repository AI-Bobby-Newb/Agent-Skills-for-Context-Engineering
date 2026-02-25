# Skill Review Checklist

Use this checklist before finalizing a new or updated skill.

## Metadata

- `name` is lowercase hyphen-case and under 64 chars
- `description` explains when to use the skill with concrete intent keywords
- Description avoids first-person phrasing and vague language

## SKILL.md body

- Activation section includes explicit triggers
- Core workflow is actionable and ordered
- Instructions are concise and avoid redundant theory
- Guidance level matches fragility (high/medium/low freedom)
- At least one realistic usage example is included

## Resource organization

- Detailed domain docs moved to `references/`
- Deterministic repeated operations moved to `scripts/`
- Output templates/resources moved to `assets/` when applicable
- No unnecessary auxiliary docs (README, changelog, installation guide)

## Progressive disclosure

- `SKILL.md` links directly to any reference files
- No deep reference chains required to perform common tasks
- Content is not duplicated across files

## Final quality gate

- Skill can be understood quickly from `description` + first sections of `SKILL.md`
- A new contributor can implement the workflow without external clarification
- The skill minimizes token cost while preserving reliability
