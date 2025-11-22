from ..node_class.misc.program_node import ProgramNode
from ..node_class.misc.declarations_node import DeclarationsNode
from ..node_class.misc.block_node import BlockNode
from .statement.statement_builder import build_statements
from .declaration.declaration_builder import build_declaration

def build_ast(parse_tree):
    if parse_tree.name != "<program>":
        raise ValueError(f"Expected <program>, got {parse_tree.name}")
    
    program_header_node = parse_tree.children[0]
    program_name = program_header_node.children[1].name.split('(')[1][:-1]
    program_node = ProgramNode(program_name)

    declarations_node = DeclarationsNode()
    
    block_node = BlockNode()
    
    for child in parse_tree.children:
        if child.name == "<declaration-part>":
            declaration_nodes = build_declaration(child)
            for declaration_node in declaration_nodes:
                declarations_node.add_child(declaration_node)
        elif child.name == "<compound-statement>":
            statement_list = child.children[1]
            statements = build_statements(statement_list)
            for statement in statements:
                block_node.add_child(statement)

    program_node.add_child(declarations_node)
    program_node.add_child(block_node)
    
    return program_node