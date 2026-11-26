import argparse
import re
from collections import Counter

WORD = re.compile(r"[a-z']+")


def count_words(text):
    return Counter(WORD.findall(text.lower()))


def format_counts(counts):
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [f"{word} {n}" for word, n in ranked]


def positive_int(value):
    try:
        n = int(value)
    except ValueError:
        n = 0
    if n < 1:
        raise argparse.ArgumentTypeError(f"must be a positive integer, got {value!r}")
    return n


def main(argv=None):
    parser = argparse.ArgumentParser(prog="tally", description="Count word frequencies.")
    parser.add_argument("file", help="text file to count")
    parser.add_argument("--top", type=positive_int, metavar="N",
                        help="print only the N most frequent words (default: all)")
    args = parser.parse_args(argv)
    with open(args.file, encoding="utf-8") as f:
        counts = count_words(f.read())
    lines = format_counts(counts)
    if args.top is not None:
        lines = lines[:args.top]
    for line in lines:
        print(line)
    return 0
