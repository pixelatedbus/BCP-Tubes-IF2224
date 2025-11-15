from .node import ParseNode
from .declaration.formal_parameter_list import parse_formal_parameter_list
from .declaration.parameter_group import parse_parameter_group
from .declaration.function_declaration import parse_function_declaration
from .declaration.procedure_declaration import parse_procedure_declaration

class DeclarationParser():
    def __init__(self, parent):
        self.parent = parent
    
    def parse_declarations(self):
        # Placeholder for declaration parsing logic
        pass

    def parse_const_declaration(self):
        # Placeholder for constant declaration parsing logic
        pass

    def parse_type_declaration(self):
        # Placeholder for type declaration parsing logic
        pass

    def parse_var_declaration(self):
        # Placeholder for variable declaration parsing logic
        pass

    def parse_identifier_list(self):
        # Placeholder for identifier list parsing logic
        pass

    def parse_type(self):
        # Placeholder for type parsing logic
        pass

    def parse_array_type(self):
        # Placeholder for array type parsing logic
        pass

    def parse_range(self):
        # Placeholder for range parsing logic
        pass

    def parse_subprogram_declaration(self):
        # Placeholder for subprogram declaration parsing logic
        pass

    def parse_function_declaration(self):
        return parse_function_declaration(self.parent)

    def parse_procedure_declaration(self):
        return parse_procedure_declaration(self.parent)

    def parse_formal_parameter_list(self):
        return parse_formal_parameter_list(self.parent)

    def parse_parameter_group(self):
        return parse_parameter_group(self.parent)

