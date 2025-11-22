from .factor_node import FactorNode

class ParenthesizedExpressionNode(FactorNode):
    """
    Represents a parenthesized expression for grouping.
    Example: (a + b), ((x * y) + z)
    """
    def __init__(self, expression):
        super().__init__()
        self.expression = expression  # ExpressionNode: the inner expression
        
        self.add_child(expression)
    
    def __str__(self):
        return f"ParenthesizedExpressionNode(({self.expression}))"
