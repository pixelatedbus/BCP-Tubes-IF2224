from ..misc.ast_node import ASTNode

class CompoundStatementNode(ASTNode):
    def __init__(self):
        super().__init__()

    def evaluate(self):
        print("Evaluating CompoundStatement Node")
        return None