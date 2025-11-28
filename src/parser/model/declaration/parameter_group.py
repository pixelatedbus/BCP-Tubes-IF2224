from ..node import ParseNode

def parse_parameter_group(parser):
    """
    Parse a parameter group with optional 'var' keyword.
    Syntax: [var] <identifier_list> : <type>
    
    Examples:
        var a, b: integer  (pass by reference)
        x, y: real         (pass by value)
    """
    parameter_group_node = ParseNode("<parameter-group>")

    # Check for optional 'var' keyword (for pass-by-reference)
    token = parser.current_token()
    if token and token[0] == "KEYWORD" and token[1] == "var":
        parser.advance()  # Consume the 'var' keyword
        parameter_group_node.add_child(ParseNode("KEYWORD(var)"))

    identifier_list_node = parser.declaration_parser.parse_identifier_list()
    parameter_group_node.add_child(identifier_list_node)

    parser.check_token("COLON", ":")
    parameter_group_node.add_child(ParseNode("COLON(:)"))

    type_node = parser.declaration_parser.parse_type()
    parameter_group_node.add_child(type_node)

    return parameter_group_node