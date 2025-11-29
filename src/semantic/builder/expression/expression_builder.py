from ...node_class.expression import (
    ExpressionNode,
    SimpleExpressionNode,
    TermNode,
    FactorNode,
    LiteralNode,
    NumberLiteral,
    CharLiteral,
    StringLiteral,
    IdentifierNode,
    FunctionCallNode,
    ArrayAccessNode,
    ParenthesizedExpressionNode,
    UnaryExpressionNode,
)
from ...node_class.expression.field_access_node import FieldAccessNode


def build_expression(parse_node):
    """
    Convert <expression> parse node to ExpressionNode AST.
    Structure: <expression> → <simple_expression> [<relational_operator> <simple_expression>]
    """
    if parse_node.name != "<expression>":
        raise ValueError(f"Expected <expression>, got {parse_node.name}")
    
    left_operand = None
    operator = None
    right_operand = None
    
    for child in parse_node.children:
        if child.name == "<simple_expression>":
            if left_operand is None:
                left_operand = build_simple_expression(child)
            else:
                right_operand = build_simple_expression(child)
        elif child.name == "<relational_operator>":
            operator = extract_relational_operator(child)
    
    return ExpressionNode(left_operand, operator, right_operand)


def build_simple_expression(parse_node):
    """
    Convert <simple_expression> parse node to SimpleExpressionNode AST.
    Structure: <simple_expression> → [+|-] <term> {(+|-|atau) <term>}
    """
    if parse_node.name != "<simple_expression>":
        raise ValueError(f"Expected <simple_expression>, got {parse_node.name}")
    
    simple_expr = SimpleExpressionNode()
    current_operator = None
    
    for child in parse_node.children:
        if child.name == "<term>":
            term = build_term(child)
            simple_expr.add_term(term, current_operator)
            current_operator = None
        elif child.name.startswith("ARITHMETIC_OPERATOR"):
            op_value = extract_token_value(child.name)
            if len(simple_expr.terms) == 0:
                # This is a unary sign
                simple_expr.sign = op_value
            else:
                # This is a binary operator
                current_operator = op_value
        elif child.name.startswith("LOGICAL_OPERATOR"):
            op_value = extract_token_value(child.name)
            if op_value == "atau":
                current_operator = op_value
    
    return simple_expr


def build_term(parse_node):
    """
    Convert <term> parse node to TermNode AST.
    Structure: <term> → <factor> {(*|/|bagi|mod|dan) <factor>}
    """
    if parse_node.name != "<term>":
        raise ValueError(f"Expected <term>, got {parse_node.name}")
    
    term = TermNode()
    current_operator = None
    
    for child in parse_node.children:
        if child.name == "<factor>":
            factor = build_factor(child)
            term.add_factor(factor, current_operator)
            current_operator = None
        elif child.name.startswith("ARITHMETIC_OPERATOR") or child.name.startswith("MULTIPLICATIVE_OPERATOR"):
            current_operator = extract_token_value(child.name)
        elif child.name.startswith("LOGICAL_OPERATOR"):
            op_value = extract_token_value(child.name)
            if op_value == "dan":
                current_operator = op_value
    
    return term


def build_factor(parse_node):
    """
    Convert <factor> parse node to appropriate FactorNode subclass.
    Factor can be:
    - Literal (NUMBER, CHAR_LITERAL, STRING_LITERAL)
    - Identifier (variable)
    - Function call (IDENTIFIER followed by LPAREN)
    - Array access (IDENTIFIER followed by LBRACKET)
    - Parenthesized expression (LPAREN <expression> RPAREN)
    - Unary expression (tidak <factor>)
    """
    if parse_node.name != "<factor>":
        raise ValueError(f"Expected <factor>, got {parse_node.name}")
    
    # Check for literal values
    for child in parse_node.children:
        if child.name.startswith("NUMBER"):
            value = extract_token_value(child.name)
            return NumberLiteral(value)
        elif child.name.startswith("CHAR_LITERAL"):
            value = extract_token_value(child.name)
            return CharLiteral(value)
        elif child.name.startswith("STRING_LITERAL"):
            value = extract_token_value(child.name)
            return StringLiteral(value)
    
    # Check for unary NOT operator
    if len(parse_node.children) >= 2:
        if parse_node.children[0].name.startswith("LOGICAL_OPERATOR"):
            op = extract_token_value(parse_node.children[0].name)
            if op == "tidak":
                operand = build_factor(parse_node.children[1])
                return UnaryExpressionNode(op, operand)
    
    # Check for parenthesized expression
    if len(parse_node.children) >= 3:
        if parse_node.children[0].name.startswith("LPAREN"):
            # Find the expression node
            for child in parse_node.children:
                if child.name == "<expression>":
                    inner_expr = build_expression(child)
                    return ParenthesizedExpressionNode(inner_expr)
    
    # Check for identifier (variable, function call, array access, or field access)
    if parse_node.children and parse_node.children[0].name.startswith("IDENTIFIER"):
        identifier = extract_token_value(parse_node.children[0].name)
        current_node = IdentifierNode(identifier)
        i = 1
        
        # Process chained accessors (function call, array index, field access)
        while i < len(parse_node.children):
            child = parse_node.children[i]
            
            if child.name.startswith("LPAREN"):
                # Function call
                arguments = []
                for j in range(i, len(parse_node.children)):
                    if parse_node.children[j].name == "<parameter_list>":
                        arguments = build_parameter_list(parse_node.children[j])
                        break
                current_node = FunctionCallNode(identifier if isinstance(current_node, IdentifierNode) else str(current_node), arguments)
                i += 1
                # Skip to RPAREN
                while i < len(parse_node.children) and not parse_node.children[i].name.startswith("RPAREN"):
                    i += 1
                i += 1
                
            elif child.name.startswith("LBRACKET"):
                # Array access
                i += 1
                if i < len(parse_node.children) and parse_node.children[i].name == "<expression>":
                    index = build_expression(parse_node.children[i])
                    current_node = ArrayAccessNode(
                        identifier if isinstance(current_node, IdentifierNode) else current_node,
                        index
                    )
                    i += 1
                # Skip RBRACKET
                if i < len(parse_node.children) and parse_node.children[i].name.startswith("RBRACKET"):
                    i += 1
                    
            elif child.name.startswith("DOT"):
                # Field access
                i += 1
                if i < len(parse_node.children) and parse_node.children[i].name.startswith("IDENTIFIER"):
                    field_name = extract_token_value(parse_node.children[i].name)
                    current_node = FieldAccessNode(current_node, field_name)
                    i += 1
            else:
                i += 1
        
        return current_node
    
    raise ValueError(f"Unable to parse factor: {parse_node.name}")


def build_parameter_list(parse_node):
    """
    Convert <parameter_list> parse node to list of ExpressionNode.
    """
    if parse_node.name != "<parameter_list>":
        raise ValueError(f"Expected <parameter_list>, got {parse_node.name}")
    
    arguments = []
    for child in parse_node.children:
        if child.name == "<expression>":
            arguments.append(build_expression(child))
    
    return arguments


def extract_relational_operator(parse_node):
    """Extract the relational operator from <relational_operator> node."""
    if parse_node.name != "<relational_operator>":
        raise ValueError(f"Expected <relational_operator>, got {parse_node.name}")
    
    for child in parse_node.children:
        if child.name.startswith("RELATIONAL_OPERATOR"):
            return extract_token_value(child.name)
    
    return None


def extract_token_value(token_name):
    """
    Extract the value from a token name.
    Example: "NUMBER(42)" → "42", "IDENTIFIER(x)" → "x"
    """
    if "(" in token_name and ")" in token_name:
        return token_name.split("(")[1].rstrip(")")
    return token_name
