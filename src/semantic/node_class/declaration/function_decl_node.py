from ..misc.ast_node import ASTNode

class FunctionDeclNode(ASTNode):
    def __init__(self, name: str, parameters=None, return_type: str = None, declarations=None, body=None):
        super().__init__()
        self.name = name
        self.parameters = parameters if parameters else []  # List of parameter nodes
        self.return_type = return_type  # Return type (integer, real, etc.)
        self.declarations = declarations if declarations else []  # Local declarations
        self.body = body  # Statement node (compound statement)
    
    def __str__(self):
        return f"FunctionDecl Node(name={self.name}, params={len(self.parameters)}, return_type={self.return_type})"
    
    def evaluate(self):
        print(f"Evaluating FunctionDecl Node: {self.name}")
        return None
