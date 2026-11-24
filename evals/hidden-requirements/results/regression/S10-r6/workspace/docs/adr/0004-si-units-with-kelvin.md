# 4. Use SI units, with temperatures in Kelvin and displayed in °C

## Status

proposed

## Context

Found in the code: `HeatingLib/Interfaces.mo` types temperatures in K, with `displayUnit = "degC"`, and heat flow in W. Every Real in the models carries a `unit` attribute. This serves R-1: the temperature shown must be correct.

## Decision

We use SI units throughout. Temperatures are in K internally and displayed in °C.

## Consequences

Every new Real carries a `unit` attribute. The °C display applies to output only; model equations stay in K.

Question for the architect: keep SI with Kelvin as the rule?
