from src.parser.model.node import ParseNode
from src.parser.model.expression.simple import parse_simple_expression

class ExpressionParser():
    def __init__(self, parent):
        self.parent = parent
        
    def parse_expression(self):
        # Placeholder for expression parsing logic
        pass

    def parse_simple_expression(self):
        # Placeholder for simple expression parsing logic
        return parse_simple_expression(self.parent)

    def parse_term(self):
        # Placeholder for term parsing logic
        pass

    def parse_factor(self):
        # Placeholder for factor parsing logic
        pass

    def parse_relational_operator(self):
        # Placeholder for relational operator parsing logic
        pass

    def additive_operator(self):
        # Placeholder for additive operator parsing logic
        pass

    def multiplicative_operator(self):
        # Placeholder for multiplicative operator parsing logic
        pass