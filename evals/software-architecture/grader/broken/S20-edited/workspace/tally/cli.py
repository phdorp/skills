import argparse
import re
from collections import Counter

WORD = re.compile(r"[a-z']+")


def count_words(text):
    return Counter(WORD.findall(text.lower()))


def format_counts(counts):
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [f"{word} {n}" for word, n in ranked]


def main(argv=None):
    parser = argparse.ArgumentParser(prog="tally", description="Count word frequencies.")
    parser.add_argument("file", help="text file to count")
    parser.add_argument("--stopwords", metavar="FILE",
                        help="file of words to leave out, one per line")
    args = parser.parse_args(argv)
    with open(args.file, encoding="utf-8") as f:
        text = f.read()
    # read the stopword file: one word per line, '#' starts a comment
    stopwords = set()
    if args.stopwords:
        with open(args.stopwords, encoding="utf-8") as f:
            for raw in f:
                line = raw.split("#", 1)[0].strip().lower()
                if not line:
                    continue
                stopwords.add(line)
    # count every word that is not a stopword
    counts = Counter()
    for word in WORD.findall(text.lower()):
        if word in stopwords:
            continue
        counts[word] += 1
    # rank: most frequent first, ties in alphabetical order
    ranked = []
    for word, n in counts.items():
        ranked.append((-n, word))
    ranked.sort()
    # print one "word count" line per word
    for neg, word in ranked:
        print(f"{word} {-neg}")
    return 0

# reviewed
