# Feature Specification: Cancellation-Triggered Refund

**Status**: Draft

**Input**: "When a customer cancels within the refund window, cancel their
subscription locally and issue the refund through our payment provider,
without double-refunding if anything hiccups."

## User Scenarios & Testing

### User Story 1 - Cancel and refund together (Priority: P1)

A customer cancels a subscription that is still within its refund window.
The subscription becomes cancelled, and the payment provider issues a
refund for the current billing period.

**Acceptance Scenarios**:

1. **Given** a subscription within its refund window, **When** the
   customer cancels it, **Then** the subscription's status becomes
   `cancelled` and a refund request is sent to the payment provider for
   the current period's charge.
2. **Given** a subscription outside its refund window, **When** the
   customer cancels it, **Then** the subscription's status becomes
   `cancelled` and no refund request is sent.

### Edge Cases

- What happens if the customer cancels a subscription that's already
  cancelled? The request is accepted without error and no second refund
  request is sent, since the subscription was already `cancelled`.

## Requirements

### Functional Requirements

- **FR-001**: When a customer cancels a subscription within its refund
  window, the system MUST set the subscription's status to `cancelled`.
- **FR-002**: When a subscription's status becomes `cancelled` and it was
  within its refund window, the system MUST send a refund request to the
  payment provider for the current period's charge.
- **FR-003**: Cancelling an already-`cancelled` subscription MUST be
  accepted without error and MUST NOT send a second refund request.
- **FR-004**: The refund request sent to the payment provider MUST
  identify the specific charge being refunded, so the provider can
  associate the refund with the correct transaction.

### Key Entities

- **Subscription**: Has a status (`active`, `cancelled`) and a refund
  window computed from its billing period.
- **Refund Request**: A call to the external payment provider identifying
  a charge to refund (FR-004).

## Success Criteria

- **SC-001**: Every eligible cancellation (within the refund window)
  results in exactly one refund request reaching the payment provider.
- **SC-002**: No customer is ever refunded twice for the same
  cancellation.

## Assumptions

- The payment provider's own refund-processing behavior (how long a
  refund takes to post, retries on their side) is out of scope here.
- Subscriptions are cancelled one at a time via an explicit customer or
  support action; there is no bulk-cancellation path in scope.
