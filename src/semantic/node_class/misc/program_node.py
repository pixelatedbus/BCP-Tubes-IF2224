from ast_node import ASTNode

class ProgramNode(ASTNode):
    def __init__(self, name, declarations, block):
        super().__init__()
        self.name = name
        self.add_child(declarations)
        self.add_child(block)

