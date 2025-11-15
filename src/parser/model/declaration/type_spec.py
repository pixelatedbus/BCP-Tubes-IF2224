from ..node import ParseNode


def parse_type_spec(parser):
    """
    Parse type specification (definisi tipe)
    Examples:
        - integer
        - real
        - 1..10 (range)
    """
    token = parser.current_token()
    
    if not token:
        raise SyntaxError("Expected type specification, got end of input")
    
    if token[0] == "KEYWORD" and token[1] in ["integer", "real", "boolean", "char"]:
        return parse_simple_type(parser)
    
    if token[0] == "NUMBER":
        return parse_range_type(parser)
    
    raise SyntaxError(f"Unexpected token in type specification: {token}")


def parse_simple_type(parser):
    """
    Parse simple type: integer, real, boolean, char
    """
    type_node = ParseNode("<simple_type>")
    
    token = parser.current_token()
    if token and token[0] == "KEYWORD" and token[1] in ["integer", "real", "boolean", "char"]:
        keyword_node = ParseNode(f"KEYWORD({token[1]})")
        type_node.add_child(keyword_node)
        parser.advance()
        return type_node
    
    raise SyntaxError(f"Expected simple type, got {token}")


def parse_range_type(parser):
    """
    Parse range type: expression .. expression
    
    Example:
        1..10
        0..99
    """
    range_node = ParseNode("<range_type>")
    
    start_expr = parser.expression_parser.parse_expression()
    range_node.add_child(start_expr)
    
    token = parser.current_token()
    # Masih ga pasti apa pake double DOT atau RANGE_OPERATOR
    if token and token[0] == "DOT":
        parser.advance()
        token = parser.current_token()
        if token and token[0] == "DOT":
            range_node.add_child(ParseNode("RANGE(..)"))
            parser.advance()
            
            end_expr = parser.expression_parser.parse_expression()
            range_node.add_child(end_expr)
            
            return range_node
        else:
            raise SyntaxError(f"Expected '..' in range type, got single '.'")
    else:
        raise SyntaxError(f"Expected '..' in range type, got {token}")
