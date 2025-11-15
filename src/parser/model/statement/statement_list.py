from ..node import ParseNode

def parse_statement(parser):
    token = parser.current_token()
    token_type, token_value = token

    if token_type == "IDENTIFIER":
        next_token = parser.peek()

        if next_token and next_token[0] == "LPAREN":
            return parser.statement_parser.parse_function_call()
        
        return parser.statement_parser.parse_assignment_statement()
    
    if token_type == "KEYWORD" and token_value == "jika":
        return parser.statement_parser.parse_if_statement()
    
    if token_type == "KEYWORD" and token_value == "selama":
        return parser.statement_parser.parse_while_statement()
    
    if token_type == "KEYWORD" and token_value == "untuk":
        return parser.statement_parser.parse_for_statement()

def parse_statement_list(parser):
    statement_list_node = ParseNode("<statement-list>")

    first_statement = parse_statement(parser, statement_list_node)
    statement_list_node.add_child(first_statement)

    while parser.current_token() and parser.current_token()[0] == "SEMICOLON":
        parser.check_token("SEMICOLON")
        statement_list_node.add_child(ParseNode("SEMICOLON(;)"))

        next_statement = parse_statement(parser, statement_list_node)
        statement_list_node.add_child(next_statement)

    return statement_list_node







