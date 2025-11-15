from ..node import ParseNode

def parse_procedure_function_call(parser):
    call_node = ParseNode('<procedure/function-call>')

    # Parse identifier (procedure/function name)
    token = parser.current_token()
    if token and token[0] == 'IDENTIFIER':
        identifier_node = ParseNode(f'IDENTIFIER({token[1]})')
        call_node.add_child(identifier_node)
        parser.advance()
    else:
        raise SyntaxError(f"Expected identifier in procedure/function call, got {token}")
    
    # Parse LPAREN
    token = parser.current_token()
    if token and token[0] == 'LPAREN':
        lparen_node = ParseNode('LPAREN(()')
        call_node.add_child(lparen_node)
        parser.advance()
    else:
        raise SyntaxError(f"Expected '(' in procedure/function call, got {token}")

    # Parse parameter list (actual parameters)
    parameter_list_node = parser.statement_parser.parse_parameter_list()
    call_node.add_child(parameter_list_node)

    # Parse RPAREN
    token = parser.current_token()
    if token and token[0] == 'RPAREN':
        rparen_node = ParseNode('RPAREN())')
        call_node.add_child(rparen_node)
        parser.advance()
    else:
        raise SyntaxError(f"Expected ')' in procedure/function call, got {token}")

    return call_node
    