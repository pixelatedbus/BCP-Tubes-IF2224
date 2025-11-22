from ..misc.ast_node import ASTNode

class IfStatementNode(ASTNode):
    def __init__(self, compare, ifbody, elsebody=None):
        super().__init__()
        self.name = "if_statement"
        self.compare = compare
        self.ifbody = ifbody
        self.elsebody = elsebody

    def __str__(self):
        return f"If Statement Node(compare={self.compare}, ifbody={self.ifbody}, elsebody={self.elsebody})"
    
    def evaluate(self):
        print("Evaluating If Statement Node")
        return None