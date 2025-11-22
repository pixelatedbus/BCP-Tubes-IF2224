from ..misc.ast_node import ASTNode

class ConstDeclNode(ASTNode):
    def __init__(self, name: str, value):
        super().__init__()
        self.name = name
        self.value = value  # Expression node
    
    def __str__(self):
        return f"ConstDecl Node(name={self.name}, value={self.value})"
    
    def evaluate(self):
        print(f"Evaluating ConstDecl Node: {self.name}")
        return None
