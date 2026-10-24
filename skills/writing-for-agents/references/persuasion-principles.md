# Persuasion principles

Part of [`writing-for-agents`](../SKILL.md). Use this when a discipline skill still loses under pressure after the wording is clear: the levers here raise the odds that a rule the agent knows survives a competing incentive.

Two cautions before the list:

- **Positive framing first.** State the target behaviour. A prohibition drags the banned behaviour into context and makes it more available; persuasion amplifies whatever the sentence already does. Fix the framing, then consider the principle.
- **Discipline skills only.** A reference skill gets clarity. Persuasion applied to reference material adds pressure without a rule to hold, and reads as noise.

## Research foundation

Meincke et al. (2025) tested seven persuasion principles across 28,000 LLM conversations: compliance with the requested behaviour rose from 33% to 72% (p < .001). Authority, commitment, and scarcity were the strongest. The effect appears because models are trained on human text in which these patterns accompany compliance; the same wording that moves a person moves the model.

## The principles

### Authority

Deference to expertise, credentials, or official sources.

- Imperative framing: "You must", "No exceptions", "Every case".
- A named source: the project's standards, the upstream spec, the incident that motivated the rule.

Use it for established practice and safety-critical steps. Authority removes the "is this an exception?" decision, which is where most discipline failures start.

```markdown
Write code before the test? Delete it. Start over. No exceptions.
```

### Commitment

Consistency with a prior statement or action.

- Require an explicit choice: "Choose A, B, or C."
- Require an announcement: "State which skill you are using."
- Track with a checklist or todo the agent ticks off.

Use it for multi-step processes and for anything where the agent could quietly skip a step. A stated choice is harder to reverse than an unstated one.

### Scarcity

Urgency from a limit: time, a window, a dependency.

- "Before proceeding", "Immediately after X", "Only when the check passes".
- Sequence the dependency so the next step is blocked until this one completes.

Use it for verification steps that otherwise drift to "later". Scarcity that is not real reads as pressure and damages trust in the rest of the document.

### Social proof

Conformity to what is normal or universal.

- "Every time", "Always", "X without Y fails".
- A failure mode stated as a norm: "Checklists without tracking get skipped."

Use it to describe universal practice and common failures. It establishes the baseline the agent compares itself against.

```markdown
A checklist without tracking gets skipped. Every time.
```

### Unity

Shared identity and belonging.

- "Our codebase", "we", "as colleagues".
- A shared goal: "we both want the review to catch this".

Use it for collaborative workflows and for honest pushback. It fits a skill that asks the agent to disagree with the user.

### Reciprocity

Obligation to return a benefit. Use it sparingly; it can read as manipulation, and it rarely adds anything to a skill.

### Liking

Preference for cooperating with someone liked. For compliance, rely on authority, commitment, and unity instead: liking pushes toward agreement, which is the opposite of the honest judgement a discipline skill needs.

## Combinations by document type

| Document | Use | Avoid |
|---|---|---|
| Discipline skill | Authority + commitment + social proof | Liking, reciprocity |
| Technique or guidance | Moderate authority + unity | Heavy authority |
| Collaborative workflow | Unity + commitment | Authority, liking |
| Reference | Clarity only | All persuasion |

## Why it works

- **Bright lines reduce rationalization.** "You must" removes the exception question; absolute framing plus named anti-rationalizations closes the specific exits an agent finds under pressure. See [bulletproofing.md](bulletproofing.md).
- **Implementation intentions automate behaviour.** "When X, do Y" outperforms "generally do Y", because the trigger is observable and the action is attached to it.
- **Models are parahuman.** Authority language precedes compliance in training data; commitment sequences (statement, then action) are common; "everyone does X" establishes a norm. The patterns work for the same reason they work on people.

## Ethical use

Legitimate: making a critical practice survive pressure, writing documentation an agent can follow, preventing a predictable failure.

Illegitimate: manufacturing urgency, guilt, or a false consensus to get a behaviour the user would reject if they understood the technique.

The test: would this technique serve the user's genuine interests if they read it in full? If not, cut it.

## Quick reference

1. What type of document is it: discipline, guidance, collaborative, or reference?
2. What behaviour is failing, and under which pressure?
3. Which principle addresses that pressure? (Usually authority plus commitment for discipline.)
4. Is the positive target stated before the pressure?
5. Does the technique survive the ethical test?

## Citations

- Cialdini, R. B. (2021). *Influence: The Psychology of Persuasion (New and Expanded).* Harper Business.
- Meincke, L., Shapiro, D., Duckworth, A. L., Mollick, E., Mollick, L., & Cialdini, R. (2025). *Call Me A Jerk: Persuading AI to Comply with Objectionable Requests.* University of Pennsylvania.
