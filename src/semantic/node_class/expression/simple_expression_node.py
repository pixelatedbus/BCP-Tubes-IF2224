from ..misc.ast_node import ASTNode

class SimpleExpressionNode(ASTNode):
    """
    Represents an additive expression or logical OR expression.
    Can be unary (with sign) or a chain of terms with additive operators.
    Example: +a, a + b - c, x atau y
    """
    def __init__(self, sign=None):
        super().__init__()
        self.sign = sign  # Optional '+' or '-' for unary expressions
        self.terms = []  # List of TermNode
        self.operators = []  # List of operators: '+', '-', 'atau'
    
    def add_term(self, term, operator=None):
        """Add a term to the expression. Operator is the one that comes BEFORE this term."""
        if len(self.terms) > 0 and operator is None:
            raise ValueError("Operator required for additional terms")
        
        self.terms.append(term)
        self.add_child(term)
        
        if operator:
            self.operators.append(operator)
    
    def is_unary(self):
        """Returns True if this is a unary expression with a sign."""
        return self.sign is not None and len(self.terms) == 1
    
    def __str__(self):
        if self.is_unary():
            return f"SimpleExpressionNode({self.sign}{self.terms[0]})"
        
        result = str(self.terms[0]) if self.terms else ""
        for i, op in enumerate(self.operators):
            if i + 1 < len(self.terms):
                result += f" {op} {self.terms[i + 1]}"
        return f"SimpleExpressionNode({result})"
