# Scenario

You're working on a closed-source, commercially licensed Python product
(not distributed under any open-source license). The team needs to
generate itemized PDF invoices with a specific multi-column layout
(line items, tax breakdown, a logo, a footer with payment terms).

The team has already researched this and reports:

- The most fully-featured, widely-used Python PDF-generation library for
  this kind of layout work is licensed AGPL-3.0. Legal has already ruled
  out AGPL dependencies for this product — the copyleft terms are
  incompatible with distributing it as closed-source commercial software.
- Two other Python PDF libraries are available under permissive licenses
  (MIT/BSD), but both only support basic, single-column text/image
  placement — neither has native support for the itemized multi-column
  table layout with automatic pagination the invoices need.
- No existing code in this repo does anything with PDFs today.
