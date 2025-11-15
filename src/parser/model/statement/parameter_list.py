from ..node import ParseNode

def parse_parameter_list(parser):
    param_list_node = ParseNode('<parameter_list>')

    expression_node = parser.expression_parser.parse_expression()
    param_list_node.add_child(expression_node)
    
    token = parser.current_token()

    while token[0] == 'COMMA':
        param_list_node.add_child(ParseNode('COMMA(,)'))
        
        parser.advance()
        token = parser.current_token()

        expression_node = parser.expression_parser.parse_expression()
        param_list_node.add_child(expression_node)
        
        parser.advance()
        token = parser.current_token()

    return param_list_node