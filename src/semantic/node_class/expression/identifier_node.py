from .factor_node import FactorNode

class IdentifierNode(FactorNode):
    """
    Represents a variable reference.
    Example: x, myVar, counter
    """
    def __init__(self, name):
        super().__init__()
        self.name = name  # String: the identifier name
    
    def __repr__(self):
        return f"IdentifierNode({self.name})"
