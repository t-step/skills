# Feature Specification: Suspicious Upload Quarantine

**Status**: Draft

**Input**: "When an uploaded file trips the malware scanner, hold it
somewhere safe instead of either serving it or silently deleting it, so a
human can look at it."

## User Scenarios & Testing

### User Story 1 - Quarantine a file that fails scanning (Priority: P1)

A file is uploaded and scanned. If the scan flags it, it must not be
served to any user, but it also must not simply vanish -- someone needs to
be able to review it.

**Acceptance Scenarios**:

1. **Given** a newly uploaded file, **When** the scanner flags it,
   **Then** the file's status becomes `quarantined` and it is not served
   to any requester.
2. **Given** a newly uploaded file, **When** the scanner clears it,
   **Then** the file's status becomes `active` and it is served normally.
3. **Given** an `active` file, **When** a user deletes it, **Then** its
   status becomes `deleted` and it is no longer served.

### Edge Cases

- What happens if the scanner itself is unreachable when a file is
  uploaded? The upload is held in `pending_scan` status until the scanner
  responds; it is never served while `pending_scan`.
- What happens if a user attempts to delete a file that is currently
  `pending_scan`? The deletion is accepted immediately and the file moves
  directly to `deleted`, skipping scanning.

## Requirements

### Functional Requirements

- **FR-001**: Every uploaded file MUST have a status of exactly one of:
  `pending_scan`, `active`, `quarantined`, `deleted`.
- **FR-002**: A file MUST transition from `pending_scan` to `active` when
  the scanner clears it, or to `quarantined` when the scanner flags it.
- **FR-003**: A file MUST transition from `pending_scan` to `deleted`
  directly if a user deletes it before scanning completes (see Edge
  Cases).
- **FR-004**: A file MUST transition from `active` to `deleted` when a
  user deletes it.
- **FR-005**: A `quarantined` file MUST NOT be served to any requester
  under any circumstance.
- **FR-006**: A `deleted` file's content MUST be permanently and
  irrecoverably removed from storage.

### Key Entities

- **Upload**: A file with a stable identifier and a status as enumerated
  in FR-001.

## Success Criteria

- **SC-001**: A quarantined file is never served, in any test scenario,
  regardless of who requests it.
- **SC-002**: A deleted file's content is unrecoverable from storage after
  deletion completes.
- **SC-003**: Every file that completes scanning ends up in exactly one of
  `active` or `quarantined`, with no file left in `pending_scan`
  indefinitely under normal operation.

## Assumptions

- The malware scanner's own detection accuracy and false-positive rate are
  out of scope for this specification.
- A human reviewer is expected to periodically look at quarantined files,
  though the review workflow itself is out of scope for this iteration.
