from ..misc.ast_node import ASTNode

class ExpressionNode(ASTNode):
    """
    Represents a binary expression with a relational operator.
    Example: a = b, x < 5, y >= 10
    """
    def __init__(self, left_operand, operator=None, right_operand=None):
        super().__init__()
        self.left_operand = left_operand  # SimpleExpressionNode
        self.operator = operator  # String: '=', '<>', '<', '<=', '>', '>='
        self.right_operand = right_operand  # SimpleExpressionNode (optional)
        
        self.add_child(left_operand)
        if operator and right_operand:
            self.add_child(right_operand)
    
    def is_comparison(self):
        """Returns True if this is a comparison expression, False if just a simple expression."""
        return self.operator is not None
    
    def __repr__(self):
        if self.is_comparison():
            return f"ExpressionNode({self.left_operand} {self.operator} {self.right_operand})"
        return f"ExpressionNode({self.left_operand})"
