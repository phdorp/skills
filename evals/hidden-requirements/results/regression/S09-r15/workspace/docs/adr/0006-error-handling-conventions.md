# 6. Error handling conventions

## Status

proposed

## Context

Users see errors in the terminal and in their scripts (R-2, QG-2). Error handling is a central crosscutting convention (ADR 0001). Found in the docstring and `main` of `pantry/cli.py`.

## Decision

Exit code 0 means success, 1 means a user error (an unreadable date, or removing an item that is not there), and 2 means bad usage (argparse errors). User errors print a message starting with `pantry:` to standard error. Help exits with 0. The `dates.parse` function raises `ValueError`, and `cli` turns it into exit code 1.

## Consequences

New commands return these codes and print their user errors the same way. Changing a code or the message prefix changes what scripts see.
