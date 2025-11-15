from ..node import ParseNode

def parse_type(parser):
    type_node = ParseNode('<type>')
    
    token = parser.current_token()

    if token[0] == 'KEYWORD' and token[1] in ['integer', 'real', 'boolean', 'char']:
        child_node = ParseNode(f'{token[0]}({token[1]})')

        type_node.add_child(child_node)
        parser.advance()
        return type_node