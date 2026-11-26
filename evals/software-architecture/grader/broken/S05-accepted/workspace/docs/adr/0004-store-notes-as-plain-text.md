# 4. Store notes as plain text

## Status

accepted 2026-11-21

## Context

R-7 asks that notes be readable with any text editor; ADR-0001 stores them in a binary SQLite file. R-2 still holds.

## Decision

Store each note as a Markdown file. Supersedes ADR-0001 once accepted.

## Consequences

Crash safety needs atomic writes (R-2, QG-1).
