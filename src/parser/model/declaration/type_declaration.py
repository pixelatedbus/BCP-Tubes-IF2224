from ..node import ParseNode
from .type_spec import parse_type_spec

def parse_type_declaration(parser):
    """
    Parse type declaration (deklarasi tipe baru)
    
    Args:
        parser: Parser instance dengan current_token(), advance(), dll
    
    Returns:
        ParseNode representing type declaration
    
    Example:
        tipe TArray = larik [1..10] dari integer;
        tipe Range = 1..10;
        tipe TRecord = rekaman x : integer; y : real; selesai;
        tipe TInteger = integer;
    """
    type_decl_node = ParseNode("<type_declaration>")
    
    token = parser.current_token()
    if token and token[0] == "KEYWORD" and token[1] == "tipe":
        type_keyword_node = ParseNode(f"KEYWORD({token[1]})")
        type_decl_node.add_child(type_keyword_node)
        parser.advance()
        
        # Parse identifier (type name)
        token = parser.current_token()
        if token and token[0] == "IDENTIFIER":
            identifier_node = ParseNode(f"IDENTIFIER({token[1]})")
            type_decl_node.add_child(identifier_node)
            parser.advance()
            
            # Check for '='
            token = parser.current_token()
            if token and token[0] == "RELATIONAL_OPERATOR" and token[1] == "=":
                equal_node = ParseNode(f"RELATIONAL_OPERATOR({token[1]})")
                type_decl_node.add_child(equal_node)
                parser.advance()
                
                # Parse type specification (definisi tipe sebenarnya)
                type_spec_node = parse_type_spec(parser)
                type_decl_node.add_child(type_spec_node)
                
                # Check for semicolon
                token = parser.current_token()
                if token and token[0] == "SEMICOLON":
                    semicolon_node = ParseNode(f"SEMICOLON({token[1]})")
                    type_decl_node.add_child(semicolon_node)
                    parser.advance()
                    return type_decl_node
                else:
                    raise SyntaxError(f"Expected ';' after type declaration, got {token}")
            else:
                raise SyntaxError(f"Expected '=' in type declaration, got {token}")
        else:
            raise SyntaxError(f"Expected identifier in type declaration, got {token}")
    else:
        raise SyntaxError(f"Expected 'tipe' keyword, got {token}")