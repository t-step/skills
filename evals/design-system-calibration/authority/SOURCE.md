# Cloudscape authority snapshot — provenance

- **Source URL:** https://cloudscape.design/llms.txt
- **Fetched:** 2026-09-01 (HTTP `Last-Modified: Tue, 01 Sep 2026 13:32:56 GMT`)
- **Content:** `cloudscape-llms.txt`, 296 lines / 56,981 bytes
- **Integrity:** ETag `27d274e60f5f6aa9d8ab0e874ff7f6f5` (matches MD5 of the stored file)

## What this is

`llms.txt` is Cloudscape's own discovery/index file: a flat list of links into
`cloudscape.design` (components, patterns, foundations, dev guides), each with
a one-line description and, for components, a link to a machine-readable API
JSON doc. It is **not** itself component documentation — it's a table of
contents an agent uses to decide which of those linked pages to fetch next.

## How this fits the future skill

Per the task that created this snapshot: the eventual skill must not
hard-code a Cloudscape URL or a Cloudscape-specific fetch path. Cloudscape is
the proving ground for a more general "design-system calibration pack"
mechanism; a future pack for a different design system would supply its own
manually curated material, not necessarily an `llms.txt`-shaped index.

This snapshot exists only so the *experiment* (this evaluation round) has a
fixed, versioned view of what authoritative Cloudscape guidance is
discoverable right now, independent of whatever cloudscape.design serves on
a later date. It is evaluation/experiment material, not skill logic.
