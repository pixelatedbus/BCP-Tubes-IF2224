from ..node import ParseNode

def parse_factor(parser):
    factor_node = ParseNode("<factor>")

    token = parser.current_token()
    if token is None:
        raise SyntaxError("Unexpected end of input while parsing factor")
    
    token_type, token_value = token

    if token_type == "IDENTIFIER":
        parser.advance()
        factor_node.add_child(ParseNode(f"IDENTIFIER({token_value})"))
        
        # Check for function call, array index, or record field access
        while True:
            next_token = parser.current_token()
            if not next_token:
                break
                
            if next_token[0] == "LPAREN":
                # Function call
                parser.advance()
                factor_node.add_child(ParseNode("LPAREN(()"))
                param_list = parser.statement_parser.parse_parameter_list()
                factor_node.add_child(param_list)
                parser.check_token("RPAREN")
                factor_node.add_child(ParseNode("RPAREN())"))
            elif next_token[0] == "LBRACKET":
                # Array indexing
                parser.advance()
                factor_node.add_child(ParseNode("LBRACKET([)"))
                index_expr = parser.expression_parser.parse_expression()
                factor_node.add_child(index_expr)
                parser.check_token("RBRACKET")
                factor_node.add_child(ParseNode("RBRACKET(]))"))
            else:
                break
                
        return factor_node
    
    if token_type in ["NUMBER", "CHAR_LITERAL", "STRING_LITERAL"]:
        parser.check_token(token_type)
        factor_node.add_child(ParseNode(f"{token_type}({token_value})"))
        return factor_node
    
    if token_type == "LPAREN":
        parser.check_token("LPAREN", "(")
        factor_node.add_child(ParseNode("LPAREN(()"))   
        expression_node = parser.expression_parser.parse_expression()
        factor_node.add_child(expression_node)
        parser.check_token("RPAREN", ")")
        factor_node.add_child(ParseNode("RPAREN())"))
        return factor_node
    
    if token_type == "LOGICAL_OPERATOR" and token_value == "tidak":
        parser.check_token("LOGICAL_OPERATOR", "tidak")
        factor_node.add_child(ParseNode("LOGICAL_OPERATOR(tidak)"))
        inner_factor_node = parse_factor(parser)
        factor_node.add_child(inner_factor_node)
        return factor_node