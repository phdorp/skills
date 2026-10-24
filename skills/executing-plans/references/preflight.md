# The Preflight Scan

Part of [executing-plans](../SKILL.md). Run it once, before Task 1, in every mode.

Scan the plan once for conflicts, writing down what you checked as you check it:

- tasks that contradict each other or the plan's Global Constraints;
- anything the plan explicitly mandates that a review rubric treats as a defect (a test that asserts nothing, verbatim duplication of a logic block).

The scan's output is a table, not a verdict:

- One row for every pair of tasks that share a file or an interface: the two tasks, what one produces against what the other consumes, and what you found.
- One row for every task: whether its own text agrees with itself — the tests it specifies against the code it specifies, the files it creates against the files it later touches.

"The scan is clean" without those rows is not a scan you ran. Write the table to the ledger.

Rule on everything the rows surface before execution begins: the spec is the binding authority, the plan is its argument. Record each ruling beside its row, then start Task 1. The review loop remains the net for conflicts that only emerge from implementation.

A plan whose tasks share nothing gets the single line `Pre-flight: no shared interfaces`.
