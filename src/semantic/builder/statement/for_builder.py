import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from node_class.statement.for_statement_node import ForStatementNode
from .helpers import extract_identifier, extract_keyword, extract_expression_node


def build_for_statement(parse_node):
    if parse_node.name != "<for_statement>":
        raise ValueError(f"Expected <for_statement>, got {parse_node.name}")
    
    variable = "unknown"
    start_expr = None
    end_expr = None
    direction = "ke"
    body = None
    
    i = 0
    children = parse_node.children
    
    # Skip 'untuk' keyword
    if i < len(children) and children[i].name.startswith("KEYWORD"):
        i += 1
    
    # Get variable identifier
    if i < len(children) and children[i].name.startswith("IDENTIFIER"):
        variable = extract_identifier(children[i])
        i += 1
    
    # Skip ':=' operator
    if i < len(children) and children[i].name.startswith("ASSIGN_OPERATOR"):
        i += 1
    
    # Get start expression
    if i < len(children) and children[i].name == "<expression>":
        start_expr = extract_expression_node(children[i])
        i += 1
    
    # Get direction keyword (ke or turun-ke)
    if i < len(children) and children[i].name.startswith("KEYWORD"):
        direction = extract_keyword(children[i])
        i += 1
    
    # Get end expression
    if i < len(children) and children[i].name == "<expression>":
        end_expr = extract_expression_node(children[i])
        i += 1
    
    # Skip 'lakukan' keyword
    if i < len(children) and children[i].name.startswith("KEYWORD"):
        i += 1
    
    # Get body statement
    if i < len(children):
        # TODO: Replace with actual statement builder
        body = children[i]
    
    return ForStatementNode(variable, start_expr, end_expr, body)
