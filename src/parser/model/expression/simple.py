from ..node import ParseNode

def parse_simple_expression(parser):
    simple_expr_node = ParseNode("<simple_expression>")
    
    token = parser.current_token()
    if token and token[0] == "ARITHMETIC_OPERATOR" and token[1] in ["+", "-"]:
        additive_operator_node = parser.expression_parser.additive_operator()
        simple_expr_node.add_child(additive_operator_node)
    
    term_node = parser.expression_parser.parse_term()
    simple_expr_node.add_child(term_node)
    
    while parser.current_token():
        token = parser.current_token()
        
        if token[0] == "ARITHMETIC_OPERATOR" and token[1] in ["+", "-"]:
            second_additive_node = parser.expression_parser.additive_operator()
            simple_expr_node.add_child(second_additive_node)
            
            term_node = parser.expression_parser.parse_term()
            simple_expr_node.add_child(term_node)
        elif token[0] == "LOGICAL_OPERATOR" and token[1] == "atau":
            second_additive_node = parser.expression_parser.additive_operator()
            simple_expr_node.add_child(second_additive_node)
            
            term_node = parser.expression_parser.parse_term()
            simple_expr_node.add_child(term_node)
        else:
            raise SyntaxError("Unexpected token in simple expression")
    
    return simple_expr_node