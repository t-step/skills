import { ThirdPartyWidget } from "widget-lib";

// @ts-expect-error - widget-lib's type definitions mark `onClose` as
// required even though the widget works fine without it; this is a known
// upstream typing bug (widget-lib#482), not a mistake in our usage
const widget = new ThirdPartyWidget({ title: "Settings" });

export default widget;
