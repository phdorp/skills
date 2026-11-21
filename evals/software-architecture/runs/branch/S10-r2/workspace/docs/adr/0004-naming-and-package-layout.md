# 4. Naming and package layout

## Status

proposed

## Context

Found in the code, not decided by the architect: everything lives in the package `HeatingLib`
(`package.mo`), one class per file, each file begins with `within HeatingLib;`, and
`package.order` lists the load order. This is on the accepted list ("Naming and package
layout"). It serves R-3 and QG-3: `tests/check.mos` loads the package by its path.

## Decision

Classes are named in the `HeatingLib` package, one class per file, each file starts with
`within HeatingLib;`, and `package.order` lists the files in load order.

## Consequences

Adding a model means adding a file and a line in `package.order`. Renaming a class or file
changes `tests/check.mos` and any dependent `within` clause. Changing this layout waits for this
ADR's acceptance.
