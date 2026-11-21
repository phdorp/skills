# tally

Counts word frequencies in a text file.

```sh
python3 -m tally notes.txt
```

Prints one `word count` line per word, most frequent first, ties in alphabetical order.
Pass `--top N` to print only the N most frequent words:

```sh
python3 -m tally --top 10 notes.txt
```

Run the tests with `python3 -m unittest`.
