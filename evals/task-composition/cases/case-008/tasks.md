# Tasks: Two New CLI Subcommands

This is the complete plan and task list for this piece of work. There is
no other backlog, roadmap, or context beyond what's written here.

`cli/commands.py` has a documented extension pattern at the top of the
file:

```
# Extension pattern: each subcommand defines its own handler function
# above this line, then registers itself with one line:
#   COMMANDS["name"] = handler_fn
# Existing entries are never modified or reordered when a new one is
# added; COMMANDS is a plain dict and registration order has no effect
# on behavior.
COMMANDS = {
    "status": status_cmd,
}
```

- T1: Add an `export_cmd(args)` handler function in `cli/commands.py`
  that writes the current dataset to a CSV file, and register it with
  `COMMANDS["export"] = export_cmd` per the file's documented pattern.
  Does not read or depend on anything `import_cmd` (T2) adds.
- T2: Add an `import_cmd(args)` handler function in `cli/commands.py`
  that reads a CSV file and creates records from it, and register it
  with `COMMANDS["import"] = import_cmd` per the file's documented
  pattern. Does not read or depend on anything `export_cmd` (T1) adds.
- T3: Add test `tests/test_export_cmd.py` covering T1.
- T4: Add test `tests/test_import_cmd.py` covering T2.

Both new handler functions are self-contained blocks added above the
`COMMANDS` dict per the stated pattern; combining two independent
additions to `cli/commands.py` is a plain textual merge, not a semantic
one. No priority is stated between T1/T3 and T2/T4.
