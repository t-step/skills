# Product state — Quillset

No review, retro, or backlog exists in this repository. This is a snapshot
of directly observable current product state.

Quillset is an internal template-rendering library used by other
engineering teams to generate PDF reports from a template plus a data
object. It has no external users; its consumers are other internal
engineering teams who import it as a dependency.

`README.md`'s "Future ideas" section lists three possibilities, each
written as a bare bullet with no further detail:

- SVG watermark support
- A plugin system for custom renderers
- A caching layer for repeated renders of the same template+data pair

None of these has a linked ticket, an incident report, a message from a
consuming team, or any usage data attached. There is no issue tracker
entry, support channel, or internal chat reference mentioning any of them,
and no note anywhere describing a team that tried to do something with
Quillset and couldn't. The library's existing test suite and the two
consuming teams' own code (which this repository does not include) are the
only other evidence available, and neither is described here beyond what's
stated above.
