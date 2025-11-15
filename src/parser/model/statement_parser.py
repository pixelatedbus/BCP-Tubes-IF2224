from .node import ParseNode
from .statement.while_statement import parse_while_statement
from .statement.for_statement import parse_for_statement
    

class StatementParser():
    def __init__(self, parent):
        self.parent = parent
    
    def parse_statement(self):
        # Placeholder for statement parsing logic
        pass

    def parse_statement_list(self):
        # Placeholder for statement list parsing logic
        pass
    
    def parse_assignment_statement(self):
        # Placeholder for assignment statement parsing logic
        pass

    def parse_if_statement(self):
        # Placeholder for if statement parsing logic
        pass
    
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