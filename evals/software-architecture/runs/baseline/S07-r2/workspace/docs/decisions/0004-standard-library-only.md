# 4. Use only the Python standard library

## Context

shelf is a personal tool. It should run on any machine with Python 3 and without installing
packages, a virtualenv, or a lock file.

## Decision

The package and its tests import only the standard library: `argparse`, `json`, `os`, `pathlib`
and `unittest`. There is no `requirements.txt` and no packaging dependency.

## Consequences

- Installation is copying the package and running `python3 -m shelf`.
- Features that would need a third-party library, such as an online ISBN lookup or a richer CLI,
  are out of scope unless this decision is revisited.
- ISBN validation is implemented by hand in `shelf/isbn.py` (see [ADR 0002](0002-validate-isbn-locally.md)).
