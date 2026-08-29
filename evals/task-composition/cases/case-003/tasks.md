# Tasks: Dynamic Agent Dispatch

This is the complete plan and task list for this piece of work. There is
no other backlog, roadmap, or context beyond what's written here.

## Config subsystem

- T1: Add an `AgentConfig` schema in `config/schema.py` (fields: `name`,
  `model`, `max_tokens`, `tools`).
- T2: Add `validate_agent_config(cfg)` in `config/validate.py`,
  validating T1's schema.
- T3: Add test `tests/test_config_validate.py` covering T1 and T2.

## Coding-agent subsystem

- T4: Implement a `CodingAgent` class in `agents/coding_agent.py` with a
  `run()` / `step()` interface.
- T5: Add test `tests/test_coding_agent.py` exercising T4's `run()` /
  `step()` interface directly, against a hand-built stub config (not
  `AgentConfig`).

## Dispatch

- T6: Implement `dispatch(cfg: AgentConfig) -> CodingAgent` in
  `dispatch/dispatch.py`. This requires a validated `AgentConfig` (T1
  through T3) and a working `CodingAgent` (T4 and T5) to both already
  exist.
- T7: Add end-to-end test `tests/test_dispatch_e2e.py` that validates a
  real `AgentConfig`, dispatches an agent through T6, and runs one step.

## Final checks

- T8: Run the linter across the changed files and update
  `CHANGELOG.md`.

The config subsystem and the coding-agent subsystem don't reference any
of the same files. No priority is stated between them.
