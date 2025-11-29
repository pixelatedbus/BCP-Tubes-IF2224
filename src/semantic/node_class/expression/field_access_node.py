from .factor_node import FactorNode

class FieldAccessNode(FactorNode):
    """
    Represents record field access.
    Example: point.x, person.name
    """
    def __init__(self, record_expr, field_name):
        super().__init__()
        self.record_expr = record_expr  # ExpressionNode or identifier string
        self.field_name = field_name  # String: name of the field
        
        # If record_expr is a node, add it as a child
        if hasattr(record_expr, 'add_child'):
            self.add_child(record_expr)
    
    def __str__(self):
        if isinstance(self.record_expr, str):
            return f"FieldAccessNode({self.record_expr}.{self.field_name})"
        return f"FieldAccessNode({self.record_expr}.{self.field_name})"
