import argparse
import re
from collections import Counter

WORD = re.compile(r"[a-z']+")


def count_words(text):
    return Counter(WORD.findall(text.lower()))


def format_counts(counts, top=None):
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    if top is not None:
        ranked = ranked[:top]
    return [f"{word} {n}" for word, n in ranked]


def positive_int(value):
    n = int(value)
    if n < 1:
        raise argparse.ArgumentTypeError(f"must be at least 1, got {value}")
    return n


def main(argv=None):
    parser = argparse.ArgumentParser(prog="tally", description="Count word frequencies.")
    parser.add_argument("file", help="text file to count")
    parser.add_argument("--top", type=positive_int, metavar="N",
                        help="print only the N most frequent words")
    args = parser.parse_args(argv)
    with open(args.file, encoding="utf-8") as f:
        counts = count_words(f.read())
    for line in format_counts(counts, top=args.top):
        print(line)
    return 0
