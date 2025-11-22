import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from node_class.statement.statement_list_node import StatementListNode


def build_statement_list(parse_node):
    if parse_node.name != "<statement-list>":
        raise ValueError(f"Expected <statement-list>, got {parse_node.name}")
    
    statement_list = StatementListNode("statement_list")
    
    for child in parse_node.children:
        # Skip semicolons
        if child.name.startswith("SEMICOLON"):
            continue
        
        if child.name.startswith("<") or child.name.startswith("IDENTIFIER"):
            # TODO: Replace with actual statement builder dispatch
            statement_list.add_child(child)
    
    return statement_list
