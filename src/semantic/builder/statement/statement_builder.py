
from .assignment_builder import build_assignment_statement
from .if_builder import build_if_statement
from .for_builder import build_for_statement
from .while_builder import build_while_statement
from .compound_builder import build_compound_statement
from .statement_list_builder import build_statement_list
from .procedure_function_call_builder import build_procedure_function_call


def build_statement(parse_node):
    node_name = parse_node.name
    
    # Map node names to builder functions
    builders = {
        "<assignment-statement>": build_assignment_statement,
        "<if-statement>": build_if_statement,
        "<for_statement>": build_for_statement,
        "<while_statement>": build_while_statement,
        "<compound_statement>": build_compound_statement,
        "<statement-list>": build_statement_list,
        "<procedure/function-call>": build_procedure_function_call,
    }
    
    if node_name in builders:
        return builders[node_name](parse_node)
    
    if node_name.startswith("IDENTIFIER"):
        raise ValueError(f"Unexpected statement node: {node_name}")
    
    raise ValueError(f"Unknown statement type: {node_name}")
