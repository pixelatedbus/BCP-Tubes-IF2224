from ..node import ParseNode
from .array_type import parse_array_type


def parse_type_spec(parser):
    """
    Parse type specification (definisi tipe)
    Examples:
        - integer
        - real
        - 1..10 (range)
        - CustomTypeName (user-defined type)
    """
    token = parser.current_token()
    
    if not token:
        raise SyntaxError("Expected type specification, got end of input")
    
    if token[0] == "KEYWORD" and token[1] in ["integer", "real", "boolean", "char"]:
        return parse_simple_type(parser)

    if token[0] == "KEYWORD" and token[1] == "rekaman":
        return parse_record_type(parser)

    if token[0] == "KEYWORD" and token[1] == "larik":
        return parse_array_type(parser)
    
    if token[0] == "NUMBER" or token[0] == "CHAR_LITERAL":
        return parse_range_type(parser)
    
    # Handle custom type names (user-defined types)
    if token[0] == "IDENTIFIER":
        return parse_custom_type(parser)
    
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


def parse_custom_type(parser):
    type_node = ParseNode("<custom_type>")
    
    token = parser.current_token()
    if token and token[0] == "IDENTIFIER":
        identifier_node = ParseNode(f"IDENTIFIER({token[1]})")
        type_node.add_child(identifier_node)
        parser.advance()
        return type_node
    
    raise SyntaxError(f"Expected identifier for custom type, got {token}")


def parse_range_type(parser):
    range_node = ParseNode("<range_type>")
    
    start_expr = parser.expression_parser.parse_expression()
    range_node.add_child(start_expr)
    
    token = parser.current_token()
    # Masih ga pasti apa pake double DOT atau RANGE_OPERATOR
    if token and token[0] == "RANGE_OPERATOR":
        # parser.advance()
        # token = parser.current_token()
        # if token and token[0] == "DOT":
        range_node.add_child(ParseNode("RANGE(..)"))
        parser.advance()
        
        end_expr = parser.expression_parser.parse_expression()
        range_node.add_child(end_expr)
        
        return range_node
        # else:
        #     raise SyntaxError(f"Expected '..' in range type, got single '.'")
    else:
        raise SyntaxError(f"Expected '..' in range type, got {token}")
    
def parse_record_type(parser):
    """
    Parse record type (rekaman)
    
    Example:
        rekaman
            x : integer;
            y : real;
        selesai;
    """
    record_node = ParseNode("<record_type>")
    token = parser.current_token()
    if token and token[0] == "KEYWORD" and token[1] == "rekaman":
        rekaman_node = ParseNode(f"KEYWORD({token[1]})")
        record_node.add_child(rekaman_node)
        parser.advance()
    else:
        raise SyntaxError(f"Expected 'rekaman' keyword, got {token}")
    
    while True:
        token = parser.current_token()
        if token and token[0] == "KEYWORD" and token[1] == "selesai":
            selesai_node = ParseNode(f"KEYWORD({token[1]})")
            record_node.add_child(selesai_node)
            parser.advance()
            break
        
        if token and token[0] == "IDENTIFIER":
            identifier_node = ParseNode(f"IDENTIFIER({token[1]})")
            record_node.add_child(identifier_node)
            parser.advance()
            
            token = parser.current_token()
            if token and token[0] == "COLON":
                colon_node = ParseNode(f"COLON({token[1]})")
                record_node.add_child(colon_node)
                parser.advance()
                
                type_spec_node = parse_type_spec(parser)
                record_node.add_child(type_spec_node)
                
                token = parser.current_token()
                if token and token[0] == "SEMICOLON":
                    semicolon_node = ParseNode(f"SEMICOLON({token[1]})")
                    record_node.add_child(semicolon_node)
                    parser.advance()
                else:
                    raise SyntaxError(f"Expected ';' after field declaration, got {token}")
            else:
                raise SyntaxError(f"Expected ':' after field name, got {token}")
    return record_node
    