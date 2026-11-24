# 0002. Host on the club's NAS with Docker, written in Python

## Status

proposed

## Context

The club's budget is 0 EUR per month, and its data must stay on club hardware with no third-party cloud (arc42 section 2). Coach names and phone numbers are personal data under GDPR (QG-4). One volunteer who knows only Python maintains the system, and a successor must be able to take it over (QG-5). The club's Synology NAS already runs Docker.

## Decision

We will run Kit Tracker as Docker containers on the club's Synology NAS, and write it in Python.

## Consequences

Whoever maintains the system needs Python and Docker. Data and backups stay on club hardware: a nightly backup goes to a second club-owned disk. The storage engine and the third-party libraries are decided separately, under the list in [ADR-0001](0001-record-architecture-decisions.md), and both must run on the NAS.
