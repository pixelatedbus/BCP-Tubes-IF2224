from .factor_node import FactorNode

class UnaryExpressionNode(FactorNode):
    """
    Represents a unary expression (logical NOT).
    Example: tidak flag, tidak (a = b)
    """
    def __init__(self, operator, operand):
        super().__init__()
        self.operator = operator  # String: 'tidak' (not)
        self.operand = operand  # FactorNode: the operand
        
        self.add_child(operand)
    
    def __str__(self):
        return f"UnaryExpressionNode({self.operator} {self.operand})"
