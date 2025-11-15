class ParseNode:
    def __init__(self, name):
        self.name = name
        self.children = []
    
    def add_child(self, child):
        if child:
            self.children.append(child)

    def to_string(self, prefix="", is_last=True):
        if prefix == "":
            result = self.name + "\n"
        else:
            connector = "└── " if is_last else "├── "
            result = prefix + connector + self.name + "\n"

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
        return self.to_string()