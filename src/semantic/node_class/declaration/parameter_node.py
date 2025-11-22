from ..misc.ast_node import ASTNode

class ParameterNode(ASTNode):
    def __init__(self, name: str, param_type: str, is_var: bool = False):
        super().__init__()
        self.name = name
        self.param_type = param_type  # Parameter type (integer, real, etc.)
        self.is_var = is_var  # True if parameter is passed by reference (var)
    
    def __repr__(self):
        var_str = "var " if self.is_var else ""
        return f"Parameter Node({var_str}{self.name}: {self.param_type})"
    
    def evaluate(self):
        print(f"Evaluating Parameter Node: {self.name}")
        return None
