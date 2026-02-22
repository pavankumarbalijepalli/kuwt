"""Print JSON tree structure utility.

Provides `print_json_tree(data, ...)` which pretty-prints nested JSON
(dicts and lists) as a tree. Also includes a small CLI to load a JSON
string or file and display its structure.
"""
from __future__ import annotations
import json
import argparse
from typing import Any, Optional


def _format_value(v: Any, max_len: int = 80) -> str:
    s = repr(v)
    if len(s) > max_len:
        return s[: max_len - 3] + "..."
    return s


def print_json_tree(data: Any, show_values: bool = True, max_depth: Optional[int] = None) -> None:
    """Print the tree structure of `data` (a Python object from JSON).

    - `show_values`: whether to include primitive values on leaf nodes.
    - `max_depth`: optional limit (root depth = 0).
    """

    def walk(node: Any, name: Optional[str], prefix: str, is_last: bool, depth: int) -> None:
        if max_depth is not None and depth > max_depth:
            return

        connector = "└─ " if is_last else "├─ "
        label = name if name is not None else "(root)"

        if isinstance(node, dict):
            print(f"{prefix}{connector}{label} (dict, {len(node)} keys)")
            child_prefix = prefix + ("    " if is_last else "│   ")
            for i, (k, v) in enumerate(node.items()):
                last = i == len(node) - 1
                walk(v, str(k), child_prefix, last, depth + 1)
        elif isinstance(node, list):
            print(f"{prefix}{connector}{label} (list, {len(node)} items)")
            child_prefix = prefix + ("    " if is_last else "│   ")
            for i, item in enumerate(node):
                last = i == len(node) - 1
                walk(item, f"[{i}]", child_prefix, last, depth + 1)
        else:
            if show_values:
                print(f"{prefix}{connector}{label}: {_format_value(node)} ({type(node).__name__})")
            else:
                print(f"{prefix}{connector}{label} ({type(node).__name__})")

    # Start from root; show top-level type without an extra connector
    if isinstance(data, dict):
        print(f"(root) dict, {len(data)} keys")
        for i, (k, v) in enumerate(data.items()):
            last = i == len(data) - 1
            walk(v, str(k), "", last, 1)
    elif isinstance(data, list):
        print(f"(root) list, {len(data)} items")
        for i, item in enumerate(data):
            last = i == len(data) - 1
            walk(item, f"[{i}]", "", last, 1)
    else:
        if show_values:
            print(f"(root) {type(data).__name__}: {_format_value(data)}")
        else:
            print(f"(root) {type(data).__name__}")


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Print JSON tree structure")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="Path to JSON file")
    group.add_argument("-s", "--string", help="JSON string to parse")
    p.add_argument("--no-values", action="store_true", help="Do not show primitive values")
    p.add_argument("--max-depth", type=int, default=None, help="Maximum recursion depth (root=0)")
    return p.parse_args()


def _main() -> None:
    args = _parse_args()
    if args.file:
        with open(args.file, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    else:
        data = json.loads(args.string)

    print_json_tree(data, show_values=not args.no_values, max_depth=args.max_depth)


if __name__ == "__main__":
    _main()
