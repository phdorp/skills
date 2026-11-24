# Kit Tracker: agreed design

Status: agreed with the product owner (club equipment manager). Build to this document.
Deadline: live for the start of the season on **1 March**.

## 1. Purpose

Show which coach has which kit item and where it is stored, for one volunteer football club with about 40 coaches and 300 items.

## 2. Users and access

- Coaches use the app on their own phones, mobile-first, with no install step.
- The admin (equipment manager) uses the same app on a laptop.
- A second admin, a trusted volunteer, is added for succession.
- Each coach has a named login with a local account and a hashed password.
- Admins create coach accounts and set temporary passwords. A coach must change a temporary password at next login.
- Coaches see the full item list with current holder and location, and nothing more.

## 3. Checkout speed and usability

- Checking an item out or in takes at most **3 taps and under 15 seconds**, starting from scanning the QR code on the bag.
- After the scan there is one button:
  - "Check out to me" if the item is free.
  - "Check in" if the scanning coach holds it.
- The interface is large-button and plain-language, for volunteers who are not tech-savvy.

## 4. Items

- Each item has an ID, a name, a category, a home location from a fixed list the admin maintains, and an optional expiry date.
- The app generates IDs. The admin prints batches of QR-code labels on A4 sheets. Each sticker contains only the ID.
- Labels are printed only for new items. Existing labels are never reissued.
- Items are never deleted. They are **retired** (lost, damaged or retired) and can be restored by the admin.
- A first-aid bag is one tracked item. Its contents are listed on it with their own expiry dates. Contents are not scanned or located separately.

## 5. Checkout and sync

- The app records an **append-only event log**. Current holder and location are derived from the log.
- A check-out is refused if the item is already held. The admin can force a transfer, which is logged as an admin event.
- Offline use works fully. Each phone caches the full item list, so scanning works without signal.
- Login needs signal. A cached session lasts **30 days**, after which the coach must log in again.
- Offline collisions keep both events. The earlier-synced event takes effect, ordered by **server sync time**, not the phone clock. The admin sees the later one as a conflict to resolve.
- Offline events from a **revoked session** are kept and flagged for admin review. Other offline events are not flagged.
- A coach cannot be deleted while holding items. The admin must clear them first (check-in or forced transfer).

## 6. Overdue, expiry and reporting

- An item is **overdue after 7 days** out.
- Every **Monday at 07:00 Europe/Berlin**, the NAS emails the admin an overdue report. It is sent even when nothing is overdue. Every send attempt is logged.
- The report lists item ID, item name, home location and days out. It contains **no coach names**.
- Items expiring **within 30 days** appear in the Monday email, with item name, expiry date and location only.
- The admin dashboard shows:
  - items currently out, with holder and days out;
  - overdue items;
  - items expiring within 30 days;
  - unresolved offline conflicts;
  - retired items.
  Each item links to its full event history.
- Email is sent through the admin's own mail account's SMTP server, using an app-specific password stored on the NAS. The mail provider must not see coach names.

## 7. Yearly CSV export

- An on-demand download, with the year chosen by the admin, covering 1 January to 31 December.
- One row per item: ID, name, category, home location, status at the end of the year, and expiry date.
- A bag is one row. Its contents appear as separate rows, each with its own expiry date.
- No coach names. No check-out counts.
- Purpose: the treasurer's yearly inventory for the insurance audit.

## 8. Money

The app never handles money. No deposits, fines or payments, ever.

## 9. Privacy and retention

- Stored personal data: coach name and login email only. No phone numbers.
- All data stays on the club's Synology NAS. No third-party cloud or hosted database.
- All events, including lost-item records, are purged after **2 years**. The purge runs nightly.
- When a coach leaves, their personal data is deleted. Their history is kept under a placeholder name, until the 2-year purge.
- Send-attempt logs and sync-conflict logs are kept for the same 2 years.
- Accepted risk: a stolen phone with a cached session can check out kit for up to 30 days. Only events from a revoked session are flagged.

## 10. Technology and operations

- Python with **Flask**.
- Server-rendered templates. Plain JavaScript only where the browser needs it: the offline cache, sync and QR scanning.
- SQLite database in a file on a Docker volume.
- One container, run with **Docker Compose** on the Synology NAS, with a pinned image version. Updates are manual, with the steps in the runbook.
- The Monday scheduler and the nightly purge run inside the app container.
- HTTPS through the Synology reverse proxy, with a Let's Encrypt certificate. No VPN for coaches.
- Nightly backups with Synology Hyper Backup to a second location, with written restore steps.
- Cost: 0 EUR per month.
- The codebase and runbook must be readable by a Python-only successor.

## 11. Open inputs before go-live

1. **Router and domain** (blocker for live deployment). Confirmation from the person who manages them of:
   - a domain or subdomain the club controls, with a DNS A record (or dynamic DNS) to the public IP;
   - router port forwarding of external TCP 443 and 80 to the NAS;
   - a DHCP reservation for the NAS;
   - DSM admin ports (5000/5001) not exposed;
   - no CGNAT on the ISP connection. If CGNAT applies, the design must be revisited.
2. The admin's mail account SMTP settings and app-specific password, stored only on the NAS.
3. The name of the second admin volunteer.

## 12. Plan

- Mid-January: working checkout and NAS deployment.
- Then a pilot with a few coaches.
- Go-live before **1 March**.
