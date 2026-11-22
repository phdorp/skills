# Standards sources and the smell baseline

The Standards axis asks whether the diff conforms to how this repo writes code. Two kinds of source answer that: what the repo documents, and a fixed baseline of code smells for what it does not.

## 1. Find the documented standards

Search the repo for every file that says how code should be written. Typical candidates:

- `CODING_STANDARDS.md`, `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`, `README.md` sections on style.
- `docs/` conventions, ADRs, architecture notes, review checklists, `STYLE.md`. When `docs/architecture/arc42.md` exists, ADRs and arc42 belong to the Architecture axis ([architecture-axis.md](architecture-axis.md)), not here.
- Linter and formatter configs (`.eslintrc*`, `eslint.config.*`, `ruff.toml`, `pyproject.toml`, `.golangci.yml`, `.rubocop.yml`, `.editorconfig`) — these show what tooling enforces, which you must not re-report.
- Language- or area-specific docs (`docs/api-guidelines.md`, `packages/*/README.md`).
- Domain vocabulary in `GLOSSARY.md`: a name that contradicts the glossary is a Mysterious Name finding with a documented fix.

List the files you found and check they exist in the checkout at `HEAD`. The reviewer has no other way to read them if you only name a path, so either pass their contents or confirm the reviewer can read them in its own checkout.

**Skip anything tooling already enforces.** A linter, formatter, or type checker that runs in CI owns those findings. Re-reporting them wastes the reviewer's budget and buries the judgement calls.

## 2. Apply the smell baseline

On top of whatever the repo documents, always carry this fixed set of Fowler code smells (_Refactoring_, ch. 3). Two rules bind it:

- **The repo overrides.** A documented repo standard always wins. Where a repo standard endorses something the baseline would flag, suppress the smell and say nothing.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. A documented-standard breach can be hard; a smell cannot.

Each smell reads *what it is* → *how to fix*. **(OO)** marks a smell that assumes objects and classes; its entry names the dataflow counterpart (blocks, connections, signals, as in `codebase-design`) where one exists. Match it against the diff:

- **Long Method**: a function so long that its parts need comments or names of their own. → extract the parts into named functions.
- **Large Class**: a class or module holding many unrelated fields or responsibilities. → split it along its responsibilities.
- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy** (OO): a method that reaches into another object's data more than its own. → move the method onto the data it envies. Dataflow: a block reading another block's internal variables instead of its outputs → read its output signal, or add one.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains** (OO): long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object. Dataflow: a connection reaching through nested sub-blocks → expose the signal on the outer block's connector.
- **Middle Man** (OO): a class or function that mostly just delegates onward. → cut it, call the real target direct. Dataflow: a pass-through block → connect the real source and target directly.
- **Refused Bequest** (OO, no dataflow counterpart): a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

## 3. Report a Standards finding

For each finding, give:

1. The location: `file:line`, not "somewhere in the parser".
2. The source: the standards file and the rule it states, or the smell name as a judgement call.
3. The evidence: quote the hunk.
4. The fix: one sentence, or "you decide" when the design call belongs to the implementer.

Label judgement calls as such ("possible Feature Envy"). Never promote a smell to a hard violation, and never let a smell override a documented standard.
