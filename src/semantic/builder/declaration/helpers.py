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
    return "unknown"


def extract_type_spec(parse_node):
    """Extract type specification from <simple_type>, <range_type>, etc."""
    if parse_node.name == "<simple_type>":
        for child in parse_node.children:
            if child.name.startswith("KEYWORD"):
                return child.name.split("(")[1].rstrip(")")
    
    elif parse_node.name == "<range_type>":
        return "range"
    
    elif parse_node.name == "<array_type>":
        return "array"
    
    elif parse_node.name == "<record_type>":
        return "record"
    
    return "unknown"


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
