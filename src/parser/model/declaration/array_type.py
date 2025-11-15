from ..node import ParseNode
from range import parse_range
from type import parse_type

def parse_type(parser):
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

    array_type_node.add_child(parse_range(parser))
    token = parser.current_token()

    if token[0] == 'RBRACKET' and token[1] == ']':
        array_type_node.add_child(ParseNode('RBRACKET(])'))
        parser.advance()
        token = parser.current_token()
    if token[0] == 'KEYWORD' and token[1] == 'dari':
        array_type_node.add_child(ParseNode('KEYWORD(dari)'))
        parser.advance()
        token = parser.current_token()

    array_type_node.add_child(parse_type(parser))        

    return array_type_node