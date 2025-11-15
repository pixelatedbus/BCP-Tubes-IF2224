from ..node import ParseNode

def parse_term(parser):
    term_node = ParseNode("<term>")
    
    factor_node = parser.expression_parser.parser_factor(parser)
    term_node.add_child(factor_node)
    
    while parser.current_token():
        token = parser.current_token()
        
        if token[0] == "ARITHMETIC_OPERATOR" and token[1] in ["*", "/", "bagi", "mod"]:
            op_token = token
            parser.advance()
            term_node.add_child(ParseNode(f"MULTIPLICATIVE_OPERATOR({op_token[1]})"))
            
            factor_node = parser.expression_parser.parser_factor(parser)
            term_node.add_child(factor_node)
        elif token[0] == "LOGICAL_OPERATOR" and token[1] == "dan":
            op_token = token
            parser.advance()
            term_node.add_child(ParseNode(f"MULTIPLICATIVE_OPERATOR({op_token[1]})"))
            
            factor_node = parser.expression_parser.parser_factor(parser)
            term_node.add_child(factor_node)
        else:
            break
    
    return term_node