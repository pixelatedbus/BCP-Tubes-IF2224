import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from node_class.declaration.function_decl_node import FunctionDeclNode
from .helpers import extract_parameters, extract_type


def build_function_declaration(parse_node):
    from .declaration_builder import build_declaration
    
    i = 0
    children = parse_node.children
    
    if children[i].name.startswith("KEYWORD"):
        i += 1
    
    func_name = "unknown"
    if children[i].name.startswith("IDENTIFIER"):
        func_name = children[i].name.split("(")[1].rstrip(")")
        i += 1
    
    parameters = []
    if i < len(children) and children[i].name == "<formal-parameter-list>":
        parameters = extract_parameters(children[i])
        i += 1
    
    if i < len(children) and children[i].name.startswith("COLON"):
        i += 1
    
    return_type = "unknown"
    if i < len(children) and children[i].name == "<type>":
        return_type = extract_type(children[i])
        i += 1
    
    if i < len(children) and children[i].name.startswith("SEMICOLON"):
        i += 1
    
    declarations = []
    if i < len(children) and children[i].name == "<declaration-part>":
        declarations = build_declaration(children[i])
        i += 1
    
    body = None
    if i < len(children) and children[i].name == "<compound-statement>":
        body = children[i]
        i += 1
    
    return FunctionDeclNode(func_name, parameters, return_type, declarations, body)
