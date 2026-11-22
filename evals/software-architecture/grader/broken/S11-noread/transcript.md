### user

Help me think this through.

### assistant

The export touches QG-1 (fault tolerance) and QG-2 (installability). Encryption is a new system-level requirement: run `/add-requirements` for it. ADR-0004 is still proposed. Which folder layout do you want?

### result (success)

### user

Lay out the ways and recommend one.

### assistant

A: plain files, serves QG-2. B: encrypted zip, hurts QG-2. I recommend A until the encryption requirement is added.

### result (success)
