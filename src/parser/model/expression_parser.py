import sys
from pathlib import Path
from .node import ParseNode
from .expression.simple import parse_simple_expression
from .expression.term import parse_term
from .expression.factor import parse_factor
from .expression.relational_operator import parse_relational_operator
from .expression.additive import parse_additive_expression
from .expression.multiplicative import parse_multiplicative_expression

class ExpressionParser():
    def __init__(self, parent):
        self.parent = parent
        
    def parse_expression(self):
        expression_node = ParseNode("<expression>")
        simple_expression_node = self.parse_simple_expression()
        expression_node.add_child(simple_expression_node)

        token = self.parent.current_token()

        if token is not None:
            token_type, token_value = token
            if token_type == "RELATIONAL_OPERATOR" and token_value in ["=", "<>", "<", "<=", ">", ">="]:
                relational_operator_node = self.parse_relational_operator()
                expression_node.add_child(relational_operator_node)
                second_simple_expression_node = self.parse_simple_expression()
                expression_node.add_child(second_simple_expression_node)

        return expression_node


    def parse_simple_expression(self):
        return parse_simple_expression(self.parent)

    def parse_term(self):
        return parse_term(self.parent)

    def parse_factor(self):
        return parse_factor(self.parent)

    def parse_relational_operator(self):
        return parse_relational_operator(self.parent)
    
    def additive_operator(self):
        return parse_additive_expression(self.parent)

    def multiplicative_operator(self):
        return parse_multiplicative_expression(self.parent)