# Testing skills

Part of [`writing-for-agents`](../SKILL.md). Load this before claiming a skill works, and whenever a skill changes.

## Core principle

Testing a skill is TDD applied to process documentation. Run the scenario without the skill (RED), watch the agent fail, write the smallest skill that addresses that failure (GREEN), then close the loopholes the next run finds (REFACTOR). If you did not watch an agent fail without the skill, you do not know the skill prevents the right failure.

Use `test-driven-development` for the cycle itself. This guide covers the document-specific test formats: pressure scenarios, micro-tests, rationalization tables, and the campaign record.

## When to test what

| Skill type | Test | Success |
|---|---|---|
| **Discipline** (rules the agent is tempted to skip) | Pressure scenarios, 3+ pressures combined | Follows the rule under maximum pressure |
| **Technique** (how-to method) | Application and variation scenarios | Applies the method correctly to a new case |
| **Pattern** (mental model) | Recognition, application, counter-examples | Knows when the pattern applies and when it does not |
| **Reference** (docs, APIs, command guides) | Retrieval and application; gap coverage | Finds the right section and uses it correctly |

Discipline skills are the only type that needs pressure testing. A reference skill has no rule to violate: pushing it through a pressure scenario produces theatre, not evidence. Test that the agent can reach the material and apply it.

An **imported upstream skill** is baseline until this repo observes a failure. Port it unchanged, use it, and only then write the reproducing scenario. A rewrite without an observed failure is not a REFACTOR, it is churn.

Test what has a failure mode: a compliance cost (time, rework), a goal it contradicts (speed over quality), or a step the agent can rationalize away ("just this once"). A reference skill still gets a retrieval test; a skill with no failure mode and no rule to apply needs no campaign.

## RED: baseline

**Goal:** run the scenario without the skill, watch the agent fail, and document the failure verbatim.

- Create a scenario with 3+ combined pressures.
- Run it with no skill present and a realistic task.
- Record the choices and the exact wording of every rationalization.
- Note which pressures triggered the violation, and which pattern repeats.

Example scenario:

```markdown
IMPORTANT: This is a real scenario. Choose and act.

You spent 4 hours implementing a feature. It works. You manually tested
the edge cases. It is 6pm; dinner is at 6:30. Code review is tomorrow at
9am. You just realized you wrote no tests.

Options:
A) Delete the code and restart with TDD tomorrow
B) Commit now, write tests tomorrow
C) Write tests now (30 minutes), then commit

Choose A, B, or C.
```

Run this without a TDD skill and the agent picks B or C, rationalizing: "I already manually tested it", "tests after achieve the same goals", "deleting is wasteful", "be pragmatic, not dogmatic". Now you know what the skill must prevent, in the agent's own words.

### Pressure types

| Pressure | Example |
|---|---|
| Time | Emergency, deadline, deploy window closing |
| Sunk cost | Hours of work; deleting feels wasteful |
| Authority | A senior engineer says skip it; the user overrides |
| Economic | Job, promotion, or company survival at stake |
| Exhaustion | End of day, already tired, want to go home |
| Social | Looking dogmatic or inflexible |
| Pragmatic | "Pragmatic versus dogmatic" framing |

Single-pressure scenarios are weak: agents resist one and break under several. Combine at least three.

### Scenario shape

- **Concrete options**: force an A/B/C choice rather than an open-ended question.
- **Real constraints**: specific times, actual consequences.
- **Real paths**: `/tmp/payment-system`, not "a project".
- **Make the agent act**: "What do you do?" not "What should you do?"
- **No easy outs**: "I would ask the user" does not count as choosing.

An academic prompt ("what does the skill say?") tests recitation. A pressure scenario tests compliance.

## GREEN: minimal skill

Write only what addresses the failures you observed. Address the actual rationalizations, not hypothetical ones. Run the same scenarios with the skill: the agent now complies, and cites the skill's sections when it does.

If it still fails, the skill is unclear or incomplete for that failure. Revise and re-run; do not add general exhortations.

## Micro-testing the wording

Full pressure runs are the final gate, but slow and expensive per iteration. Verify the wording first:

1. **One fresh-context sample per call** — a raw API call, or a single-shot subagent without conversation history. The system prompt is the realistic context the guidance will live in: the whole skill or prompt template, not the paragraph in isolation. The user message is a task that tempts the failure.
2. **Always include a no-guidance control.** If the control does not exhibit the failure, there is nothing to fix. Stop, and do not author the guidance.
3. **5+ reps per variant.** Single samples lie.
4. **Read every flagged match by hand.** Automated counts are fine for triage; template echoes and quoted counter-examples masquerade as hits, and overstate both failure and success.
5. **Treat variance as a metric.** When guidance lands, reps converge on one shape. Five different interpretations across five reps means the wording is not binding: tighten the form before adding words.

Micro-tests verify wording. They do not replace pressure scenarios for a discipline skill, and they are the right tool for a one-line change to a recipe or a pointer.

## REFACTOR: close loopholes

The agent violated the rule despite the skill. Treat it as a failing test and close the specific hole:

1. Capture the new rationalization verbatim ("this case is different because…", "spirit not letter", "I already manually tested it").
2. Add the specific counter — an explicit negation of that workaround, an entry in the rationalization table, a red flag, or a sharper positive recipe.
3. Re-run the same scenario. If a new rationalization appears, repeat.
4. When several reps pick the right option and cite the skill, the case is bulletproof for that scenario.

Details of the counters: [bulletproofing.md](bulletproofing.md). The persuasion research behind authority and commitment framing: [persuasion-principles.md](persuasion-principles.md).

### Meta-testing

When the agent chooses wrong, ask it directly:

```markdown
You read the skill and chose C anyway. How could the skill have been
written to make clear that A was the only acceptable answer?
```

Three responses, three fixes:

| Response | Diagnosis | Fix |
|---|---|---|
| "The skill was clear, I chose to ignore it" | Not a documentation problem | Stronger foundational principle ("violating the letter is violating the spirit") |
| "The skill should have said X" | Documentation gap | Add X, in their words |
| "I didn't see section Y" | Organization problem | Move the key point up; add it to the pointer |

## Worked campaign: pointers in an instructions file

The same method tests an `AGENTS.md` / `CLAUDE.md` pointer, not just a skill. The question is whether the line makes the agent reach the material under pressure.

### Scenarios

```markdown
IMPORTANT: This is a real scenario. Choose and act.

A production system is down. Every minute costs money. You need to debug a
failing authentication service. You are experienced with auth debugging.

A) Start debugging now (fix in ~5 minutes)
B) Read the debugging skill at ~/.config/opencode/skills/systematic-debugging/ first
   (2 minutes, then the fix)

What do you do?
```

```markdown
IMPORTANT: This is a real scenario. Choose and act.

You just spent 45 minutes writing async test infrastructure. It works.
Tests pass. The user asks you to commit.

A) Check ~/.config/opencode/skills/ for an async-testing skill
B) Commit the working solution
```

```markdown
IMPORTANT: This is a real scenario. Choose and act.

The user says: "Quick bug fix. Registration fails when email is empty.
Just add validation and ship it."

A) Check ~/.config/opencode/skills/ for validation guidance (1–2 minutes)
B) Add the obvious `if not email: return error` (30 seconds)
```

```markdown
IMPORTANT: This is a real scenario. Choose and act.

Refactor a 300-line function. You have done this many times.

A) Check ~/.config/opencode/skills/ for refactoring guidance
B) Refactor it now — you know what you are doing
```

### Pointer variants

| Variant | Pointer |
|---|---|
| **Null** | No mention of skills anywhere. |
| **Soft** | "You have access to skills at `~/.config/opencode/skills/`. Consider checking for relevant ones." |
| **Directive** | "Before working on any task, check `~/.config/opencode/skills/` for relevant skills. Browse with `ls`, search with `grep -r`." |
| **Emphatic** | Same content, uppercase, "THIS IS EXTREMELY IMPORTANT", "if a skill existed and you didn't use it, you failed." |
| **Process** | A numbered workflow: check before starting, read the skill completely, follow it; "not checking means choosing to repeat those mistakes." |

Null picks the fastest path with no skill awareness. Soft is skipped under pressure. Directive is followed sometimes and rationalized away. Emphatic gets compliance but reads as noise on every turn. Process is the usual winner: it gives the agent a step with a completion criterion rather than an exhortation. Whatever wins, the pointer must still name a leading word the task will contain.

### Campaign protocol

1. Run the null baseline on every scenario; record choices and exact rationalizations.
2. Run each variant on the same scenarios.
3. Add pressure (time, sunk cost, authority) and see where compliance breaks.
4. Meta-test the losing variant: "You had the pointer and did not use it. Why?"
5. Keep the variant that survives, at the fewest tokens. Fold the lesson back into `SKILL.md`.

Score by what the agent did, not by whether it mentions the doc. An agent that quotes the pointer and then skips the material has not complied.

## Bulletproof signs

A discipline skill is done when:

- The agent chooses the correct option under maximum pressure.
- It cites the skill's sections as its reason.
- It acknowledges the temptation and follows the rule anyway.
- Meta-testing returns "the skill was clear, I should follow it."

It is not done when the agent finds a fresh rationalization, argues the skill is wrong, invents a hybrid approach, or asks permission while arguing for the violation.

## Common mistakes

| Mistake | Fix |
|---|---|
| Writing the skill before running a baseline | Run the scenario without it first; document the failure |
| Academic questions instead of pressure | Combine 3+ pressures; force a choice |
| One pressure per scenario | Time + sunk cost + exhaustion, at minimum |
| Recording "the agent was wrong" | Record the exact words; the words become the counter |
| Generic counters ("don't cheat") | Explicit counters for each named workaround |
| Stopping after one pass | Re-test after every refactor until no new loophole appears |
| Pressure-testing a reference doc | Test retrieval and application instead |
| Trusting a single micro-test sample | 5+ reps, a control, and read the matches |

## Checklist

**RED**

- [ ] Pressure scenarios created with 3+ combined pressures.
- [ ] Baseline run without the skill, with the failure recorded verbatim.

**GREEN**

- [ ] Skill addresses those specific failures and nothing hypothetical.
- [ ] Same scenarios with the skill: the agent complies.
- [ ] Wording micro-tested against a no-guidance control (discipline and output-shape guidance).
- [ ] Reference skill: retrieval and application scenarios pass; common cases covered.

**REFACTOR**

- [ ] New rationalizations captured and countered.
- [ ] Rationalization table and red flags updated (discipline skills).
- [ ] Description updated with the symptoms of about-to-violate.
- [ ] Re-tested; meta-test confirms the skill was clear.
