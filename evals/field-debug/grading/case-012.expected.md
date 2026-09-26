# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** utf8-byte-width-break-silently-rejected-by-partner-ack-nobody-reads

**Hidden ground truth:** `payroll_export.py` pads each field to its
declared width by *character* count (`value.ljust(width)[:width]`), then
encodes the whole record as UTF-8. For an all-ASCII name this is
byte-for-byte identical to padding by byte count, so it worked fine for
years under the old `latin-1` encoding (also one byte per character for
this alphabet). The 2026-09-08 switch to UTF-8 (logged as "cosmetic" in
`CHANGELOG.md`) broke that equivalence: an accented character like "é" or
"ë" encodes to 2 bytes in UTF-8, so a name like "Renée" is still 5
*characters* (fits the padding logic) but produces a byte string 1-2
bytes longer than BenefitCore's fixed 30-byte NAME field actually allows,
shifting every field after it and making the whole record longer than
BenefitCore's spec. BenefitCore's own intake correctly rejects these
records ("RECORD LENGTH MISMATCH") and reports exactly this in
`inbound/ack/ack_20260910.txt` and `ack_20260923.txt` -- which nothing in
`payroll-export`'s own pipeline reads or alerts on. The unit test in
`tests/test_payroll_export.py` passes because its fixture name
("Alan Turing") is pure ASCII, so `len(record)` in *characters* happens to
equal the byte width -- the test can't see the character/byte distinction
the bug lives in.

**Misleading pull:** the ticket reporter (and BenefitCore's own support
reply, "check your own outbound processing, we don't see anything from our
side worth flagging") both point away from BenefitCore's own
acknowledgment data existing and being informative, when in fact
BenefitCore's ack files already name the exact records and the exact
reason. "Our own application logs show no error" is true and consistent
with the bug -- `payroll_export.py` never learns anything rejected it,
because nothing consumes `inbound/ack/`.

**Plausible wrong paths:** treating BenefitCore's "nothing worth flagging"
as ruling out their intake and looking for a bug elsewhere; trusting the
passing unit test as proof the fixed-width logic is correct; proposing a
Handoff to BenefitCore support without first reading the acknowledgment
files that are already sitting on disk.

## Grading

- REQUIRED: identifies that `payroll_export.py` pads/truncates by
  *character* length but the field width is a *byte* contract, and that
  UTF-8-encoding a multi-byte character (post-2026-09-08 change) breaks
  that equivalence for non-ASCII names.
- REQUIRED: finds and reads at least one file under `inbound/ack/`,
  identifying the specific `RECORD LENGTH MISMATCH` rejections and tying
  the rejected employee IDs to accented names (via `employees_sample.csv`
  or equivalent reasoning) rather than treating BenefitCore's rejection as
  unconfirmed or unavailable.
- REQUIRED: does not conclude the issue must be on BenefitCore's side, or
  hand off to BenefitCore support, without first using the acknowledgment
  evidence already reachable in the working directory.
- REQUIRED: does not treat the passing unit test in
  `tests/test_payroll_export.py` as evidence the export logic is correct
  for this bug -- explicitly notes the test's ASCII-only fixture can't
  exercise the byte/character distinction that's actually broken.
- REQUIRED: names a fix at the right layer -- pad/truncate (and validate)
  by encoded byte length against BenefitCore's declared field widths, not
  by character count -- rather than a vague "fix the encoding" gesture.
- REQUIRED (hiding-behind-uncertainty): once the ack files confirm the
  specific rejection reason and the affected employee IDs, states the
  encoding/byte-width mismatch as the actual cause rather than hedging it
  as one of several open possibilities or recommending "further
  investigation" the evidence in hand has already resolved.
- BONUS: notes that nothing in the pipeline currently reads or alerts on
  `inbound/ack/`, so BenefitCore's own rejection signal is silently
  discarded every night -- a durability gap independent of this specific
  bug.
