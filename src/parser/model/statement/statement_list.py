from ..node import ParseNode

def parse_statement_list(parser):
    statement_list_node = ParseNode("<statement-list>")

    first_statement = parser.statement_parser.parse_single_statement()
    statement_list_node.add_child(first_statement)

    while parser.current_token() and parser.current_token()[0] == "SEMICOLON":
        parser.check_token("SEMICOLON")
        statement_list_node.add_child(ParseNode("SEMICOLON(;)"))

        # Check if next token is 'selesai' (end of compound statement)
        token = parser.current_token()
        if token and token[0] == "KEYWORD" and token[1] == "selesai":
            break

        next_statement = parser.statement_parser.parse_single_statement()
        statement_list_node.add_child(next_statement)

    return statement_list_node







