from ..node import ParseNode

def parse_range(parser):
    range_node = ParseNode('<range>')

    expression_node = parser.expression_parser.parse_expression()

    range_node.add_child(expression_node)

    token = parser.current_token()

    if token[0] == 'RANGE_OPERATOR' and token[1] == '..':
        range_node.add_child(ParseNode('RANGE_OPERATOR(..)'))
        parser.advance()
    
    expression_node = parser.expression_parser.parse_expression()

    range_node.add_child(expression_node)

    return range_node