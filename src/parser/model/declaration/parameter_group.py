from ..node import ParseNode

def parse_parameter_group(parser):
    parameter_group_node = ParseNode("<parameter-group>")

    parameter_list_node = parser.statement_parser.parse_parameter_list()
    parameter_group_node.add_child(parameter_list_node)

    parser.check_token("COLON", ":")
    parameter_group_node.add_child(ParseNode("COLON(:)"))

    type_node = parser.declaration_parser.parse_type()
    parameter_group_node.add_child(type_node)

    return parameter_group_node