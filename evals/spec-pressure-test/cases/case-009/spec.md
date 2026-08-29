# Feature Specification: Import Tickets from the Support Desk

**Status**: Draft

**Input**: "Pull tickets from our support desk tool into our internal
tracker so engineers don't have to context-switch to look them up, and
keep a link back to the original ticket."

## User Scenarios & Testing

### User Story 1 - Import a ticket and keep a durable link to its source (Priority: P1)

An engineer runs an import for a support-desk project, pulling its open
tickets into the internal tracker as internal items, each carrying a
pointer back to the ticket it came from.

**Acceptance Scenarios**:

1. **Given** a support-desk project with open tickets, **When** an
   engineer runs the import for that project, **Then** each ticket becomes
   one internal item, and each internal item records a source reference
   pointing back to its originating ticket.
2. **Given** an internal item already exists for a given ticket, **When**
   the same project is imported again, **Then** the import updates that
   item's title/description from the ticket's current content rather than
   creating a duplicate internal item.

### Edge Cases

- What happens if a ticket's title or description changes after import?
  Re-running the import updates the internal item's title/description to
  match (Acceptance Scenario 2); the internal item's own status and any
  work already recorded against it are untouched.

## Requirements

### Functional Requirements

- **FR-001**: Importing a ticket MUST create exactly one internal item per
  ticket, recording a source reference containing the ticket's number as
  reported by the support desk.
- **FR-002**: Re-running an import for a project MUST detect tickets that
  were already imported (by matching source reference) and update their
  title/description in place rather than creating a second internal item
  for the same ticket.
- **FR-003**: An internal item's source reference MUST remain a stable,
  permanent pointer to its originating ticket for the lifetime of the
  internal item.
- **FR-004**: Deleting or closing a ticket on the support desk side MUST
  NOT delete or modify the corresponding internal item -- the internal
  item's own lifecycle is independent once created.

### Key Entities

- **Support Desk Ticket**: An external record, identified by a ticket
  number that the support desk assigns within a given project. The support
  desk hosts multiple independent projects, each with its own tickets.
- **Internal Item**: A tracker item created by import, carrying a source
  reference (FR-001) used by FR-002 to detect re-imports.

## Success Criteria

- **SC-001**: Re-running an import for a project never produces a second
  internal item for a ticket that was already imported.
- **SC-002**: An internal item's source reference always resolves back to
  the correct originating ticket.

## Assumptions

- The support desk's own ticket numbering and project structure are
  outside this specification's control.
- Engineers may import more than one support-desk project into the same
  internal tracker over time.
