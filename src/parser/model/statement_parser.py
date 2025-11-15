from .node import ParseNode
from .statement.while_statement import parse_while_statement
from .statement.for_statement import parse_for_statement
from .statement.assignment_statement import parse_assignment_statement
from .statement.if_statement import parse_if_statement
from .statement.statement_list import parse_statement_list

class StatementParser():
    def __init__(self, parent):
        self.parent = parent
    
    def parse_statement(self):
        # Placeholder for statement parsing logic
        pass

    def parse_statement_list(self):
        return parse_statement_list(self.parent)
    
    def parse_assignment_statement(self):
        return parse_assignment_statement(self.parent)

    def parse_if_statement(self):
        return parse_if_statement(self.parent)
    
    def parse_while_statement(self):
        return parse_while_statement(self.parent)

    def parse_for_statement(self):
        return parse_for_statement(self.parent)

    def parse_function_call(self):
        # Placeholder for function call parsing logic
        pass

    def parse_parameter_list(self):
        # Placeholder for parameter list parsing logic
        pass