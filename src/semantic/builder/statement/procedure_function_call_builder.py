import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from node_class.statement.procedure_function_call_node import procedureFunctionCallNode
from .helpers import extract_identifier, extract_expression_node


def build_procedure_function_call(parse_node):
    if parse_node.name != "<procedure/function-call>":
        raise ValueError(f"Expected <procedure/function-call>, got {parse_node.name}")
    
    function_name = "unknown"
    arguments = []
    
    i = 0
    children = parse_node.children
    
    if i < len(children) and children[i].name.startswith("IDENTIFIER"):
        function_name = extract_identifier(children[i])
        i += 1
    
    # Skip LPAREN
    if i < len(children) and children[i].name.startswith("LPAREN"):
        i += 1
    
    # Get parameter list
    if i < len(children) and children[i].name == "<parameter_list>":
        param_list_node = children[i]
        for param_child in param_list_node.children:
            if param_child.name == "<expression>":
                # TODO: Replace with actual expression builder
                arguments.append(extract_expression_node(param_child))
        i += 1
        
    return procedureFunctionCallNode(function_name, arguments)
