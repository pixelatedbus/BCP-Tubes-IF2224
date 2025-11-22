"""
Helper functions for statement builders
"""

def extract_identifier(parse_node):
    if parse_node.name.startswith("IDENTIFIER"):
        return parse_node.name.split("(")[1].rstrip(")")
    return "unknown"


def extract_keyword(parse_node):
    if parse_node.name.startswith("KEYWORD"):
        return parse_node.name.split("(")[1].rstrip(")")
    return "unknown"


def find_child_by_name(parse_node, name):
    for child in parse_node.children:
        if child.name == name:
            return child
    return None


def find_children_by_name(parse_node, name):
    return [child for child in parse_node.children if child.name == name]


def extract_expression_node(parse_node):
    """
    TODO: Implement proper expression builder
    """
    # For now, return the parse node itself
    # This should be replaced with actual expression AST node builder
    return parse_node
