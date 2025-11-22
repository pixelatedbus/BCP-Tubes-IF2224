from ..misc.ast_node import ASTNode

class TypeDeclNode(ASTNode):
    def __init__(self, name: str, type_spec):
        super().__init__()
        self.name = name
        self.type_spec = type_spec  # Type specification (simple_type, range_type, etc.)
    
    def __str__(self):
        return f"TypeDecl Node(name={self.name}, type_spec={self.type_spec})"
    
    def evaluate(self):
        print(f"Evaluating TypeDecl Node: {self.name}")
        return None
