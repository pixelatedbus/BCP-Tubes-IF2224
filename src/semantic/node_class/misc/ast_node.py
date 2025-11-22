class ASTNode:
    def __init__(self, children=None):
        if children is None:
            children = []
        self.children = children
    
    def add_child(self, child):
        self.children.append(child)

    