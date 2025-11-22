import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from node_class.statement.while_statement_node import WhileStatementNode
from .helpers import extract_expression_node


def build_while_statement(parse_node):
    if parse_node.name != "<while_statement>":
        raise ValueError(f"Expected <while_statement>, got {parse_node.name}")
    
    condition = None
    body = None
    
    i = 0
    children = parse_node.children
    
    # Skip 'selama' 
    if i < len(children) and children[i].name.startswith("KEYWORD"):
        i += 1
    
    if i < len(children) and children[i].name == "<expression>":
        condition = extract_expression_node(children[i])
        i += 1
    
    # Skip 'lakukan' 
    if i < len(children) and children[i].name.startswith("KEYWORD"):
        i += 1
    
    if i < len(children):
        # TODO: Replace with actual statement builder
        body = children[i]
    
    return WhileStatementNode(condition, body)
