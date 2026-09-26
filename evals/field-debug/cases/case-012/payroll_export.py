"""Builds BenefitCore's nightly fixed-width payroll file.

BenefitCore's intake spec (per their onboarding PDF, not included here) is
strict fixed-width, byte-for-byte: EMPLOYEE_ID 8 bytes, NAME 30 bytes,
NET_PAY 12 bytes, one record per line, no delimiters. Every field is
padded/truncated to its declared byte width before being written.
"""

ENCODING = "utf-8"  # changed from "latin-1" on 2026-09-08, see CHANGELOG.md

FIELD_WIDTHS = {"employee_id": 8, "name": 30, "net_pay": 12}


def build_record(employee):
    fields = []
    for key, width in FIELD_WIDTHS.items():
        value = str(employee[key])
        # Pads/truncates by *character* count to the declared width.
        fields.append(value.ljust(width)[:width])
    record = "".join(fields)
    return record.encode(ENCODING)


def write_file(employees, out_path):
    with open(out_path, "wb") as f:
        for employee in employees:
            f.write(build_record(employee) + b"\n")
