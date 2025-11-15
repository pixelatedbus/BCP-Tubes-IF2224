from ..node import ParseNode

def parse_function_declaration(parser):
    function_declaration_node = ParseNode("<function-declaration>")

    parser.check_token("KEYWORD", "fungsi")
    function_declaration_node.add_child(ParseNode("KEYWORD(fungsi)"))

    identifier = parser.check_token("IDENTIFIER")
    function_declaration_node.add_child(ParseNode(f"IDENTIFIER({identifier[1]})"))

    current_token = parser.current_token()
    if current_token and current_token[0] == "LPAREN":
        formal_parameter_node = parser.declaration_parser.parse_formal_parameter_list()
        function_declaration_node.add_child(formal_parameter_node)

    parser.check_token("COLON")
    function_declaration_node.add_child(ParseNode("COLON(:)"))

    type_node = parser.declaration_parser.parse_type()
    function_declaration_node.add_child(type_node)
    
    parser.check_token("SEMICOLON")
    function_declaration_node.add_child(ParseNode("SEMICOLON(;)"))

    declaration_node = parser.declaration_parser.parse_declarations()
    function_declaration_node.add_child(declaration_node)

    statement_node = parser.statement_parser.parse_statement()
    function_declaration_node.add_child(statement_node)

    parser.check_token("SEMICOLON")
    function_declaration_node.add_child(ParseNode("SEMICOLON(;)"))

    return function_declaration_node
    


