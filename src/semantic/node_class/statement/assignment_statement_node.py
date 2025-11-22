from ..misc.ast_node import ASTNode

class AssignmentStatementNode(ASTNode):
    def __init__(self, variable_name: str, value):
        super().__init__()
        self.variable_name = variable_name
        self.value = value

    def __str__(self):
        return f"AssignmentStatement Node(variable_name={self.variable_name}, value={self.value})"

    def evaluate(self):
        print(f"Evaluating AssignmentStatement Node: {self.variable_name} = {self.value}")
        return None