# Dependencies

## Stated or clearly inferable, INTERNAL to this task set

- **CASSANDRA-18490 depends on CASSANDRA-18345.** 18490's stated goal is
  to checksum-validate SAI's index components "on startup, full rebuild,
  and streaming." 18345's own description says SAI's components are
  *not* currently carried by SSTable streaming at all -- the streamed
  component set is still the old fixed list. Until 18345 makes streaming
  actually carry SAI's components, there is nothing meaningful for 18490
  to checksum-validate in the streaming case. This is a real dependency,
  not just two tickets in the same area.

- **CASSANDRA-18521 originates from CASSANDRA-18217**, per its own
  description ("a discussion mentioned in CASSANDRA-18217..."). 18217 is
  already merged as of this snapshot (see `repository-state.md`), so this
  is not a dependency on anything remaining in this task list -- it's a
  follow-up to already-landed work.

## Concrete but not explicitly stated -- worth checking, not settled

- **CASSANDRA-18067 (on-disk numeric index, in progress) and
  CASSANDRA-18494 (lucene-core upgrade)** both touch the vendored Lucene
  dependency: per the CEP-7 design, SAI's numeric index is built on a
  modified Lucene block kd-tree, and 18494 proposes changing the Lucene
  version SAI vendors. Neither ticket's text references the other. It is
  not established whether bumping the vendored library mid-implementation
  of 18067 would touch code 18067 is actively changing -- this is a
  concrete, named shared dependency (a specific library), not a vague
  "both touch indexing" concern, but whether it actually creates a
  conflict is not something either ticket's text settles.

- **CASSANDRA-18280 (RAMIndexOutput initial allocation) and
  CASSANDRA-18067 (on-disk numeric index, in progress)** both involve the
  low-level on-disk postings write path: 18280's own description says
  `RAMIndexOutput` "is used to build the on-disk postings in SAI"
  generally, and 18067 is actively building a new on-disk index format.
  Whether 18067's in-progress code already uses (or will use)
  `RAMIndexOutput` in a way that would make the two non-independent is
  not stated in either ticket.

- **CASSANDRA-18166 (IndexContext code-model cleanup) and the rest of the
  list.** `IndexContext` is a shared class touched by indexing/searching
  code generally, so it's plausible other in-progress or planned work
  (particularly 18067) also touches it. Neither 18166 nor any other
  ticket states this. Treat as an open topology question, not a
  confirmed dependency in either direction.

## Genuinely EXTERNAL to this task set

- **CASSANDRA-18112 is blocked on something outside this task list
  entirely: an unresolved community design/grammar discussion.** The
  filer explicitly says the CQL syntax for index hints needs a
  mailing-list DISCUSS thread before implementation should start, and
  even questions whether the underlying feature (a general CQL hint
  mechanism) has a clear scope at all. No task in this list, and no
  amount of engineering effort by whoever picks this up, resolves that by
  itself -- it needs a decision made outside this task set's own work.

- **CASSANDRA-18345 depends on / must coordinate with a piece of the
  general Cassandra storage engine that is not part of this task list at
  all: the SSTable format's streamed-component set
  (`Components.STREAMING_COMPONENTS`).** This is core, shared SSTable
  machinery used by every SSTable-based feature, not something owned or
  decided within SAI's own task set -- SAI can propose a change to it,
  but that change has architectural blast radius beyond SAI. See
  `repository-state.md` for a concrete, already-observed instance of an
  unrelated change to this same area of the codebase forcing an
  adjustment to SAI's own code during a routine rebase.

## Not addressed by any of the above

- No task in this list states or implies a dependency on
  CASSANDRA-18067 finishing first, except through the 18345/18490 chain
  above (which runs through streaming and checksumming, not through
  18067 directly). In particular, none of the smaller cleanup/improvement
  tickets (18165, 18166, 18167, 18216, 18280, 18494, 18515, 18521) state
  or imply that they must wait for 18067.
