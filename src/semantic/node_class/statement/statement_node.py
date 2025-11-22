from ..misc.ast_node import ASTNode

class StatementNode(ASTNode):
    def __init__(self):
        super().__init__()
        self.statement_type = "statement"

    def evaluate(self):
        print("Evaluating Statement Node")
        return None