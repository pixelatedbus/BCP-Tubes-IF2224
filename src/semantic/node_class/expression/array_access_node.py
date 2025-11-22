from .factor_node import FactorNode

class ArrayAccessNode(FactorNode):
    """
    Represents array element access.
    Example: score[i], matrix[row][col]
    """
    def __init__(self, array_name, index):
        super().__init__()
        self.array_name = array_name  # String: name of the array
        self.index = index  # ExpressionNode: the index expression
        
        self.add_child(index)
    
    def __str__(self):
        return f"ArrayAccessNode({self.array_name}[{self.index}])"
