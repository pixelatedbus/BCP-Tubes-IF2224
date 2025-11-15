from ..node import ParseNode

def parse_parameter_group(parser):
    parameter_group_node = ParseNode("<parameter-group>")

    identifier_list_node = parser.declaration_parser.parse_identifier_list()
    parameter_group_node.add_child(identifier_list_node)

    parser.check_token("COLON", ":")
    parameter_group_node.add_child(ParseNode("COLON(:)"))

    type_node = parser.declaration_parser.parse_type()
    parameter_group_node.add_child(type_node)

    return parameter_group_node