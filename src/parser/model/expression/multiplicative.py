from ..node import ParseNode

def parse_multiplicative_expression(parent):
    token = parent.current_token()
    
    if token[0] == 'ARITHMETIC_OPERATOR' and token[1] in ['*', '/', 'bagi', 'mod']:
        parent.advance()
        return ParseNode(f'MULTIPLICATIVE_OPERATOR({token[1]})')
    
    if token[0] == 'LOGICAL_OPERATOR' and token[1] in ['dan']:
        parent.advance()
        return ParseNode(f'MULTIPLICATIVE_OPERATOR({token[1]})')