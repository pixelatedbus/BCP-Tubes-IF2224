from ..misc.ast_node import ASTNode

class VarDeclNode(ASTNode):
    def __init__(self, name: str, var_type: str):
        super().__init__("VarDecl")
    
    def __repr__(self):
        return f"VarDecl Node(children={self.children})"
    
    def  evaluate(self):
        print("Evaluating VarDecl Node")
        return None

