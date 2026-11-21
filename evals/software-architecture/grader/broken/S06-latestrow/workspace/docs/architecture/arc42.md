# birdlog: architecture

Structured after arc42 (https://arc42.org).

## 1. Introduction and goals

### Requirements overview

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Birders log a sighting (species, place, time, count) from the command line. | 1 | active | core use |
| R-2 | No sighting is ever lost, even if the laptop dies mid-write. | 2 | active | records are irreplaceable |
| R-3 | Runs offline on Linux, macOS and Windows with only Python installed. | 3 | active | used in the field |
| R-4 | Sightings export to the eBird CSV format. | 4 | active | birders share with eBird |
| R-5 | Logging a sighting is fast. | 5 | active | measure open |
| R-6 | `birdlog list` shows the latest sighting first. | 6 | active | interviews |

### Quality goals

| ID | goal (ISO/IEC 25010) | from | scenario |
|---|---|---|---|
| QG-1 | Reliability: fault tolerance | R-2 | QS-1 |
| QG-2 | Flexibility: installability | R-3 | QS-2 |
| QG-3 | Compatibility: interoperability | R-4 | QS-3 |


## 2. Constraints



## 3. Context and scope



## 4. Solution strategy



## 5. Building block view



## 6. Runtime view



## 7. Deployment view



## 8. Crosscutting concepts



## 9. Architecture decisions

Decisions are recorded as ADRs in [docs/adr/](../adr/).

## 10. Quality requirements

| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | power is cut during `birdlog add` | normal operation | the sighting is fully stored or absent | 0 unreadable logs in 100 trials |
| QS-2 | QG-2 | a birder runs `python -m birdlog` | fresh Linux, macOS or Windows with Python 3.11 | it works with no install step | 0 install steps |
| QS-3 | QG-3 | a birder imports the export into eBird | eBird's CSV import | every sighting is accepted | 100% of 50 sightings accepted |


## 11. Risks and technical debt



## 12. Glossary

No glossary yet; `GLOSSARY.md` is created with the first term.
