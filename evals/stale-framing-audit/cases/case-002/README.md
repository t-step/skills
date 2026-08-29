# Fleet Scheduler

## Architecture

- **WorkerRegistry** -- the service workers check in and out with.
- **Coordinator** -- manages worker state and routes incoming tasks to the
  least-loaded worker, based on the current worker registry.

The Coordinator is what the ops dashboard and the task router both talk to.
