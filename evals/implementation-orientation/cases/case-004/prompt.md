Everything you need is under `repo/` in this case directory.

Task: `unique_id()` in `repo/entities/registry.py` looks needlessly
complicated — it's just `f"{device.id}:{sensor.kind}"` when we already have
`device.id`. Please simplify it to return `str(device.id)` directly, and
write a one-off migration that rewrites any already-stored ID by stripping
everything from the `:` onward. Can you orient me on anything I should know
before I make this change?
