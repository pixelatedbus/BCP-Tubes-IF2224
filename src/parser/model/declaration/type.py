from ..node import ParseNode

def parse_type(parser):
    type_node = ParseNode('<type>')
    
    token = parser.current_token()

    # Handle basic types (integer, real, boolean, char)
    if token[0] == 'KEYWORD' and token[1] in ['integer', 'real', 'boolean', 'char']:
        child_node = ParseNode(f'{token[0]}({token[1]})')
        type_node.add_child(child_node)
        parser.advance()
        return type_node
    
    # Handle type identifiers (user-defined types)
    elif token[0] == 'IDENTIFIER':
        child_node = ParseNode(f'{token[0]}({token[1]})')
        type_node.add_child(child_node)
        parser.advance()
        return type_node
    
    # Handle array types (larik[...] dari ...)
    elif token[0] == 'KEYWORD' and token[1] == 'larik':
        array_type_node = parser.declaration_parser.parse_array_type()
        type_node.add_child(array_type_node)
        return type_node
    
    else:
        raise SyntaxError(f"Expected type, got {token}")