from ..misc.ast_node import ASTNode

class StatementListNode(ASTNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = name