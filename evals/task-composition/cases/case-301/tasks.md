# Tasks: Move common classes to ignite-commons

These are the issues filed in the tracker, as of the stated cutoff, under
the umbrella ticket for this phase of work. All are real issue keys.
Every task below except the umbrella ticket itself is formally filed as a
Jira Sub-task of it -- a stronger, more explicit relationship than "same
label" or "same epic."

- **IGNITE-24781** (Improvement, Open) -- *Move common classes to
  ignite-commons.* The umbrella ticket for this phase. Full description
  as filed:

  > Umbrella ticket for and Phase 1 of IEP-119 - Refactoring.
  >
  > We want to move all common for ignite-core and future ignite-binary
  > modules to ignite-commons module:
  > Specifically, we want to move to ignite-commons the following
  > packages:
  >
  > 1. org.apache.ignite.lang.*
  > 2. org.apache.ignite.internal.util.*
  >
  > Except the classes used only in core core - each class need to be
  > investigated separately.
  >
  > While this work in progress ignite-commons must compile classes
  > directly to ignite-core/target/classes folder to preserve binary
  > content.
  >
  > Refactoring comes from the fact that `org.apache.ignite.binary`
  > package classes heavily relies on the above packages and classes like
  > `org.apache.ignite.internal.util.typedef.internal.A`,
  > `org.apache.ignite.internal.util.typedef.internal.F`,
  > `IgniteException`, etc. therefore prior to moving even public API to
  > separate module we must move dependecy classes to something more
  > clear then ignite-core.

- **IGNITE-24782** (Sub-task of IGNITE-24781, Open) -- *Create
  ignite-commons module.* Full description as filed:

  > Create module ignite-commons with several super simple classes in it.

- **IGNITE-24792** (Sub-task of IGNITE-24781, Open) -- *Move
  org.apache.ignite.internal.util.tostring to ignite-commons.* Full
  description as filed:

  > S.toString used among many utility classes. We need to move code to
  > ignite-commons module.

- **IGNITE-24846** (Sub-task of IGNITE-24781, Open) -- *Move F to
  ignite-commons.* No description beyond the title. One stated link:
  this issue **blocks IGNITE-24850**.

- **IGNITE-24847** (Sub-task of IGNITE-24781, Open) -- *Move U to
  ignite-commons.* No description beyond the title. No links stated.

- **IGNITE-24848** (Sub-task of IGNITE-24781, Open) -- *Move GridTuple* to
  ignite-commons.* No description beyond the title. One stated link:
  this issue **blocks IGNITE-24850**.

- **IGNITE-24850** (Sub-task of IGNITE-24781, Open) -- *Split IgniteUtils
  to common and core specific methods.* Full description as filed:

  > IgniteUtils contains bunch of methods that is ignite-core specific
  > and another part of just common utility methods.
  >
  > We need to split class in two to separate methods that will be
  > keeped in ignite-core from the common ones.

  Two stated links: this issue **is blocked by IGNITE-24846** and **is
  blocked by IGNITE-24848**.

- **IGNITE-24851** (Sub-task of IGNITE-24781, Open) -- *Move
  IgniteException to ignite-commons.* No description beyond the title. No
  links stated on this issue itself -- but see IGNITE-24957 below, which
  names this issue in its own text.

- **IGNITE-24852** (Sub-task of IGNITE-24781, Open) -- *Move
  IgniteCheckedException to ignite-commons.* No description beyond the
  title. No links stated.

- **IGNITE-24941** (Sub-task of IGNITE-24781, Open) -- *Remove unused code
  from IgniteUtils.* Full description as filed:

  > It is necessary to remove unused class members.

- **IGNITE-24946** (Sub-task of IGNITE-24781, Open) -- *Replace F.eq with
  the Objects.equals.* Full description as filed (identical to the
  title):

  > Replace F.eq with the Objects.equals

- **IGNITE-24957** (Sub-task of IGNITE-24781, Open) -- *Move X to
  ignite-commons.* Full description as filed:

  > Move X to ignite-commons
  >
  > There are 4 application for that class:
  > 1. System.out and system.err related work, which is spread out and
  >    used in multiple modules.
  > 2. timeSpanXXX methods for creating string presentation of given
  >    time, which is primarly used within X itself and ignite-core.
  > 3. shallow and deep cloning logic, which is primarly used within X
  >    itself and ignite-core.
  > 4. Exceptions and Throwables handling logic, which is also spread
  >    out.
  >
  > It's safe to move this utillity class to ignite-commons completely.
  > Nevertheless the class at current state is dependent from these
  >
  > ```
  > import org.apache.ignite.IgniteException;
  > import org.apache.ignite.internal.util.GridLeanMap;
  > import org.apache.ignite.internal.util.typedef.internal.SB;
  > import org.apache.ignite.internal.util.typedef.internal.U;
  > import org.apache.ignite.lang.IgniteFuture;
  > import org.jetbrains.annotations.Nullable;
  > ```
  >
  > I suggest to move "Exceptions and Throwables handling logic, which is
  > also spread out." first within this ticket to unblock IGNITE-24851.

- **IGNITE-24958** (Sub-task of IGNITE-24781, Open) -- *Move GridLeanMap
  to ignite-commons.* Full description as filed (identical to the
  title):

  > Move GridLeanMap to ignite-commons

No task above states an explicit priority relative to any other task in
this list (Jira's own per-issue priority field is Major on every issue in
this set). No task states an estimate or a target date.
