# Goal

Fix issue #482: concurrent calls to `Counters.increment(name)` sometimes
lose updates under load (final total is less than the number of increments
performed), because the read-modify-write on the in-memory counter dict
isn't atomic.
