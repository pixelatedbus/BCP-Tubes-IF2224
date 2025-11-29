import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from node_class.declaration.parameter_node import ParameterNode


def extract_identifier_list(parse_node):
    """Extract list of identifiers from <identifier_list>"""
    identifiers = []
    for child in parse_node.children:
        if child.name.startswith("IDENTIFIER"):
            identifier = child.name.split("(")[1].rstrip(")")
            identifiers.append(identifier)
    return identifiers


def extract_type(parse_node):
    """Extract type from <type> node"""
    for child in parse_node.children:
        if child.name.startswith("KEYWORD"):
            return child.name.split("(")[1].rstrip(")")
        elif child.name.startswith("IDENTIFIER"):
            # User-defined type
            return child.name.split("(")[1].rstrip(")")
        elif child.name.startswith("<"):
            # Nested type spec (array, record, etc.)
            return extract_type_spec(child)
    return "unknown"


def extract_type_spec(parse_node):
    """Extract type specification from <simple_type>, <range_type>, etc."""
    if parse_node.name == "<simple_type>":
        for child in parse_node.children:
            if child.name.startswith("KEYWORD"):
                return child.name.split("(")[1].rstrip(")")
    
    elif parse_node.name == "<custom_type>":
        # User-defined type name
        for child in parse_node.children:
            if child.name.startswith("IDENTIFIER"):
                return child.name.split("(")[1].rstrip(")")
        return "unknown"
    
    elif parse_node.name == "<range_type>":
        return "range"
    
    elif parse_node.name == "<array_type>":
        # Extract array bounds and element type
        # Structure: larik[low..high] dari element_type
        array_info = {"type": "array"}
        
        for child in parse_node.children:
            if child.name == "<range>":
                # Extract low and high bounds
                bounds = extract_range_bounds(child)
                array_info["low"] = bounds["low"]
                array_info["high"] = bounds["high"]
            elif child.name == "<type>":
                # Extract element type
                array_info["element_type"] = extract_type(child)
        
        return array_info
    
    elif parse_node.name == "<record_type>":
        # Extract record fields
        fields = extract_record_fields(parse_node)
        return {"type": "record", "fields": fields}
    
    return "unknown"


def extract_range_bounds(range_node):
    """Extract low and high bounds from <range> node"""
    bounds = {"low": 0, "high": 0}
    numbers = []
    
    def extract_number_from_node(node):
        """Recursively extract numbers from node"""
        if node.name.startswith("NUMBER"):
            num_str = node.name.split("(")[1].rstrip(")")
            return int(num_str)
        # Numbers might be wrapped in expression nodes
        for child in node.children:
            num = extract_number_from_node(child)
            if num is not None:
                return num
        return None
    
    for child in range_node.children:
        num = extract_number_from_node(child)
        if num is not None:
            numbers.append(num)
    
    if len(numbers) >= 2:
        bounds["low"] = numbers[0]
        bounds["high"] = numbers[1]
    
    return bounds


def extract_simple_value(parse_node):
    """Extract simple constant value dari <expression> node"""
    # Untuk konstanta sederhana, cari NUMBER atau STRING_LITERAL
    if parse_node.name == "<expression>":
        for child in parse_node.children:
            if child.name == "<simple_expression>":
                return extract_simple_value(child)
    
    elif parse_node.name == "<simple_expression>":
        for child in parse_node.children:
            if child.name == "<term>":
                return extract_simple_value(child)
    
    elif parse_node.name == "<term>":
        for child in parse_node.children:
            if child.name == "<factor>":
                return extract_simple_value(child)
    
    elif parse_node.name == "<factor>":
        for child in parse_node.children:
            if child.name.startswith("NUMBER"):
                return child.name.split("(")[1].rstrip(")")
            elif child.name.startswith("STRING_LITERAL"):
                return child.name.split("(")[1].rstrip(")")
            elif child.name.startswith("CHAR_LITERAL"):
                return child.name.split("(")[1].rstrip(")")
    
    return None


def extract_parameters(parse_node):
    parameters = []
    
    for child in parse_node.children:
        if child.name == "<parameter-group>":
            identifiers = []
            param_type = "unknown"
            is_var = False
            
            for subchild in child.children:
                if subchild.name == "<identifier_list>":
                    identifiers = extract_identifier_list(subchild)
                elif subchild.name == "<type>":
                    param_type = extract_type(subchild)
                elif subchild.name.startswith("KEYWORD") and "var" in subchild.name.lower():
                    is_var = True
            
            for identifier in identifiers:
                param_node = ParameterNode(identifier, param_type, is_var)
                parameters.append(param_node)
    
    return parameters


def extract_record_fields(parse_node):
    """Extract field declarations from <record_type> node"""
    fields = []
    i = 0
    children = parse_node.children
    
    # Skip 'rekaman' keyword
    if i < len(children) and children[i].name.startswith("KEYWORD"):
        i += 1
    
    # Extract fields until 'selesai'
    while i < len(children):
        if children[i].name.startswith("KEYWORD") and "selesai" in children[i].name:
            break
        
        # Field name
        if children[i].name.startswith("IDENTIFIER"):
            field_name = children[i].name.split("(")[1].rstrip(")")
            i += 1
            
            # Skip colon
            if i < len(children) and children[i].name.startswith("COLON"):
                i += 1
            
            # Field type
            field_type = "unknown"
            if i < len(children) and children[i].name.startswith("<"):
                field_type = extract_type_spec(children[i])
                i += 1
            
            fields.append({"name": field_name, "type": field_type})
            
            # Skip semicolon
            if i < len(children) and children[i].name.startswith("SEMICOLON"):
                i += 1
        else:
            i += 1
    
    return fields
