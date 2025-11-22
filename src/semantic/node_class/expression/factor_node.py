from ..misc.ast_node import ASTNode

class FactorNode(ASTNode):
    """
    Base class for all factor nodes (primary expressions).
    Factors are the atomic units of expressions.
    """
    def __init__(self):
        super().__init__()
    
    def __repr__(self):
        return "FactorNode(base)"
