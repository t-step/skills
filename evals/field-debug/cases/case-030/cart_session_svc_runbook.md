# cart-session-svc runbook (owned by Checkout Engineering)

## Restarting a pod

**Never restart a `cart-session-svc` pod directly (`kubectl delete pod`,
rolling restart, or otherwise).** Sessions are pinned per-pod with no
shared store and no cross-pod replication -- restarting drops every
in-flight cart on that pod instantly, with no recovery and no user-facing
warning. A customer mid-payment loses their cart silently.

**Safe procedure:**

1. Flip `drain:<pod-name>` in the Checkout deploy tool
   (`deploy.checkout.internal`). This stops new sessions from being
   assigned to the pod (same effect as an SRE-side traffic-weight change,
   but also updates Checkout's own dashboards and paging rules).
2. Wait for the pod's active session count to reach 0, or 10 minutes,
   whichever comes first.
3. Only then restart the pod.

If OOM is imminent before natural drain-out completes, this is a judgment
call for Checkout on-call to make explicitly -- accepting the cart-loss
blast radius against the OOM/crash-loop alternative -- not a default
action.

## Access

The `drain:<pod>` flag lives in Checkout's own deploy-tool namespace.
