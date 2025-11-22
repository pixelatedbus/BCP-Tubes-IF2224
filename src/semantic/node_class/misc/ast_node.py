class ASTNode:
    def __init__(self, children=None):
        if children is None:
            children = []
        self.children = children
    
    def add_child(self, child):
        self.children.append(child)
    
    def to_string(self, prefix="", is_last=True):
        display_name = str(self)
        
        if prefix == "":
            result = display_name + "\n"
        else:
            connector = "└── " if is_last else "├── "
            result = prefix + connector + display_name + "\n"
        
        if prefix == "":
            new_prefix = "    "
        else:
            new_prefix = prefix + ("    " if is_last else "│   ")
        
        for i, child in enumerate(self.children):
            is_last_child = (i == len(self.children) - 1)
            result += child.to_string(new_prefix, is_last_child)
        
        return result
    
    def save_to_file(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(self.to_string())

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        else:
            return self.__class__.__name__

    