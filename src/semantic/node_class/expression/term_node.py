from ..misc.ast_node import ASTNode

class TermNode(ASTNode):
    """
    Represents a multiplicative expression or logical AND expression.
    A chain of factors with multiplicative operators.
    Example: a * b, x / y mod z, flag dan flag2
    """
    def __init__(self):
        super().__init__()
        self.factors = []  # List of FactorNode
        self.operators = []  # List of operators: '*', '/', 'bagi', 'mod', 'dan'
    
    def add_factor(self, factor, operator=None):
        """Add a factor to the term. Operator is the one that comes BEFORE this factor."""
        if len(self.factors) > 0 and operator is None:
            raise ValueError("Operator required for additional factors")
        
        self.factors.append(factor)
        self.add_child(factor)
        
        if operator:
            self.operators.append(operator)
    
    def is_single_factor(self):
        """Returns True if this term contains only one factor."""
        return len(self.factors) == 1
    
    def __repr__(self):
        if not self.factors:
            return "TermNode(empty)"
        
        result = str(self.factors[0])
        for i, op in enumerate(self.operators):
            if i + 1 < len(self.factors):
                result += f" {op} {self.factors[i + 1]}"
        return f"TermNode({result})"
