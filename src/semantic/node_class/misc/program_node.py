from .ast_node import ASTNode

class ProgramNode(ASTNode):
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    def __str__(self):
        return f"ProgramNode(name: {self.name})"
