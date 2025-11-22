from ..misc.ast_node import ASTNode

class ForStatementNode(ASTNode):
    def __init__(self, variable: str, start: int, end: int, body: list):
        super().__init__()
        self.name = "for_statement"
        self.variable = variable
        self.start = start
        self.end = end
        self.body = body

        if body:
            self.add_child(body)

    def __str__(self):
        return f"ForStatement Node(variable={self.variable}, start={self.start}, end={self.end})"

    def evaluate(self):
        print("Evaluating ForStatement Node")
        return None