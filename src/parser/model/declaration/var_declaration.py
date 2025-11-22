from ..node import ParseNode

def parse_var_declaration(parser, skip_keyword=False):
    var_decl_node = ParseNode("<var_declaration>")

    if not skip_keyword:
        token = parser.current_token()
        if token and token[0] == "KEYWORD" and token[1] == "variabel":
            var_keyword_node = ParseNode(f"KEYWORD({token[1]})")
            var_decl_node.add_child(var_keyword_node)
            parser.advance()
        else:
            raise SyntaxError(f"Expected 'variabel' keyword, got {token}")
    
    # Parse single variable declaration
    token = parser.current_token()
    if token and token[0] == "IDENTIFIER":
        identifier_list_node = parser.declaration_parser.parse_identifier_list()
        var_decl_node.add_child(identifier_list_node)
        
        token = parser.current_token()
        if token and token[0] == "COLON":
            colon_node = ParseNode(f"COLON({token[1]})")
            var_decl_node.add_child(colon_node)
            parser.advance()
            
            type_node = parser.declaration_parser.parse_type()
            var_decl_node.add_child(type_node)

            token = parser.current_token()
            if token and token[0] == "SEMICOLON":
                semicolon_node = ParseNode(f"SEMICOLON({token[1]})")
                var_decl_node.add_child(semicolon_node)
                parser.advance()
            else:
                raise SyntaxError(f"Expected ';' after variable declaration, got {token}")
        else:
            raise SyntaxError(f"Expected ':' in variable declaration, got {token}")
    else:
        raise SyntaxError(f"Expected identifier in variable declaration, got {token}")
            
    return var_decl_node