from ..node import ParseNode

def parse_procedure_declaration(parser):
    procedure_declaration_node = ParseNode("<procedure-declaration>")

    parser.check_token("KEYWORD", "prosedur")
    procedure_declaration_node.add_child(ParseNode("KEYWORD(prosedur)"))

    identifier = parser.check_token("IDENTIFIER")
    procedure_declaration_node.add_child(ParseNode(f"IDENTIFIER({identifier[1]})"))

    current_token = parser.current_token()
    if current_token and current_token[0] == "LPAREN":
        formal_parameter_node = parser.declaration_parser.parse_formal_parameter_list()
        procedure_declaration_node.add_child(formal_parameter_node)
    
    parser.check_token("SEMICOLON")
    procedure_declaration_node.add_child(ParseNode("SEMICOLON(;)"))

    declaration_node = parser.declaration_parser.parse_declarations()
    procedure_declaration_node.add_child(declaration_node)

    statement_node = parser.statement_parser.parse_statement()
    procedure_declaration_node.add_child(statement_node)

    parser.check_token("SEMICOLON")
    procedure_declaration_node.add_child(ParseNode("SEMICOLON(;)"))

    return procedure_declaration_node
    


