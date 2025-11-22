from ..misc.ast_node import ASTNode

class DeclarationNode(ASTNode):
    def __init__(self):
        super().__init__()
    
    def __repr__(self):
        return f"Declaration Node(children={self.children})"
    
    def  evaluate(self):
        print("Evaluating Declaration Node")
        return None

