from ..node import ParseNode

def parse_identifier_list(parser):
    identifier_list_node = ParseNode("<identifier_list>")
    
    token = parser.current_token()
    if token and token[0] == "IDENTIFIER":
        identifier_node = ParseNode(f"IDENTIFIER({token[1]})")
        identifier_list_node.add_child(identifier_node)
        parser.advance()
    else:
        raise SyntaxError(f"Expected identifier, got {token}")
    
    while parser.current_token():
        token = parser.current_token()
        
        if token and token[0] == "COMMA":
            comma_node = ParseNode(f"COMMA({token[1]})")
            identifier_list_node.add_child(comma_node)
            parser.advance()
            
            token = parser.current_token()
            if token and token[0] == "IDENTIFIER":
                identifier_node = ParseNode(f"IDENTIFIER({token[1]})")
                identifier_list_node.add_child(identifier_node)
                parser.advance()
            else:
                raise SyntaxError(f"Expected identifier after ',', got {token}")
        else:
            break
    
    return identifier_list_node
