from src.parser.model.node import ParseNode

def parse_relational_operator(parser):
    relational_operator_node = ParseNode("<relational_operator>")

    token = parser.current_token()

    if token is None:
        raise SyntaxError("Unexpected end of input while parsing relational operator")

    token_type, token_value = token

    if token_type == "RELATIONAL_OPERATOR" and token_value in ["=", "<>", "<", "<=", ">", ">="]:
        parser.check_token("RELATIONAL_OPERATOR", token_value)
        relational_operator_node.add_child(ParseNode(f"RELATIONAL_OPERATOR({token_value})"))
        return relational_operator_node
