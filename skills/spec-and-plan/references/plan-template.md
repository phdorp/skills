# Plan Template

Save to `docs/plans/YYYY-MM-DD-<feature>.md` unless the project prefers another path, and commit it.

Write for an engineer who has not seen this codebase or this spec. Assume they write idiomatic code in the project's language once they know the exact interface and the exact test, and that they make a reasonable choice wherever the plan leaves one open. What they cannot know is what you decided: which files, which names and signatures, which values from the spec, which tests prove each task.

## Header

```markdown
# <Feature Name> Implementation Plan

**Goal:** <one sentence describing what this builds>

**Architecture:** <2-3 sentences about the approach>

**Tech Stack:** <key technologies and libraries>

**Spec:** <path to the spec or design doc this plan implements>
```

## Global Constraints

The spec's project-wide requirements, one line each, with exact values copied verbatim from the spec:

- version floors
- dependency limits
- naming and copy rules
- platform requirements

Every task's requirements implicitly include this section.

## Review Focus

The five input classes or failure modes the spec implies but no task's tests exercise, most likely to bite a person using the software, one line each, most likely first. Name the input or condition and the behaviour a reasonable person would expect.

The spec is a vision document: it says what the software must do, not everything it will meet, and its silence on an input is not permission for that input to break the program. Write this list once with the spec in front of you. Then, for each line, add the test that pins it to the task that owns the code, in that task's own step style.

## File Structure

Map what is created or modified and what each file is responsible for, before defining tasks.

```markdown
- `exact/path/to/file.ext` - responsibility
- `exact/path/to/existing.ext` - responsibility, and what changes
- `tests/exact/path/to/test.ext` - what it proves
```

- One clear responsibility per file.
- Prefer focused files over large ones that do too much.
- Split by responsibility, not by technical layer.
- Files that change together live together.
- Follow established patterns in an existing codebase.

## Tasks

A task is the smallest unit that carries its own test cycle and is worth a fresh reviewer's gate. Fold setup, configuration, scaffolding, and documentation into the task that needs them. Split only where a reviewer could reject one task while approving its neighbour. Every task ends with an independently testable deliverable.

````markdown
### Task N: <Component Name>

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Interfaces:**
- Consumes: <what this task uses from earlier tasks, with exact signatures>
- Produces: <what later tasks rely on: exact function names, parameter and return types>

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Implement `function(input: InputType) -> ResultType` in `exact/path/to/file.py`**

One line on the approach when the signature and the test leave a choice.
A code block only for an algorithm they do not determine.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## What a step contains

A step is done when the implementer can write exactly one reasonable thing from it. Unambiguous, not complete.

- **Test step**: the test's name and assertions as code, with the spec's exact values in them.
- **Code step**: the exact signature (name, parameters, return type), the file, and the specific values the spec pins. The implementer writes the body. A body appears only for an algorithm the signature and tests do not determine, or exact copy the spec fixes.
- **Verification step**: the command to run and the output that means it passed.
- **Reference to another task**: that task's Interfaces block says what to use; do not repeat its code.

A plan is the set of decisions the implementer cannot make alone. A plan longer than the code it describes has written the code instead. Lines that decide nothing ("TBD", "handle edge cases", "add appropriate validation", "write tests for the above", a type or function no task defines) are the opposite failure.

## Self-review

Run this yourself after writing the complete plan; do not dispatch it.

1. **Spec coverage**: skim each spec section and requirement. Point to the task that implements it. Add any missing task.
2. **Step scan**: every step allows exactly one reasonable action. Remove lines that decide nothing and bodies the signature and tests already determine.
3. **Type consistency**: types, method signatures, and property names in later tasks match earlier ones.
4. **Review Focus**: every listed input class or failure mode has a test in the task that owns the code.
5. **Proportion**: compare plan length to spec length. If code blocks dominate, replace bodies with signatures and test names, then check each step is still unambiguous.

Fix issues inline; no second review pass is needed.

## Execution handoff

After saving and self-reviewing, link the plan and ask the user to review it and confirm it captures what they want before implementation. Ask them to choose an execution mode when they have not already supplied one, with a one-sentence recommendation based on how much the tasks depend on each other's interfaces, how many there are, and what a shipped mistake would cost. Wait for approval, then hand off to the `executing-plans` skill.
