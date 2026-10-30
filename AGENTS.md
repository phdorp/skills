# Working in this repository

This repository is a shared skill collection. It improves by observing real sessions, not by
accumulating plausible advice. Read this before editing a skill.

## Improve a skill after a session

1. Run the `retro` skill on the session. It sorts friction into navigation, automated checks,
   standards, steering files, tool economy, and information access.
2. For each candidate, name the baseline failure you observed: what the agent did without the
   change, with evidence from the transcript.
3. Change the smallest thing that addresses that failure:
   - A mechanical rule belongs in a linter, test, hook, or CI job, not in prose.
   - A judgement call belongs in a skill or `CODING_STANDARDS.md`.
   - A missing fact belongs in a reference file reached by a pointer.
4. Test the change with the `writing-for-agents` skill. For discipline changes, run the failure
   scenario without the change (RED), then with it (GREEN), then close the new loophole.
5. Update `README.md` if the skill's description or location changed.

## Editing rules

- Keep each meaning in one place. If a rule already lives in another skill, point to it.
- Descriptions say when to use the skill; they do not summarise the workflow.
- Prefer positive instructions ("write one-line comments") over prohibitions.
- Put heavy reference, scripts, and templates in the skill directory; keep `SKILL.md` for what
  every run needs.
- Use lowercase kebab-case directory names. The directory name is the skill ID.
- Rewrite cross-references when a skill is renamed or merged. Old IDs must not survive.

## Frontmatter

```yaml
---
name: <directory id>
description: Use when ... Specific triggers and symptoms.
metadata:
  opencode/autoinvoke: false   # only for user-invoked workflows
---
```

`name` repeats the directory id, and must match it exactly. Harnesses address a skill by this
name, so the Agent Skills naming rules apply: lowercase alphanumerics with single hyphens, no
spaces, 1–64 characters. A human-readable label such as `Code Review` is not a valid name — it
breaks hosts that match skill mentions with `[a-zA-Z0-9][a-zA-Z0-9:_-]*`, and it disagrees with the
directory, which is the ID every other harness uses.

Use `disable-model-invocation: true` only when portability with other harnesses matters; it is
equivalent to `opencode/autoinvoke: false` in OpenCode.

## Validate

```sh
python3 scripts/validate-skills.py
```

The validator checks frontmatter, ID/directory agreement, relative links, and stale references.
Run it before every commit.

## Provenance

Add new upstream-derived material to `ATTRIBUTION.md`. Do not remove upstream copyright notices
from `LICENSE`.
