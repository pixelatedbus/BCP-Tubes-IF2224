from ..misc.ast_node import ASTNode

class ForStatementNode(ASTNode):
    def __init__(self, variable: str, start: int, end: int, body: list):
        super().__init__()
        self.name = "for_statement"
        self.variable = variable
        self.start = start
        self.end = end
        self.body = body

    def __repr__(self):
        return f"ForStatement Node(variable={self.variable}, start={self.start}, end={self.end}, body={self.body})"

    def evaluate(self):
        print("Evaluating ForStatement Node")
        return None