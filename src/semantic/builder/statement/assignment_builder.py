import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from node_class.statement.assignment_statement_node import AssignmentStatementNode
from .helpers import extract_identifier, extract_expression_node


def build_assignment_statement(parse_node):
    if parse_node.name != "<assignment-statement>":
        raise ValueError(f"Expected <assignment-statement>, got {parse_node.name}")
    
    variable_name = "unknown"
    expression_node = None
    
    for child in parse_node.children:
        if child.name.startswith("IDENTIFIER"):
            variable_name = extract_identifier(child)
        elif child.name == "<expression>":
            # TODO: Replace with actual expression AST node builder
            expression_node = extract_expression_node(child)
    
    return AssignmentStatementNode(variable_name, expression_node)
