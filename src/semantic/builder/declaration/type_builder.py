import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from node_class.declaration.type_decl_node import TypeDeclNode
from .helpers import extract_type_spec


def build_type_declaration(parse_node):
    i = 0
    children = parse_node.children
    
    if children[i].name.startswith("KEYWORD"):
        i += 1
    
    type_name = "unknown"
    if i < len(children) and children[i].name.startswith("IDENTIFIER"):
        type_name = children[i].name.split("(")[1].rstrip(")")
        i += 1
    
    if i < len(children) and children[i].name.startswith("RELATIONAL_OPERATOR"):
        i += 1
    
    type_spec = "unknown"
    if i < len(children) and children[i].name.startswith("<"):
        type_spec = extract_type_spec(children[i])
        i += 1
    
    return TypeDeclNode(type_name, type_spec)
