# Receiving review feedback

Review feedback is a technical claim, not a verdict. Verify it, then either implement it or refute it with evidence. Neither agreement nor gratitude moves the work forward.

## The response pattern

```
1. READ      the complete review without reacting or drafting a reply
2. RESTATE   each item in your own words (or ask)
3. VERIFY    the claim against codebase reality
4. EVALUATE  is it technically right for THIS codebase?
5. RESPOND   state the fix, or push back with reasoning
6. IMPLEMENT one item at a time, testing each
```

## Forbidden responses

| Don't write | Write instead |
|---|---|
| "You're absolutely right!" | The requirement, restated, or nothing — just fix it. |
| "Great point!" / "Excellent feedback!" | The technical consequence: "That input path does bypass validation; adding the guard in `parse.ts`." |
| "Thanks for catching that!" | "Fixed: dates now validate before the query runs (`search.ts:25`)." |
| "Let me implement that now" (before verifying) | Verify first; then say what you found and what you changed. |

Actions are the acknowledgement. If you catch yourself typing "Thanks", delete the sentence and state the fix.

## Handling unclear feedback

If any item is unclear, stop. Do not implement the items you do understand.

```
Reviewer: "Fix items 1-6."
You understand 1, 2, 3, 6. Items 4 and 5 are unclear.

Wrong: implement 1, 2, 3, 6 now, ask about 4 and 5 later.
Right: "I understand 1, 2, 3, 6. I need clarification on 4 and 5
        before implementing — 4 depends on whether the retry lives
        in the client or the queue, and 5 names a module I can't find."
```

Items in a review are usually related. Implementing the clear half often creates work that the unclear half invalidates.

## Source-specific handling

**From your human partner.** Trusted: implement after you understand it. Still ask when the scope is unclear. No performative agreement, no gratitude — start working or acknowledge technically.

**From an external reviewer** (PR comment, another team, an automated bot). Check before implementing:

1. Is it technically correct for *this* codebase?
2. Does it break existing functionality?
3. Why is the current code the way it is — is there a reason the reviewer cannot see?
4. Does the suggested version work on every platform and version this project supports?
5. Does the reviewer understand the full context, or only the diff?

If the suggestion looks wrong, push back with reasoning. If you cannot verify it, say so and ask which way to go. If it conflicts with a decision your human partner already made, stop and raise it with them rather than picking a side.

## YAGNI check

When a reviewer asks you to implement something "properly" — metrics, pagination, a plugin point, a config option — grep for actual usage first.

```
Reviewer: "Implement full metrics tracking with storage, date filters, and CSV export."

Grepped the codebase: nothing calls this endpoint, and no client sends the header.
"Nothing calls this endpoint. Remove it (YAGNI), or is there a consumer I'm missing?"
```

Both you and the reviewer report to the same person. If the feature has no user, the right fix is usually deletion.

## When to push back

Push back when:

- the suggestion breaks existing functionality;
- the reviewer lacks context the code depends on;
- it violates YAGNI — the thing has no callers;
- it is technically wrong for this stack or version floor;
- legacy or compatibility constraints make it a regression;
- it contradicts an architectural decision your human partner made.

How:

- Use technical reasoning, not defensiveness.
- Ask specific questions instead of asserting.
- Reference working tests, call sites, or docs.
- Escalate architectural conflicts to your human partner.

If pushing back out loud feels uncomfortable, name that tension to your partner along with the issue. They would rather hear it than have you implement something you believe is wrong.

**When you were wrong:** state it factually and move on.

```
"You were right — I checked the bundle target, and it does support the
newer API. Implementing now."
```

No long apology, no defence of why you pushed back.

## Implementation order

For multi-item feedback:

1. Clarify everything unclear, first.
2. Blocking issues: breaks, security holes, data loss.
3. Simple fixes: typos, imports, renames.
4. Complex fixes: refactors, logic changes.
5. Test each fix on its own; re-run the full suite at the end; confirm no regressions.

Do not batch all the edits and test once at the end. When a fix breaks something, you need to know which one.

## GitHub review threads

When replying to inline review comments on a pull request, reply **in the comment thread**, not as a top-level PR comment — a top-level comment leaves the original thread unresolved and unread.

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies \
  -f body="Fixed in 4a1c2de: the guard now runs before the query."
```

Resolve the thread once the fix is pushed. If you are pushing back, say so in the same thread with the evidence, and leave the decision visible to the reviewer rather than resolving it yourself.

## Common mistakes

| Mistake | Fix |
|---|---|
| Performative agreement | State the requirement, or just act. |
| Blind implementation | Verify against the codebase first. |
| Batch edits, one test run | One at a time, test each. |
| Assuming the reviewer is right | Check whether the change breaks something. |
| Avoiding pushback | Technical correctness beats comfort. |
| Implementing the clear half | Clarify all items first. |
| Cannot verify, proceeding anyway | State the limitation and ask for direction. |
| Replying at the PR level | Reply in the review thread. |
