from ..misc.ast_node import ASTNode

class procedureFunctionCallNode(ASTNode):
    def __init__(self, name: str, arguments: list):
        super().__init__()
        self.name = name
        self.arguments = arguments

    def __str__(self):
        args_str = ', '.join(str(arg) for arg in self.arguments)
        return f"ProcedureFunctionCall Node(name={self.name}, arguments=[{args_str}])"

    def evaluate(self):
        print("Evaluating ProcedureFunctionCall Node")
        return None