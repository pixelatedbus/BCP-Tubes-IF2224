"""Type specification parsing untuk Pascal Indonesia

Ini adalah definisi tipe itu sendiri (bukan deklarasi tipe)

Grammar:
    type_spec -> simple_type | range_type | array_type | record_type | identifier
    simple_type -> integer | real | boolean | char
    range_type -> expression .. expression
    array_type -> larik [index_range] dari type_spec
    index_range -> expression .. expression
    record_type -> rekaman field_list selesai
    field_list -> var_declaration {var_declaration}
"""

from ..node import ParseNode


def parse_type_spec(parser):
    """
    Parse type specification (definisi tipe)
    
    Args:
        parser: Parser instance dengan current_token(), advance(), dll
    
    Returns:
        ParseNode representing type specification
    
    Examples:
        - integer
        - real
        - 1..10 (range)
        - larik [1..10] dari integer (array)
        - rekaman x : integer; selesai (record)
        - TMyType (user-defined type identifier)
    """
    token = parser.current_token()
    
    if not token:
        raise SyntaxError("Expected type specification, got end of input")
    
    # Simple types: integer, real, boolean, char
    if token[0] == "KEYWORD" and token[1] in ["integer", "real", "boolean", "char"]:
        return parse_simple_type(parser)
    
    # Array type: larik [...]
    if token[0] == "KEYWORD" and token[1] == "larik":
        return parse_array_type(parser)
    
    # Record type: rekaman ...
    if token[0] == "KEYWORD" and token[1] == "rekaman":
        return parse_record_type(parser)
    
    # Could be: identifier (user-defined type) or range (number..number)
    if token[0] == "IDENTIFIER":
        return parse_identifier_type(parser)
    
    # Could be range starting with number
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
    
    # Parse start expression
    start_expr = parser.expression_parser.parse_expression()
    range_node.add_child(start_expr)
    
    # Check for '..' (range operator)
    token = parser.current_token()
    if token and token[0] == "DOT":
        # Need to check if next is also DOT (for ..)
        parser.advance()
        token = parser.current_token()
        if token and token[0] == "DOT":
            range_node.add_child(ParseNode("RANGE(..)"))
            parser.advance()
            
            # Parse end expression
            end_expr = parser.expression_parser.parse_expression()
            range_node.add_child(end_expr)
            
            return range_node
        else:
            raise SyntaxError(f"Expected '..' in range type, got single '.'")
    else:
        raise SyntaxError(f"Expected '..' in range type, got {token}")


def parse_array_type(parser):
    """
    Parse array type: larik [index_range] dari type_spec
    
    Example:
        larik [1..10] dari integer
        larik [0..99] dari char
    """
    array_node = ParseNode("<array_type>")
    
    # Parse 'larik' keyword
    token = parser.current_token()
    if token and token[0] == "KEYWORD" and token[1] == "larik":
        larik_keyword = ParseNode(f"KEYWORD({token[1]})")
        array_node.add_child(larik_keyword)
        parser.advance()
    else:
        raise SyntaxError(f"Expected 'larik' keyword, got {token}")
    
    # Parse '['
    token = parser.current_token()
    if token and token[0] == "LBRACKET":
        lbracket_node = ParseNode(f"LBRACKET({token[1]})")
        array_node.add_child(lbracket_node)
        parser.advance()
    else:
        raise SyntaxError(f"Expected '[' after 'larik', got {token}")
    
    # Parse index range (expression .. expression)
    index_range_node = parse_range_type(parser)
    array_node.add_child(index_range_node)
    
    # Parse ']'
    token = parser.current_token()
    if token and token[0] == "RBRACKET":
        rbracket_node = ParseNode(f"RBRACKET({token[1]})")
        array_node.add_child(rbracket_node)
        parser.advance()
    else:
        raise SyntaxError(f"Expected ']' after index range, got {token}")
    
    # Parse 'dari' keyword
    token = parser.current_token()
    if token and token[0] == "KEYWORD" and token[1] == "dari":
        dari_keyword = ParseNode(f"KEYWORD({token[1]})")
        array_node.add_child(dari_keyword)
        parser.advance()
    else:
        raise SyntaxError(f"Expected 'dari' keyword, got {token}")
    
    # Parse element type (recursive call)
    element_type = parse_type_spec(parser)
    array_node.add_child(element_type)
    
    return array_node


def parse_record_type(parser):
    """
    Parse record type: rekaman field_list selesai
    
    Example:
        rekaman
            x : integer;
            y : real;
        selesai
    """
    record_node = ParseNode("<record_type>")
    
    # Parse 'rekaman' keyword
    token = parser.current_token()
    if token and token[0] == "KEYWORD" and token[1] == "rekaman":
        rekaman_keyword = ParseNode(f"KEYWORD({token[1]})")
        record_node.add_child(rekaman_keyword)
        parser.advance()
    else:
        raise SyntaxError(f"Expected 'rekaman' keyword, got {token}")
    
    # Parse field declarations (same as var_declaration but without 'variabel' keyword)
    # We need at least one field
    from .var_declaration import parse_var_declaration
    
    # Parse fields until we hit 'selesai'
    while parser.current_token():
        token = parser.current_token()
        
        if token[0] == "KEYWORD" and token[1] == "selesai":
            break
        
        # Parse field (identifier_list : type ;)
        # Since it's inside record, we parse without 'variabel' keyword
        field_node = parse_record_field(parser)
        record_node.add_child(field_node)
    
    # Parse 'selesai' keyword
    token = parser.current_token()
    if token and token[0] == "KEYWORD" and token[1] == "selesai":
        selesai_keyword = ParseNode(f"KEYWORD({token[1]})")
        record_node.add_child(selesai_keyword)
        parser.advance()
    else:
        raise SyntaxError(f"Expected 'selesai' keyword to end record, got {token}")
    
    return record_node


def parse_record_field(parser):
    """
    Parse record field: identifier_list : type ;
    
    Similar to var_declaration but without 'variabel' keyword
    """
    from .identifier_list import parse_identifier_list
    
    field_node = ParseNode("<record_field>")
    
    # Parse identifier list
    identifier_list_node = parse_identifier_list(parser)
    field_node.add_child(identifier_list_node)
    
    # Parse ':'
    token = parser.current_token()
    if token and token[0] == "COLON":
        colon_node = ParseNode(f"COLON({token[1]})")
        field_node.add_child(colon_node)
        parser.advance()
    else:
        raise SyntaxError(f"Expected ':' in record field, got {token}")
    
    # Parse type
    type_node = parse_type_spec(parser)
    field_node.add_child(type_node)
    
    # Parse ';'
    token = parser.current_token()
    if token and token[0] == "SEMICOLON":
        semicolon_node = ParseNode(f"SEMICOLON({token[1]})")
        field_node.add_child(semicolon_node)
        parser.advance()
    else:
        raise SyntaxError(f"Expected ';' after record field, got {token}")
    
    return field_node


def parse_identifier_type(parser):
    """
    Parse user-defined type identifier
    
    Example:
        TMyType
        TArray
    """
    type_node = ParseNode("<identifier_type>")
    
    token = parser.current_token()
    if token and token[0] == "IDENTIFIER":
        identifier_node = ParseNode(f"IDENTIFIER({token[1]})")
        type_node.add_child(identifier_node)
        parser.advance()
        return type_node
    
    raise SyntaxError(f"Expected identifier for type, got {token}")
