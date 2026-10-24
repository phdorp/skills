# Builder Check Prompt

Dispatch a fresh subagent with this prompt once the written design exists. Fill in the domain and the document path. The point is to read the document the way its next reader will: as a builder who cannot ask the author anything.

```
You are a talented [DOMAIN, e.g. "software engineer", "event planner",
"bakery consultant"]. You have been handed a design document and asked to
put together a plan to build what it describes. You will not be able to
talk to the person who wrote it.

Read [DOCUMENT_PATH].

Report only the questions you would still need answered before you could
plan this well: places where you would have to guess and a wrong guess
would matter. For each, give the question and why the answer changes the
plan. Rank them by importance.

Skip anything the document explicitly leaves to the builder, and anything
you could reasonably decide yourself. Skip nitpicks about wording.
```

## Sorting the response

Put every question in one of three piles.

- **Answered already** by the conversation or the project. Put the answer in the document. If the answer is in the repo, include the fact, not a pointer the builder cannot follow.
- **Minor.** A sensible builder could settle it without changing what gets built. Settle it, write the decision in the document, and mark it as your call.
- **Theirs.** Only the user can answer, and the answer changes what gets built. Bring the whole pile in one message, most important first.

Do not run the check twice. Update the document with the user's answers and hand it over with a short list of the calls you made.

If no subagent tool is available, read the document as that builder yourself and follow the same three piles.
