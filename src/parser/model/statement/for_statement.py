from ..node import ParseNode


def parse_for_statement(parser):
    for_node = ParseNode("<for_statement>")
    
    token = parser.current_token()
    if token and token[0] == "KEYWORD" and token[1] == "untuk":
        untuk_node = ParseNode(f"KEYWORD({token[1]})")
        for_node.add_child(untuk_node)
        parser.advance()
    else:
        raise SyntaxError(f"Expected 'untuk' keyword, got {token}")
    
    token = parser.current_token()
    if token and token[0] == "IDENTIFIER":
        identifier_node = ParseNode(f"IDENTIFIER({token[1]})")
        for_node.add_child(identifier_node)
        parser.advance()
    else:
        raise SyntaxError(f"Expected identifier in for statement, got {token}")
    
    token = parser.current_token()
    if token and token[0] == "ASSIGN_OPERATOR" and token[1] == ":=":
        assign_node = ParseNode(f"ASSIGN_OPERATOR({token[1]})")
        for_node.add_child(assign_node)
        parser.advance()
    else:
        raise SyntaxError(f"Expected ':=' in for statement, got {token}")
    
    start_expr = parser.expression_parser.parse_expression()
    for_node.add_child(start_expr)
    
    token = parser.current_token()
    if token and token[0] == "KEYWORD" and token[1] in ["ke", "turun-ke"]:
        direction_node = ParseNode(f"KEYWORD({token[1]})")
        for_node.add_child(direction_node)
        parser.advance()
    else:
        raise SyntaxError(f"Expected 'ke' or 'turun-ke' in for statement, got {token}")
    
    end_expr = parser.expression_parser.parse_expression()
    for_node.add_child(end_expr)
    
    token = parser.current_token()
    if token and token[0] == "KEYWORD" and token[1] == "lakukan":
        lakukan_node = ParseNode(f"KEYWORD({token[1]})")
        for_node.add_child(lakukan_node)
        parser.advance()
    else:
        raise SyntaxError(f"Expected 'lakukan' keyword in for statement, got {token}")
    
    statement_node = parser.statement_parser.parse_statement()
    for_node.add_child(statement_node)
    
    return for_node