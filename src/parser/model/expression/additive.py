from ..node import ParseNode

def parse_additive_expression(parent):
    token = parent.current_token()

    if token[0] == 'ARITHMETIC_OPERATOR' and token[1] in ['+', '-']:
        parent.advance()
        return ParseNode(f'ARITHMETIC_OPERATOR({token[1]})')

    if token[0] == 'LOGICAL_OPERATOR' and token[1] in ['atau']:
        parent.advance()
        return ParseNode(f'LOGICAL_OPERATOR({token[1]})')