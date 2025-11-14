class ParseNode:
    def __init__(self, name):
        self.name = name
        self.children = []
    
    def add_child(self, child):
        if child:
            self.children.append(child)

    def to_string(self, indent=0):
        result = " " * indent + self.name + "\n"
        for child in self.children:
            result += child.to_string(indent + 2)
        return result
    
    def __str__(self):
        return self.to_string()