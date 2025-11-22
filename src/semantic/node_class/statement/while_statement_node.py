from ..misc.ast_node import ASTNode

class WhileStatementNode(ASTNode):
    def __init__(self, condition, body):
        super().__init__()
        self.name = "while_statement"
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileStatement Node(condition={self.condition}, body={self.body})"

    def evaluate(self):
        print("Evaluating WhileStatement Node")
        return None