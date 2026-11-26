### user

Review the last commit.

### assistant

# Review of HEAD~1..HEAD

## Standards

- Important (judgement call, Long Method): `main` is about 30 lines with comment-labelled parts
  (read stopwords, count, rank, print). Extract `load_stopwords` and reuse `format_counts`.

## Spec

- No findings: `--stopwords` ignores case, comments and blank lines as the spec asks.

Worst per axis: Standards Important (Long Method); Spec none.

### result (success)
