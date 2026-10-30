---
name: systematic-debugging
description: Use when something is broken, throwing, failing intermittently, or slower than it should be — any bug, test failure, build failure, integration problem, or performance regression — before proposing a fix.
---

# Systematic Debugging

**Core principle:** find the root cause before attempting a fix. A symptom fix is a failure.

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

## When it applies

Every technical issue: test failures, production bugs, unexpected behavior, performance regressions, build failures, integration problems.

Use it **especially** when:

- You are under time pressure — emergencies make guessing tempting.
- "One quick fix" looks obvious.
- You have already tried fixes, or the last one didn't work.
- You do not fully understand the issue.

Do not skip because the issue looks simple. Simple bugs have root causes too, and rushing guarantees rework.

## Redact first

This process has you show commands, outputs, and captured artifacts. **Redact every secret first**: write `<REDACTED>` in its place. Build loops against environment variables, so the credential stays in the environment rather than in what you show. Captured artifacts carry auth headers: quote only the lines that carry the signal.

If the redacted output is not enough to diagnose the bug, say so and ask the user.

## Phase 1: Build a feedback loop

**This phase is the skill.** Everything else is mechanical. A **tight** pass/fail signal that goes red on *this* bug will find the cause; bisection, hypothesis testing, and instrumentation all just consume it. Without one, no amount of staring at code will save you.

Spend disproportionate effort here. Be aggressive. Be creative. Refuse to give up.

### Ways to construct one, roughly in this order

1. **Failing test** at whatever seam reaches the bug: unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright/Puppeteer) that drives the UI and asserts on DOM, console, or network.
5. **Replay a captured trace.** Save a real request, payload, or event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** Boot a minimal subset of the system that exercises the bug path with one function call.
7. **Property / fuzz loop.** If the output is "sometimes wrong", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** Automate "boot at state X, check, repeat" so `git bisect run` can drive it.
9. **Differential loop.** Run the same input through old versus new version, or two configs, and diff the outputs.
10. **HITL script.** Last resort. When a human must click, drive *them* with [scripts/hitl-loop.template.sh](scripts/hitl-loop.template.sh) so the loop stays structured.

### Tighten the loop

Treat the loop as a product. Once you have one, make it:

- **Faster** — cache setup, skip unrelated init, narrow the scope.
- **Sharper** — assert the specific symptom, not "didn't crash".
- **More deterministic** — pin time, seed the RNG, isolate the filesystem, freeze the network.

A 30-second flaky loop is barely better than no loop; a 2-second deterministic one is a debugging superpower.

### Non-deterministic bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop the trigger 100×, parallelise, add stress, narrow timing windows, inject sleeps. A 50% flake is debuggable; 1% is not. Keep raising the rate until it is. In test harnesses, wait on conditions rather than guessing delays: [references/condition-based-waiting.md](references/condition-based-waiting.md).

### Completion criterion

Phase 1 is done when you can name **one command** you have **already run at least once** (show the invocation and its redacted output), and it is:

- [ ] **Red-capable** — drives the actual bug path and asserts the user's exact symptom, so it goes red on this bug and green once fixed. Not "runs without erroring".
- [ ] **Deterministic** — same verdict every run; for flaky bugs, a pinned high reproduction rate.
- [ ] **Fast** — seconds, not minutes.
- [ ] **Agent-runnable** — you can run it unattended; a human only through the HITL script.

If you catch yourself reading code to build a theory before this command exists, stop. **Jumping to a hypothesis is the exact failure this skill prevents.** No red-capable command, no Phase 2.

### When you genuinely cannot build one

Stop and say so. List what you tried. Ask the user for (a) access to an environment that reproduces it, (b) a redacted captured artifact (HAR file, log dump, core dump, timestamped screen recording), or (c) permission to add temporary production instrumentation. Do not proceed to hypothesise without a loop.

## Phase 2: Reproduce and minimise

Run the loop and watch it go red.

Confirm:

- [ ] The loop produces the failure mode the **user** described, not a neighbouring failure. Wrong bug, wrong fix.
- [ ] It reproduces across runs, or at a high enough rate to debug.
- [ ] You captured the exact symptom — error message, wrong output, slow timing — so later phases can verify the fix addresses it.

Then investigate before hypothesising:

**Read the error messages carefully.** Don't skip past errors or warnings; they often contain the exact solution. Read stack traces completely, and note line numbers, file paths, and error codes.

**Check recent changes.** `git diff`, recent commits, new dependencies, config changes, environment differences. "It worked yesterday" usually names the culprit.

**Gather evidence at every component boundary** in multi-component systems (CI → build → signing, API → service → database). For each component, log what enters and what exits, verify environment and config propagation, and check state at each layer. Run once to learn *where* it breaks, then investigate that component. Check presence, not values: `IDENTITY: SET` or `UNSET` beats printing a secret.

**Trace the data flow backwards.** When the error is deep in the stack, find the immediate cause, ask what called this with that value, and keep going up until you find where the bad value originated. Fix at the source, not where the error surfaced. Full technique: [references/root-cause-tracing.md](references/root-cause-tracing.md).

### Minimise

Shrink the repro to the smallest scenario that still goes red. Cut inputs, callers, config, data, and steps **one at a time**, re-running the loop after each cut. Keep only what is load-bearing for the failure.

A minimal repro shrinks the hypothesis space in Phase 3 and becomes the clean regression test in Phase 5. Done when removing any remaining element makes the loop go green.

Do not proceed until you have reproduced **and** minimised.

## Phase 3: Hypothesise

First, **analyse the pattern**. Find working examples of the same thing in this codebase. Read any reference implementation completely — don't skim, and don't "adapt the pattern". List every difference between working and broken, however small. Understand the dependencies, settings, and assumptions each side makes.

Then generate **3–5 ranked hypotheses** before testing any of them. A single hypothesis anchors on the first plausible idea.

Each must be **falsifiable** — state the prediction it makes:

> "If <X> is the cause, then <changing Y> will make the bug disappear" or "...<changing Z> will make it worse."

Cannot state the prediction? It is a vibe. Discard or sharpen it.

**Show the ranked list to the user before testing.** Domain knowledge re-ranks instantly ("we just deployed #3") or rules hypotheses out entirely. Don't block on the answer; proceed with your ranking if they are away.

## Phase 4: Instrument

Every probe maps to a specific prediction. **Change one variable at a time.**

Tool preference, in order:

1. **Debugger / REPL inspection** where the environment supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup becomes one grep; untagged logs survive.

**Performance regressions** take a different instrument: a baseline measurement first — timing harness, `performance.now()`, profiler, query plan — then bisect. Measure first, fix second.

**Did it work?** Confirmed → Phase 5. Not confirmed → discard the hypothesis, form a new one. Don't stack another fix on top.

## Phase 5: Fix at the root, with a regression test

Write the regression test **before the fix**, but only at a **correct seam** — one where the test exercises the real bug pattern as it occurs at the call site. A shallow seam (a single-caller test for a bug that needs multiple callers, a unit test that cannot replicate the chain) gives false confidence.

**If no correct seam exists, that is itself the finding.** Note it: the architecture is preventing the bug from being locked down. Say so in your report, and raise the seam question with the user; `codebase-design` has the vocabulary.

If a correct seam exists:

1. Turn the minimised repro into a failing test there, following `test-driven-development` (watch it fail before writing the fix).
2. Watch it fail. If you forced red by mutating code or a fixture, `diff` against a pristine copy to prove the mutation landed.
3. Apply one fix for the root cause. No "while I'm here" improvements, no bundled refactoring.
4. Watch it pass.
5. Re-run the Phase 1 loop against the original, un-minimised scenario.
6. Run the full suite.

For invalid data reaching a dangerous operation, validate at every layer it passes through so the bug becomes structurally impossible: [references/defense-in-depth.md](references/defense-in-depth.md).

## Phase 6: Cleanup

- [ ] Original repro no longer reproduces (Phase 1 loop re-run)
- [ ] Regression test passes, or the absence of a seam is documented
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` the prefix)
- [ ] Throwaway prototypes deleted, or moved to a clearly marked debug location
- [ ] The correct hypothesis stated in the commit or PR message, so the next debugger learns

Then verify the completion claim with [verification-before-completion](../verification-before-completion/SKILL.md). Never claim "fixed" from a code change alone.

## If three fixes fail: question the architecture

Count your fixes. At three, stop and do not attempt a fourth.

The pattern that means architecture rather than hypothesis:

- Each fix reveals new shared state or coupling in a different place.
- Each fix requires a big refactor to implement.
- Each fix creates new symptoms elsewhere.

That is not a failed hypothesis; it is a wrong design. Ask whether the pattern is fundamentally sound, whether you are sticking with it through inertia, and whether to refactor the architecture instead of fixing symptoms. Discuss with the user before touching more code.

## Common rationalizations

| Excuse | Reality |
|---|---|
| "Issue is simple, no process needed" | Simple issues have root causes too. The process is fast for simple bugs. |
| "Emergency, no time" | Systematic debugging is faster than guess-and-check thrashing. |
| "Just try this first, then investigate" | The first fix sets the pattern. Do it right from the start. |
| "I'll write the test after confirming the fix" | Untested fixes don't stick. The test proves it. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms is not understanding the root cause. |
| "One more attempt" after two failures | Three failures means an architectural problem. Question the pattern. |

## Red flags — STOP and return to Phase 1

- "Quick fix now, investigate later"
- "Just try changing X and see if it works"
- "Add several changes and run the tests"
- "Skip the test, I'll verify manually"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "The pattern says X but I'll adapt it differently"
- Listing fixes before tracing the data flow
- "One more fix attempt" when you have already tried two
- Each fix reveals a new problem in a different place

All of these mean: stop, return to Phase 1.

## When the process finds "no root cause"

If investigation shows the issue is truly environmental, timing-dependent, or external: you have completed the process. Document what you investigated, add the appropriate handling (retry, timeout, error message), and add monitoring for next time.

95% of "no root cause" cases are incomplete investigation.

## Techniques

| File | Use |
|---|---|
| [references/root-cause-tracing.md](references/root-cause-tracing.md) | Trace a bug backwards through the call stack to its original trigger |
| [references/defense-in-depth.md](references/defense-in-depth.md) | Validate at every layer so invalid data cannot reach the dangerous operation |
| [references/condition-based-waiting.md](references/condition-based-waiting.md) | Replace arbitrary sleeps with condition polling in tests and harnesses |
| [references/condition-based-waiting-example.ts](references/condition-based-waiting-example.ts) | Complete `waitFor` helpers from a real flaky-test fix |
| [scripts/find-polluter.sh](scripts/find-polluter.sh) | Bisect which test creates unwanted files or state |
| [scripts/hitl-loop.template.sh](scripts/hitl-loop.template.sh) | Drive a human through a reproduction when the loop needs clicks |
