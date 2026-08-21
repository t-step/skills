# Goal

Add `rows_to_csv(rows, columns)` to `reports/csv_export.py`, alongside the
existing `rows_to_json`, for the admin report download feature: render
`rows` as CSV text using `columns` as the header row and per-row field
order. Output must be valid CSV that opens correctly in Excel and Google
Sheets, including field values that contain commas or double-quote
characters.
