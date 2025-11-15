from ..node import ParseNode


def parse_while_statement(parser):
    while_node = ParseNode("<while_statement>")
    
    token = parser.current_token()
    if token and token[0] == "KEYWORD" and token[1] == "selama":
        selama_node = ParseNode(f"KEYWORD({token[1]})")
        while_node.add_child(selama_node)
        parser.advance()
    else:
        raise SyntaxError(f"Expected 'selama' keyword, got {token}")
    
    expression_node = parser.expression_parser.parse_expression()
    while_node.add_child(expression_node)
    
    token = parser.current_token()
    if token and token[0] == "KEYWORD" and token[1] == "lakukan":
        lakukan_node = ParseNode(f"KEYWORD({token[1]})")
        while_node.add_child(lakukan_node)
        parser.advance()
    else:
        raise SyntaxError(f"Expected 'lakukan' keyword, got {token}")
    
    statement_node = parser.statement_parser.parse_statement()
    while_node.add_child(statement_node)
    
    return while_node