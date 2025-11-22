from .ast_node import ASTNode

class DeclarationsNode(ASTNode):
    def __init__(self):
        super().__init__()
        self.name = "Declarations"
    
    def __str__(self):
        return "Declarations"
