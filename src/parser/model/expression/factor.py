from ..node import ParseNode

def parse_factor(parser):
    factor_node = ParseNode("<factor>")

    token = parser.current_token()
    if token is None:
        raise SyntaxError("Unexpected end of input while parsing factor")
    
    token_type, token_value = token

    if token_type == "IDENTIFIER":
        if parser.position + 1 < len(parser.tokens):
            next_token_type, _ = parser.tokens[parser.position + 1]
            if next_token_type == "LPAREN":
                function_call_node = parser.statement_parser.parse_function_call()
                factor_node.add_child(function_call_node)
                return factor_node

    if token_type in ["IDENTIFIER", "NUMBER", "CHAR_LITERAL", "STRING_LITERAL"]:
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

        

    

    