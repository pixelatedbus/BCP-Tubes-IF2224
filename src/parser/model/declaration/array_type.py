from ..node import ParseNode

def parse_array_type(parser):
    array_type_node = ParseNode('<array_type>')
    
    token = parser.current_token()

    if token[0] == 'KEYWORD' and token[1] == 'larik':
        array_type_node.add_child(ParseNode('KEYWORD(larik)'))
        parser.advance()
        token = parser.current_token()
    if token[0] == 'LBRACKET' and token[1] == '[':
        array_type_node.add_child(ParseNode('LBRACKET([)'))
        parser.advance()
        token = parser.current_token()

    array_type_node.add_child(parser.declaration_parser.parse_range())
    token = parser.current_token()

    if token[0] == 'RBRACKET' and token[1] == ']':
        array_type_node.add_child(ParseNode('RBRACKET(])'))
        parser.advance()
        token = parser.current_token()
    if token[0] == 'KEYWORD' and token[1] == 'dari':
        array_type_node.add_child(ParseNode('KEYWORD(dari)'))
        parser.advance()
        token = parser.current_token()

    array_type_node.add_child(parser.declaration_parser.parse_type())        

    return array_type_node