# MUI Design-System Review — hk-independent-bus-eta (route → stop-ETA → stop-detail flow)

## Inferred user task

A rider is looking up a specific bus route: they land on a route page showing the route number, origin/destination, and a live map, scroll or tap through an ordered, single-open-at-a-time accordion list of every stop the route serves (each row showing live ETAs plus per-stop actions — pin, share, favorite, set an arrival alarm), and can tap a stop to open a detail dialog with the stop's full route listing, a bookmark toggle, and shortcuts to open the stop's location in Google Maps or navigate to its own dedicated stop page. A separate "Bookmarked stops" page and a standalone stop-ETA page reuse the same stop-route-list building block outside of the route-map context. Occasionally a banner appears telling the rider the underlying route database is stale and inviting them to refresh it.

## Findings

### 1. `RouteUpdateNotice.tsx` reimplements a persistent notice banner with `Box` instead of `Alert`

**Where:** `/Users/thomasestep/Developer/mui-eval-fixtures/hk-independent-bus-eta/src/components/route-eta/RouteUpdateNotice.tsx`, lines 29–49.

The component renders a plain `Box` with hand-rolled border/padding/border-radius styling, a click handler on the whole box (`onClick={renewDb}`) that triggers a data-refresh action, and a single `Typography` line ("⁉️ {t('db-renew-text')}"):

```tsx
<Box sx={rootSx} onClick={renewDb}>
  <Typography>⁉️ {t("db-renew-text")}</Typography>
</Box>
```

with `rootSx` manually reconstructing an alert-like surface (`borderStyle: "solid"`, `borderWidth: 1`, `borderRadius`, `cursor: "pointer"`).

**MUI documentation:** `https://mui.com/material-ui/react-alert.md`
- "Alerts display brief messages for the user without interrupting their use of the app."
- On the dedicated action pattern: "### Actions / Add an action to your Alert with the `action` prop." — "This lets you insert any element — an HTML tag, an SVG icon, or a React component such as a Material UI Button — after the Alert's message, justified to the right."

For contrast, the *transient/toast* counterpart is explicitly scoped elsewhere — `https://mui.com/material-ui/react-snackbar.md`: "Snackbars (also known as toasts) are used for brief notifications of processes that have been or will be performed" and "Snackbars are not intended to convey critical information or block the user from interacting with the rest of the app." This confirms the notice in question (a standing, non-transient, page-level condition — "your local data is out of date" — that persists across renders until the user acts or the condition clears, per the `show` state gated on `updatedAt > updateTime`) is exactly the persistent/contextual case `Alert` is built for, not the toast case `Snackbar` is built for.

**Why it matters:** `Alert` is the component MUI's own docs describe for exactly this shape of message (a standing, dismissible-or-actionable contextual notice), and it ships a documented `action` prop purpose-built for "renew now" as a clickable affordance instead of making the entire message row an ambiguous click target. Choosing `Alert severity="warning"` with `action={<Button onClick={renewDb}>...</Button>}` would replace hand-authored border/color/radius styling with the design system's own severity-driven color and iconography, and would make the clickable region an explicit, discoverable button rather than the whole banner being an unlabeled click surface.

---

### 2. `StopDialog.tsx` fights `Dialog`'s default sizing with manual CSS instead of using the documented `fullScreen` prop

**Where:** `/Users/thomasestep/Developer/mui-eval-fixtures/hk-independent-bus-eta/src/components/route-eta/StopDialog.tsx`, lines 68 and 103–112.

```tsx
<Dialog open={open} onClose={onClose} sx={rootSx}>
  ...
const rootSx: SxProps<Theme> = {
  "& .MuiPaper-root": {
    width: "100%",
    marginTop: "90px",
    height: "calc(100vh - 100px)",
  },
  "& .MuiDialogContent-root": {
    padding: 0,
  },
};
```

This dialog is used to show a stop's entire route listing (`StopRouteList`, a scrollable, potentially long list) — a task that needs most of the viewport, not the default centered/sized `Dialog` surface. Rather than reach for `Dialog`'s own full-viewport mode, the code overrides the internal `MuiPaper-root` class with a magic-number `marginTop: 90px` and `height: calc(100vh - 100px)` to fake an edge-to-edge, near-fullscreen sheet.

**MUI documentation:** `https://mui.com/material-ui/react-dialog.md`
- The Dialog API/props table lists `fullScreen` as a documented boolean prop (default `false`) whose purpose is exactly this: expand the dialog to fill the entire screen.
- The docs' "Responsive full-screen" section demonstrates the intended pattern for exactly this "make it full screen, especially on small/mobile viewports" need: `const fullScreen = useMediaQuery(theme.breakpoints.down('md'));` passed straight into `<Dialog fullScreen={fullScreen} ...>`.

**Why it matters:** This app is a PWA aimed at transit riders, i.e., predominantly a mobile/small-viewport surface — precisely the scenario the docs' `fullScreen` + `useMediaQuery` responsive pattern targets. Using the documented `fullScreen` prop (optionally gated by `useMediaQuery` for larger screens) would let `Dialog` manage the full-viewport surface itself — safe-area handling, consistent slide/enter transitions for a full-screen sheet, and no `MuiPaper-root` override — instead of a bespoke, viewport-fragile CSS override (`calc(100vh - 100px)` breaks on iOS Safari's dynamic viewport chrome and doesn't track safe-area insets) standing in for a one-prop, documented feature built for this exact case.

---

### 3. `RouteHeader.tsx` recreates a top-bar layout (leading action / title / trailing action) with `Paper` + manual flexbox instead of `AppBar`/`Toolbar`

**Where:** `/Users/thomasestep/Developer/mui-eval-fixtures/hk-independent-bus-eta/src/components/route-eta/RouteHeader.tsx`, lines 25–43.

```tsx
<Paper id="route-eta-header" sx={PaperSx} elevation={0}>
  <ReverseButton routeId={routeId} stopId={stopId} />
  <Box sx={centerColumnSx}>
    <Box sx={routeNoRowSx}>
      <RouteNo routeNo={t(route)} component="h1" align="center" />
      <RouteStarButton routeId={routeId} />
    </Box>
    <Typography component="h2" variant="caption" align="center">
      {t("往")} {toProperCase(dest[language])} ...
    </Typography>
  </Box>
  <Box sx={rightColumnSx}>
    <Divider orientation="vertical" flexItem />
    <TimetableButton routeId={routeId} />
  </Box>
</Paper>
```

This is a leading icon action (`ReverseButton`), a centered title/subtitle block (route number + destination), and a trailing icon action (`TimetableButton`) — assembled from a bare `Paper` plus three hand-built `sx` flex containers (`PaperSx`, `centerColumnSx`, `routeNoRowSx`, `rightColumnSx`) rather than the component MUI documents for exactly this composition.

**MUI documentation:** `https://mui.com/material-ui/react-app-bar.md`
- Opening definition: "The App Bar displays information and actions relating to the current screen." The page describes it being used for "branding, screen titles, navigation, and actions," with `Toolbar` as the content container inside it, and worked examples composing a leading `IconButton` (`edge="start"`), a `Typography` title, and trailing `IconButton`/`Button` actions — the same three-slot leading-action / title / trailing-action shape this route header hand-assembles.

**Why it matters:** `RouteHeader` is functionally a per-screen title bar for the route-detail screen (route identity + a reversal/navigation action + a timetable action), which is precisely the "information and actions relating to the current screen" role `AppBar`/`Toolbar` is documented for. Composing it from `Paper` + three bespoke `sx` blocks forfeits the built-in `Toolbar` slot/spacing conventions (`edge="start"`, `flexGrow` title behavior, consistent min-height/gutters) that the documented `AppBar`/`Toolbar` pairing already codifies for this exact leading/title/trailing pattern, in favor of reinventing the same layout by hand.

## Not flagged

- `StopAccordionList.tsx` / `StopAccordion.tsx`: the single-expansion, externally-controlled `Accordion` list (`expanded={stopIdx === idx}`, one stop open at a time, driven by parent state) matches MUI's own controlled-accordion pattern; no better-fitting core component was identified for this per-stop expand/collapse-with-live-content structure.
- The "copied to clipboard" `Snackbar` in `StopAccordionList.tsx` (lines 65–73) is a textbook fit for Snackbar's documented "brief, temporary, non-critical" scope — correctly distinguished from the persistent-notice case in Finding 1.
- `StopEtaListPage.tsx` and `BookmarkedStopPage.tsx` layouts (plain `Box`/`Typography`/`Divider` scaffolding) did not present a clear case where a different core `@mui/material` component would more natively express the task; no finding raised there.
