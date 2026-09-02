# MUI Component-Fit Review — ntfy Subscribe/Publish Dialog Surface

**Scope reviewed:** `SubscribeDialog.jsx`, `PublishDialog.jsx`, `ReserveTopicSelect.jsx`, `DialogFooter.jsx`, `AttachmentIcon.jsx`, `EmojiPicker.jsx` (pinned copies under `/Users/thomasestep/Developer/mui-eval-fixtures/ntfy/web/src/components/`).

**Inferred user task:** A visitor to the ntfy web app is either (a) subscribing to a pub/sub "topic" — typing or generating a topic name, optionally reserving it with an access-control level, and optionally pointing the subscription at a self-hosted ntfy server with its own login — or (b) composing and publishing a push notification to a topic: a title/message/tags/priority, plus a long tail of optional advanced fields (click-through URL, e-mail/phone relay, delayed delivery, and a file attachment either by URL or by drag-and-drop/paste/file-picker upload) that are revealed on demand via chips and can each be individually collapsed again. Both flows are MUI `Dialog`-based forms with a shared footer pattern for status text and action buttons.

This review only addresses whether the chosen `@mui/material` components/composition match what MUI's own docs describe those components as being for. Implementation defects, accessibility markup, deprecated APIs, and general UX/hierarchy critique are out of scope.

---

## Finding 1 — File-upload progress is rendered as plain text instead of `LinearProgress`

**Where:** `PublishDialog.jsx`, `progressFn` at lines 164–176, consumed via `setStatus(...)` and rendered through `<DialogFooter status={status}>` at line 753.

```jsx
const progressFn = (ev) => {
  if (ev.loaded > 0 && ev.total > 0) {
    setStatus(
      t("publish_dialog_progress_uploading_detail", {
        loaded: formatBytes(ev.loaded),
        total: formatBytes(ev.total),
        percent: Math.round((ev.loaded * 100.0) / ev.total),
      }),
    );
  } else {
    setStatus(t("publish_dialog_progress_uploading"));
  }
};
```

The code already computes an exact `percent` (0–100) from `ev.loaded`/`ev.total` during attachment upload (`api.publishXHR(url, body, headers, progressFn)`, line 177), but only ever turns that number into an interpolated sentence rendered as `DialogContentText` inside `DialogFooter`. No progress bar is rendered anywhere in the file.

**MUI documentation:** `https://mui.com/material-ui/react-progress.md` — "To show the progress on the loading bar, use the `determinate` value for the `variant` prop, along with the `value` prop." The page's own worked example for this exact prop combination is captioned "Uploading photos…", i.e. it is MUI's canonical example for a numeric upload-progress indicator.

**Why it matters:** This is not a cosmetic nit — the component whose entire documented purpose is "render a numeric percentage from a value prop" already has the numeric input sitting unused (`ev.loaded * 100.0 / ev.total`) two lines above where it gets stringified instead. `LinearProgress variant="determinate" value={percent}` is a closer structural match to what the code is already computing than a text sentence is, and it is the component the docs point to for this exact scenario (bytes transferred out of a known total).

---

## Finding 2 — `EmojiPicker` hand-assembles `Popper` + `ClickAwayListener` + `Fade` instead of composing `Popover`

**Where:** `EmojiPicker.jsx`, lines 47–113 (whole `EmojiPicker` render).

```jsx
<Popper open={open} anchorEl={props.anchorEl} placement="bottom-start" sx={{ zIndex: 10005 }} transition>
  {({ TransitionProps }) => (
    <ClickAwayListener onClickAway={props.onClose}>
      <Fade {...TransitionProps} timeout={350}>
        <Box sx={{ boxShadow: 3, padding: 2, ... }}>
          ...
        </Box>
      </Fade>
    </ClickAwayListener>
  )}
</Popper>
```

This manually wires: (1) an `anchorEl`/`open` pair, (2) click-away-to-close via `ClickAwayListener`, (3) an entrance transition via `Fade`, and (4) elevation via a hand-set `boxShadow: 3` on a plain `Box`.

**MUI documentation:** `https://mui.com/material-ui/react-popover.md` — "A Popover can be used to display some content on top of another." The component takes exactly `open`, `anchorEl`, and `onClose`. Critically: "Popover blocks scrolling and dismisses on click-away by default, unlike Popper" — i.e., click-away dismissal is a documented built-in behavior of `Popover`, not something that has to be wired up by hand as it is here with `ClickAwayListener`. The docs also note "Popover uses Grow by default" with a default `elevation` (the docs example uses `elevation={8}`), meaning the transition and the elevated-surface `Paper` styling are likewise built in rather than something to reproduce with `Fade` + a manual `boxShadow`.

**Why it matters:** The emoji popup's required behavior — anchored, open/close by `anchorEl`, dismiss on outside click, transition in, elevated surface — is a one-for-one match for `Popover`'s documented feature set. The current code re-implements each of those four behaviors individually on top of the lower-level `Popper` primitive, which the docs explicitly distinguish from `Popover` as *not* having click-away-to-close built in. This is composition that already exists one layer up in the same library.

---

## Finding 3 — Repeated "field + inline clear button" rows reimplement `InputAdornment`, which the same codebase already uses correctly elsewhere

**Where:** `PublishDialog.jsx`, `ClosableRow` component (lines 791–803), used at: the topic/server override row (305–350), Click URL (461–487), E-mail (488–514), Attach URL + filename (545–605), and Delay (622–651). Also the "generate topic name" affordance in `SubscribeDialog.jsx` (lines 171–197).

```jsx
const ClosableRow = (props) => {
  const closable = props.closable !== undefined ? props.closable : true;
  return (
    <Row>
      {props.children}
      {closable && (
        <DialogIconButton disabled={props.disabled} onClick={props.onClose} sx={{ marginLeft: "6px" }} aria-label={props.closeLabel}>
          <Close />
        </DialogIconButton>
      )}
    </Row>
  );
};
```

Each of these is a `TextField` (or `FormControl`/`Select`) sitting in a manually flexed `<div role="row">`, followed by a separately styled `IconButton` (`DialogIconButton`, lines 805–820, with hand-tuned `height: "45px"`/`marginTop: "17px"` to visually align it with the standard-variant field) whose only job is to clear/collapse that one field.

Contrast this with `EmojiPicker.jsx` lines 74–89, in the same codebase, where the equivalent "clear this text input" affordance is built correctly:

```jsx
slotProps={{
  input: {
    endAdornment: (
      <InputAdornment position="end" sx={{ display: search ? "" : "none" }}>
        <IconButton size="small" onClick={handleSearchClear} edge="end" aria-label={t("emoji_picker_search_clear")}>
          <Close />
        </IconButton>
      </InputAdornment>
    ),
  },
}}
```

**MUI documentation:** `https://mui.com/material-ui/react-text-field.md` — "The main way is with an `InputAdornment`. This can be used to add a prefix, a suffix, or an action to an input." The documented pattern for an action embedded at the end of a field is literally an `IconButton` wrapped in `InputAdornment position="end"` (the docs' own worked example is a password-visibility toggle using this exact shape).

**Why it matters:** `PublishDialog`'s `ClosableRow`/`DialogIconButton` pair re-derives, field-by-field, the layout math (`marginTop: "17px"`, `height: "45px"`) needed to make an externally-flexed `IconButton` line up with a `TextField`, for the sole purpose of putting a clear action next to a field — which is precisely the case `InputAdornment` exists to handle without any manual alignment work, and which `EmojiPicker.jsx` already demonstrates correctly one file away. This is an internal inconsistency in component choice for the identical UI need ("field with an inline dismiss/clear action"), not a hypothetical alternative.

---

## Finding 4 — Small, fixed, icon-labeled option sets (priority, reservation access) are hidden behind a `Select` dropdown rather than shown as a `ToggleButtonGroup`

**Where:** `PublishDialog.jsx` priority picker, lines 426–459; `ReserveTopicSelect.jsx`, entire file (`Select` at lines 12–49).

Both selectors share the same shape: a small, exhaustive, mutually-exclusive set of options (5 priorities, 4 permission levels), where the authors already did the extra work of giving every option a distinct icon plus text inside a `MenuItem`:

```jsx
// PublishDialog.jsx
<Select value={priority} onChange={(ev) => setPriority(ev.target.value)} ...>
  {[5, 4, 3, 2, 1].map((p) => (
    <MenuItem key={`priorityMenuItem${p}`} value={p} ...>
      <div style={{ display: "flex", alignItems: "center" }}>
        <img src={priorities[p].file} ... />
        <div>{priorities[p].label}</div>
      </div>
    </MenuItem>
  ))}
</Select>
```

```jsx
// ReserveTopicSelect.jsx
<Select value={props.value} onChange={(ev) => props.onChange(ev.target.value)} ...>
  <MenuItem value={Permission.DENY_ALL}>
    <ListItemIcon><PermissionDenyAll /></ListItemIcon>
    <ListItemText primary={...} />
  </MenuItem>
  {/* ...3 more, one per permission level... */}
</Select>
```

**MUI documentation:** `https://mui.com/material-ui/react-toggle-button.md` — "A Toggle Button can be used to group related options. To emphasize groups of related Toggle buttons, a group should share a common container," and "With exclusive selection, selecting one option deselects any other." The docs' own worked examples for exclusive `ToggleButtonGroup` are small closed sets rendered as icon buttons in one row (text alignment: left/center/right/justify) — structurally the same shape as a 4-way permission picker or a 5-way priority picker.

I want to be precise about the strength of this claim: the MUI docs do **not** explicitly say "prefer `ToggleButtonGroup` over `Select` for small sets" — that comparison isn't made on either page. What the docs do establish is that `ToggleButtonGroup` is the documented component for "a group of related, mutually-exclusive options," and both of these pickers are exactly that (closed sets of 4–5 items, one active at a time). A `Select` hides every option behind a click and a scroll, which is the right trade-off when there are many options or limited horizontal space; here there are 4–5 items that already carry a distinct glyph each, i.e. the authors have already done the work needed to lay them out as a single visible row of toggle buttons instead of a dropdown that hides all but the current selection.

**Why it matters:** This is a genuine "was the right component chosen for a small closed set" question rather than a UX-density opinion — the docs draw a clear line between `Select`'s use case (native-`<select>`-equivalent, appropriate for larger or more open-ended lists — see also `https://mui.com/material-ui/react-select.md`: "The Select component is meant to be interchangeable with a native `<select>` element") and `ToggleButtonGroup`'s use case (a small visible group of related, exclusive options). Both pickers here match the latter description far more closely than the former.

---

## Finding 5 — The full-viewport drag-and-drop overlay reimplements `Backdrop`

**Where:** `PublishDialog.jsx`, `DropArea` (lines 914–940) and `DropBox` (lines 942–975), rendered together at lines 294 and 304 while `dropZone` is true.

```jsx
const DropBox = () => {
  const { t } = useTranslation();
  return (
    <Box
      sx={{
        position: "absolute",
        left: 0, top: 0, right: 0, bottom: 0,
        zIndex: 10000,
        backgroundColor: "#ffffffbb",
      }}
    >
      <Box sx={{ position: "absolute", border: "3px dashed #ccc", ... }}>
        <Typography variant="h5">{t("publish_dialog_drop_file_here")}</Typography>
      </Box>
    </Box>
  );
};
```

This is a hand-built, absolutely-positioned, semi-transparent full-viewport layer (plus a second absolutely-positioned `DropArea` layer above it at `zIndex: 10002` to capture the actual drag events) whose job is to dim the page and focus attention on the "drop file here" affordance while a drag is in progress.

**MUI documentation:** `https://mui.com/material-ui/react-backdrop.md` — "The Backdrop component narrows the user's focus to a particular element on the screen." "In its simplest form, the Backdrop component will add a dimmed layer over your application." "The Backdrop signals a state change within the application and can be used for creating loaders, dialogs, and more."

**Why it matters:** The stated purpose of `Backdrop` — narrow focus by dimming the rest of the app in response to a state change — is a near-exact description of what `dropZone` state is being used for here (drag-enter signals a state change; the app dims everything so the "drop here" target stands out). The current implementation reproduces the dimmed full-screen layer with manual `position: "absolute"`/`inset` styling and a hard-coded `backgroundColor: "#ffffffbb"` instead of composing the component whose documented purpose is exactly that dimmed-layer behavior (with theme-aware opacity/color rather than a hard-coded hex+alpha value).

---

## What I checked and did not flag

- `SubscribeDialog.jsx`'s use of `Autocomplete freeSolo` for the "another server" base-URL field (lines 241–261) is a good fit: it needs free text entry with suggestions drawn from the user's existing subscriptions, which is exactly what `Autocomplete`'s `freeSolo` mode is documented for.
- The `Chip` "add more fields" action bar in `PublishDialog.jsx` (lines 656–743) is a defensible use of `Chip` as a click target that reveals a field — MUI documents chips as usable for actions, not only for tags/attributes, so I did not flag this even though a `ButtonGroup` or plain `Button` row is also plausible; there isn't a clear documented mismatch here.
- `Switch` for the single "reserve this topic" / "use another server" toggles in `SubscribeDialog.jsx` is consistent with MUI's own checkbox-vs-switch guidance (`https://mui.com/material-ui/react-checkbox.md`: "If you have a single option, avoid using a checkbox and use an on/off switch instead") — I considered flagging this because the toggle doesn't take effect until the dialog's main submit button is pressed, but the docs' stated distinction is single-vs-multiple options, not immediate-vs-deferred effect, so this does not hold up as a documented mismatch and I dropped it.

I did not find a material mismatch in `AttachmentIcon.jsx` or `DialogFooter.jsx` beyond what's covered above — both are small, and their component choices (`Box component="img"` plus `Link`; a `Box` combining `DialogContentText` and `DialogActions`) don't contradict anything in the MUI docs I checked.
