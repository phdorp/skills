# Hidden requirements (known only to the architect; never shown to the designer)

H1  Coaches use phones at the pitch where there is often no mobile signal. Checking kit out and in
    must work offline and sync when the phone is back online. (reliability / availability)
H2  Coaches' names and phone numbers are personal data (GDPR). Data must stay on the club's own
    hardware; no third-party cloud. (security / compliance, constraint)
H3  It must run on the club's existing Synology NAS (Docker available). Budget is 0 EUR per month.
    (constraint)
H4  The kit manager wants an overdue report e-mailed every Monday morning. (feature)
H5  Many volunteers are not tech-savvy: checking out an item must take at most 3 taps and under
    15 seconds, by scanning a QR code stuck on the kit bag. (usability, measurable)
H6  The treasurer needs a yearly inventory export as CSV for the insurance audit. (export format)
H7  Scale is tiny: about 40 coaches, 300 items. Performance is NOT a concern. (non-goal)
H8  The only maintainer is one volunteer who knows Python only; a successor must be able to take
    it over. (maintainability, technology constraint)
H9  History of lost items must be kept for 2 years (insurance). (data retention)
H10 First-aid bags contain items with expiry dates; the kit manager wants a warning 30 days before
    an expiry. (feature)
H11 Anti-goal: no money handling — no deposits, fines or payments. (non-goal)
H12 It must be live for the start of the season on 1 March. (schedule constraint)
