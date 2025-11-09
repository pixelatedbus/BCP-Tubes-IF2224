from .model.declaration_parser import DeclarationParser
from .model.expression_parser import ExpressionParser
from .model.statement_parser import StatementParser

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
    
    def check_token(self, expected_type, expected_value=None):
        token = self.current_token()
        if token is None:
            raise SyntaxError("Unexpected end of input")
        
        token_type, token_value = token
        if token_type != expected_type:
            raise SyntaxError(f"Expected token type {expected_type}, got {token_type}")
        if expected_value and token_value != expected_value:
            raise SyntaxError(f"Expected token value {expected_value}, got {token_value}")
        
        self.advance()
        return token

    def parse_program_header(self):
        self.check_token("KEYWORD", "program")
        self.check_token("IDENTIFIER")
        self.check_token("SEMICOLON")

    def parse_program(self):
        self.parse_program_header()
        self.declaration_parser.parse_declarations() #Will change after implementing declaration parser
        self.statement_parser.parse_statements()     #Will change after implementing statement parser
        self.check_token("DOT")