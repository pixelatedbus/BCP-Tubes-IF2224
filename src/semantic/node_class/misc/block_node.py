from .ast_node import ASTNode

class BlockNode(ASTNode):
    def __init__(self):
        super().__init__()
        self.name = "Block"
