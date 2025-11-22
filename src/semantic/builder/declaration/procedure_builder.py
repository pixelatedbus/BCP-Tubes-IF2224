import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from node_class.declaration.procedure_decl_node import ProcedureDeclNode
from .helpers import extract_parameters


def build_procedure_declaration(parse_node):
    from .declaration_builder import build_declaration_part
    
    i = 0
    children = parse_node.children
    
    if children[i].name.startswith("KEYWORD"):
        i += 1
    
    proc_name = "unknown"
    if children[i].name.startswith("IDENTIFIER"):
        proc_name = children[i].name.split("(")[1].rstrip(")")
        i += 1
    
    parameters = []
    if i < len(children) and children[i].name == "<formal-parameter-list>":
        parameters = extract_parameters(children[i])
        i += 1
    
    if i < len(children) and children[i].name.startswith("SEMICOLON"):
        i += 1
    
    declarations = []
    if i < len(children) and children[i].name == "<declaration-part>":
        declarations = build_declaration_part(children[i])
        i += 1
    
    body = None
    if i < len(children) and children[i].name == "<compound-statement>":
        body = children[i]
        i += 1
    
    return ProcedureDeclNode(proc_name, parameters, declarations, body)
