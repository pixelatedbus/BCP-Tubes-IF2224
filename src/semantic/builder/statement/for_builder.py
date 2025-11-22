import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from .statement_builder import build_statement
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
    
    # Skip 'untuk' 
    if i < len(children) and children[i].name.startswith("KEYWORD"):
        i += 1
    
    if i < len(children) and children[i].name.startswith("IDENTIFIER"):
        variable = extract_identifier(children[i])
        i += 1
    
    # Skip ':=' 
    if i < len(children) and children[i].name.startswith("ASSIGN_OPERATOR"):
        i += 1
    
    if i < len(children) and children[i].name == "<expression>":
        start_expr = extract_expression_node(children[i])
        i += 1
    
    if i < len(children) and children[i].name.startswith("KEYWORD"):
        direction = extract_keyword(children[i])
        i += 1
    
    if i < len(children) and children[i].name == "<expression>":
        end_expr = extract_expression_node(children[i])
        i += 1
    
    # Skip 'lakukan' 
    if i < len(children) and children[i].name.startswith("KEYWORD"):
        i += 1
    
    
    if i < len(children):
        # Recursively build loop body statement
        body = build_statement(children[i])
    
    return ForStatementNode(variable, start_expr, end_expr, body)
