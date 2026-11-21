# `birdlog list` shows the latest sighting first

Parent: R-1 (feature-level).

`birdlog list` shows sightings in order, latest first.

Assumption made at setup: "latest" means the time of the sighting (the `time` field), not the time it was logged. If the architect means the logging time, change this before implementation.

Measured by QG-3 (QS-3): 0 wrong orderings in the round-trip test suite.
