from .node import ParseNode
from .statement.while_statement import parse_while_statement
from .statement.for_statement import parse_for_statement
from .statement.assignment_statement import parse_assignment_statement
from .statement.if_statement import parse_if_statement
from .statement.statement_list import parse_statement_list
from .statement.procedure_function_call import parse_procedure_function_call
from .statement.parameter_list import parse_parameter_list

class StatementParser():
    def __init__(self, parent):
        self.parent = parent
    
    def parse_statement(self):
        compound_statement_node = ParseNode("<compound-statement>")

        self.parent.check_token("KEYWORD", "mulai")
        compound_statement_node.add_child(ParseNode("KEYWORD(mulai)"))

        statement_list_node = self.parse_statement_list()
        compound_statement_node.add_child(statement_list_node)

        self.parent.check_token("KEYWORD", "selesai")
        compound_statement_node.add_child(ParseNode("KEYWORD(selesai)"))

        return compound_statement_node

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
        return parse_procedure_function_call(self.parent)

    def parse_parameter_list(self):
        return parse_parameter_list(self.parent)