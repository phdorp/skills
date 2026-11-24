# Kit Tracker: agreed design

Status: confirmed by the maintainer. This is the reference for implementation.

## Purpose

Coaches check kit out and back in by scanning a QR code on each bag or box, so the club always knows who holds what. Used on phones at the pitch, often without signal.

## Users

- **Coach:** individual account (name, login, passcode of at least 6 digits). Scans, takes out, returns.
- **Admin / equipment manager:** same scan flow, plus admin pages for bags, QR codes, expiry dates, accounts, and reports. Admins also check kit out.
- No parents or players.

## Tracking model

- Each bag or box is one inventory line with its own QR code and a group of contents with quantities (e.g. "bib set A, 20 bibs").
- Loose items live in a labelled box, so every checkout is "scan, confirm".
- First-aid bags stay one line. Their contents are listed with expiry dates and are not checked out individually.
- QR codes hold only a random ID. Admins can reprint a code and revoke the old one from the admin pages. An unknown code shows "unknown bag".

## Checkout and check-in

- **Checkout:** scan, then one "Take out" tap with everything pre-filled. A +/- stepper handles partial takes. Two taps usually, three with a quantity change. Target: under 15 seconds.
- **Due date:** defaults to 7 days from checkout; the coach can change it.
- **Held by someone else:** show "held by [name] since [date]" and allow a one-tap transfer, logged in history.
- **Check-in:** scan, see the coach's own items from that bag pre-filled, one "Return" tap.
- Admins use the same flow for checkout and check-in.

## Offline behaviour

- The phone stores the session (90 days) and the data it needs, so checkouts and check-ins work without signal.
- Each action is stored as an event: who, what, how many, phone time, and server receipt time.
- On sync, events are replayed in phone-time order.
- Nothing offline is rejected. A negative balance is flagged as a discrepancy for the admin.
- Events where phone time differs from server time by more than 24 hours are flagged for the admin.
- The app is installed to the home screen once, at home, so the offline cache is ready. A first load with no signal is not supported.

## Alerts and reports

- **Overdue:** the due date has passed and the item is still out. Listed in the Monday report.
- **Expiry:** the warning starts 30 days before expiry and repeats in each Monday report. After the date it is marked "expired" until the admin updates the date.
- **Monday report:** sent at 07:00 Europe/Berlin to one shared admin mailbox, via SMTP from a free club mailbox with an app password. Credentials live only in the NAS configuration, never in the code.
- **Yearly CSV export:** one row per bag or box, with bag code, name, contents and quantities, first-aid expiry dates, status at export time, and last checkout (coach and date). Retired bags are included with status and retirement date.

## Data, privacy and retention

- Stored personal data: coach name and login only. No phone numbers.
- Leavers are deactivated, not deleted, so their name stays on history.
- History is kept for 2 years, then deleted automatically by a scheduled job.
- Coaches receive a short privacy note stating what is stored and for how long.
- All data stays on the club's Synology NAS. No cloud or paid services.

## Security

- Login required for all pages. HTTPS via the NAS's built-in Let's Encrypt certificate, behind a Synology DDNS name.
- Five wrong passcodes lock the account for 15 minutes. Admins can unlock an account and reset a passcode; a reset forces a change at next login.
- A one-time setup screen creates the first admin, then locks itself.

## Tech stack and deployment

- Python with Flask; SQLite, in one Docker container on the NAS.
- Server-rendered HTML. JavaScript is limited to what offline mode needs, plus one vendored QR-decoding file for camera scanning.
- Backup: nightly copy of the SQLite file via Hyper Backup to an external drive or a second NAS folder. Test restore before 1 March and once per season.
- Time zone: Europe/Berlin throughout.

## Build order and deadline

Live by 1 March 2027 (start of the season).

1. Login, bag and box setup, and QR codes
2. Checkout and check-in online
3. Offline storage and sync
4. Live view
5. Expiry warnings and Monday e-mail (working by season start)
6. Yearly CSV export (may slip past 1 March)

## Open implementation choices (not design decisions)

These are left to the implementer: the QR-decoding library, the SMTP provider (any free one that supports app passwords), and the internal data model (tables, IDs, event schema).
