# 1. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. The kit tracker must be easy for volunteers to use (R-2, QG-1), must keep every record (R-3, QG-3), and must keep the loan history accountable for two years (R-1, R-6, QG-4). It runs on the club's Synology NAS in Docker, in Python, at no cost, with personal data kept on the club's hardware.

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- storage of the kit and loan records, and their on-disk format;
- the CSV export format for the yearly inventory (R-5);
- interfaces between building blocks, and the dependency rule between them;
- third-party dependencies, including the framework and the Docker base image on the Synology NAS;
- crosscutting conventions: naming, units (dates, counts), error handling, logging;
- versioning of the data format and the CSV export, once coaches and the treasurer rely on them.

Left to the building blocks (no ADR):

- internal helpers and the structure inside one block;
- test layout.

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
