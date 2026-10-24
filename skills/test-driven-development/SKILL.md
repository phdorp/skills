---
name: Test-Driven Development
description: Use when implementing a feature, fixing a bug, or changing behavior, and the work needs a test that proves it — especially when the user mentions red-green-refactor, test-first, integration tests, or asks for TDD.
---

# Test-Driven Development

## The iron law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Wrote code before the test? Delete it. Start over. Don't keep it as "reference", don't adapt it while writing tests, don't look at it. Delete means delete. Implement fresh from the test.

**Violating the letter of the rules is violating the spirit of the rules.**

## When it applies

Always: new features, bug fixes, behavior changes, and refactors that change behavior. Ask the user first for throwaway prototypes (`prototype`), generated code, and configuration files. Thinking "skip TDD just this once"? That is the rationalization this skill exists to catch.

## Seams: agree where tests go before writing any

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** Before writing the first test, write down the seams under test and confirm them with the user. No test at an unconfirmed seam.

Ask: "What's the public interface, and which seams should we test?" Give each proposed seam one line on what it catches and what it misses.

Choose seams that:

- Sit where the user's symptom or the feature's value is observable — a caller-facing interface, an HTTP route, a CLI invocation.
- Exercise the real bug pattern as it occurs at the call site. A seam too shallow to reproduce the chain that triggered the bug gives false confidence.
- Are few. You cannot test everything; the agreed seams put effort on critical paths and complex logic instead of every edge case.

When the interface shape is itself in question — how deep the module is, where the seam belongs, what the interface should expose — consult `codebase-design` for the shared vocabulary. It is a reference to consult, not a session to run.

## Vertical slices, not horizontal

Work in **vertical slices**: one test → one implementation → repeat. Each test is a **tracer bullet** that responds to what the last cycle taught you.

**Horizontal slicing** — writing all the tests first, then all the implementation — verifies *imagined* behavior. You test the *shape* of things rather than user-facing behavior, the tests go insensitive to real change, and you commit to test structure before understanding the implementation.

## The loop

### 1. RED — write one failing test

One behavior, one logical assertion, a name that reads like a specification ("user can checkout with valid cart").

Before the body, name the production change that should make this test fail, and confirm that change is a bug rather than an intentional decision. Can't name one? Redesign around observable behavior.

Derive the expected value independently: a known-good literal, a worked example, the spec. Never recompute it with the code under test.

### 2. VERIFY RED — watch it fail for the right reason

Run the test. Mandatory, never skipped.

Confirm:

- It fails, not errors.
- The failure message is the expected one.
- It fails because the feature is missing, not because of a typo.

Passes immediately? You are testing existing behavior — fix the test. Errors? Fix the error and re-run until it fails correctly.

If you didn't watch it fail, you don't know it tests the right thing.

### 3. GREEN — the minimal code

Write the simplest code that makes this one test pass. No extra parameters, no speculative options, no future features, no drive-by improvements.

**Minimal green** means every line is load-bearing: delete a line and the test should fail. If it still passes, that line was not part of the fix.

### 4. VERIFY GREEN — run the whole suite

Run the full project test command (bare `pytest`, `npm test`, `cargo test`), not just your file. A green run of the test you wrote is not a green suite.

Confirm:

- Your test passes.
- Every other test still passes.
- Output is pristine: no errors, no warnings.

Test fails? Fix the code, not the test. Other test fails? Fix it now. Any failure the run shows — including one you didn't cause — goes in your report by name.

### 5. TIDY — only the code you just wrote

After green, tidy **only what this cycle produced**: remove duplication in the new lines, fix names you just introduced, inline a helper that no longer earns its place. Keep the suite green; add no behavior.

Structural refactoring — moving seams, splitting modules, reshaping interfaces — belongs to **review**, not to the red-green cycle. Do not expand the loop into work the current test does not cover.

### 6. REPEAT

Next failing test for the next behavior.

## Good tests

A test exists to catch a specific break. It should:

- Test behavior a caller cares about, through a public interface.
- Describe WHAT, not HOW.
- Survive an internal refactor that leaves behavior unchanged.
- Be minimal: "and" in the name means split it.
- Read like a specification of the capability.
- Fail for the named reason when the production code breaks.

## Anti-patterns

**Implementation-coupled.** Mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.

**Tautological / mirror assertion.** The assertion recomputes the expected value the way the code does — `expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself. It passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a literal, a worked example, the spec.

**Change detector.** Only intentional decisions can fail the test — a constant's value, exact message wording, private structure. It fires on redesign and sleeps through bugs. Test the behavior that depends on the decision: not `expect(MAX_RETRIES).toBe(5)` but "a failing call is retried 5 times and the 6th attempt never happens."

**Horizontal slicing.** All tests first, then implementation, as above.

## Mock at system boundaries

Mock only:

- External APIs (payment, email)
- Databases, sometimes — prefer a test database
- Time and randomness
- The file system, sometimes

Don't mock your own classes or modules, internal collaborators, or anything you control.

At a boundary, design for mockability: inject the dependency instead of constructing it inside, and prefer SDK-style functions (`getUser(id)`, `createOrder(data)`) over one generic fetcher with conditional logic. Each mock then returns one specific shape and test setup needs no branching.

**The mock earns no assertions.** Asserting that a mock was called passes when the mock is present and fails when it is absent; it says nothing about your code. Assert the real component's behavior, or unmock it.

## Rationalizations

| Excuse | Reality |
|---|---|
| "Too simple to test" | Simple code breaks. The test takes 30 seconds. |
| "I'll test after" | A test written after passes immediately, which proves nothing. You never watched it fail, so you never proved it can catch the bug. |
| "Tests after achieve the same goals" | Tests-after answer "what does this do?"; tests-first answer "what should this do?" You verify the cases you remembered, not the ones you'd have discovered. |
| "Already manually tested" | Manual testing leaves no record and cannot re-run when code changes. "Worked when I tried it" is not coverage. |
| "Deleting hours of work is wasteful" | Sunk cost. The choice is rewrite with TDD (high confidence) versus keep untrusted code (low confidence, likely bugs). |
| "Keep it as reference" | You will adapt it. That is testing after. Delete means delete. |
| "This is hard to test" | Listen to the test. Hard to test means hard to use. |
| "TDD slows me down" | TDD catches bugs before commit and lets you refactor without fear. Shortcuts mean debugging in production. |
| "Existing code has no tests" | You are improving it. Add tests as you touch it. |

## Red flags — STOP and start over

- Code before test
- Test written after the implementation
- Test passes the first time you run it
- You can't explain why the test failed
- "Just this once"
- "I already manually tested it"
- "Keep as reference" or "adapt existing code"
- "TDD is dogmatic; I'm being pragmatic"
- "This is different because ..."

All of these mean: delete the untested code and start over with TDD.

## When stuck

| Problem | Move |
|---|---|
| Don't know how to test it | Write the wished-for API and the assertion first. Ask the user. |
| Test too complicated | The design is too complicated. Simplify the interface. |
| Must mock everything | The code is too coupled. Inject the dependency. |
| Test setup is huge | Extract a test utility. Still complex? Simplify the design. |
| Test must reach inside | The seam is wrong. Move it to a public boundary; consult `codebase-design`. |
| Requirement is unclear | Don't guess in code. Get the example that decides it, then test that. |

## Example: bug fix

**Bug:** empty email accepted. Find the cause with `systematic-debugging`; the fix starts with the failing test that reproduces it.

**RED**
```typescript
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});
```

**Verify RED**
```bash
$ npm test
FAIL: expected 'Email required', got undefined
```

**GREEN**
```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: 'Email required' };
  }
  // ...
}
```

**Verify GREEN**
```bash
$ npm test
PASS
```

## Completion checklist

- [ ] Seams agreed with the user and written down before the first test
- [ ] Every new behavior has a test
- [ ] Watched each test fail before implementing
- [ ] Each failure was the expected one, for the missing feature
- [ ] Implementation is minimal; no speculative features
- [ ] Full project suite passes and output is pristine
- [ ] Tests use real code; mocks only at system boundaries
- [ ] Edge cases and error paths covered
- [ ] Mutation check run on the changed production code
- [ ] Verified with `verification-before-completion` before claiming done

Cannot check every box? You skipped TDD. Start over.

For the mutation check, mock-level rules, complete fixtures, and the full warning-sign list, read [references/tests-and-mocks.md](references/tests-and-mocks.md).
