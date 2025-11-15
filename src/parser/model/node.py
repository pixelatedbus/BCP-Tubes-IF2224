class ParseNode:
    def __init__(self, name):
        self.name = name
        self.children = []
    
    def add_child(self, child):
        if child:
            self.children.append(child)

    def to_string(self, prefix="", is_last=True):
        connector = "└── " if is_last else "├── "
        result = prefix + connector + self.name + "\n"

        if is_last:
            new_prefix = prefix + "    "
        else:
            new_prefix = prefix + "│   "

        for i, child in enumerate(self.children):
            is_last_child = (i == len(self.children) - 1)
            result += child.to_string(new_prefix, is_last_child)

        return result

    def __str__(self):
        return self.to_string()