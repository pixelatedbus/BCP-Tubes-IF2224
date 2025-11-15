from ..node import ParseNode

def parse_procedure_function_call(parser):
    call_node = ParseNode('<procedure/function-call>')

    token = parser.current_token()
    if token[0] == 'KEYWORD' and token[1] in ['prosedur', 'fungsi']:
        call_node.add_child(f'{token[0]}({token[1]})')
        parser.advance()
        token = parser.current_token()
    
    if token[0] == 'KEYWORD' and token[1] == 'LPAREN':
        call_node.add_child('LPAREN(()')
        parser.advance()
        token = parser.current_token()

    call_node.add_child(parser.declaration_parser.parse_parameter_list)


    if token[0] == 'KEYWORD' and token[1] == 'RPAREN':
        call_node.add_child('RPAREN())')
        parser.advance()
        token = parser.current_token()


    return call_node
    