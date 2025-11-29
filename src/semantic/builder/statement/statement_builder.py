import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from node_class.statement.assignment_statement_node import AssignmentStatementNode
from node_class.statement.if_statement import IfStatementNode
from node_class.statement.for_statement_node import ForStatementNode
from node_class.statement.while_statement_node import WhileStatementNode
from node_class.statement.procedure_function_call_node import procedureFunctionCallNode
from node_class.statement.statement_list_node import StatementListNode
from node_class.misc.block_node import BlockNode
from .helpers import extract_identifier, extract_keyword
from ..expression.expression_builder import build_expression
from ...node_class.expression.array_access_node import ArrayAccessNode
from ...node_class.expression.field_access_node import FieldAccessNode
from ...node_class.expression.identifier_node import IdentifierNode


def build_assignment_statement(parse_node):
    if parse_node.name != "<assignment-statement>":
        raise ValueError(f"Expected <assignment-statement>, got {parse_node.name}")
    
    # Build left-hand side (can be identifier, array access, or field access)
    lhs = None
    expression_node = None
    
    i = 0
    children = parse_node.children
    
    # Get base identifier
    if i < len(children) and children[i].name.startswith("IDENTIFIER"):
        identifier = extract_identifier(children[i])
        lhs = IdentifierNode(identifier)
        i += 1
        
        # Process array indexing and/or field access
        while i < len(children) and not children[i].name.startswith("ASSIGN_OPERATOR"):
            if children[i].name.startswith("LBRACKET"):
                # Array access
                i += 1
                if i < len(children) and children[i].name == "<expression>":
                    index = build_expression(children[i])
                    # Use current lhs (could be identifier string or node) as base
                    if isinstance(lhs, IdentifierNode):
                        lhs = ArrayAccessNode(lhs.name, index)
                    else:
                        lhs = ArrayAccessNode(lhs, index)
                    i += 1
                # Skip RBRACKET
                if i < len(children) and children[i].name.startswith("RBRACKET"):
                    i += 1
            elif children[i].name.startswith("DOT"):
                # Field access
                i += 1
                if i < len(children) and children[i].name.startswith("IDENTIFIER"):
                    field_name = extract_identifier(children[i])
                    lhs = FieldAccessNode(lhs, field_name)
                    i += 1
            else:
                i += 1
    
    # Skip ASSIGN_OPERATOR and get right-hand side expression
    while i < len(children):
        if children[i].name == "<expression>":
            expression_node = build_expression(children[i])
            break
        i += 1
    
    # Create assignment node with LHS node
    # For backward compatibility, extract variable name from LHS
    if isinstance(lhs, IdentifierNode):
        variable_name = lhs.name
    elif isinstance(lhs, ArrayAccessNode):
        # Extract base array name
        if isinstance(lhs.array_name, str):
            variable_name = lhs.array_name
        elif isinstance(lhs.array_name, IdentifierNode):
            variable_name = lhs.array_name.name
        else:
            variable_name = str(lhs.array_name)
    elif isinstance(lhs, FieldAccessNode):
        # Extract base record name
        if isinstance(lhs.record_expr, IdentifierNode):
            variable_name = lhs.record_expr.name
        elif isinstance(lhs.record_expr, str):
            variable_name = lhs.record_expr
        else:
            variable_name = str(lhs.record_expr)
    else:
        variable_name = "unknown"
    
    # Create assignment node - store both variable_name and lhs_node
    assignment_node = AssignmentStatementNode(variable_name, expression_node)
    assignment_node.lhs_node = lhs  # Store the full LHS access node
    return assignment_node


def build_if_statement(parse_node):
    if parse_node.name != "<if-statement>":
        raise ValueError(f"Expected <if-statement>, got {parse_node.name}")
    
    condition = None
    then_body = None
    else_body = None
    
    i = 0
    children = parse_node.children
    
    # Skip 'jika' 
    if i < len(children) and children[i].name.startswith("KEYWORD"):
        i += 1
    
    if i < len(children) and children[i].name == "<expression>":
        condition = build_expression(children[i])
        i += 1
    
    # Skip 'maka' 
    if i < len(children) and children[i].name.startswith("KEYWORD"):
        i += 1
    
    if i < len(children) and (children[i].name.startswith("<") or children[i].name.startswith("IDENTIFIER")):
        then_body = build_statement(children[i])
        i += 1
    
    if i < len(children) and children[i].name.startswith("KEYWORD") and "selain_itu" in children[i].name:
        i += 1
        if i < len(children):
            else_body = build_statement(children[i])
    
    return IfStatementNode(condition, then_body, else_body)


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
        start_expr = build_expression(children[i])
        i += 1
    
    if i < len(children) and children[i].name.startswith("KEYWORD"):
        direction = extract_keyword(children[i])
        i += 1
    
    if i < len(children) and children[i].name == "<expression>":
        end_expr = build_expression(children[i])
        i += 1
    
    # Skip 'lakukan' 
    if i < len(children) and children[i].name.startswith("KEYWORD"):
        i += 1
    
    if i < len(children):
        body = build_statement(children[i])
    
    return ForStatementNode(variable, start_expr, end_expr, body)


def build_while_statement(parse_node):
    if parse_node.name != "<while_statement>":
        raise ValueError(f"Expected <while_statement>, got {parse_node.name}")
    
    condition = None
    body = None
    
    i = 0
    children = parse_node.children
    
    # Skip 'selama' 
    if i < len(children) and children[i].name.startswith("KEYWORD"):
        i += 1
    
    if i < len(children) and children[i].name == "<expression>":
        condition = build_expression(children[i])
        i += 1
    
    # Skip 'lakukan' 
    if i < len(children) and children[i].name.startswith("KEYWORD"):
        i += 1
    
    if i < len(children):
        body = build_statement(children[i])
    
    return WhileStatementNode(condition, body)


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
                arguments.append(build_expression(param_child))
        i += 1
        
    return procedureFunctionCallNode(function_name, arguments)


def build_compound_statement(parse_node):
    if parse_node.name != "<compound-statement>":
        raise ValueError(f"Expected <compound-statement>, got {parse_node.name}")
    
    block_node = BlockNode()
    
    for child in parse_node.children:
        if child.name == "<statement-list>":
            statements = build_statements(child)
            for stmt in statements:
                block_node.add_child(stmt)
            break
    
    return block_node


def build_statement(parse_node):
    node_name = parse_node.name
    
    builders = {
        "<assignment-statement>": build_assignment_statement,
        "<if-statement>": build_if_statement,
        "<for_statement>": build_for_statement,
        "<while_statement>": build_while_statement,
        "<compound-statement>": build_compound_statement,
        "<procedure/function-call>": build_procedure_function_call,
    }
    
    if node_name in builders:
        return builders[node_name](parse_node)
    
    if node_name.startswith("IDENTIFIER"):
        return build_procedure_function_call(parse_node)
    
    raise ValueError(f"Unknown statement type: {node_name}")


def build_statements(parse_node):
    all_statements = []
    
    for child in parse_node.children:
        if child.name.startswith("KEYWORD") or child.name.startswith("SEMICOLON"):
            continue
        
        if child.name.startswith("<") or child.name.startswith("IDENTIFIER"):
            all_statements.append(build_statement(child))
    
    return all_statements