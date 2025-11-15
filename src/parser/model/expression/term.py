from ..node import ParseNode

def parse_term(parser):
    term_node = ParseNode("<term>")
    
    factor_node = parser.expression_parser.parse_factor()
    term_node.add_child(factor_node)
    
    while parser.current_token():
        token = parser.current_token()
        
        if token[0] == "ARITHMETIC_OPERATOR" and token[1] in ["*", "/", "bagi", "mod"]:
            multiplicative_op_node = parser.expression_parser.multiplicative_operator()
            term_node.add_child(multiplicative_op_node)
            
            factor_node = parser.expression_parser.parse_factor()
            term_node.add_child(factor_node)
        elif token[0] == "LOGICAL_OPERATOR" and token[1] == "dan":
            multiplicative_op_node = parser.expression_parser.multiplicative_operator()
            term_node.add_child(multiplicative_op_node)
            
            factor_node = parser.expression_parser.parse_factor()
            term_node.add_child(factor_node)
        else:
            raise SyntaxError(f"Unexpected token in term: {token}")
    
    return term_node