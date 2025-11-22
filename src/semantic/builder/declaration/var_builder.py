import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from node_class.declaration.var_decl_node import VarDeclNode
from .helpers import extract_identifier_list, extract_type


def build_var_declaration(parse_node):
    var_nodes = []
    i = 0
    children = parse_node.children
    
    if children[i].name.startswith("KEYWORD"):
        i += 1
    
    identifiers = []
    if i < len(children) and children[i].name == "<identifier_list>":
        identifiers = extract_identifier_list(children[i])
        i += 1
    
    if i < len(children) and children[i].name.startswith("COLON"):
        i += 1
    
    var_type = "unknown"
    if i < len(children) and children[i].name == "<type>":
        var_type = extract_type(children[i])
        i += 1
    
    for identifier in identifiers:
        var_node = VarDeclNode(identifier, var_type)
        var_nodes.append(var_node)
    
    return var_nodes
