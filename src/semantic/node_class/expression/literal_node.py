from .factor_node import FactorNode

class LiteralNode(FactorNode):
    """
    Represents a literal value (number, character, or string).
    Example: 42, 'a', "hello"
    """
    def __init__(self, value, literal_type):
        super().__init__()
        self.value = value  # The actual value
        self.literal_type = literal_type  # 'NUMBER', 'CHAR_LITERAL', 'STRING_LITERAL'
    
    def __str__(self):
        return f"LiteralNode({self.literal_type}: {self.value})"


class NumberLiteral(LiteralNode):
    """Represents a numeric literal."""
    def __init__(self, value):
        super().__init__(value, 'NUMBER')
    
    def __str__(self):
        return f"NumberLiteral({self.value})"


class CharLiteral(LiteralNode):
    """Represents a character literal."""
    def __init__(self, value):
        super().__init__(value, 'CHAR_LITERAL')
    
    def __str__(self):
        return f"CharLiteral({self.value})"


class StringLiteral(LiteralNode):
    """Represents a string literal."""
    def __init__(self, value):
        super().__init__(value, 'STRING_LITERAL')
    
    def __str__(self):
        return f"StringLiteral({self.value})"
