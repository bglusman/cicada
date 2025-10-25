#!/usr/bin/env python
"""Debug script to see how tree-sitter parses aliases."""

import tree_sitter_elixir as ts_elixir
from tree_sitter import Language, Parser

code = b"""
defmodule Test do
  alias MyApp.Database, as: DB
end
"""

language = Language(ts_elixir.language())
parser = Parser(language)

tree = parser.parse(code)
root = tree.root_node

def print_tree(node, indent=0):
    """Print tree structure."""
    print("  " * indent + f"{node.type}: {code[node.start_byte:node.end_byte].decode('utf-8')[:50]}")
    for child in node.children:
        print_tree(child, indent + 1)

print_tree(root)
