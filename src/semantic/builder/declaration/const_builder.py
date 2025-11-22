import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from node_class.declaration.const_decl_node import ConstDeclNode
from .helpers import extract_simple_value


def build_const_declaration(parse_node):
    i = 0
    children = parse_node.children
    
    if children[i].name.startswith("KEYWORD"):
        i += 1
    
    const_name = "unknown"
    if i < len(children) and children[i].name.startswith("IDENTIFIER"):
        const_name = children[i].name.split("(")[1].rstrip(")")
        i += 1
    
    if i < len(children) and children[i].name.startswith("RELATIONAL_OPERATOR"):
        i += 1
    
    expression_value = None
    if i < len(children) and children[i].name == "<expression>":
        expression_value = extract_simple_value(children[i])
        i += 1
    
    return ConstDeclNode(const_name, expression_value)
