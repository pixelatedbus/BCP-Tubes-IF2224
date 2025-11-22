from ..misc.ast_node import ASTNode

class procedureFunctionCallNode(ASTNode):
    def __init__(self, name: str, arguments: list):
        super().__init__()
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return f"ProcedureFunctionCall Node(name={self.name}, arguments={self.arguments})"

    def evaluate(self):
        print("Evaluating ProcedureFunctionCall Node")
        return None