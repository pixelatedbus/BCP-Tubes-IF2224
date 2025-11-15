from ..node import ParseNode

def parse_const_declaration(parser):
    const_decl_node = ParseNode("<const_declaration>")

    token = parser.current_token()
    if token and token[0] == "KEYWORD" and token[1] == "konstanta":
        const_keyword_node = ParseNode(f"KEYWORD({token[1]})")
        const_decl_node.add_child(const_keyword_node)
        parser.advance()
        
        token = parser.current_token()
        if token and token[0] == "IDENTIFIER":
            identifier_node = ParseNode(f"IDENTIFIER({token[1]})")
            const_decl_node.add_child(identifier_node)
            parser.advance()
            
            token = parser.current_token()
            # Konstanta menggunakan '=' yang merupakan RELATIONAL_OPERATOR
            if token and token[0] == "RELATIONAL_OPERATOR" and token[1] == "=":
                equal_node = ParseNode(f"RELATIONAL_OPERATOR({token[1]})")
                const_decl_node.add_child(equal_node)
                parser.advance()
                
                # Parse expression (bisa number, string, atau expression lainnya)
                expression_node = parser.expression_parser.parse_expression()
                const_decl_node.add_child(expression_node)
                
                # Check for semicolon
                token = parser.current_token()
                if token and token[0] == "SEMICOLON":
                    semicolon_node = ParseNode(f"SEMICOLON({token[1]})")
                    const_decl_node.add_child(semicolon_node)
                    parser.advance()
                    return const_decl_node
                else:
                    raise SyntaxError(f"Expected ';' after constant declaration, got {token}")
            else:
                raise SyntaxError(f"Expected '=' in constant declaration, got {token}")
        else:
            raise SyntaxError(f"Expected identifier in constant declaration, got {token}")
    else:
        raise SyntaxError(f"Expected 'konstanta' keyword, got {token}")