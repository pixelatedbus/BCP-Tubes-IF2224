from ..node import ParseNode

def parse_assignment_statement(parser):
    assignment_node = ParseNode("<assignment-statement>")

    identifier = parser.check_token("IDENTIFIER")
    assignment_node.add_child(ParseNode(f"IDENTIFIER({identifier[1]})"))

    token = parser.current_token()
    if token and token[0] == "LBRACKET":
        lbracket_node = ParseNode(f"LBRACKET({token[1]})")
        assignment_node.add_child(lbracket_node)
        parser.advance()
        
        index_expr = parser.expression_parser.parse_expression()
        assignment_node.add_child(index_expr)
        
        rbracket = parser.check_token("RBRACKET", "]")
        assignment_node.add_child(ParseNode(f"RBRACKET({rbracket[1]})"))

    assignment_operator = parser.check_token("ASSIGN_OPERATOR", ":=")
    assignment_node.add_child(ParseNode(f"ASSIGN_OPERATOR({assignment_operator[1]})"))

    expression_node = parser.expression_parser.parse_expression()
    assignment_node.add_child(expression_node)

    return assignment_node  