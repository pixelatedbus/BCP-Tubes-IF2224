from ..node import ParseNode

def parse_subprogram_declaration(parser):
    subprogram_declaration_node = ParseNode("<subprogram-declaration>")

    token = parser.current_token()

    if token[0] == 'KEYWORD' and token[1] == 'fungsi':
        function_declaration_node = parser.declaration_parser.parse_function_declaration()
        subprogram_declaration_node.add_child(function_declaration_node)
        return subprogram_declaration_node

    elif token[0] == 'KEYWORD' and token[1] == 'prosedur':
        procedure_declaration_node = parser.declaration_parser.parse_procedure_declaration()
        subprogram_declaration_node.add_child(procedure_declaration_node)
        return subprogram_declaration_node

    else:
        raise SyntaxError("Expected 'fungsi' or 'prosedur' keyword")