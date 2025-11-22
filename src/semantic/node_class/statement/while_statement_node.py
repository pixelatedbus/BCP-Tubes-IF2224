from ..misc.ast_node import ASTNode

class WhileStatementNode(ASTNode):
    def __init__(self, condition, body):
        super().__init__()
        self.name = "while_statement"
        self.condition = condition
        self.body = body
        
        if body:
            self.add_child(body)

    def __str__(self):
        return f"WhileStatement Node(condition={self.condition})"

    def evaluate(self):
        print("Evaluating WhileStatement Node")
        return None