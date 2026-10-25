---
name: Conventional Commits
description: Use when writing or amending a git commit message, or when a repository enforces commit conventions. Triggers include "commit this", "write a commit message", "amend the commit", and "which type should this commit be".
---

# Conventional Commits

Every commit message names its type and states what changed, in a shape changelogs and release tools parse. The specification is Conventional Commits 1.0.0: <https://www.conventionalcommits.org/en/v1.0.0/>.

## The format

```
<type>[(<scope>)][!]: <description>

<body>

<footer(s)>
```

- `<type>`: one noun from the table below. Required.
- `(<scope>)`: optional noun naming the section of the codebase. The parentheses are part of the syntax.
- `!`: optional marker for a breaking change. It goes immediately before the colon.
- `<description>`: a short summary on the same line as the prefix, at most 50 characters including the type and scope. Required.
- `<body>`: the implementation details and their justification, one blank line after the description, every line at most 72 characters. Required.
- `<footer(s)>`: one blank line after the body. Required when the commit closes an issue; see *Write the footers*.

## Choose the type

| Type | Use when the commit |
|---|---|
| `feat` | adds a new feature |
| `fix` | fixes a bug |
| `docs` | changes documentation only |
| `style` | changes formatting or whitespace without changing behaviour |
| `refactor` | restructures code without fixing a bug or adding a feature |
| `perf` | improves performance |
| `test` | adds or corrects tests |
| `build` | changes the build system or dependencies |
| `ci` | changes CI configuration or scripts |
| `chore` | does maintenance the other types do not cover |
| `revert` | reverts an earlier commit |

`feat` and `fix` are the two types the specification defines; the rest are the conventional set used by `@commitlint/config-conventional`. When a change fits two types, split it into two commits. `refactor` and `style` earn their keep by keeping behaviour changes out of a commit whose type promises none.

If the repository documents its own types in `CONTRIBUTING.md`, a commitlint config, or `.gitmessage`, follow those; this table is the default.

## Write the description

| Rule | Example |
|---|---|
| Keep the whole header within 50 characters | `docs(readme): list supported flags` |
| Imperative mood, as if completing "This commit will …" | `add retry to upload` |
| Lowercase first letter unless a proper noun | `feat(api): add OAuth login` |
| No trailing period | `fix: reject empty tokens` |
| Say what the change does, not which files moved | `fix(parser): handle nested brackets` |
| Specific enough to read as a changelog line | `perf(query): cache user lookups for 60s` |

## Add a scope when one section owns the change

A scope names the part of the codebase the commit touches, in the project's own vocabulary: `feat(parser):`, `fix(auth):`, `docs(readme):`. Omit it when the change spans the repository or no single section owns it. Do not invent a scope to make the header look complete.

## Mark breaking changes

A breaking change alters an interface callers depend on. Mark it either way, or both:

```
feat(api)!: drop support for Node 6

Supporting Node 6 forced a transpile step and blocked native async.
Callers still on Node 6 must upgrade to a maintained release.

BREAKING CHANGE: use JavaScript features not available in Node 6.
```

- The `!` sits between the type/scope and the colon.
- The footer uses the uppercase words `BREAKING CHANGE`, a colon, a space, and a description. `BREAKING-CHANGE` is accepted as the same token.
- Any type can be breaking. Breaking changes map to a MAJOR version bump, `feat` to MINOR, and `fix` to PATCH.

## Write the body

The body carries the additional implementation details a reader cannot infer from the diff, and the justification for them: what changed, how it works, and the problem or requirement that makes the change worth making. A reviewer should be able to accept the commit from the body alone, without opening the issue. Start the body one blank line after the description, wrap every line at 72 characters, and separate paragraphs with blank lines. The description stays the summary; it is not the first sentence of the body.

## Write the footers

A commit that closes an issue states the closing relationship in a footer: `Closes: #<issue>`. Reference a closed pull request with `Refs: #<pr>`. Footers start one blank line after the body, one per line. A footer is a hyphenated token, then `: ` or ` #`, then a value:

```
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.

Closes: #123
Refs: #45
```

Write only the footers the project or the user requires; never add an attribution footer the user did not ask for. The `Closes:` and `Refs:` footers are required when the commit closes an issue or references a closed pull request.

For a revert, use the `revert` type, write the body as any other commit, and reference the reverted commits:

```
revert: undo the noodle incident

Revert the experiment added in 676104e; it corrupted saved state and
no caller depends on it.

Refs: 676104e, a215868
```

## Commit one logical change

One commit, one reason to exist. Split when a commit would need two types, when formatting hides a behaviour change, or when a reviewer could accept half the change and reject the other half. Keep a test in the same commit as the code it proves, so every commit leaves the suite as green as its parent did.

## Compose the message in git

Because every commit carries a body, compose the message with a heredoc so the blank lines survive:

```bash
git commit -F - <<'EOF'
feat(parser): add ability to parse arrays

Handle bracketed literals so callers can nest arrays instead of
encoding them as strings. `parse` now returns `Array<Value>`, not
`Value`.

BREAKING CHANGE: `parse` now returns `Array<Value>`, not `Value`.
Closes: #123
EOF
```

To fix the message on the most recent commit, run `git commit --amend`. Amend only a commit that has not reached a shared branch; rewrite older messages with an interactive rebase when the repository's history policy allows it.

## Check before committing

- [ ] The header reads `<type>(<scope>)!: <description>` with only the optional parts omitted, and fits within 50 characters.
- [ ] The type comes from the table or the repository's documented set, and the commit holds one logical change.
- [ ] The description is imperative, lowercase, and has no trailing period.
- [ ] The scope, when present, names a section in the project's vocabulary.
- [ ] A breaking change carries `!`, a `BREAKING CHANGE:` footer, or both.
- [ ] The body starts one blank line after the description, wraps every line at 72 characters, and gives the implementation details and the justification.
- [ ] The commit closes its issue with a `Closes:` footer, or references the closed pull request with `Refs:`.
- [ ] Each footer is one line, with a hyphenated token and `: ` or ` #` before the value.

## Common rationalizations

| Excuse | Reality |
|---|---|
| "`feat` and `fix` cover everything" | A docs or test change typed `feat` inflates the changelog and the next version bump. |
| "The body will mention the breaking change" | Tooling reads `!` and the `BREAKING CHANGE:` footer; prose in the body is invisible to it. |
| "The diff shows what changed" | The body states the intent and the justification; a diff shows lines, not reasons. |
| "The issue link is in the pull request" | The `Closes:` footer is what closes the issue and survives in history; a pull-request description does not. |
| "50 characters is too tight for this change" | Keep the header a changelog line and move the detail to the body; `git log` truncates a long header. |
| "One commit is easier to write" | Two types in one commit hide half the change from history and from the changelog. |
| "The scope is optional, so any word works" | A scope names a codebase section. An invented scope misleads the reader who filters by it. |
| "I'll fix the message after the push" | Amending a shared commit rewrites history others may already have. |