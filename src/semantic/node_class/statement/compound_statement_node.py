from ..misc.ast_node import ASTNode

class CompoundStatementNode(ASTNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __repr__(self):
        return f"CompoundStatement Node(name={self.name}, children={self.children})"

    def evaluate(self):
        print("Evaluating CompoundStatement Node")
        return None