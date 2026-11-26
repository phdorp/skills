# Leave out stopwords

## Problem

Counts are dominated by words like "the" and "and".

## Behaviour

`tally FILE --stopwords WORDS` leaves out every word listed in the file WORDS. WORDS holds one
word per line; `#` starts a comment; blank lines are ignored; matching ignores case. Without
`--stopwords` the output is unchanged.

## Out of scope

A built-in stopword list.
