# 0002. Yearly inventory CSV layout

## Status

proposed

## Context

The treasurer needs a yearly inventory export (R-1, issue `03-yearly-inventory-csv-export.md`). It must open in a spreadsheet without help, and a successor who knows only Python must be able to change it (R-6, QG-7). The file is an import/export format, so its layout is a central decision (ADR 0001). Coach names are personal data, and only the equipment manager may see all coaches' data (R-4, QG-5), so the layout must decide whether holder names appear.

## Decision

We will export the yearly inventory as a CSV file named `kit-inventory-YYYY.csv`:

- one row per item, as held on the export date;
- UTF-8 with a byte-order mark, so that umlauts open correctly in a spreadsheet;
- fields separated by a semicolon, the default in German spreadsheet programs;
- a header row, with these columns in this order: `item_id`, `item_type`, `description`, `status`, `since`, `expiry_date`;
- `status` is `in store` or `out`, and `since` is the date of the item's last check-out or check-in, as `YYYY-MM-DD`;
- `expiry_date` is filled only for first-aid bag items, as `YYYY-MM-DD`, and is empty otherwise;
- no coach names: the file shows `out`, not who has the item.

## Consequences

- The treasurer sees where each item is in general, not who has it. If the treasurer needs holder names, the file would contain all coaches' data, which R-4 allows only for the equipment manager. That needs a decision from the architect before this ADR is accepted.
- Changing a column, its order or its meaning is a change to a format someone else depends on, so it needs a new ADR that supersedes this one.
- The export is written with the Python standard library's `csv` module, so it adds no dependency (ADR 0001).
- The export waits for this ADR's acceptance. Issue `03` is blocked until then.
