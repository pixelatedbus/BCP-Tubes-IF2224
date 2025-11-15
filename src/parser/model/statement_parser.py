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
        """Parse compound statement (mulai ... selesai)"""
        compound_statement_node = ParseNode("<compound-statement>")

        self.parent.check_token("KEYWORD", "mulai")
        compound_statement_node.add_child(ParseNode("KEYWORD(mulai)"))

        statement_list_node = self.parse_statement_list()
        compound_statement_node.add_child(statement_list_node)

        self.parent.check_token("KEYWORD", "selesai")
        compound_statement_node.add_child(ParseNode("KEYWORD(selesai)"))

        return compound_statement_node

    def parse_single_statement(self):
        """Parse any single statement (assignment, if, while, for, call, or compound)"""
        token = self.parent.current_token()
        if not token:
            raise SyntaxError("Expected statement, got end of input")
        
        token_type, token_value = token

        # Compound statement
        if token_type == "KEYWORD" and token_value == "mulai":
            return self.parse_statement()
        
        # If statement
        if token_type == "KEYWORD" and token_value == "jika":
            return self.parse_if_statement()
        
        # While statement
        if token_type == "KEYWORD" and token_value == "selama":
            return self.parse_while_statement()
        
        # For statement
        if token_type == "KEYWORD" and token_value == "untuk":
            return self.parse_for_statement()
        
        # Identifier (assignment or call)
        if token_type == "IDENTIFIER":
            next_token = self.parent.peek()
            if next_token and next_token[0] == "LPAREN":
                return self.parse_function_call()
            return self.parse_assignment_statement()
        
        raise SyntaxError(f"Unexpected token in statement: {token}")

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