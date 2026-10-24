---
name: Code Review
description: Use when requesting, performing, or receiving review of a branch, PR, or work-in-progress diff - reviews against Standards and Spec on separate axes and turns feedback into verified changes.
---

# Code Review

One loop with three phases: **request** a review, **perform** it on two axes, **receive** the findings and act on them.

## The two axes

- **Standards**: does the diff follow this repo's documented coding standards?
- **Spec**: does the diff faithfully implement the originating issue or spec?

Keep them separate. Code can pass one and fail the other: an implementation that ignores every convention can implement the right thing, and a beautifully conventional diff can implement the wrong thing. Reporting the axes separately stops one from masking the other.

## Requesting a review

Request review when it is mandatory: after each task in subagent-driven execution (see [executing-plans](../executing-plans/SKILL.md)), after a major feature, before merging to main. Also useful when stuck, before a refactor, and after fixing a complex bug.

1. **Pin exact commits.** Resolve full SHAs, not `HEAD~1`:
   ```bash
   BASE_SHA=$(git merge-base origin/main HEAD)   # or the commit this task started from
   HEAD_SHA=$(git rev-parse HEAD)
   ```
2. **Craft the context.** Fill [references/reviewer-prompt.md](references/reviewer-prompt.md). Hand the reviewer the diff command, the commit list, the spec, and the standards sources. Never hand it your session history: the reviewer judges the work product, not your reasoning.
3. **Confirm the range is real** before dispatching: `git rev-parse` both SHAs, and check the diff is non-empty. A bad ref or empty diff should fail here, not inside a subagent.
4. **Act on findings by severity**: Critical immediately, Important before continuing, Minor noted for later. Push back with evidence when the reviewer is wrong, not with deference.

Reviewing the diff yourself instead of dispatching a reviewer is a false economy: the diff and its evaluation consume the context you need to keep driving the work. Dispatch, and let only the findings come back.

## Performing the two-axis review

### 1. Pin the fixed point

The fixed point is whatever the user named: a commit SHA, branch, tag, `main`, `HEAD~5`. If they did not name one, ask.

```bash
git rev-parse <fixed-point>              # fail fast on a bad ref
git diff <fixed-point>...HEAD            # three-dot: diff against the merge-base
git log <fixed-point>..HEAD --oneline    # the commit list
```

Three-dot matters: it reviews what this branch changed, not everything that landed on the base since it forked. Confirm the diff is non-empty before going further.

### 2. Find the spec source

Look in this order:

1. Issue references in commit messages (`#123`, `Closes #45`, GitLab `!67`), fetched through the repo's tracker workflow.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch or feature name.
4. Ask the user where the spec is.

If there is no spec, skip the Spec axis and say so in the report. Do not invent one from the diff.

### 3. Find the standards sources

Search the repo for every file that documents how code should be written. `CODING_STANDARDS.md` and `CONTRIBUTING.md` go on the list whenever they exist. The full discovery list, plus the Fowler smell baseline that applies when a repo documents nothing, is in [references/standards-and-smells.md](references/standards-and-smells.md).

### 4. Run the axes in parallel

When subagents are available, issue both calls together, in the foreground, and aggregate what they return. When they are not, do two separate passes and keep the notes apart.

Give each reviewer the filled prompt from [references/reviewer-prompt.md](references/reviewer-prompt.md) with:

- the same diff command and commit list;
- that axis's sources only — standards files and the smell baseline for Standards, the spec path or contents for Spec;
- the global constraints (review is read-only, no subagents, stay under 400 words).

Each reviewer gets one axis. A reviewer that sees the other axis's findings starts reranking them, which is exactly what the separation prevents.

### 5. Aggregate

Present the two reports under `## Standards` and `## Spec`, verbatim or lightly cleaned. Do not merge, deduplicate across axes, or rerank.

Close with one line: findings per axis, and the worst issue **within each axis**. Do not pick a single winner across axes.

## Receiving review

**Core principle:** verify before implementing; technical correctness over social comfort.

1. **Read** the whole review without reacting.
2. **Restate** each item in your own words. If any item is unclear, stop and ask before implementing anything — items are often related, and partial understanding produces the wrong fix.
3. **Verify** each claim against the codebase: read the callers, run the failing case, grep for usage. The reviewer may be guessing.
4. **Evaluate** whether the suggestion is right for *this* codebase. External reviewers get extra skepticism. If it conflicts with a decision your human partner already made, raise it with them rather than silently overriding either side.
5. **Respond** technically: state what you changed, or push back with evidence. No gratitude, no "you're absolutely right", no agreement before verification.
6. **Implement** in this order: blocking issues (breaks, security), simple fixes (typos, imports), complex fixes (refactors, logic). One item at a time, testing each, then re-run the full suite.

**YAGNI check:** when a reviewer asks for a "proper" implementation of something, grep for actual usage first. Unused: propose removing it. Used: implement it properly.

Patterns, phrasing, and the GitHub thread-reply rule are in [references/receiving-feedback.md](references/receiving-feedback.md).

## Finish

- Write the regression test with [test-driven-development](../test-driven-development/SKILL.md) before fixing a logic bug.
- Use [systematic-debugging](../systematic-debugging/SKILL.md) when a finding's cause is not obvious; do not patch the symptom.
- Run [verification-before-completion](../verification-before-completion/SKILL.md) before claiming the review is addressed.
- When the review is clean, integrate with [finishing-a-development-branch](../finishing-a-development-branch/SKILL.md).

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "I'll review the diff inline instead of dispatching" | The diff and its evaluation consume the context you need to keep working. Dispatch; only findings come back. |
| "It's a simple change, skip review" | Simple changes cause outages. Mandatory means mandatory. |
| "The reviewer needs my session history" | Crafted context only. History anchors the reviewer to your reasoning instead of the work. |
| "The reviewer suggested it, so it must be right" | Verify against the codebase first. Reviewers lack context and can be wrong. |
| "I'll implement 1-6 now and ask about 4-5 later" | Partial understanding produces wrong fixes. Clarify all unclear items first. |
| "Thanks, great catch!" | State the fix. Gratitude is not evidence the feedback landed. |
| "Tests passed before my change" | Run the suite on the tree you are about to hand over. |
| "The axes mostly agree, so I'll merge them" | Merging reranks. Report each axis on its own terms. |
