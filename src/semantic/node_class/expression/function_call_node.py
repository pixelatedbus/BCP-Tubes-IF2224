from .factor_node import FactorNode

class FunctionCallNode(FactorNode):
    """
    Represents a function call in an expression.
    Example: calculateSum(a, b), max(x, y, z)
    """
    def __init__(self, function_name, arguments=None):
        super().__init__()
        self.function_name = function_name  # String: name of the function
        self.arguments = arguments if arguments is not None else []  # List of ExpressionNode
        
        # Add arguments as children
        for arg in self.arguments:
            self.add_child(arg)
    
    def add_argument(self, argument):
        """Add an argument to the function call."""
        self.arguments.append(argument)
        self.add_child(argument)
    
    def __repr__(self):
        args_str = ", ".join(str(arg) for arg in self.arguments)
        return f"FunctionCallNode({self.function_name}({args_str}))"
