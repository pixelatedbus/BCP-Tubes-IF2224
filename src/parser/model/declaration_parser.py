from .node import ParseNode
from .declaration.formal_parameter_list import parse_formal_parameter_list
from .declaration.parameter_group import parse_parameter_group
from .declaration.function_declaration import parse_function_declaration
from .declaration.procedure_declaration import parse_procedure_declaration
from .declaration.const_declaration import parse_const_declaration
from .declaration.type_declaration import parse_type_declaration
from .declaration.var_declaration import parse_var_declaration
from .declaration.identifier_list import parse_identifier_list
from .declaration.type import parse_type
from .declaration.array_type import parse_array_type
from .declaration.range import parse_range
from .declaration.subprogram_declaration import parse_subprogram_declaration

class DeclarationParser():
    def __init__(self, parent):
        self.parent = parent
    
    def parse_declarations(self):
        declaration_part_node = ParseNode("<declaration-part>")
        while True:
            current_token = self.parent.current_token()
            if current_token is None:
                break

            if current_token[0] == "KEYWORD":
                if current_token[1] == "konstanta":
                    const_declaration_node = self.parse_const_declaration()
                    declaration_part_node.add_child(const_declaration_node)
                elif current_token[1] == "tipe":
                    type_declaration_node = self.parse_type_declaration()
                    declaration_part_node.add_child(type_declaration_node)
                elif current_token[1] == "variabel":
                    var_declaration_node = self.parse_var_declaration()
                    declaration_part_node.add_child(var_declaration_node)
                elif current_token[1] in ["fungsi", "prosedur"]:
                    subprogram_declaration_node = self.parse_subprogram_declaration()
                    declaration_part_node.add_child(subprogram_declaration_node)
                else:
                    break
            else:
                break

        return declaration_part_node

    def parse_const_declaration(self):
        return parse_const_declaration(self.parent)

    def parse_type_declaration(self):
        return parse_type_declaration(self.parent)

    def parse_var_declaration(self):
        return parse_var_declaration(self.parent)

    def parse_identifier_list(self):
        return parse_identifier_list(self.parent)

    def parse_type(self):
        return parse_type(self.parent)

    def parse_array_type(self):
        return parse_array_type(self.parent)
    
    def parse_range(self):
        return parse_range(self.parent)

    def parse_subprogram_declaration(self):
        return parse_subprogram_declaration(self.parent)
    
    def parse_function_declaration(self):
        return parse_function_declaration(self.parent)

    def parse_procedure_declaration(self):
        return parse_procedure_declaration(self.parent)

    def parse_formal_parameter_list(self):
        return parse_formal_parameter_list(self.parent)

    def parse_parameter_group(self):
        return parse_parameter_group(self.parent)

