from .model.declaration_parser import DeclarationParser
from .model.expression_parser import ExpressionParser
from .model.statement_parser import StatementParser
from .model.node import ParseNode

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

        self.declaration_parser = DeclarationParser(self)
        self.expression_parser = ExpressionParser(self)
        self.statement_parser = StatementParser(self)

    def current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None
    
    def advance(self):
        self.position += 1

    def peek(self):
        peek_position = self.position + 1
        if peek_position < len(self.tokens):
            return self.tokens[peek_position]
        return None
    
    def check_token(self, expected_type, expected_value=None):
        token = self.current_token()
        if token is None:
            raise SyntaxError("Unexpected end of input")
        
        token_type, token_value = token
        if token_type != expected_type:
            raise SyntaxError(f"Expected token type {expected_type} (value: {expected_value}), got {token_type}({token_value}) at position {self.position}")
        if expected_value and token_value != expected_value:
            raise SyntaxError(f"Expected token value {expected_value}, got {token_value}")
        
        self.advance()
        return token

    def parse_program_header(self):
        program_header_node = ParseNode("<program_header>")
        
        self.check_token("KEYWORD", "program")
        identifier = self.check_token("IDENTIFIER")
        self.check_token("SEMICOLON")

        program_header_node.add_child(ParseNode(f"KEYWORD(program)"))
        program_header_node.add_child(ParseNode(f"IDENTIFIER({identifier[1]})"))
        program_header_node.add_child(ParseNode("SEMICOLON(;)"))

        return program_header_node
    
    def parse_program(self):
        program_node = ParseNode("<program>")

        program_header_node = self.parse_program_header()
        program_node.add_child(program_header_node)

        declaration_part_node = self.declaration_parser.parse_declarations()
        program_node.add_child(declaration_part_node)

        compound_statement_node = self.statement_parser.parse_statement()
        program_node.add_child(compound_statement_node)

        self.check_token("DOT")
        program_node.add_child(ParseNode("DOT(.)"))
        
        return program_node