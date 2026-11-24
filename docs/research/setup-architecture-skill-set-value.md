# Is the `setup-architecture` skill set worth its tokens?

Research note, 2026-11-23. Question from the user: "I heard that an agent-assisted software
project may not benefit from a large skill set. Is the skill set around `skills/setup-architecture`
likely to be beneficial for software quality, or is it a waste of tokens?"

This builds on [software-architecture-skill-sets.md](software-architecture-skill-sets.md), which
mapped existing architecture skill sets and the research on LLMs drafting ADRs and quality
scenarios (its §6). That note asked *what to build*. This note asks *whether what was built pays
for its context*. It does not repeat the earlier note's literature.

**Ran** marks a claim I checked by running something in this session. **Unverified** marks a
claim I could not check. Sources are numbered and listed at the end. Scratch files lived in a
`mktemp -d` directory outside the repository.

## Verdict: conditional, and the conditions mostly hold

The skill set is **likely beneficial**, and the "large skill sets hurt" finding is mostly not
about this kind of skill. Since this note was first written, a benchmark with hidden
requirements ([§5](#5-measured-hidden-requirements-and-the-code-built-from-them)) has measured
what the earlier version could not. As committed at `ba2f17d`, the set **found fewer of the
architect's unstated requirements than Matt Pocock's `grill-me`**. After it adopted grill-me's
interview, it found all of them in every run, and code built from its documents matched
grill-me's. Three conditions apply:

1. **It costs little when idle.** Outside a set-up project, the whole set costs **112 tokens**
   of skill listing per session, plus about **1.2k tokens** of arc42 pointer lines. Those lines
   load only when a host skill (`design-dialogue`, `code-review` and others) is invoked
   (**Ran**, [§3](#3-token-cost-measured)). The research that finds context hurts agents studied
   **always-loaded** context files. Those cost the full file on every task [5][6]. That is a
   different mechanism.
2. **It helps where its job is to hold the agent back.** In the repo's own eval suite, the
   architecture scenarios went from mostly failing to mostly passing (S06/S07/S09/S10 grader
   scores 0.00–0.07 → 1.00, [§2](#2-evidence-from-this-repos-evals)). The four control scenarios
   held, with one small regression. The suite measures *process conformance*: did the agent
   propose instead of decide, and stop at `proposed` ADRs? It does **not** measure downstream
   software quality. §5 measures that for one product: the interview, not the documentation
   process, decides how much of the hidden requirements the code meets.
3. **It is worth its cost only for projects that actually have an architect.** The value is
   keeping decisions with a human architect and keeping them traceable. In a solo or small
   project, the setup session's roughly 8–13k tokens, two or more turns and process overhead may
   buy nothing. The skill is user-invoked (`opencode/autoinvoke: false`; scenarios invoke it with
   `/sa:setup-architecture`), so such projects never pay that part.

It is **not** a waste of tokens. The two cheap fixes worth making are trimming the set-up
session's fan-out and dropping the always-on description ([§6](#6-recommendations)). The
interview fix of §5 mattered more than either.

## 1. What "large skill set hurts" actually measured

| Study | What was loaded | Finding (from the abstract) | Applies here? |
|---|---|---|---|
| Gloaguen et al., *Evaluating AGENTS.md* (arXiv 2602.11988, v3 2026-09-29) [5] | Repository-level context files (`AGENTS.md`), loaded on every task | "does not generally improve task success rates", "increasing inference cost by over 20% on average"; repository overviews "are not helpful"; instructions in the files are "well followed" | **Partly.** That mechanism is always-on context. Here, only the 112-token listing is always on. The lesson "unnecessary requirements make tasks harder" does apply to the pointer lines in host skills ([§4](#4-risks)). |
| Lulla et al., *On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents* (arXiv 2601.20404, v2) [6] | `AGENTS.md`, 124 PRs, 10 repos | "lower median runtime", "reduced output token consumption", "comparable task completion behavior" | It contradicts [5] on efficiency. Same mechanism, small sample. |
| SkillsBench (arXiv 2602.12670, v4 2026-06-14) [7] | Curated **on-demand** Agent Skills vs none | Curated Skills raise the average pass rate "from 33.9% to 50.5%"; "Focused Skills with at most three modules outperform larger or exhaustive bundles" | **Yes, the closest evidence.** It supports focused, curated skills. It warns against exhaustive bundles, and this set's setup session loads up to 9 files ([§3](#3-token-cost-measured)). |
| IFScale, *How Many Instructions Can LLMs Follow at Once?* (arXiv 2507.11538) [8] | Up to 500 keyword-inclusion instructions in one prompt | "even the best frontier models only achieve 68% accuracy at the max density of 500 instructions"; "bias towards earlier instructions" | **Weakly.** It shows many simultaneous rules degrade, but it is a synthetic report-writing task, not coding. |
| Anthropic, *Effective context engineering* [4] | (guidance, not a study) | Context is "a finite resource with diminishing marginal returns"; aim for "the smallest possible set of high-signal tokens" | It is the design rule both ways: keep idle cost low, keep loaded content high-signal. |

The papers' own wording on how skills differ (not their claims):

- Anthropic's Agent Skills overview says "you can install many Skills without context penalty:
  until a Skill is triggered, only its name and description occupy context". It puts metadata at
  "~100 tokens per Skill" and the triggered body at "Under 5k tokens" [1, §"Level 1" and the
  levels table].
- The Agent Skills spec gives the same figures: "Metadata (~100 tokens)", "Instructions
  (< 5000 tokens recommended)", "Keep your main `SKILL.md` under 500 lines" [3, §"Progressive
  disclosure"].
- Claude Code qualifies the "no penalty" claim. A loaded skill "stays in context across turns, so
  every line is a recurring token cost" [2, §"Types of skill content"]. After compaction, skills
  are re-attached at up to 5,000 tokens each within a 25,000-token shared budget [2, §"Skill
  content lifecycle"].

**Not found:** a study of on-demand skills on SWE-bench-style coding tasks that varies the
*number* of installed skills. SkillsBench varies the presence and size of skills per task, not
the size of the library. Whether a 33-skill library slows task selection or misfires triggers is
**Unverified** by published evidence.

SkillsBench's v1 abstract also reported that self-generated skills gave no benefit. The v4
abstract I read does not say so, so I do not rely on it (**Unverified** in the current version).
This repo's skills are agent-drafted but changed only through RED/GREEN runs (AGENTS.md step 4).
That is not the "self-generated without feedback" condition, whichever version applies.

## 2. Evidence from this repo's evals

Source: `evals/software-architecture/results/{baseline,branch}.json` and `README.md` [9].
Haiku 5.5 at medium effort, Opus 5.5 judge, 2 runs per scenario and arm. `baseline` = skills at
`main` (`ee3e907`, without the architecture set). `branch` = skills at `5faee30`.

| Scenario | Skill exercised | Baseline grader / judge | Branch grader / judge |
|---|---|---:|---:|
| S06 setup-fresh | `setup-architecture` | 0.000 / 0.250 | 1.000 / 1.000 |
| S07 setup-documented | `setup-architecture` | 0.071 / 0.000 | 1.000 / 1.000 |
| S09 recovery-python | `setup-architecture` + `recovery.md` | 0.000 / 0.000 | 1.000 / 1.000 |
| S10 recovery-dataflow | same | 0.000 / 0.000 | 1.000 / 0.875 |
| S04, S05 requirements | `add-requirements`, `quality-requirements` | 0.500, 0.375 / 0.750, 0.000 | 1.000 / 1.000 |
| S03, S11, S12, S15–S19, S21 | arc42-gated parts of host skills | 0.167–0.625 | 0.750–1.000 |
| **Controls** S01, S13, S14, S20 (no arc42) | must stay ordinary | 1.000 / 1.000 | 1.000, **0.900**, 1.000, 1.000 / 1.000 |

What the baseline did without the set, quoted from the suite's README [9]:

- "set up the architecture" became "a coded program in turn 1, with nothing proposed to confirm
  and no arc42 or ADR" (S06).
- It "rewrote or duplicated the README's architecture" (S07).
- In S09/S10 it "wrote a whole architecture document in turn 1, proposed no 'made centrally'
  list, marked nothing as found".

These are the failure modes the set exists to prevent.

Limits of this evidence:

- **It measures conformance, not quality.** The rubric (`RUBRIC.md`) checks behaviour the skills
  prescribe. For example, S06 J1 asks for "a triage outcome for each of the six requirements …
  and asks the architect to confirm". A baseline agent that never heard of the R-list cannot
  pass. The scores show the skills change behaviour as designed. They do not show the resulting
  software is better (**Unverified**).
- **n = 2 per arm.** The README says so itself: "Two runs per scenario cannot detect small
  effects."
- **The controls show a small cost on unrelated work.** S13 dropped to 0.900 because a run
  "says mid-run that the repo has no arc42 doc". S11 still fails 1 of 2 runs, because the agent
  skipped the gated reference. Gated pointers are cheap, but they are not free of behaviour.
- **Run cost:** all 42 runs cost $0.955 (baseline) vs $1.113 (branch), **+17%**. On the four
  setup scenarios it was $0.308 vs $0.430. The baseline runs were cheaper partly because they
  skipped the confirmation turn's work. They are not a like-for-like price (**Ran**, summed from
  `results/*.json`).

## 3. Token cost, measured

Method (**Ran**): I used `claude` CLI 2.1.326 with `claude-haiku-5-5`, `--setting-sources
project`, `--strict-mcp-config`, a clean environment, and a temp workspace. The prompt "Reply
OK." ran with each skill collection, built from `git archive HEAD`, loaded as the plugin `sa`.
The figure is the API's reported input tokens (`input + cache_creation + cache_read`). Each arm
ran twice and gave identical totals. For file sizes, I prompted "Reply OK.\n\n<file>" with no
skills and subtracted the bare prompt. That counts with the real tokenizer of Haiku 5.5, which
other Claude models may tokenize differently (**Unverified**). One file needed a re-run with
`--tools ""`, because the agent acted on the template's text and used tools (6 turns, 99k).

**Always on (every session, every project):**

| Collection loaded | Input tokens | Δ |
|---|---:|---:|
| no skills (CLI built-ins only) | 16,240 | — |
| all 33 skills except `setup-architecture`, `add-requirements`, `quality-requirements` | 18,188 | +1,948 |
| all except `setup-architecture` | 18,300 | +112 vs previous |
| full collection | 18,350 | **+50** vs previous |

- `setup-architecture`'s description costs **50 tokens**, and the three skills together cost
  **112**. That is under Anthropic's "~100 tokens per Skill" estimate [1].
- The whole 33-skill listing costs 1,948 tokens, about 1% of a 200k window.
- `opencode/autoinvoke: false` does **not** hide the description in Claude Code. The `init` event
  listed `sa:setup-architecture` (**Ran**). In Claude Code, only `disable-model-invocation: true`
  gives "Description not in context" [2, §"Control who invokes a skill"].

**On invocation of `/setup-architecture`:**

| File | Tokens | When |
|---|---:|---|
| `setup-architecture/SKILL.md` | 2,170 | always |
| `references/arc42-skeleton.md` | 1,063 | turn 1, always |
| `references/made-centrally-adr.md` | 551 | turn 1, always |
| `quality-requirements/SKILL.md` | 1,655 | "Load both before you write any file" |
| `domain-modeling/SKILL.md` + `ADR-FORMAT.md` | 2,922 | same |
| `add-requirements/SKILL.md` | 1,676 | for the triage checks (S06-r1 loaded it, r2 did not [9, campaign 04]) |
| `quality-requirements/references/*` (two files) | 1,661 | when scenarios are written (**Unverified** how often) |
| `references/recovery.md` | 1,120 | undocumented projects only |

- The total is **≈ 8.4k** tokens for the files always loaded. Up to **≈ 12.8k** tokens if every
  linked file is read, about 6% of a 200k window.
- Per Claude Code [2], this stays in context for the rest of the session.
- Every file is under the spec's 5k-token body guideline [3].
- The cost is paid once per project setup, a rare event.

**In a set-up project only** (gated on `docs/architecture/arc42.md`), each reference loads
when its host skill is invoked:

| Reference | Tokens |
|---|---:|
| `design-dialogue/references/architecture.md` | 1,195 |
| `spec-and-plan/references/quality-requirements.md` | 591 |
| `executing-plans/references/architecture-decisions.md` | 1,305 |
| `code-review/references/architecture-axis.md` | 1,546 |

**The pointer tax on every project:** the arc42 pointer lines are spread over seven host files.
Those files are `design-dialogue`, `spec-and-plan`, `code-review`, `executing-plans` (with
`implementer-prompt.md`), `improve-codebase-architecture`, `domain-modeling` and
`setup-project-workflow`. Together the lines cost **≈ 1,185 tokens**. They load whenever those
host skills load, even with no arc42. The lines are my own `grep` selection, so this figure is
approximate.

## 4. Risks

- **The set fans out to many files.** SkillsBench found focused skills with "at most three
  modules" beat exhaustive bundles [7]. A setup session reads 5–9 files across four skills. The
  split keeps one meaning in one place (AGENTS.md "Editing rules"), which is a real
  maintainability gain. But it costs context and gives the agent places to skip a step. The
  "Load both" instruction is one sentence. Whether the agent obeys it under Opus or Sonnet is
  **Unverified**: evals ran Haiku only.
- **Gated pointers leak into ordinary work.** The S13 control regressed, and S11-r1 skipped its
  gated reference [9]. This is the always-loaded-context problem of [5], at small scale: rules
  that do not apply still shape behaviour.
- **Triggers could overlap.** The listing has three architecture-flavoured descriptions:
  `setup-architecture`, `improve-codebase-architecture` and `codebase-design`. There are also two
  setup skills: `setup-architecture` and `setup-project-workflow`. The descriptions name
  distinct objects (architecture documentation, deepening opportunities, module interfaces,
  issue tracker), and every setup scenario was slash-invoked. So mis-triggering is
  **Unverified**, neither seen nor tested: no scenario gives an unprompted "document our
  architecture" request. The README's known gaps also list that the CLI's built-in `code-review`
  collides with `sa:code-review`.
- **Process overhead on small projects.** Two or more confirmation turns, an R-list, QG/QS
  tables and a `proposed` ADR gate are heavy for a weekend tool. The research note's premise
  that "the human is the architect" [10] is the condition under which this pays off. Without an
  architect, the set's main effect is to make the agent wait.
- **The quality claim is untested.** No eval measures defect rates, maintainability or
  conformance of later code to the recorded architecture. The earlier note's literature [10 §6]
  supports "agent drafts, human decides" for ADR quality. That is evidence for the *process*, not
  for better software.

## 5. Measured: hidden requirements and the code built from them

Harness, transcripts and judgements: [`evals/hidden-requirements/`](../../evals/hidden-requirements/README.md)
(**Ran**). A simulated architect (Sonnet 5.5) held twelve requirements that a three-sentence
product idea leaves out: offline use at the pitch, GDPR and no cloud, a NAS at 0 EUR, a Monday
report, a 3-tap QR check-out, a CSV export, tiny scale, a Python-only maintainer, 2-year history,
expiry warnings, no money handling, and a go-live date. A Haiku 5.5 designer ran each arm. A
fresh Haiku 5.5 agent **without skills** then built the product from the documents alone. Opus
5.5 scored the documents and the code against the hidden list.

| arm | design /24 | hidden reqs written /12 | designer messages | code /24 | code quality /10 |
|---|---|---|---|---|---|
| `setup-architecture` at `ba2f17d` | 16, 7 | 8, 3 | 5, 3 | 19, 15 | 8, 6 |
| upstream `grill-me` | 24, 19 | 12, 9 | 11, 8 | 23, 23 | 8, 8 |
| `setup-architecture` with the interview (iteration 3) | 24, 24, 24 | 12, 12, 12 | 3, 3, 4 | 23, 22, 23 | 8, 8, 8 |
| final skills (gap questions without a recommendation) | 24, 24 | 12, 12 | 5, 3 | – | – |

What it shows:

- **The old set asked too narrowly.** It triaged the requirements in the brief and asked a few
  ISO 25010 gap questions. Nothing asked about scope, platform, budget, maintainers, data
  retention, non-goals or deadlines. One run asked two gap questions and recorded 3 of 12
  requirements. Grill-me's first round ("where does it run and who maintains it?", "what must
  the first version do?") brought out most of the list.
- **Requirements found decide the code.** The build from the 3-of-12 documents scored 15/24.
  With no maintainer constraint recorded, it came out in Node.js, and the Monday report and
  expiry warnings were missing. Builds from complete documents scored 22–23. The builder fills
  gaps with plausible defaults (grill-me's 9-of-12 documents still gave 23), but it cannot
  invent a constraint like "Python only".
- **Code quality did not separate the arms** once requirements were complete. All final builds
  scored 8/10, and every build's tests passed. The set adds no measurable code quality beyond the
  requirements it finds, but it needs fewer architect turns than grill-me (3–4 vs 8–11), and it
  leaves technology choices to ADRs (one grill-me run recommended Flask and SQLite, and the
  architect simply accepted).

The change, in three RED/GREEN iterations: `quality-requirements` › Gap question became
› Interview. It asks the frontier in numbered rounds with a recommended answer, covering a fixed
territory (users and scale, scope, non-goals, platform and cost, maintainers, data and law,
deadline, neighbours, uncovered 25010 characteristics). Each answer is sorted into the R-list,
constraints, out of scope, stakeholders, figures or ruled-out qualities. `setup-architecture`
repeats the proposal plus the next round until the frontier is empty. Iteration 2 added scale
(H7 was missed once), and iteration 3 gave figures and ruled-out qualities a place in arc42 (H7
was asked but not written in 2 of 3 runs). The longer first turn then cost two process rules
on the existing suite. In S06 the "did you leave out" question came with a pre-filled answer,
so gap questions now carry no recommendation. In undocumented projects, the recovery report and
the hold on sections 4–8 and 11 slipped. After those fixes, 5 of 6 regression runs on the
final skills pass every grader check, and 5 of 6 pass every judged criterion. The two misses
are in steps this work did not change
([`results/regression/`](../../evals/hidden-requirements/results/regression/README.md)).

Limits: 2–3 runs per arm, one product, Haiku only, and a judge that saw the hidden list. The
simulated architect rewards broad questions by answering with a whole cluster of facts.

## 6. Recommendations

Each one needs the RED/GREEN check AGENTS.md step 4 requires before it is adopted.

1. **Keep the set.** It is cheap when idle, and it fixes observed, severe failure modes: coding
   instead of documenting, and deciding for the architect.
2. **Add `disable-model-invocation: true` to `setup-architecture` and `add-requirements`.** Both
   are user-invoked already, so this saves about 90 always-on tokens in Claude Code. AGENTS.md
   allows the flag "when portability with other harnesses matters". The gain is marginal, so do
   it only if a host's listing budget gets tight. Claude Code's budget is 1% of the context
   window [2]; this figure is model-summarised from the docs page and **Unverified** verbatim.
3. **Trim the setup fan-out.** Make `add-requirements` step 1's checks a short inline list or a
   shared reference, so setup does not load a whole second workflow skill (1,676 tokens). Check
   whether `domain-modeling`'s ADR lifecycle table is needed at setup, which writes exactly one
   `proposed` ADR. Measure whether S06/S07 still pass.
4. **Shrink the pointer tax.** Each host skill needs only one gated line, "If
   `docs/architecture/arc42.md` exists, read X". Move the rationalisation-table rows about arc42
   (for example `design-dialogue` line 143 and `domain-modeling` line 117) into the gated
   references, so projects without arc42 never read them. Re-run the S01/S13/S14/S20 controls.
   S13's regression is the signal this targets.
5. **Measure quality, not only conformance.** §5 now grades code built from the set-up
   documents. Still missing: a scenario where a later ordinary ticket must respect an accepted
   ADR or a QS-n, graded on the resulting code. Run it with and without
   the set. Until such a scenario exists, "beneficial for software quality" stays a reasoned
   claim, not a measured one.
6. **Run at least one non-Haiku arm** on S06/S09 and the controls. Instruction-following
   degradation depends on the model [8].

## Unverified or not checked

- Downstream software quality beyond one product and one model (§5 has n = 2–3 per arm).
- Full texts of [5]–[8]: only the abstracts (current versions) were read. SkillsBench's v4
  abstract does not repeat v1's self-generated-skills or per-domain figures (search summaries
  gave a software-engineering gain of +4.5 pp in v1), so neither is relied on.
- Claude Code's listing budget figure ("1% of the model's context window") came from a
  model-summarised read of [2], not a verbatim quote.
- Token counts for models other than Haiku 5.5.
- How often `quality-requirements/references/*` and `add-requirements` are read in a setup
  session (campaign 04 shows 1 of 2 runs loading `add-requirements`).
- Trigger accuracy for unprompted architecture requests, and the effect of a much larger library
  on skill selection.

## Sources

1. Anthropic, *Agent Skills overview* — <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview>, §"Level 1: Metadata (always loaded)", §"Level 2: Instructions", §"Level 3: Resources and code", §"The Skills architecture".
2. Anthropic, *Claude Code: Skills* — <https://code.claude.com/docs/en/skills>, §"Control who invokes a skill", §"Types of skill content", §"Add supporting files", §"Skill content lifecycle", §"Frontmatter reference".
3. *Agent Skills specification* — <https://agentskills.io/specification>, §"Progressive disclosure".
4. Anthropic Engineering, *Effective context engineering for AI agents* (2025-09-29) — <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>, §"Why context engineering is important…", §"The anatomy of effective context". See also *Equipping agents for the real world with Agent Skills* (2025-10-16) — <https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills>, §"The anatomy of a skill" ("Progressive disclosure is the core design principle").
5. T. Gloaguen, N. Mündler, M. Müller, V. Raychev, M. Vechev, "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?", arXiv 2602.11988 (v3, 2026-09-29; ICLR 2026) — <https://arxiv.org/abs/2602.11988>, abstract.
6. Lulla et al., "On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents", arXiv 2601.20404 (v2, 2026-03-30; ICSE JAWs 2026) — <https://arxiv.org/abs/2601.20404>, abstract.
7. "SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks", arXiv 2602.12670 (v4, 2026-06-14) — <https://arxiv.org/abs/2602.12670>, abstract.
8. D. Jaroslawicz, B. Whiting, P. Shah, K. Maamari, "How Many Instructions Can LLMs Follow at Once?", arXiv 2507.11538 (2025-07-15) — <https://arxiv.org/abs/2507.11538>, abstract.
9. This repo: `evals/software-architecture/README.md` (Results, Known gaps), `RUBRIC.md`, `TASKS.md`, `results/baseline.json`, `results/branch.json`, `campaigns/04-setup-fresh.md`; `skills/setup-architecture/` and the skills it links; `AGENTS.md`.
10. [software-architecture-skill-sets.md](software-architecture-skill-sets.md) (this directory), §§5–6, 8.
