from ..misc.ast_node import ASTNode

class ProcedureDeclNode(ASTNode):
    def __init__(self, name: str, parameters=None, declarations=None, body=None):
        super().__init__()
        self.name = name
        self.parameters = parameters if parameters else []  # List of parameter nodes
        self.declarations = declarations if declarations else []  # Local declarations
        self.body = body  # Statement node (compound statement)
    
    def __repr__(self):
        return f"ProcedureDecl Node(name={self.name}, params={len(self.parameters)}, decls={len(self.declarations)})"
    
    def evaluate(self):
        print(f"Evaluating ProcedureDecl Node: {self.name}")
        return None
