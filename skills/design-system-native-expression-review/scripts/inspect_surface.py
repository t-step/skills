#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["tree-sitter==0.25.0", "tree-sitter-typescript==0.23.2"]
# ///
"""Emit facts about design-system usage in one or more .tsx/.ts files.

This script is deliberately design-system-agnostic: it does not know what
"Cloudscape" is. Callers pass the import-source prefixes that count as
"design-system imports" for their audit (e.g. --package-prefix
'@cloudscape-design/'); a different design-system audit would pass a
different prefix and get the same shape of output.

It emits FACTS only, not judgments:
  - which design-system-matching modules are imported, and what named
    exports are pulled from them
  - every JSX tag used, split into "native" (lowercase first letter, a
    plain DOM element per JSX convention) vs "component" (uppercase,
    could be a design-system component, a local wrapper, or a third-party
    component -- this script does not attempt to resolve which)
  - which native interactive HTML elements appear (a fixed, generic list:
    input, select, textarea, button, a, label, option, fieldset, legend,
    progress, meter, details, summary, dialog, form), with line + observed
    attribute names
  - every JSX element carrying a style/className/class attribute, with the
    tag, line, attribute name, and the attribute's raw source text
  - literal hex colors and CSS length values (px/rem/em/vh/vw/%) found
    inside those captured style attribute spans only -- never scanned
    across the whole file, to avoid picking up unrelated string literals

No recommendation, no pass/fail, no "this is wrong" -- an agent (or a
skill's reasoning) decides what these facts mean against authoritative
design-system guidance.

Usage:
  uv run inspect_surface.py --package-prefix '@cloudscape-design/' FILE [FILE ...]
  uv run inspect_surface.py --package-prefix '@cloudscape-design/' --package-prefix 'my-org/ds-' FILE [FILE ...]
"""

import argparse
import json
import re
import sys
from pathlib import Path

import tree_sitter_typescript as tstsx
from tree_sitter import Language, Node, Parser

NATIVE_INTERACTIVE_TAGS = {
    "input", "select", "textarea", "button", "a", "label", "option",
    "fieldset", "legend", "progress", "meter", "details", "summary",
    "dialog", "form",
}

HEX_COLOR_RE = re.compile(r"#(?:[0-9a-fA-F]{3,4}){1,2}\b")
CSS_LENGTH_RE = re.compile(r"-?\d+(?:\.\d+)?(?:px|rem|em|vh|vw|vmin|vmax|%)\b")

TSX_LANGUAGE = Language(tstsx.language_tsx())


def node_text(node: Node, src: bytes) -> str:
    return src[node.start_byte:node.end_byte].decode("utf-8", "replace")


def line_of(node: Node) -> int:
    return node.start_point[0] + 1


def jsx_tag_name(opening_or_self_closing: Node, src: bytes) -> str | None:
    for child in opening_or_self_closing.children:
        if child.type in ("identifier", "nested_identifier", "member_expression"):
            return node_text(child, src)
    return None


def jsx_attributes(element: Node) -> list[Node]:
    return [c for c in element.children if c.type == "jsx_attribute"]


def attribute_name(attr: Node, src: bytes) -> str | None:
    for child in attr.children:
        if child.type == "property_identifier":
            return node_text(child, src)
    return None


def import_source(stmt: Node, src: bytes) -> str | None:
    for child in stmt.children:
        if child.type == "string":
            for frag in child.children:
                if frag.type == "string_fragment":
                    return node_text(frag, src)
    return None


def import_specifiers(stmt: Node, src: bytes) -> list[str]:
    names = []
    for child in stmt.children:
        if child.type != "import_clause":
            continue
        for sub in child.children:
            if sub.type == "identifier":
                names.append(node_text(sub, src))  # default import
            elif sub.type == "named_imports":
                for spec in sub.children:
                    if spec.type == "import_specifier":
                        names.append(node_text(spec, src))
            elif sub.type == "namespace_import":
                names.append(node_text(sub, src))
    return names


def walk(node: Node):
    yield node
    for child in node.children:
        yield from walk(child)


def inspect_file(path: Path, prefixes: list[str]) -> dict:
    src = path.read_bytes()
    parser = Parser(TSX_LANGUAGE)
    tree = parser.parse(src)

    design_system_imports = []
    jsx_tag_counts: dict[str, int] = {}
    native_interactive = []
    style_class_usage = []
    literal_values = []

    for node in walk(tree.root_node):
        if node.type == "import_statement":
            source = import_source(node, src)
            if source and any(source.startswith(p) for p in prefixes):
                design_system_imports.append({
                    "source": source,
                    "specifiers": import_specifiers(node, src),
                    "line": line_of(node),
                })
        elif node.type in ("jsx_opening_element", "jsx_self_closing_element"):
            tag = jsx_tag_name(node, src)
            if tag is None:
                continue
            jsx_tag_counts[tag] = jsx_tag_counts.get(tag, 0) + 1

            attrs = jsx_attributes(node)
            attr_names = [attribute_name(a, src) for a in attrs]
            attr_names = [a for a in attr_names if a]

            if tag in NATIVE_INTERACTIVE_TAGS:
                native_interactive.append({
                    "tag": tag,
                    "line": line_of(node),
                    "attributes": attr_names,
                })

            for attr in attrs:
                name = attribute_name(attr, src)
                if name not in ("style", "className", "class"):
                    continue
                raw = node_text(attr, src)
                style_class_usage.append({
                    "tag": tag,
                    "line": line_of(node),
                    "attribute": name,
                    "raw": raw[:300],
                })
                if name == "style":
                    for m in HEX_COLOR_RE.finditer(raw):
                        literal_values.append({
                            "tag": tag, "line": line_of(node),
                            "kind": "hex-color", "value": m.group(0),
                        })
                    for m in CSS_LENGTH_RE.finditer(raw):
                        literal_values.append({
                            "tag": tag, "line": line_of(node),
                            "kind": "css-length", "value": m.group(0),
                        })

    return {
        "file": str(path),
        "design_system_imports": design_system_imports,
        "jsx_tag_counts": jsx_tag_counts,
        "native_interactive_elements": native_interactive,
        "style_class_usage": style_class_usage,
        "literal_style_values": literal_values,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument(
        "--package-prefix", action="append", required=True, dest="prefixes",
        help="Import-source prefix that counts as a design-system import "
             "(repeatable). E.g. '@cloudscape-design/'.",
    )
    args = ap.parse_args()

    results = []
    for f in args.files:
        if not f.exists():
            print(f"inspect_surface: no such file: {f}", file=sys.stderr)
            return 1
        results.append(inspect_file(f, args.prefixes))

    json.dump({"package_prefixes": args.prefixes, "files": results}, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
