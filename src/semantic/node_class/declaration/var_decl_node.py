from ..misc.ast_node import ASTNode

class VarDeclNode(ASTNode):
    def __init__(self, name: str, var_type: str):
        super().__init__("VarDecl")
        self.name = name
        self.var_type = var_type
    
    def __repr__(self):
        return f"VarDecl Node(name={self.name}, type={self.var_type})"
    
    def  evaluate(self):
        print("Evaluating VarDecl Node")
        return None

