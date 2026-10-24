# Authoring best practices

Adapted from Anthropic's agent-skills authoring guidance. Part of [`writing-for-agents`](../SKILL.md). Use it as the checklist after the writing in `SKILL.md`; where the two differ, the repo's own rules win.

## Core principles

### Concise is key

The context window is shared with the system prompt, conversation history, other skills' metadata, and the actual request. At startup only metadata (name and description) is loaded; the body loads when the skill fires, and extra files only as needed. Once loaded, every token competes with the conversation, so concision still matters.

Default assumption: the agent is already very smart. Add only context it does not already have. Challenge each passage:

- Does the agent need this explanation?
- Can I assume it knows this?
- Does this paragraph justify its token cost?

Concise:

````markdown
## Extract PDF text

Use pdfplumber for text extraction:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
````

Verbose: three paragraphs explaining what a PDF is and that libraries exist before reaching the same six lines. The concise version assumes the agent knows what a PDF is.

### Set the degree of freedom

Match specificity to the fragility and variability of the task.

**High freedom** — text instructions. Multiple valid approaches, decisions depend on context, heuristics guide the work. A code review: analyse structure, find edge cases, suggest improvements, check conventions.

**Medium freedom** — pseudocode or a script with parameters. A preferred pattern exists, some variation is acceptable, configuration changes the behaviour.

**Low freedom** — one exact command, few or no parameters. The operation is fragile, consistency is critical, the sequence must be followed. A migration: run exactly this script, do not add flags.

The analogy: a narrow bridge with cliffs demands exact steps; an open field means give direction and trust the agent. Low freedom where a wrong step is expensive, high freedom where judgement is the point.

### Test across the models you use

A skill is an addition to a model, so its effect depends on the model. A smaller, faster model may need the explicit steps; a stronger reasoning model may find the same steps over-explaining. Test with the smallest and the largest you plan to support, and aim for instructions that hold for both.

## Structure

### Frontmatter

Two required fields:

- `name` — human-readable name, 64 characters maximum.
- `description` — the conditions that should trigger the skill, 1024 characters maximum.

The repo adds `metadata` for harness hints and, for user-invoked skills, `metadata: {opencode/autoinvoke: false}`.

### Naming

Prefer active, verb-first or gerund names that describe the activity: "Writing documentation", "Testing code", "Processing PDFs". Noun phrases and imperative forms are acceptable ("PDF Processing", "Process PDFs"). Avoid vague names ("Helper", "Utils", "Tools"), overly generic names ("Documents", "Data", "Files"), and inconsistent patterns within a collection.

Consistent naming makes a skill easy to reference in prose, understand at a glance, and find in a directory listing.

### Descriptions

Write in third person, and lead with the specific conditions that should fire the skill. A brief naming of the domain is fine; a summary of the workflow is not, because the agent will follow the summary instead of reading the body.

- Good: "Extracts text and tables from PDF files, fills forms, merges documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."
- Avoid: "Helps with documents", "Processes data", "I can help you process Excel files".

The description is the selection signal among many skills, so it must let an agent decide whether to load this one now. See [discovery.md](discovery.md) for keyword and anti-summary guidance.

### Progressive disclosure

`SKILL.md` is the overview that points to detail, like an onboarding guide's table of contents.

- Keep the body under about 500 lines.
- Split when approaching the limit.
- Put detail in files the agent opens only when needed.

A complete directory:

```
pdf/
├── SKILL.md              # instructions, loaded when the skill fires
├── FORMS.md              # form-filling guide, loaded as needed
├── reference.md          # API reference, loaded as needed
├── examples.md           # usage examples
└── scripts/
    ├── analyze_form.py   # executed, not loaded
    ├── fill_form.py
    └── validate.py
```

**Pattern 1: guide with references.** A quick start in `SKILL.md`, then one line per advanced topic pointing at its file, linked relatively.

```markdown
## Advanced features

**Form filling**: See `FORMS.md` for the complete guide.
**API reference**: See `reference.md` for all methods.
**Examples**: See `examples.md` for common patterns.
```

**Pattern 2: domain organisation.** One file per domain, so a sales question loads only sales reference. Grep commands in `SKILL.md` help an agent jump straight to the right file.

```
bigquery/
├── SKILL.md
└── reference/
    ├── finance.md
    ├── sales.md
    ├── product.md
    └── marketing.md
```

**Pattern 3: conditional detail.** Basic content inline, advanced content behind a pointer; the agent reads the advanced file only when the task needs that feature.

**One level deep.** A file referenced from a referenced file gets previewed (`head -100`) rather than read, and the agent proceeds on a fragment. Every reference file should be linked directly from `SKILL.md`.

**Contents list.** For a reference file over ~100 lines, open with a short contents list so a partial read still shows the scope.

## Workflows and feedback loops

Break a complex operation into ordered steps. For a long workflow, give a checklist the agent can copy and tick off; the checklist makes progress visible and makes a skipped step obvious.

```markdown
Copy this checklist and track your progress:

- [ ] Step 1: Read all source documents
- [ ] Step 2: Identify key themes
- [ ] Step 3: Cross-reference claims
- [ ] Step 4: Write the structured summary
- [ ] Step 5: Verify citations

**Step 1: Read all source documents.** Review each file in `sources/`. Note
the main arguments and the supporting evidence.

**Step 2: Identify key themes.** Look for repetition and disagreement.
...
**Step 5: Verify citations.** Every claim names the correct source. If a
citation is incomplete, return to Step 3.
```

For code-bearing workflows, the same shape with commands:

```markdown
- [ ] Step 1: Analyse the form — `python3 scripts/analyze_form.py input.pdf`
- [ ] Step 2: Map fields — edit `fields.json`
- [ ] Step 3: Validate — `python3 scripts/validate_fields.py fields.json`
- [ ] Step 4: Fill — `python3 scripts/fill_form.py input.pdf fields.json out.pdf`
- [ ] Step 5: Verify — `python3 scripts/verify_output.py out.pdf`

Fix validation errors before continuing. If verification fails, return to Step 2.
```

### Feedback loops

The common pattern is run validator → fix → repeat:

1. Make the change.
2. Validate immediately.
3. On failure, read the message, fix, validate again.
4. Proceed only when validation passes.
5. Verify the final output.

The validator can be a script or a reference document the agent checks against (a style guide, a standards file). The loop catches errors while the change is small.

### Plan, validate, execute

For batch or destructive work, have the agent write a plan in a structured file, validate the plan, then execute. This catches non-existent targets, conflicting values, and missing fields before anything is changed, and makes the plan reviewable and repeatable. Keep the validator's error messages specific about what was expected and what was found.

## Content guidelines

### Avoid time-sensitive information

Anything that will be wrong later is a liability. Instead of "before August 2025 use the old API, after use the new one", give the current method and an "old patterns" section for the deprecated one.

### Use consistent terminology

Choose one term and keep it: "API endpoint" throughout, not endpoint/URL/route/path. One term for "field", one for "extract". Consistency is what lets an agent map an instruction onto a codebase without guessing synonyms.

### Templates

For strict output, give the exact template and say it is exact:

```markdown
ALWAYS use this exact structure:

# [Analysis Title]

## Executive summary
[One paragraph]

## Key findings
- Finding with supporting data

## Recommendations
1. Specific action
```

For flexible output, give a sensible default and say judgement is expected. The difference is explicit; a template that looks strict but is meant flexibly gets followed literally.

### Examples

When output quality depends on style, give input/output pairs and name the pattern they share. Two or three good pairs beat a description of the style.

### Conditional workflows

At a decision point, route explicitly:

```markdown
1. Determine the modification type:
   **Creating new content?** → Creation workflow below
   **Editing existing content?** → Editing workflow below

2. Creation workflow: build from scratch, export.
3. Editing workflow: unpack, modify, validate after each change, repack.
```

If the branches grow large, give each its own file and point to the right one.

## Evaluation

Build the evaluation before the extensive documentation:

1. **Identify gaps**: run the agent on representative tasks without the skill; record specific failures and missing context.
2. **Write scenarios**: three that exercise those gaps, each with a query, the files involved, and the expected behaviour.
3. **Establish the baseline**: run them without the skill.
4. **Write the minimum**: just enough to pass.
5. **Iterate**: run, compare to baseline, refine.

This keeps the document aimed at real problems rather than anticipated ones. The full test method, including pressure scenarios for discipline skills, is in [testing-skills.md](testing-skills.md).

Development can be collaborative: one agent instance helps draft and refine the instructions, another runs them on real tasks. Observe where the second instance hesitates, reads a file in an unexpected order, misses a pointer, or repeatedly consults the same section. Those observations choose the next edit better than speculation.

## Anti-patterns

- **Windows-style paths**: use forward slashes everywhere (`scripts/helper.py`), including on Windows.
- **A menu of options**: give a default and one escape hatch ("use pdfplumber; for scanned files use OCR") rather than five libraries.
- **Magic constants in scripts**: a timeout of 47 with no comment is unguessable. State the reasoning.
- **Punting errors to the agent**: a script that raises a bare exception for a predictable missing file should handle it and say what it did.
- **Deep nested references**: see "one level deep" above.
- **Narrative history**: a story about one session is not a reusable technique.
- **Multi-language dilution**: one excellent runnable example beats five mediocre ports.
- **Unstated execution intent**: say "run this script" or "read this script", not both.

## Checklist

- [ ] Description is specific, third person, and includes triggers and key terms.
- [ ] Body is under ~500 lines; detail is in separate files.
- [ ] No time-sensitive claims, or they sit in an "old patterns" section.
- [ ] Terminology is consistent.
- [ ] Examples are concrete and runnable.
- [ ] File references are one level deep and use forward slashes.
- [ ] Progressive disclosure matches the branches.
- [ ] Workflows have ordered steps, checkable criteria, and a feedback loop.
- [ ] Scripts solve their own errors, justify constants, and state how to run them.
- [ ] Three or more evaluation scenarios exist, with a recorded baseline.
- [ ] Tested with the smallest and largest models you support.
