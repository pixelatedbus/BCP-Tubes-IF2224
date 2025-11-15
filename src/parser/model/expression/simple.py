from ..node import ParseNode

def parse_simple_expression(parser):
    simple_expr_node = ParseNode("<simple_expression>")
    
    token = parser.current_token()
    if token and token[0] == "ARITHMETIC_OPERATOR" and token[1] in ["+", "-"]:
        sign_token = token
        parser.advance()
        simple_expr_node.add_child(ParseNode(f"ARITHMETIC_OPERATOR({sign_token[1]})"))
    
    term_node = parser.expression_parser.parse_term(parser)
    simple_expr_node.add_child(term_node)
    
    while parser.current_token():
        token = parser.current_token()
        
        if token[0] == "ARITHMETIC_OPERATOR" and token[1] in ["+", "-"]:
            op_token = token
            parser.advance()
            simple_expr_node.add_child(ParseNode(f"ARITHMETIC_OPERATOR({op_token[1]})"))
            
            term_node = parser.expression_parser.parse_term(parser)
            simple_expr_node.add_child(term_node)
        elif token[0] == "LOGICAL_OPERATOR" and token[1] == "atau":
            op_token = token
            parser.advance()
            simple_expr_node.add_child(ParseNode(f"ARITHMETIC_OPERATOR({op_token[1]})")) # Gak konsisten, tapi biar sama kaya di grammar
            
            term_node = parser.expression_parser.parse_term(parser)
            simple_expr_node.add_child(term_node)
        else:
            break
    
    return simple_expr_node