from ..node import ParseNode

def parse_if_statement(parser):
    if_statement_node = ParseNode("<if-statement>")

    parser.check_token("KEYWORD", "jika")
    if_statement_node.add_child(ParseNode("KEYWORD(jika)"))

    expression_node = parser.expression_parser.parse_expression()
    if_statement_node.add_child(expression_node)

    parser.check_token("KEYWORD", "maka")
    if_statement_node.add_child(ParseNode("KEYWORD(maka)"))

    statement_node = parser.statement_parser.parse_statement()
    if_statement_node.add_child(statement_node)

    token = parser.current_token()
    if token and token[0] == "KEYWORD" and token[1] == "selain-itu":
        parser.check_token("KEYWORD", "selain-itu")
        if_statement_node.add_child(ParseNode("KEYWORD(selain-itu)"))

        else_statement_node = parser.statement_parser.parse_statement()
        if_statement_node.add_child(else_statement_node)

    return if_statement_node