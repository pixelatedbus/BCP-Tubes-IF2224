import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from node_class.statement.if_statement import IfStatementNode
from .helpers import extract_expression_node, find_child_by_name


def build_if_statement(parse_node):
    if parse_node.name != "<if-statement>":
        raise ValueError(f"Expected <if-statement>, got {parse_node.name}")
    
    condition = None
    then_body = None
    else_body = None
    
    i = 0
    children = parse_node.children
    
    # Skip 'jika' 
    if i < len(children) and children[i].name.startswith("KEYWORD"):
        i += 1
    
    if i < len(children) and children[i].name == "<expression>":
        condition = extract_expression_node(children[i])
        i += 1
    
    # Skip 'maka' 
    if i < len(children) and children[i].name.startswith("KEYWORD"):
        i += 1
    
    if i < len(children) and (children[i].name.startswith("<") or children[i].name.startswith("IDENTIFIER")):
        # TODO: Replace with actual statement builder
        then_body = children[i]
        i += 1
    
    if i < len(children) and children[i].name.startswith("KEYWORD") and "selain_itu" in children[i].name:
        i += 1
        # Get else statement
        if i < len(children):
            # TODO: Replace with actual statement builder
            else_body = children[i]
    
    return IfStatementNode(condition, then_body, else_body)
