from .const_builder import build_const_declaration
from .type_builder import build_type_declaration
from .var_builder import build_var_declaration
from .procedure_builder import build_procedure_declaration
from .function_builder import build_function_declaration


def build_declaration(parse_node):
    all_declarations = []
    
    for child in parse_node.children:
        if child.name == "<const_declaration>":
            const_node = build_const_declaration(child)
            all_declarations.append(const_node)
        
        elif child.name == "<type_declaration>":
            type_node = build_type_declaration(child)
            all_declarations.append(type_node)
        
        elif child.name == "<var_declaration>":
            var_nodes = build_var_declaration(child)
            all_declarations.extend(var_nodes)
        
        elif child.name == "<subprogram-declaration>":
            for subchild in child.children:
                if subchild.name == "<procedure-declaration>":
                    proc_node = build_procedure_declaration(subchild)
                    all_declarations.append(proc_node)
                elif subchild.name == "<function-declaration>":
                    func_node = build_function_declaration(subchild)
                    all_declarations.append(func_node)
    
    return all_declarations
