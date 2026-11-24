# 0001. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. Check-out records must work offline on coaches' phones and survive crashes (R-3, R-5, QG-3, QG-4), and personal data must stay on the club's NAS (R-4, QG-5). Both needs are shaped by which decisions are made centrally.

## Decision

We record architecture decisions as ADRs in `docs/adr/`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- Storage engine and on-disk and wire data formats: where check-out records and the sync log live on the NAS, and their format on the phone.
- Import and export formats: the yearly inventory CSV (R-8).
- Interfaces between building blocks and the dependency rule between them: the phone app, the sync service, the record store, the Monday report job, and the export.
- Versioning of anything others depend on: the CSV export and the phone-to-NAS sync protocol.
- Crosscutting conventions: naming, units (dates and currency), error handling, logging.
- Third-party dependencies: Docker on the Synology NAS, Python for the maintainer (R-9), and the delivery path for the Monday report (R-7, section 11 risk).

Left to the building blocks (no ADR):

- Internal helpers, the structure inside one block, and the test layout.

## Consequences

Work that depends on a decision on this list waits until its ADR is accepted.
