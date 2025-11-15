from ..node import ParseNode

def parse_formal_parameter_list(parser):
    formal_parameter_list_node = ParseNode("<formal-parameter-list>")

    parser.check_token("LPAREN")
    formal_parameter_list_node.add_child(ParseNode("LPAREN(()"))

    parameter_group_node = parser.declaration_parser.parse_parameter_group()
    formal_parameter_list_node.add_child(parameter_group_node)

    while parser.current_token() and parser.current_token()[0] == "SEMICOLON":
        parser.check_token("SEMICOLON")
        formal_parameter_list_node.add_child(ParseNode("SEMICOLON(;)"))

        parameter_group_node = parser.declaration_parser.parse_parameter_group()
        formal_parameter_list_node.add_child(parameter_group_node)

    parser.check_token("RPAREN")
    formal_parameter_list_node.add_child(ParseNode("RPAREN())"))

    return formal_parameter_list_node
