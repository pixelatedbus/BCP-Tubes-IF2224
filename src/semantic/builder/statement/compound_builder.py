import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from node_class.statement.compound_statement_node import CompoundStatementNode
from .statement_list_builder import build_statement_list


def build_compound_statement(parse_node):
    if parse_node.name != "<compound_statement>":
        raise ValueError(f"Expected <compound_statement>, got {parse_node.name}")
    
    statement_list_node = None
    
    for child in parse_node.children:
        if child.name == "<statement-list>":
            statement_list_node = build_statement_list(child)
            break
    
    compound_node = CompoundStatementNode("compound_statement")
    if statement_list_node:
        compound_node.add_child(statement_list_node)
    
    return compound_node
