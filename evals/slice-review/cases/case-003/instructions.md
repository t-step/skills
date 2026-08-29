# Repo instructions (excerpt)

- When a module is retired, either delete it or leave it with a `# deprecated,
  do not call` comment — but a deprecation comment alone does not satisfy a
  ticket that says something should be "replaced"; call sites must actually
  move to the new path.
- New code needs a test.
