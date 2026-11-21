You are judging one recorded run of a coding agent against a rubric. You cannot run anything;
everything you need is below. Judge only what the run shows.

## The task the agent was given

{{TASK}}

## Criteria

{{CRITERIA}}

## Evidence

The transcript (`transcript.md`) shows the agent's messages, tool calls and tool results in
order. The workspace files are what the agent left behind.

=== transcript.md ===
{{TRANSCRIPT}}

{{FILES}}

## How to answer

For every criterion give exactly one verdict with:

- `criterion`: the criterion ID, e.g. `J1`.
- `pass`: `true` or `false`.
- `quote`: a passage copied character for character from the evidence above, which shows the
  verdict. A script checks that the quote occurs in the named source; a paraphrased or shortened
  quote with changed words invalidates the verdict. For a "did not do X" criterion, quote the
  passage that shows what the agent did instead, such as its final report.
- `source`: `transcript.md`, or `workspace/<path>` for a workspace file, exactly as named in its
  `===` header.
- `reason`: one sentence.

End your answer with a single fenced `json` block holding the list of verdicts and nothing after
it, for example:

```json
[{"criterion": "J1", "pass": true, "quote": "...", "source": "transcript.md", "reason": "..."}]
```
