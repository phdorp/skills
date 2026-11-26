# Existing agent skill sets for human-led software architecture

Research note, 2026-11-21. Question: do agent skill sets (Agent Skills / `SKILL.md` collections,
Cursor rules, Copilot instructions, Codex/OpenCode prompts, MCP servers, plugin marketplaces)
already implement the architecture method in `software-architecture-fundamentals.md` [1]? The
method has these parts: the boundary between architecture and development, quality requirements as
ISO/IEC 25010 quality scenarios, choosing paradigms and patterns for those goals, ADRs, arc42,
programming principles, and patterns, anti-patterns and smells. The goal of the planned skill set
is that **the human is the architect** and the agent works as a coworker on requirements,
decisions and implementation. This note maps what exists, so the skill set can reuse it, adapt it,
or differ from it on purpose.

Every claim cites its source (numbered, listed at the end). **Ran:** marks a claim checked by
running something in this session: `gh api` metadata, shallow clones read with `grep`, `sed` and a
small frontmatter checker. **Unverified** marks a claim I could not check. Clones and scratch files
lived in a `mktemp -d` directory outside the repo. Downloaded content was read but never run.
Repository metadata was read on 2026-11-21. "Last commit" is the date of the default branch's HEAD
in a shallow clone. Star counts change, so treat them as an order of magnitude.

## Short answer

1. **No single skill set implements the whole method.** The pieces exist separately. The strongest
   are arc42 authoring and review (four serious sets), quality scenarios in the six-part form, and
   ADRs (dozens of skills). Nothing I found covers the method's **architecture/development
   boundary** (§2 of [1]). Nothing covers **choosing a paradigm or pattern *because* of a quality
   goal** (§4), and nothing links a pattern or smell review back to quality goals and ADRs.
2. **Four candidates match the "human is the architect" stance and are reusable:**
   - `LLM-Coding/Semantic-Anchors` `arc42-documentation`: cross-section traceability rules (Apache-2.0).
   - `MSiccDev/arc42-toolkit`: interview-first, one skill per arc42 section, with metric coaching (MIT).
   - `docs-as-code-toolkit/architecture-knowledge-toolkit`: "AI output stays *proposed* until a
     human acceptance is recorded" (MIT).
   - `skillrecordings/adr-skill`: "a human approves the decision; an agent implements it". It has
     **no licence**, so the ideas can be used but the text cannot be copied.
3. **The popular general packs either decide for the human or are thin.** Anthropic's
   `feature-dev` architect agent is told to make "confident architectural decisions" [15], and
   wshobson's `architect-review` agent says "Use PROACTIVELY for architectural decisions" [14].
   `45ck/software-architecture-skills` repeats the same 39 lines across all 14 of its skills
   (**Ran**) [13].
4. **The ISO 25010 edition is mostly stale.** The method uses ISO/IEC 25010:2023 (nine
   characteristics) [1]. Of the skills that list the characteristics, only `jabrena/plinth` uses the 2023 model [10].
   Semantic-Anchors and spec2ship still list the 2011 model's eight characteristics (Usability,
   Portability, Maturity) [3][7] (**Ran**).
5. **Licences limit copying arc42 material.** The arc42 template and quality.arc42.org are
   CC BY-SA 4.0 [16][17], and so is `arc42agentic` [6]. Text copied from them into this MIT repo
   would have to stay ShareAlike. MADR is `MIT OR CC0-1.0` [19] and can be reused freely.
6. **Research supports "the agent drafts, the human decides".** LLMs produce relevant ADR
   decisions but fall short of human level [24]. They check code-visible decisions well but
   deployment and organisational decisions poorly [27]. ATAM-style scenario analysis by an LLM
   beat students' work, but the comparison was with students [28][29].
7. **Recommendation: combine.** Build thin skills in this repo's style. Adapt the traceability
   rules from Semantic-Anchors and the interview pattern and metric coaching from MSiccDev, with
   attribution. Adopt MADR 4 as an optional, richer form of the existing `domain-modeling` ADR
   format. Link to arc42 and Q42 rather than copying them. Write the boundary skill, the
   goal-driven pattern choice and the traceable pattern/smell review from scratch. See
   [Recommendation](#8-recommendation).

## 1. How I searched

- **GitHub repo search** (`gh search repos`) for "arc42 skill", "arc42 claude", "arc42 agent",
  "arc42 llm", "arc42 mcp", "architecture decision record agent", "adr skill claude", "adr mcp
  server", "ISO 25010 llm", "quality attribute scenario", "software architect claude code",
  "C4 model skill", "architecture skills claude" and "software-architecture skill" (**Ran**).
  Multi-word repo search is strict: most phrases returned nothing, and "software-architecture
  skill" returned 14 repos.
- **GitHub code search** (`gh search code`, 40 hits per query) for `SKILL.md` files that mention
  arc42, ISO 25010, "25010", "quality attribute scenario", MADR, "architecture decision record",
  ATAM, "C4 model", "Lava Flow", "Golden Hammer", "Shotgun Surgery" + "Feature Envy" and "Gang of
  Four". Also searched for arc42 in `.cursor/rules`, `.cursorrules`, `copilot-instructions.md` and
  `AGENTS.md` (**Ran**). Code search caps results, so this is a sample and not a census.
- **First-party sources:** the `arc42` and `adr` GitHub organisations (all repos listed), the arc42
  sites' own `.claude/` folders, MADR, `anthropics/skills` and `anthropics/claude-plugins-official`
  (**Ran**: cloned and searched with grep).
- **Literature:** the arXiv API, searched for LLMs combined with architectural design decisions,
  ADRs, software architecture, quality attributes/ATAM, ISO 25010, architecture knowledge, arc42,
  design patterns and code smells. I read the abstracts of 12 papers (**Ran**). I did not read the
  full texts.
- **Frontmatter check** (**Ran**): a short script checked every `SKILL.md` of the main candidates
  against this repo's naming rule [2]: `name` is lowercase kebab-case, at most 64 characters, the
  same as the directory, and a `description` is present.

Not covered: Cursor/Copilot rule *marketplaces* (only GitHub was searched), and skill registries
that mirror other repos (for example `majiayu000/claude-skill-registry`, which showed up in the
hits as a mirror). **Unverified:** whether those hold originals not found on GitHub.

## 2. First-party sources

| Source | What exists | Relevance |
|---|---|---|
| **Anthropic** `anthropics/skills` (20 skills), `anthropics/claude-plugins-official` (57 `SKILL.md`) [15] | No skill mentions arc42, ISO 25010, quality attributes, ATAM or ADRs (**Ran**: grep). The `feature-dev` plugin's `code-architect` agent "delivers comprehensive, actionable architecture blueprints ... making confident architectural decisions". | Agent decides. The opposite role model. |
| **arc42 org** [17][18] | No arc42 *authoring* skill. `quality.arc42.org-site` has `.claude/skills/write-requirement`, `write-approach` and `write-standards`, but these maintain the site's own pages ("Do **not** commit — the author reviews"). `arc42/eTSU` (created 2026-09-06) is a requirements wiki with a `grill-requirements` skill, "Adapted from mattpocock/skills grill-with-docs", the same upstream as this repo's `design-dialogue` [2]. | Q42 is the best data source: 228 quality pages, 150 example requirements, 56 approaches (tactics), 48 standards (**Ran**: file counts). Licence CC BY-SA 4.0. |
| **adr org** [19][20] | MADR 4.0.0 (2024-09-17), licence `MIT OR CC0-1.0`. Template sections: Context and Problem Statement, Decision Drivers, Considered Options, Decision Outcome, Consequences, **Confirmation**, Pros and Cons of the Options. `madrlint` (Java) lints MADR files. No AI skills. | MADR's *Decision Drivers* can point to quality goals, and its *Confirmation* section can hold a scenario's measure. `madrlint` is the kind of mechanical check AGENTS.md prefers to prose [2]. |
| **`architecture-decision-record/architecture-decision-record`** (Joel Parker Henderson, ★17,498) [21] | `skills/architecture-decision-record-skill/SKILL.md` (123 lines). It covers whether a decision needs an ADR, picking a template, naming and superseding. | Solid ADR basics, but the licence is **CC BY-NC-SA** (NonCommercial), which is incompatible with MIT. Use as reading only. |

## 3. Coverage matrix

Legend: ✔ substantive coverage in the skill files; ◐ partial or mention-only; – none found. "Role"
is who makes the architectural decision according to the skill text.

| Candidate | §2 Boundary | §3 ISO 25010 / scenarios | §4 Tradeoffs / choice | §5 ADR | §6 arc42 | §7 Principles | §8 Patterns / smells | Role |
|---|---|---|---|---|---|---|---|---|
| Semantic-Anchors `arc42-documentation` [3] | – | ◐ 2011 model; ✔ six-part scenario with "literal figure" | ◐ 3-point Pugh matrix per ADR | ✔ Nygard + Pugh | ✔ 5 traceability rules | ◐ anchor catalogue only | ◐ anchor catalogue only | Human fills `?` and "(inferred)" gaps |
| MSiccDev `arc42-toolkit` [4] | – | ◐ Q42 tags, not 25010; ✔ scenario coaching | ◐ alternatives table | ✔ Nygard + alternatives | ✔ 12 section skills + lint + review | – | – | Human answers; agent drafts |
| docs-as-code `architecture-knowledge-toolkit` [5] | – | ✔ six-part, "never invent a target" | – | ✔ (not read in depth) | ✔ AsciiDoc, own metamodel | – | – | AI output *proposed* until human acceptance is recorded |
| `matthiasnissen/arc42agentic` [6] | – | ✔ ISO 25010 / Q42 reference, scenario template | – | ✔ §9 skill | ✔ write + 24 review/conflict agents | – | – | Interactive, 3–5 questions per round |
| `spec2ship/spec2ship` [7] | – | ◐ 2011 model, NFR IDs | ◐ multi-persona "roundtable" | ✔ MADR | ◐ templates | – | – | Agent personas reach consensus; user approves |
| `tractorjuice/arc-kit` (★2,290) [8] | – | ✔ Q42, "Target needed" if no metric | ✔ options with "Do Nothing" baseline | ✔ MADR 4 + UK Gov | ✔ assembled from artefacts | – | – | Never decides, but takes "(Recommended)" defaults and "never block[s]" |
| `skillrecordings/adr-skill` [9] | ◐ "proactive ADR triggers" | – | ◐ options in interview | ✔ four-phase, human gate | – | – | – | Human approves; agent implements |
| `jabrena/plinth` [10] | – | ✔ **2023 model**, review report | – | ✔ interactive | – | – | ◐ `123-java-design-patterns` (not read) | Escalates to "qualified owners" |
| `florianbuetow/claude-code` arc42 plugin [11] | – | ◐ §10 marked `GAP:human-input` | – | – | ✔ generated from code | – | – | "Flag, never fabricate" |
| `zircote-plugins/adr` [12] | – | – | ◐ decision drivers | ✔ 7 formats, compliance, quality | – | – | – | Not assessed |
| `45ck/software-architecture-skills` [13] | – | ◐ title only | ◐ title only | ◐ | – | – | – | Boilerplate |
| `gauravs19/enterprise-architecture-skill` [22] | – | ◐ review rubric | – | ✔ MADR (reference) | ✔ (reference) | – | – | Not assessed |
| wshobson `agents` [14] | – | ◐ keyword list | – | ✔ generic ADR skill | – | ◐ keyword list | ◐ keyword list | Agent decides ("Use PROACTIVELY") |
| arxitect, agent-playbook [23] | – | – | – | – | – | ✔ SOLID/DRY review | ✔ GoF + anti-pattern checklist | Reviewer; not tied to goals |
| **This repo** [2] | – | – | ◐ `design-dialogue` decision tree | ✔ `domain-modeling` (minimal) | – | ◐ `codebase-design` (depth, seams) | ◐ `code-review` 12-smell baseline | Human decides |

## 4. The best candidates in depth

### 4.1 `LLM-Coding/Semantic-Anchors`: `arc42-documentation` and `socratic-code-theory-recovery` [3]

- **Metadata (Ran):** ★546, Apache-2.0 (repo `LICENSE`), last commit 2026-11-15, created
  2025-11-10. The top contributors are `raifdmueller` (bio: "It's me - Claude! In Disguise"),
  `rdmueller` (Ralf D. Müller), `claude` and `Copilot`. Agent Skills format, plus a Claude plugin
  copy under `plugins/semantic-anchors/`. Frontmatter: 6/6 pass (**Ran**).
- **What it does:** `arc42-documentation` (80 lines) is a procedure for authoring arc42. It
  scaffolds the arc42 "with-help" template through docToolchain instead of "pasting a chapter
  skeleton from memory". Diagrams are C4-PlantUML. ADRs use Nygard format with a 3-point Pugh
  matrix. It adds **five cross-section traceability rules** that "arc42 templates do not enforce",
  for example "Every Chapter 1.2 quality goal maps to a named approach in Chapter 4" and
  "Chapter 6 includes at least one error/recovery scenario". Chapter 10 scenarios use the six-part
  form (Source, Stimulus, Artifact, Environment, Response, Response Measure), and the Response
  Measure must carry "a literal figure". Chapter 11 keeps Risks (probability, impact, priority) and
  Technical Debt (tied to a building block) apart, and every ADR consequence references a risk ID.
- **Role model:** when the rationale is unconfirmed, the ADR status is "Accepted (inferred)", and
  Pugh cells "that need team judgement" get `?` "rather than guessing a number". The brownfield
  skill `socratic-code-theory-recovery` splits questions into `[ANSWERED]` (with file:line evidence)
  and `[OPEN]` (routed to a role). It refuses Phase 2 synthesis until every open leaf is answered
  or deferred, "even when the user explicitly requests it".
- **Gaps:** its ISO 25010 reference lists "8 characteristics" (Usability, Portability, Maturity),
  which is the 2011 model, not the 2023 model the method uses (**Ran**: `references/iso-25010.md`).
  The repo's anchor catalogue has entries for SOLID, GoF patterns, code smells, ATAM, MADR, LASR,
  Pugh matrix and quality-attribute scenarios (**Ran**: `docs/anchors/` file list). They are short
  vocabulary entries, not skills.
- **Quality and reuse:** substantive and precise. It is the closest existing match to method §§3,
  5 and 6. The frontmatter says `license: MIT` while the repository is Apache-2.0 (**Ran**), so
  attribute it under Apache-2.0 to be safe. Its "architecture-documentation" contract (which pins
  the vocabulary) was not located in the clone (**Unverified**).

### 4.2 `MSiccDev/arc42-toolkit` [4]

- **Metadata (Ran):** ★51, MIT, last commit 2026-07-07. Author Marco Siccardi ("Software Architect
  / Senior Software Developer"). It has 14 skills: `arc42-section-01` … `-12`, `arc42-review` and
  `arc42-lint`, totalling 2,380 lines, plus a Python linter `scripts/arc42-lint.py` (not run).
  Frontmatter: 14/14 pass (**Ran**).
- **What it does:** each section skill has a "Step 1 — Ask These Questions First" block that says
  "**Do not generate any documentation yet.** Ask all questions below and wait for the answers".
  The skill then drafts, runs a self-check list, and iterates. Section 10 has a **metric coaching
  rule**: "If a user provides a vague quality statement … do not accept it. Push back
  immediately". It also keeps scenario IDs stable (retired, never renumbered). The ADRs in
  Section 9 are Nygard plus an alternatives table, and the skill says which parts are toolkit
  additions and not arc42 requirements.
- **Role model:** the human supplies every fact and decision, and the agent asks, drafts and
  checks. This matches the planned skill set best.
- **Gaps:** quality goals use Q42 tags and not ISO 25010. The tag list has **8 entries and leaves
  out `#maintainable`**, folding maintainability into `#flexible`. The quality.arc42.org data uses
  nine dimensions, including `#maintainable` (19 pages tagged) (**Ran**: counted tags in
  `_qualities/`). The site itself is inconsistent: one figure caption still says "eight quality
  dimensions" [17]. The toolkit has nothing on principles, patterns or the development boundary.
  The 12 near-identical section skills cost description budget. This repo would rather keep one
  skill with section references.

### 4.3 `docs-as-code-toolkit/architecture-knowledge-toolkit` [5]

- **Metadata (Ran):** ★4, MIT ("Copyright (c) 2026 Dieter Baier and contributors"), last commit
  2026-11-09. It has 21 skills, among them `architecture-core`, `adr`, `quality-scenario`, `risk`,
  `traceability-review`, `architecture-impact`, `grilling` and `domain-modeling`. It ships adapters
  for Copilot and others under `adapters/`. Frontmatter: 19/21 pass; 2 have a `name` that differs
  from the directory (**Ran**). The README says the product model is "explicitly non-commercial"
  even though the licence is MIT.
- **What it does:** `architecture-core` sets the rule "Keep AI-created or AI-modified architecture
  content draft or proposed unless human acceptance is already recorded". `quality-scenario`
  inspects existing documents and code, drafts six-part scenarios, and says "If no threshold can
  be justified, write an open question instead of inventing a target". It proposes metadata
  relations to quality objectives, ADRs and risks, then runs a validator.
- **Role model:** the most explicit statement of "the human is the architect" that I found.
- **Gaps and fit:** tied to its own AsciiDoc metamodel, docToolchain and generators. Much of its
  workflow (`grilling`, `domain-modeling`, `slice-issues`, `commit-message`) overlaps with skills
  this repo already has. Reuse the stance and the "open question instead of an invented target"
  rule, not the machinery.

### 4.4 `matthiasnissen/arc42agentic` [6]

- **Metadata (Ran):** ★55, last commit 2026-10-06. GitHub reports the licence as `NOASSERTION`;
  the `LICENSE` file is **CC BY-SA 4.0**. Written in German. It has 17 skills and 24 `.agent.md`
  files: 3 review orchestrators, 12 section reviewers, 7 cross-section "conflict" agents (for
  example quality-vs-strategy and risks-vs-quality), and interactive and from-code writers. An
  optional GraphML knowledge-graph mode comes with a scorecard script. The repo includes
  comparison runs of Opus/Sonnet 5.5 and GPT-6.1 as Markdown files.
- **Role model:** the writer asks "at most 3–5 questions" per round and fills sections from the
  answers.
- **Fit:** the most thorough arc42 *review* design found, especially the cross-section conflict
  agents. ShareAlike and German text make direct copying unattractive. Use it as a design
  reference for an arc42 review step.

### 4.5 `spec2ship/spec2ship` [7]

- **Metadata (Ran):** ★32, MIT, last commit 2026-07-12. It is a Claude Code plugin with skills
  `iso25010-requirements`, `madr-decisions`, `arc42-templates`, `roundtable-*`, `threat-modeling`
  and others.
- **Content:** ISO 25010 with "8 characteristics and 31 sub-characteristics" (2011 model), an ID
  scheme (`NFR-PERF-001`, `ARCH-001`, …), MADR naming and lifecycle.
- **Role model:** "Roundtables" of agent personas (PM, UX researcher, BA, QA) debate or reach
  consensus. The user reviews and approves at the end (`AskUserQuestion to approve / refine`). The
  agents produce the decision content and the human approves it afterwards.
- **Quality:** 11/12 skills use human-readable `name` values such as `ISO 25010 Requirements
  Structure`, which breaks this repo's naming rule (**Ran**) [2]. Not a basis for reuse.

### 4.6 `tractorjuice/arc-kit` [8]

- **Metadata (Ran):** ★2,290, last commit 2026-11-20. MIT, **except** `plugins/arckit-uk-gcloud/`
  (proprietary), and the arc42 overlay's template and Q42 material are CC BY-SA 4.0. Its core plugin ships
  76 slash commands (**Ran**: `ls commands`) for enterprise architecture governance, oriented to the UK government (TCoP,
  Secure by Design, G-Cloud, Wardley maps), with ports for Codex, OpenCode and Copilot.
- **arc42 overlay:** `/arckit:arc42` assembles the 12 sections from existing artefacts and lists
  uncovered sections in a "Gap Register". `/arckit:arc42-quality` "classified by the nine Q42
  dimensions; goals without a measurable target are listed, never estimated". The README states
  "They never make architecture decisions or invent targets".
- **ADR command:** 529 lines, MADR v4.0 plus UK government governance. It always includes a "Do
  Nothing" baseline, the default status is Proposed, and it names "Deciders". However, "An
  unanswered question takes its **(Recommended)** option … With no question tool available, take
  every default and never block".
- **Fit:** heavyweight and governance-oriented. Its rule against inventing targets and its gap
  register are worth copying as ideas.

### 4.7 `skillrecordings/adr-skill` [9]

- **Metadata (Ran):** ★90, **no licence**, last commit 2026-02-13, single contributor `joelhooks`.
  It has one 311-line skill with Node scripts (`new_adr.js`, `set_adr_status.js`).
- **What it does:** "ADRs created with this skill are **executable specifications for coding
  agents**. A human approves the decision; an agent implements it". It interviews "one at a time",
  passes an *intent summary gate* ("Do NOT proceed to Phase 2 until the human confirms"), adds an
  Implementation Plan and verification checkboxes, and reviews against a checklist. Its proactive
  triggers tell an agent to "stop and propose an ADR" when it hits a significant decision while
  coding.
- **Fit:** the best statement of the agent-as-coworker loop for decisions. Without a licence it
  cannot be copied; reimplement the ideas.

### 4.8 `jabrena/plinth` [10]

- **Metadata (Ran):** ★463, Apache-2.0, last commit 2026-11-18. It has 124 skills, all for Java
  enterprise work, and they pass the frontmatter check (**Ran**).
- **`814-regulations-iso-25010`:** the **only** skill found that uses ISO/IEC 25010:2023 with all
  nine characteristics. Its reference file contains the 2023 sub-characteristics (faultlessness,
  inclusivity, resistance, operational constraint, hazard warning, …) and none of the 2011 terms
  "maturity" or "portability" (**Ran**: grep). It produces an engineering *review report* and does
  not write specs, and it escalates conformity questions to "qualified owners".
- **`030-architecture-adr-general`:** an interactive ADR skill that confirms "alignment with the
  user before creating the ADR artifact".
- **Fit:** Java-specific framing, but its 25010:2023 reference summary is a reusable, licensed
  starting point for a language-neutral checklist.

### 4.9 Briefly

- **`florianbuetow/claude-code` `arc42-framework` [11]** (★21, MIT): generates arc42 from code.
  Sections 1, 10 and 11 are classed as "human-input": the skill emits `GAP:human-input` with a
  specific question there and never fabricates. A useful rule for brownfield work.
- **`zircote-plugins/adr` [12]** (★6, MIT): 12 skills covering Nygard, MADR, structured MADR,
  Y-statement, Tyree-Akerman, Alexandrian and business-case formats, plus decision drivers,
  compliance and quality. Not read in depth (**Unverified** beyond the frontmatter).
- **`45ck/software-architecture-skills` [13]** (★32, MIT): 14 skills (quality-attribute scenario
  writer, tradeoff writer, ADR writer, …). Every skill shares 39 identical non-empty lines out of
  about 58 (**Ran**), and none has a `description` field (0/14 pass, **Ran**). Thin.
- **`gauravs19/enterprise-architecture-skill` [22]** (★25, MIT): one 174-line router across C4 +
  Structurizr, ArchiMate, TOGAF and arc42 + MADR, with references. Broad but shallow per topic (not
  read beyond `SKILL.md`).
- **wshobson `agents` [14]** (★42,754, MIT): a generic ADR skill (166 lines). The
  `architect-review` agent is a keyword list ("SOLID Principles & Design Patterns", "Quality
  Attributes Assessment") with "Use PROACTIVELY for architectural decisions". The plugin
  `c4-architecture` has four C4 agents (not read).
- **Pattern and smell review [23]:** `andonimichael/arxitect` `oo-design-review` (★67, MIT) reviews
  SOLID, DRY and GoF applicability. `HunterGerlach/agent-playbook` `review-design-patterns` (★4,
  MIT) aims at "*appropriate* pattern usage" and has an anti-pattern checklist (Lava Flow, …).
  Neither links a pattern to a quality goal or an ADR (**Ran**: grep for quality/goal/ADR).
- **MCP servers:** only two small ADR servers turned up, `abest0/adr-mcp` and
  `matiaschediek/adr-mcp-server` (0 stars each). Not inspected (**Unverified**).
- **Not inspected, from names or descriptions only:** `jhl-labs/atam-skill`,
  `moeedhy/assessing-software-architecture-quality-skill` (an evidence-led review with an optional
  "49-factor" score; only the first 40 lines were read), `jQrgen/tdt4240-software-architecture-skill`
  (an NTNU course skill on quality attributes and tactics; CC BY-SA 4.0),
  `satishTheLegend/principal-architect-review`, `MonsieurBon/arc42-skill` (326 lines; its first rule
  is "Ask before assuming").

## 5. Overlap with this repo's skills

| Method part [1] | Existing skill [2] | Overlap and difference |
|---|---|---|
| §2 boundary: which decisions are central | none | No skill asks the team to agree which decisions are made centrally and recorded. The ADR "three criteria" test in `domain-modeling` (hard to reverse, surprising, real trade-off) is the nearest proxy. |
| §3 quality goals and scenarios | none | `spec-and-plan`'s spec template has no quality-requirements section (**Ran**: grep found only "links to ADRs"). Quality goals are therefore never elicited. |
| §4 choosing solutions | `design-dialogue`, `codebase-design`, `prototype` | `design-dialogue` grills a decision tree but does not use quality goals as the criteria. `codebase-design` is Ousterhout-style depth and seams, a concrete form of information hiding [1 §4]. |
| §5 ADRs | `domain-modeling` (`ADR-FORMAT.md`) | Deliberately minimal (1–3 sentences; Status, Considered Options and Consequences optional). The method asks for Nygard's five fields, supersede-never-delete, and MADR when options matter. A richer optional form is needed, not a replacement. |
| §6 arc42 | `domain-modeling` (`GLOSSARY.md` ≈ arc42 §12), `improve-codebase-architecture` | No arc42 skill. |
| §7 principles | `codebase-design` | Uses its own vocabulary (module, seam, depth) and avoids words like "component" and "boundary". A new skill must reuse these terms or say how they map to SOLID and to arc42's "building block". |
| §8 patterns, smells | `code-review` (`standards-and-smells.md`) | 12 Fowler smells as judgement calls. Of the five smells the method names, **Long Method and Large Class are missing**. No GoF or anti-pattern vocabulary. |

The pattern is that this repo is strong on dialogue, specs and module design, but has no
**quality** thread: no quality goals, no scenarios, and no criteria that tie decisions back to
quality.

## 6. What the research says

- **ADR generation:** with zero-shot prompting, GPT-4 "generate[s] relevant and accurate Design
  Decisions, although they fall short of human-level performance" [24]. Few-shot, RAG and
  fine-tuning improve the output, and combining them (DRAFT) helps most [25]. Context matters more
  than model size: "a small recency window (typically 3–5 prior records)" of earlier ADRs works
  best [26]. A skill should therefore load the latest few ADRs before drafting a new one. Agentic
  decomposition (extract, retrieve, generate, validate) produced better ADRs than a single prompt
  in a 29-repository user study [31].
- **Checking decisions:** across 980 ADRs in 109 repos, LLMs reached "strong accuracy for
  explicit, code-inferable decisions" but fell short "for implicit or deployment-oriented
  decisions", and are "not yet replacing human expertise" [27].
- **Quality scenarios and ATAM:** MS Copilot's analysis of quality-attribute scenarios (risks,
  sensitivity points, tradeoffs) was "in most cases better and more accurate" than students' and
  was compared with experienced architects' output [28][29]. Small, course-based samples.
- **Deriving quality requirements:** LLMs derived NFRs from functional requirements using the
  ISO/IEC 25010:2023 attributes. 80.4% of the attributes the LLMs assigned matched the experts'
  choices, and the median validity was 5/5 [35]. This supports an agent *proposing* candidate
  quality characteristics for the architect to prioritise.
- **ADR templates:** in a controlled experiment, Nygard's template beat MADR on an overall
  comprehension and usability score. Experts screened Nygard and MADR as the top two of five
  [32]. This supports Nygard as the default and MADR as the option for multi-option decisions,
  which is what the method says [1 §5].
- **Smells and patterns:** LLMs do well on structurally simple smells (Large Class, Long Method),
  and combining them with static analysis wins on five of nine smells, at the cost of more false
  positives on complex smells [33]. Pattern detection is promising but at pilot stage (five GoF
  patterns) [34]. Smell findings should therefore stay labelled judgement calls, as `code-review`
  already does.
- **Overview:** an SLR of 18 papers found LLMs "often outperform baselines" but "mostly use simple
  prompting". It names conformance checking and code generation from architecture as
  underexplored [30].

I read abstracts only; sample sizes and limitations beyond the abstracts are **Unverified**.

## 7. Licences that matter for reuse

| Source | Licence | Consequence for this MIT repo |
|---|---|---|
| arc42 template and docs [16]; quality.arc42.org [17]; arc42agentic [6]; arc-kit's arc42 overlay template [8]; jQrgen course skill | CC BY-SA 4.0 | Link and paraphrase in our own words. Copied text must stay CC BY-SA with attribution. |
| Henderson ADR repo [21] | CC BY-NC-SA | Do not copy. |
| `skillrecordings/adr-skill` [9] | none (all rights reserved) | Ideas only. |
| MADR [19] | MIT OR CC0-1.0 | Free to reuse the template. |
| Semantic-Anchors [3], plinth [10] | Apache-2.0 | Reusable with notice; record in `ATTRIBUTION.md`. |
| MSiccDev [4], docs-as-code toolkit [5], florianbuetow [11], zircote [12], arxitect [23] | MIT | Reusable with notice; record in `ATTRIBUTION.md`. |

This is not legal advice. I took the licences from each repo's `LICENSE` file and the GitHub API
(**Ran**).

## 8. Recommendation

**Combine: build thin skills here, adapting four sources with attribution and linking to the
CC BY-SA material instead of copying it.** No candidate is worth adopting whole. The ones closest
to the human-as-architect stance are either tied to their own toolchain (docToolchain/AsciiDoc in
[3][5]), split into 12 per-section skills [4][6], or unlicensed [9]. The ones that are
complete [7][8] either let agents decide or carry heavy governance.

What to adapt:

| Piece | Take from | Change |
|---|---|---|
| Quality goals and scenarios | MSiccDev's "ask first, push back on vague metrics" [4]; docs-as-code's "open question instead of an invented target" [5]; plinth's 25010:2023 summary [10] | Language-neutral, 2023 model, top 3–5 goals, six-part scenario. Link Q42 for examples. Hook into `spec-and-plan` so a spec carries its quality goals. |
| ADRs | MADR 4 [19] as the optional richer form; skillrecordings' intent-summary gate and proactive triggers (reimplemented) [9]; load the last 3–5 ADRs as context [26] | Extend `domain-modeling/ADR-FORMAT.md`: Nygard by default, MADR when options matter; *Decision Drivers* name the quality goals and *Confirmation* names the scenario. Mechanical lint in `scripts/` or via `madrlint` [20], not prose. |
| arc42 | Semantic-Anchors' five traceability rules and Risk/Debt split [3]; arc42agentic's cross-section conflict checks [6] as a review design | One skill with per-section references, Markdown, linked to the arc42 docs. Section 12 points to the existing `GLOSSARY.md` and section 9 to `docs/adr/`. |
| Pattern and smell review | `code-review` baseline [2]; arxitect/agent-playbook [23] as checklists | Add Long Method and Large Class, and the anti-pattern vocabulary of [1 §8.2], with each finding traced to the quality goal or ADR it threatens. |

What has **no good existing coverage** and must be written:

1. **The architecture/development boundary (§2):** a step where the architect states which
   decision classes are central (interfaces, data formats, dependency rules, crosscutting
   conventions) and which are left to developers. Agents then know when to stop and propose an ADR
   and when to just decide. This is the core of the coworker role, and I found nothing like it.
2. **Goal-driven solution choice (§4):** options evaluated against the prioritised quality goals,
   with the architect choosing. Semantic-Anchors' Pugh matrix is the nearest idea.
3. **Paradigm awareness:** the method's point that in dataflow languages "the signals are the
   interfaces" [1 §4]. No skill touches paradigm-dependent coupling. This matters for the
   repo's `openmodelica` domain.
4. **Traceability from code back to goals:** principles, patterns and smells checked against the
   recorded quality goals and ADRs, not as a generic checklist.
5. **Current ISO 25010:2023** in a language-neutral form. Only the Java-specific [10] has it.

## Unverified or not checked

- Full texts of the cited papers; only the abstracts were read.
- `zircote-plugins/adr`, `jhl-labs/atam-skill`, `satishTheLegend/principal-architect-review`,
  `abest0/adr-mcp`, `matiaschediek/adr-mcp-server`, wshobson's C4 agents, plinth's
  `123-java-design-patterns`, and the docs-as-code `adr` skill beyond their frontmatter or
  headers.
- Semantic-Anchors' "architecture-documentation" contract text, which I could not locate.
- No linter or script from any candidate was run (untrusted code). Claims about what
  `arc42-lint.py`, `madrlint` or the ADR scripts do come from their READMEs and skill text.
- Cursor and Copilot rule marketplaces outside GitHub, and skill registries that mirror other
  repos.
- Whether any of these skills *work* in practice. Nothing here was evaluated by running a
  session. Per AGENTS.md [2], any adopted piece should go through a RED/GREEN test with
  `writing-for-agents`.

## Sources

1. `software-architecture-fundamentals.md` (seminar summary; `/root/repos/software-architectrue/`), §§1–8.
2. This repo: `AGENTS.md`; `skills/domain-modeling/SKILL.md`, `ADR-FORMAT.md`; `skills/design-dialogue/SKILL.md`; `skills/codebase-design/SKILL.md`; `skills/spec-and-plan/SKILL.md`, `references/spec-template.md`; `skills/code-review/references/standards-and-smells.md`; `ATTRIBUTION.md`.
3. LLM-Coding/Semantic-Anchors — <https://github.com/LLM-Coding/Semantic-Anchors>: `skill/arc42-documentation/SKILL.md`, `skill/socratic-code-theory-recovery/SKILL.md`, `…/references/iso-25010.md`, `docs/anchors/`, `LICENSE`.
4. MSiccDev/arc42-toolkit — <https://github.com/MSiccDev/arc42-toolkit>: `skills/arc42-section-01`, `-09`, `-10`, `arc42-lint`, `arc42-review` `SKILL.md`; `LICENSE`.
5. docs-as-code-toolkit/architecture-knowledge-toolkit — <https://github.com/docs-as-code-toolkit/architecture-knowledge-toolkit>: `README.md`, `skills/architecture-core/SKILL.md`, `skills/quality-scenario/SKILL.md`, `LICENSE`.
6. matthiasnissen/arc42agentic — <https://github.com/matthiasnissen/arc42agentic>: `README.md`, `LICENSE`, `.agents/arc42-write.agent.md`, `.agents/skills/arc42-write-s10-quality/SKILL.md`.
7. spec2ship/spec2ship — <https://github.com/spec2ship/spec2ship>: `skills/iso25010-requirements/SKILL.md`, `skills/madr-decisions/SKILL.md`, `skills/roundtable-strategies/SKILL.md`, `skills/roundtable-execution/SKILL.md`, `commands/design.md`.
8. tractorjuice/arc-kit — <https://github.com/tractorjuice/arc-kit>: `LICENSE`, `plugins/arckit-arc42/README.md`, `plugins/arckit-arc42/templates/arc42-LICENSE.md`, `plugins/arckit-claude/commands/adr.md`.
9. skillrecordings/adr-skill — <https://github.com/skillrecordings/adr-skill>: `skills/adr-skill/SKILL.md`.
10. jabrena/plinth — <https://github.com/jabrena/plinth>: `skills/814-regulations-iso-25010/SKILL.md` and `references/814-regulations-iso-25010-chapters-summary.md`; `skills/030-architecture-adr-general/SKILL.md`.
11. florianbuetow/claude-code — <https://github.com/florianbuetow/claude-code>: `plugins/arc42/skills/arc42-framework/SKILL.md`, `LICENSE`.
12. zircote-plugins/adr — <https://github.com/zircote-plugins/adr>: `skills/*/SKILL.md` frontmatter.
13. 45ck/software-architecture-skills — <https://github.com/45ck/software-architecture-skills>: `skills/*/SKILL.md`.
14. wshobson/agents — <https://github.com/wshobson/agents>: `plugins/comprehensive-review/agents/architect-review.md`, `plugins/documentation-generation/skills/architecture-decision-records/SKILL.md`, `plugins/c4-architecture/`.
15. anthropics/skills — <https://github.com/anthropics/skills>; anthropics/claude-plugins-official — <https://github.com/anthropics/claude-plugins-official>: `plugins/feature-dev/agents/code-architect.md`.
16. arc42/arc42-template — <https://github.com/arc42/arc42-template>: `LICENSE.txt`.
17. arc42/quality.arc42.org-site — <https://github.com/arc42/quality.arc42.org-site>: `_qualities/`, `_requirements/`, `_approaches/`, `_standards/`, `_pages/05-how-to-use-this-site.md`, `_pages/10-quality-dimensions.md`, `.claude/skills/write-requirement/SKILL.md`, `LICENSE`.
18. arc42/eTSU — <https://github.com/arc42/eTSU>: `README.md`, `.claude/skills/grill-requirements/SKILL.md`.
19. adr/madr — <https://github.com/adr/madr>: `template/adr-template.md`, `CHANGELOG.md`, `LICENSE`.
20. adr/madrlint — <https://github.com/adr/madrlint>: `README.md`.
21. architecture-decision-record/architecture-decision-record — <https://github.com/architecture-decision-record/architecture-decision-record>: `skills/architecture-decision-record-skill/SKILL.md`, `LICENSE.md`.
22. gauravs19/enterprise-architecture-skill — <https://github.com/gauravs19/enterprise-architecture-skill>: `SKILL.md`.
23. andonimichael/arxitect — <https://github.com/andonimichael/arxitect>: `skills/oo-design-review/SKILL.md`; HunterGerlach/agent-playbook — <https://github.com/HunterGerlach/agent-playbook>: `skills/review-design-patterns/SKILL.md`.
24. R. Dhar, K. Vaidhyanathan, V. Varma, "Can LLMs Generate Architectural Design Decisions? An Exploratory Empirical Study", ICSA 2024 — <https://arxiv.org/abs/2403.01709>.
25. R. Dhar et al., "DRAFT-ing Architectural Design Decisions using LLMs", 2025 — <https://arxiv.org/abs/2504.08207>.
26. A. Gupta, R. Dhar, D. Feitosa, K. Vaidhyanathan, "Context Matters: Evaluating Context Strategies for Automated ADR Generation Using LLMs", EASE 2026 — <https://arxiv.org/abs/2604.03826>.
27. R. Su et al., "Evaluating Large Language Models for Detecting Architectural Decision Violations", 2026 — <https://arxiv.org/abs/2602.07609>.
28. R. Capilla, J. A. Díaz-Pace, Y. Ramírez, J. Pérez, "Supporting architecture evaluation for ATAM scenarios with LLMs", 2025 — <https://arxiv.org/abs/2506.00150>.
29. R. Capilla et al., "Towards Supporting Quality Architecture Evaluation with LLM Tools", 2026 — <https://arxiv.org/abs/2603.28914>.
30. L. Schmid et al., "Software Architecture Meets LLMs: A Systematic Literature Review", 2025 — <https://arxiv.org/abs/2505.16697>.
31. R. Dhar, K. Vaidhyanathan, V. Varma, "AgenticAKM: Enroute to Agentic Architecture Knowledge Management", 2026 — <https://arxiv.org/abs/2602.04445>.
32. F. Nogueira, N. Silva, T. Conte, "One Size Fits All? An Empirical Comparison of ADR Templates regarding Comprehension, Usability, and Ease of Adoption", 2026 — <https://arxiv.org/abs/2604.27333>.
33. S. Souza et al., "Beyond Strict Rules: Assessing the Effectiveness of Large Language Models for Code Smell Detection", 2026 — <https://arxiv.org/abs/2601.09873>.
34. O. Chowdhury, B. T. R. Savarimuthu, S. A. Licorish, "A Pilot Study on Detecting Software Design Patterns with Large Language Models", ENASE 2026 — <https://arxiv.org/abs/2604.17329>.
35. J. T. Almonte et al., "Automated Non-Functional Requirements Generation in Software Engineering with Large Language Models: A Comparative Study", 2025 — <https://arxiv.org/abs/2503.15248>.
