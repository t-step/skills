# Context: Apache Ignite -- moving common classes into their own module

Apache Ignite's server (`ignite-core`) and its thin client both currently
depend on a set of plain utility and language classes (closures, tuples,
string-formatting helpers, exception types, and similar) that live inside
`ignite-core` even though nothing about most of them is actually
server-specific. That coupling is one of several the project is working
through as part of a longer-running, multi-phase internal effort whose
later phases include eventually letting the thin client ship independent
of the full server.

This phase's own stated motivation is narrower and more concrete: the
`org.apache.ignite.binary` package -- itself a preexisting internal
subsystem, not something this phase is building -- already depends
heavily on several of these utility/language classes, so before even
`org.apache.ignite.binary`'s own public API can be moved out of
`ignite-core` in a later phase, these shared dependency classes need
somewhere clearer to live than `ignite-core` itself. The plan is to
create a new module, `ignite-commons`, and move the classes genuinely
shared across `ignite-core` and future modules into it -- specifically
everything in the `org.apache.ignite.lang` and
`org.apache.ignite.internal.util` packages, except whatever turns out, on
a class-by-class look, to actually be core-specific. This is described,
across the broader initiative this phase belongs to, as pure internal
refactoring: nothing about the server's or the client's observable
behavior is meant to change.
