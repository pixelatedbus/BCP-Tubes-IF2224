from .node import ParseNode
from .declaration.formal_parameter_list import parse_formal_parameter_list
from .declaration.parameter_group import parse_parameter_group
from .declaration.function_declaration import parse_function_declaration
from .declaration.procedure_declaration import parse_procedure_declaration
from .declaration.const_declaration import parse_const_declaration
from .declaration.type_declaration import parse_type_declaration
from .declaration.var_declaration import parse_var_declaration
from .declaration.identifier_list import parse_identifier_list

class DeclarationParser():
    def __init__(self, parent):
        self.parent = parent
    
    def parse_declarations(self):
        # Placeholder for declaration parsing logic
        pass

    def parse_const_declaration(self):
        return parse_const_declaration(self.parent)

    def parse_type_declaration(self):
        return parse_type_declaration(self.parent)

    def parse_var_declaration(self):
        return parse_var_declaration(self.parent)

    def parse_identifier_list(self):
        return parse_identifier_list(self.parent)

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

