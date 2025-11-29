from .symbol_table import SymbolTable

class SemanticError(Exception):
    pass

class ASTDecorator:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
        self.current_function = None
        self.ast_output = []  # Store decorated AST output
    
    def decorate(self, ast_root):
        try:
            self.visit(ast_root)
        except Exception as e:
            self.errors.append(f"Decoration error: {str(e)}")
        
        return self.symbol_table, self.errors
    
    def get_decorated_ast_string(self, node=None, indent=0, prefix="", is_last=True):
        """Generate tree-like string representation of decorated AST"""
        if node is None:
            return ""
        
        result = []
        node_type = type(node).__name__
        
        # Build node representation with annotations
        node_repr = self._build_node_repr(node, node_type)
        
        # Add tree structure
        if indent == 0:
            result.append(node_repr)
        else:
            connector = "└─ " if is_last else "├─ "
            result.append(prefix + connector + node_repr)
        
        # Visit children
        children = self._get_node_children(node, node_type)
        
        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)
            if indent == 0:
                child_prefix = " "
            else:
                child_prefix = prefix + ("   " if is_last else "│  ")
            
            child_str = self.get_decorated_ast_string(child, indent + 1, child_prefix, is_last_child)
            if child_str:
                result.append(child_str)
        
        return "\n".join(result)
    
    def _build_node_repr(self, node, node_type):
        """Build node representation with semantic annotations"""
        parts = [node_type]
        
        # Add node-specific information
        if node_type == "ProgramNode":
            parts[0] = f"ProgramNode(name: '{node.name}')"
            if hasattr(node, 'symbol_idx'):
                parts.append(f" → tab_index:{node.symbol_idx}")
        
        elif node_type in ["VarDeclNode", "ConstDeclNode", "TypeDeclNode"]:
            name = node.name if hasattr(node, 'name') else '?'
            parts[0] = f"{node_type}('{name}')"
            if hasattr(node, 'symbol_idx'):
                parts.append(f" → tab_index:{node.symbol_idx}")
            if hasattr(node, 'type_code'):
                type_name = self._type_code_to_name(node.type_code)
                parts.append(f", type:{type_name}")
            if hasattr(node, 'symbol_idx') and node.symbol_idx < len(self.symbol_table.tab):
                entry = self.symbol_table.tab[node.symbol_idx]
                parts.append(f", lev:{entry.lev}")
        
        elif node_type in ["ProcedureDeclNode", "FunctionDeclNode"]:
            name = node.name if hasattr(node, 'name') else '?'
            parts[0] = f"{node_type}('{name}')"
            if hasattr(node, 'symbol_idx'):
                parts.append(f" → tab_index:{node.symbol_idx}")
            if hasattr(node, 'block_idx'):
                parts.append(f", block_index:{node.block_idx}")
            if node_type == "FunctionDeclNode" and hasattr(node, 'type_code'):
                type_name = self._type_code_to_name(node.type_code)
                parts.append(f", return_type:{type_name}")
        
        elif node_type == "AssignmentStatementNode":
            var_name = node.variable_name if hasattr(node, 'variable_name') else '?'
            parts[0] = f"Assign('{var_name}' := ...)"
            if hasattr(node, 'variable_type'):
                type_name = self._type_code_to_name(node.variable_type)
                parts.append(f" → type:{type_name}")
            if hasattr(node, 'symbol_idx'):
                parts.append(f", tab_index:{node.symbol_idx}")
        
        elif node_type == "IdentifierNode":
            name = node.name if hasattr(node, 'name') else '?'
            parts[0] = f"Identifier('{name}')"
            if hasattr(node, 'symbol_idx'):
                parts.append(f" → tab_index:{node.symbol_idx}")
            if hasattr(node, 'expression_type'):
                type_name = self._type_code_to_name(node.expression_type)
                parts.append(f", type:{type_name}")
        
        elif node_type == "NumberLiteral":
            value = node.value if hasattr(node, 'value') else '?'
            parts[0] = f"NumberLiteral({value})"
            if hasattr(node, 'expression_type'):
                type_name = self._type_code_to_name(node.expression_type)
                parts.append(f" → type:{type_name}")
        
        elif node_type in ["CharLiteral", "StringLiteral"]:
            value = node.value if hasattr(node, 'value') else '?'
            parts[0] = f"{node_type}('{value}')"
            if hasattr(node, 'expression_type'):
                type_name = self._type_code_to_name(node.expression_type)
                parts.append(f" → type:{type_name}")
        
        elif node_type == "ExpressionNode":
            if hasattr(node, 'operator') and node.operator:
                parts[0] = f"Expression(op: '{node.operator}')"
            else:
                parts[0] = "Expression"
            if hasattr(node, 'expression_type'):
                type_name = self._type_code_to_name(node.expression_type)
                parts.append(f" → type:{type_name}")
        
        elif node_type == "SimpleExpressionNode":
            if hasattr(node, 'operators') and node.operators:
                parts[0] = f"SimpleExpression(ops: {node.operators})"
            else:
                parts[0] = "SimpleExpression"
            if hasattr(node, 'expression_type'):
                type_name = self._type_code_to_name(node.expression_type)
                parts.append(f" → type:{type_name}")
        
        elif node_type == "TermNode":
            if hasattr(node, 'operators') and node.operators:
                parts[0] = f"Term(ops: {node.operators})"
            else:
                parts[0] = "Term"
            if hasattr(node, 'expression_type'):
                type_name = self._type_code_to_name(node.expression_type)
                parts.append(f" → type:{type_name}")
        
        elif node_type in ["IfStatementNode", "WhileStatementNode", "ForStatementNode"]:
            if node_type == "ForStatementNode" and hasattr(node, 'variable'):
                parts[0] = f"ForStatement(var: '{node.variable}')"
            else:
                parts[0] = node_type
        
        elif node_type in ["FunctionCallNode", "ProcedureFunctionCallNode"]:
            name = node.function_name if hasattr(node, 'function_name') else (node.name if hasattr(node, 'name') else '?')
            parts[0] = f"{node_type}('{name}')"
            if hasattr(node, 'symbol_idx'):
                parts.append(f" → tab_index:{node.symbol_idx}")
            if hasattr(node, 'expression_type'):
                type_name = self._type_code_to_name(node.expression_type)
                parts.append(f", type:{type_name}")
        
        elif node_type == "ArrayAccessNode":
            name = node.array_name if hasattr(node, 'array_name') else '?'
            parts[0] = f"ArrayAccess('{name}')"
            if hasattr(node, 'symbol_idx'):
                parts.append(f" → tab_index:{node.symbol_idx}")
            if hasattr(node, 'expression_type'):
                type_name = self._type_code_to_name(node.expression_type)
                parts.append(f", elem_type:{type_name}")
        
        return "".join(parts)
    
    def _type_code_to_name(self, type_code):
        type_map = {
            SymbolTable.TYPE_NOTYPE: "notype",
            SymbolTable.TYPE_INTEGER: "integer",
            SymbolTable.TYPE_REAL: "real",
            SymbolTable.TYPE_BOOLEAN: "boolean",
            SymbolTable.TYPE_CHAR: "char",
            SymbolTable.TYPE_ARRAY: "array",
            SymbolTable.TYPE_RECORD: "record"
        }
        return type_map.get(type_code, f"unknown({type_code})")
    
    def _get_node_children(self, node, node_type):
        children = []
        
        # Handle special cases with specific child ordering
        if node_type == "ProgramNode":
            if hasattr(node, 'children'):
                children.extend(node.children)
        
        elif node_type == "DeclarationsNode":
            if hasattr(node, 'children'):
                children.extend(node.children)
        
        elif node_type in ["ProcedureDeclNode", "FunctionDeclNode"]:
            if hasattr(node, 'parameters') and node.parameters:
                for param in node.parameters:
                    children.append(param)
            if hasattr(node, 'declarations') and node.declarations:
                for decl in node.declarations:
                    children.append(decl)
            if hasattr(node, 'children'):
                children.extend(node.children)
        
        elif node_type == "AssignmentStatementNode":
            if hasattr(node, 'value'):
                children.append(node.value)
        
        elif node_type == "ExpressionNode":
            if hasattr(node, 'left_operand'):
                children.append(node.left_operand)
            if hasattr(node, 'right_operand') and node.right_operand:
                children.append(node.right_operand)
        
        elif node_type == "SimpleExpressionNode":
            if hasattr(node, 'terms'):
                children.extend(node.terms)
        
        elif node_type == "TermNode":
            if hasattr(node, 'factors'):
                children.extend(node.factors)
        
        elif node_type == "IfStatementNode":
            if hasattr(node, 'compare'):
                children.append(node.compare)
            if hasattr(node, 'ifbody'):
                children.append(node.ifbody)
            if hasattr(node, 'elsebody') and node.elsebody:
                children.append(node.elsebody)
        
        elif node_type == "WhileStatementNode":
            if hasattr(node, 'condition'):
                children.append(node.condition)
            if hasattr(node, 'children'):
                children.extend(node.children)
        
        elif node_type == "ForStatementNode":
            if hasattr(node, 'start'):
                children.append(node.start)
            if hasattr(node, 'end'):
                children.append(node.end)
            if hasattr(node, 'children'):
                children.extend(node.children)
        
        elif node_type == "ArrayAccessNode":
            if hasattr(node, 'index'):
                children.append(node.index)
        
        elif node_type in ["FunctionCallNode", "ProcedureFunctionCallNode"]:
            if hasattr(node, 'arguments'):
                children.extend(node.arguments)
        
        elif hasattr(node, 'children'):
            children.extend(node.children)
        
        return children
    
    def save_decorated_ast(self, ast_root, filepath):
        """Save decorated AST to file"""
        ast_string = self.get_decorated_ast_string(ast_root)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("Decorated AST:\n")
            f.write("=" * 80 + "\n\n")
            f.write(ast_string)
            f.write("\n")
    
    def visit(self, node):
        node_type = type(node).__name__
        method_name = f'visit_{node_type}'
        
        visitor = getattr(self, method_name, self.visit_generic)
        return visitor(node)
    
    def visit_generic(self, node):
        for child in node.children:
            self.visit(child)
    
    def visit_ProgramNode(self, node):
        # Add program name to symbol table
        idx = self.symbol_table.enter(
            name=node.name,
            obj=SymbolTable.OBJ_PROGRAM,
            typ=SymbolTable.TYPE_NOTYPE,
            nrm=1,
            adr=0
        )
        node.symbol_idx = idx
        
        # Program is at global scope (level 0)
        for child in node.children:
            self.visit(child)
    
    def visit_DeclarationsNode(self, node):
        for child in node.children:
            self.visit(child)
    
    def visit_VarDeclNode(self, node):
        idx, existing = self.symbol_table.lookup_current_scope(node.name)
        if existing is not None:
            self.errors.append(
                f"Error: Variable '{node.name}' already declared in current scope"
            )
            return
        
        # Process type spec (handles strings, dicts, etc.)
        type_code, ref = self.process_type_spec(node.var_type)
        
        # Calculate address based on scope
        if self.symbol_table.current_level == 0:
            # Global variable: use global data size
            adr = self.symbol_table.global_data_size
            type_size = self.symbol_table.get_type_size(type_code, ref)
            self.symbol_table.global_data_size += type_size
        else:
            # Local variable: use block vsze
            adr = self.calculate_address()
        
        idx = self.symbol_table.enter(
            name=node.name,
            obj=SymbolTable.OBJ_VARIABLE,
            typ=type_code,
            ref=ref,
            nrm=1,
            adr=adr
        )
        
        node.symbol_idx = idx
        node.type_code = type_code
        
        # Update block table: last pointer and VSize for local variables
        if self.symbol_table.current_level > 0 and self.symbol_table.current_block < len(self.symbol_table.btab):
            # Only add to VSize if this is a local variable (not a parameter)
            # Parameters have already been counted in PSize
            block = self.symbol_table.btab[self.symbol_table.current_block]
            
            # Check if this variable comes after the last parameter
            if block.lpar == 0 or idx > block.lpar:
                type_size = self.symbol_table.get_type_size(type_code, ref)
                block.vsze += type_size
            
            # Always update the last pointer to the most recent identifier
            block.last = idx
    
    def visit_ConstDeclNode(self, node):
        idx, existing = self.symbol_table.lookup_current_scope(node.name)
        if existing is not None:
            self.errors.append(
                f"Error: Constant '{node.name}' already declared in current scope"
            )
            return
        
        type_code = self.infer_constant_type(node.value)
        
        # Store constant value in adr field
        const_value = node.value
        if isinstance(const_value, str):
            # Try to convert string to int
            try:
                const_value = int(const_value)
            except ValueError:
                try:
                    const_value = int(float(const_value))
                except ValueError:
                    const_value = 0
        
        idx = self.symbol_table.enter(
            name=node.name,
            obj=SymbolTable.OBJ_CONSTANT,
            typ=type_code,
            adr=const_value
        )
        
        node.symbol_idx = idx
        node.type_code = type_code
    
    def visit_TypeDeclNode(self, node):
        idx, existing = self.symbol_table.lookup_current_scope(node.name)
        if existing is not None:
            self.errors.append(
                f"Error: Type '{node.name}' already declared in current scope"
            )
            return
        
        ref = 0
        type_code = SymbolTable.TYPE_NOTYPE
        
        if hasattr(node, 'type_spec'):
            type_code, ref = self.process_type_spec(node.type_spec)
        
        idx = self.symbol_table.enter(
            name=node.name,
            obj=SymbolTable.OBJ_TYPE,
            typ=type_code,
            ref=ref
        )
        
        node.symbol_idx = idx
        node.type_code = type_code
    
    def visit_ProcedureDeclNode(self, node):
        idx, existing = self.symbol_table.lookup_current_scope(node.name)
        if existing is not None:
            self.errors.append(
                f"Error: Procedure '{node.name}' already declared in current scope"
            )
            return
        
        # Create new block for procedure
        block_idx = self.symbol_table.enter_scope()
        
        # Enter procedure name in symbol table with reference to its block
        idx = self.symbol_table.enter(
            name=node.name,
            obj=SymbolTable.OBJ_PROCEDURE,
            typ=SymbolTable.TYPE_NOTYPE,
            ref=block_idx,
            lev=self.symbol_table.current_level - 1  # Procedure declared in parent scope
        )
        
        node.symbol_idx = idx
        node.block_idx = block_idx
        
        if hasattr(node, 'parameters') and node.parameters:
            self.process_parameters(node.parameters, block_idx)
        
        # Visit local declarations
        if hasattr(node, 'declarations') and node.declarations:
            for decl in node.declarations:
                self.visit(decl)
        
        # Visit body and other children
        for child in node.children:
            self.visit(child)
        
        self.symbol_table.exit_scope()
    
    def visit_FunctionDeclNode(self, node):
        idx, existing = self.symbol_table.lookup_current_scope(node.name)
        if existing is not None:
            self.errors.append(
                f"Error: Function '{node.name}' already declared in current scope"
            )
            return
        
        # Create new block for function
        block_idx = self.symbol_table.enter_scope()
        self.current_function = node.name
        
        return_type = self.get_type_code(node.return_type)
        
        # Enter function name in symbol table with reference to its block
        idx = self.symbol_table.enter(
            name=node.name,
            obj=SymbolTable.OBJ_FUNCTION,
            typ=return_type,
            ref=block_idx,
            lev=self.symbol_table.current_level - 1  # Function declared in parent scope
        )
        
        node.symbol_idx = idx
        node.block_idx = block_idx
        node.type_code = return_type
        
        if hasattr(node, 'parameters') and node.parameters:
            self.process_parameters(node.parameters, block_idx)
        
        # Visit local declarations
        if hasattr(node, 'declarations') and node.declarations:
            for decl in node.declarations:
                self.visit(decl)
        
        # Visit body and other children
        for child in node.children:
            self.visit(child)
        
        self.current_function = None
        self.symbol_table.exit_scope()
    
    def process_parameters(self, parameters, block_idx):
        param_offset = 0
        last_param_idx = 0
        
        for param in parameters:
            type_code = self.get_type_code(param.param_type)
            nrm = 0 if param.is_var else 1
            
            idx = self.symbol_table.enter(
                name=param.name,
                obj=SymbolTable.OBJ_VARIABLE,
                typ=type_code,
                nrm=nrm,
                adr=param_offset
            )
            
            param.symbol_idx = idx
            param.type_code = type_code
            
            type_size = self.symbol_table.get_type_size(type_code)
            param_offset += type_size
            last_param_idx = idx
        
        if block_idx < len(self.symbol_table.btab):
            self.symbol_table.btab[block_idx].lpar = last_param_idx
            self.symbol_table.btab[block_idx].psze = param_offset
    
    def visit_BlockNode(self, node):
        for child in node.children:
            self.visit(child)
    
    def visit_AssignmentStatementNode(self, node):
        # Handle composite LHS (array access, field access)
        if hasattr(node, 'lhs_node') and node.lhs_node is not None:
            lhs_type = self.get_lhs_type(node.lhs_node)
            node.variable_type = lhs_type
        else:
            # Simple variable assignment
            idx, entry = self.symbol_table.lookup(node.variable_name)
            if entry is None:
                self.errors.append(
                    f"Error: Undefined variable '{node.variable_name}'"
                )
                return
            
            if entry.obj != SymbolTable.OBJ_VARIABLE:
                self.errors.append(
                    f"Error: '{node.variable_name}' is not a variable"
                )
                return
            
            node.symbol_idx = idx
            node.variable_type = entry.type
            lhs_type = entry.type
        
        if hasattr(node, 'value'):
            expr_type = self.visit_expression(node.value)
            node.expression_type = expr_type
            
            if not self.types_compatible(lhs_type, expr_type):
                self.errors.append(
                    f"Error: Type mismatch in assignment to '{node.variable_name}'"
                )
    
    def visit_expression(self, node):
        node_type = type(node).__name__
        
        if node_type == 'ExpressionNode':
            return self.visit_ExpressionNode(node)
        elif node_type == 'SimpleExpressionNode':
            return self.visit_SimpleExpressionNode(node)
        elif node_type == 'TermNode':
            return self.visit_TermNode(node)
        else:
            return self.visit_factor(node)
    
    def visit_ExpressionNode(self, node):
        left_type = self.visit_expression(node.left_operand)
        
        if node.operator is not None:
            right_type = self.visit_expression(node.right_operand)
            
            if not self.types_compatible(left_type, right_type):
                self.errors.append("Error: Type mismatch in comparison")
            
            node.expression_type = SymbolTable.TYPE_BOOLEAN
            return SymbolTable.TYPE_BOOLEAN
        
        node.expression_type = left_type
        return left_type
    
    def visit_SimpleExpressionNode(self, node):
        if not node.terms:
            return SymbolTable.TYPE_NOTYPE
        
        result_type = self.visit_expression(node.terms[0])
        
        if node.operators and 'atau' in node.operators:
            result_type = SymbolTable.TYPE_BOOLEAN
        
        for i, term in enumerate(node.terms[1:]):
            term_type = self.visit_expression(term)
            
            if i < len(node.operators):
                op = node.operators[i]
                if op in ['+', '-']:
                    if result_type == SymbolTable.TYPE_REAL or term_type == SymbolTable.TYPE_REAL:
                        result_type = SymbolTable.TYPE_REAL
        
        node.expression_type = result_type
        return result_type
    
    def visit_TermNode(self, node):
        if not node.factors:
            return SymbolTable.TYPE_NOTYPE
        
        result_type = self.visit_factor(node.factors[0])
        
        if node.operators and 'dan' in node.operators:
            result_type = SymbolTable.TYPE_BOOLEAN
        
        for i, factor in enumerate(node.factors[1:]):
            factor_type = self.visit_factor(factor)
            
            if i < len(node.operators):
                op = node.operators[i]
                if op in ['*', '/', 'bagi', 'mod']:
                    if result_type == SymbolTable.TYPE_REAL or factor_type == SymbolTable.TYPE_REAL:
                        result_type = SymbolTable.TYPE_REAL
        
        node.expression_type = result_type
        return result_type
    
    def visit_factor(self, node):
        node_type = type(node).__name__
        
        if node_type == 'NumberLiteral':
            if '.' in str(node.value):
                node.expression_type = SymbolTable.TYPE_REAL
                return SymbolTable.TYPE_REAL
            node.expression_type = SymbolTable.TYPE_INTEGER
            return SymbolTable.TYPE_INTEGER
        
        elif node_type == 'CharLiteral':
            node.expression_type = SymbolTable.TYPE_CHAR
            return SymbolTable.TYPE_CHAR
        
        elif node_type == 'StringLiteral':
            node.expression_type = SymbolTable.TYPE_CHAR
            return SymbolTable.TYPE_CHAR
        
        elif node_type == 'IdentifierNode':
            idx, entry = self.symbol_table.lookup(node.name)
            if entry is None:
                self.errors.append(f"Error: Undefined identifier '{node.name}'")
                return SymbolTable.TYPE_NOTYPE
            
            node.symbol_idx = idx
            node.expression_type = entry.type
            return entry.type
        
        elif node_type == 'UnaryExpressionNode':
            operand_type = self.visit_factor(node.operand)
            node.expression_type = SymbolTable.TYPE_BOOLEAN
            return SymbolTable.TYPE_BOOLEAN
        
        elif node_type == 'ParenthesizedExpressionNode':
            expr_type = self.visit_expression(node.expression)
            node.expression_type = expr_type
            return expr_type
        
        elif node_type == 'FunctionCallNode':
            return self.visit_FunctionCallNode(node)
        
        elif node_type == 'ArrayAccessNode':
            return self.visit_ArrayAccessNode(node)
        
        elif node_type == 'FieldAccessNode':
            return self.visit_FieldAccessNode(node)
        
        return SymbolTable.TYPE_NOTYPE
    
    def visit_FunctionCallNode(self, node):
        idx, entry = self.symbol_table.lookup(node.function_name)
        if entry is None:
            self.errors.append(f"Error: Undefined function '{node.function_name}'")
            return SymbolTable.TYPE_NOTYPE
        
        if entry.obj != SymbolTable.OBJ_FUNCTION and entry.obj != SymbolTable.OBJ_PROCEDURE:
            self.errors.append(f"Error: '{node.function_name}' is not a function")
            return SymbolTable.TYPE_NOTYPE
        
        node.symbol_idx = idx
        node.expression_type = entry.type
        
        for arg in node.arguments:
            self.visit_expression(arg)
        
        return entry.type
    
    def visit_ArrayAccessNode(self, node):
        # Get type and ref info from array base (string or nested node)
        array_ref = None
        
        if isinstance(node.array_name, str):
            # Simple case: array_name is identifier string
            idx, entry = self.symbol_table.lookup(node.array_name)
            if entry is None:
                self.errors.append(f"Error: Undefined array '{node.array_name}'")
                return SymbolTable.TYPE_NOTYPE
            
            if entry.type != SymbolTable.TYPE_ARRAY:
                self.errors.append(f"Error: '{node.array_name}' is not an array")
                return SymbolTable.TYPE_NOTYPE
            
            node.symbol_idx = idx
            array_ref = entry.ref
        else:
            # Nested access: array_name is another node
            base_type = self.visit_factor(node.array_name)
            
            # Get the ref based on base node type
            if base_type == SymbolTable.TYPE_ARRAY:
                # Base is array - get eref from the array's atab entry
                if hasattr(node.array_name, 'array_ref'):
                    array_ref = node.array_name.array_ref
                else:
                    self.errors.append(f"Error: Cannot determine array element type")
                    return SymbolTable.TYPE_NOTYPE
            elif base_type == SymbolTable.TYPE_RECORD:
                # This shouldn't happen for array access - field should come first
                self.errors.append(f"Error: Indexed expression is not an array")
                return SymbolTable.TYPE_NOTYPE
            else:
                self.errors.append(f"Error: Indexed expression is not an array")
                return SymbolTable.TYPE_NOTYPE
        
        # Visit the index expression
        self.visit_expression(node.index)
        
        # Get element type from atab
        if array_ref is not None and array_ref < len(self.symbol_table.atab):
            elem_type = self.symbol_table.atab[array_ref].etyp
            elem_ref = self.symbol_table.atab[array_ref].eref
            node.expression_type = elem_type
            node.array_ref = elem_ref  # Store ref for further nesting
            node.elem_type = elem_type
            return elem_type
        
        return SymbolTable.TYPE_NOTYPE
    
    def visit_FieldAccessNode(self, node):
        # Get type of the record expression (base)
        record_expr_type = self.visit_factor(node.record_expr)
        
        if record_expr_type != SymbolTable.TYPE_RECORD:
            self.errors.append(f"Error: Field access on non-record type")
            return SymbolTable.TYPE_NOTYPE
        
        # Get the btab ref from the record expression
        record_ref = None
        if hasattr(node.record_expr, 'array_ref') and hasattr(node.record_expr, 'elem_type') and node.record_expr.elem_type == SymbolTable.TYPE_RECORD:
            # Record came from array element
            record_ref = node.record_expr.array_ref
        elif hasattr(node.record_expr, 'record_ref') and node.record_expr.record_ref > 0:
            # Record came from nested field
            record_ref = node.record_expr.record_ref
        elif hasattr(node.record_expr, 'name'):
            # Simple identifier - look it up
            idx, entry = self.symbol_table.lookup(node.record_expr.name)
            if entry and entry.type == SymbolTable.TYPE_RECORD:
                record_ref = entry.ref
        
        # Look up field in btab
        if record_ref is not None and record_ref < len(self.symbol_table.btab):
            # Search for field in the record's scope
            btab_entry = self.symbol_table.btab[record_ref]
            last_idx = btab_entry.last
            
            # Search backwards through tab for field
            field_type = SymbolTable.TYPE_INTEGER  # Default assumption
            field_ref = 0
            
            # Simple field lookup - iterate through record fields
            idx = last_idx
            while idx > 0:
                entry = self.symbol_table.tab[idx]
                if entry.obj == SymbolTable.OBJ_VARIABLE and entry.name == node.field_name:
                    field_type = entry.type
                    field_ref = entry.ref
                    break
                if entry.link == 0:
                    break
                idx = entry.link
            
            node.expression_type = field_type
            node.field_type = field_type
            node.array_ref = field_ref if field_type == SymbolTable.TYPE_ARRAY else 0
            node.record_ref = field_ref if field_type == SymbolTable.TYPE_RECORD else 0
            return field_type
        
        # Fallback - assume integer field
        node.expression_type = SymbolTable.TYPE_INTEGER
        return SymbolTable.TYPE_INTEGER
    
    def get_lhs_type(self, lhs_node):
        """Get the type of a left-hand side expression (for assignments)"""
        # Just visit the node and let it determine its own type
        return self.visit_factor(lhs_node)
    
    def visit_IfStatementNode(self, node):
        if hasattr(node, 'compare'):
            cond_type = self.visit_expression(node.compare)
            if cond_type != SymbolTable.TYPE_BOOLEAN:
                self.errors.append("Error: If condition must be boolean")
        
        if hasattr(node, 'ifbody'):
            self.visit(node.ifbody)
        if hasattr(node, 'elsebody'):
            self.visit(node.elsebody)
    
    def visit_WhileStatementNode(self, node):
        if hasattr(node, 'condition'):
            cond_type = self.visit_expression(node.condition)
            if cond_type != SymbolTable.TYPE_BOOLEAN:
                self.errors.append("Error: While condition must be boolean")
        
        for child in node.children:
            self.visit(child)
    
    def visit_ForStatementNode(self, node):
        if hasattr(node, 'variable'):
            idx, entry = self.symbol_table.lookup(node.variable)
            if entry is None:
                self.errors.append(f"Error: Undefined loop variable '{node.variable}'")
            elif entry.type != SymbolTable.TYPE_INTEGER:
                self.errors.append("Error: Loop variable must be integer")
            else:
                node.symbol_idx = idx
        
        if hasattr(node, 'start'):
            self.visit_expression(node.start)
        if hasattr(node, 'end'):
            self.visit_expression(node.end)
        
        for child in node.children:
            self.visit(child)
    
    def visit_ProcedureFunctionCallNode(self, node):
        idx, entry = self.symbol_table.lookup(node.name)
        if entry is None:
            self.errors.append(f"Error: Undefined procedure/function '{node.name}'")
            return
        
        node.symbol_idx = idx
        
        if hasattr(node, 'arguments'):
            for arg in node.arguments:
                self.visit_expression(arg)
    
    def get_type_code(self, type_name):
        type_map = {
            'integer': SymbolTable.TYPE_INTEGER,
            'real': SymbolTable.TYPE_REAL,
            'boolean': SymbolTable.TYPE_BOOLEAN,
            'char': SymbolTable.TYPE_CHAR,
        }
        return type_map.get(type_name.lower(), SymbolTable.TYPE_NOTYPE)
    
    def infer_constant_type(self, value):
        return SymbolTable.TYPE_INTEGER
    
    def process_type_spec(self, type_spec):
        """Process type specification and return (type_code, ref)"""
        # Handle simple type strings
        if isinstance(type_spec, str):
            if type_spec in ['integer', 'real', 'boolean', 'char']:
                return self.get_type_code(type_spec), 0
            # Look up user-defined type
            type_idx, type_entry = self.symbol_table.lookup(type_spec)
            if type_entry and type_entry.obj == SymbolTable.OBJ_TYPE:
                return type_entry.type, type_entry.ref
            # Unknown type - return TYPE_NOTYPE
            return SymbolTable.TYPE_NOTYPE, 0
        
        # Handle array type dictionary
        if isinstance(type_spec, dict) and type_spec.get("type") == "array":
            # Get element type (can be string or nested dict)
            elem_type_info = type_spec.get("element_type", "integer")
            elem_type_code = SymbolTable.TYPE_NOTYPE
            elem_ref = 0
            
            # Check if element_type is a dict (nested array or record)
            if isinstance(elem_type_info, dict):
                # Recursively process nested type
                elem_type_code, elem_ref = self.process_type_spec(elem_type_info)
            elif isinstance(elem_type_info, str):
                # Check if it's a basic type
                if elem_type_info in ['integer', 'real', 'boolean', 'char']:
                    elem_type_code = self.get_type_code(elem_type_info)
                else:
                    # Look up user-defined type
                    type_idx, type_entry = self.symbol_table.lookup(elem_type_info)
                    if type_entry and type_entry.obj == SymbolTable.OBJ_TYPE:
                        elem_type_code = type_entry.type
                        elem_ref = type_entry.ref
            
            # Get bounds
            low = type_spec.get("low", 0)
            high = type_spec.get("high", 0)
            
            # Index type is always integer for now
            xtyp = SymbolTable.TYPE_INTEGER
            
            # Create entry in atab
            atab_idx = self.symbol_table.enter_array(
                xtyp=xtyp,
                etyp=elem_type_code,
                eref=elem_ref,
                low=low,
                high=high
            )
            
            return SymbolTable.TYPE_ARRAY, atab_idx
        
        # Handle record type dictionary
        if isinstance(type_spec, dict) and type_spec.get("type") == "record":
            fields = type_spec.get("fields", [])
            
            # Create entry in rtab
            rtab_idx = self.symbol_table.enter_record(fields)
            
            return SymbolTable.TYPE_RECORD, rtab_idx
        
        return SymbolTable.TYPE_NOTYPE, 0
    
    def calculate_address(self):
        if self.symbol_table.current_block < len(self.symbol_table.btab):
            return self.symbol_table.btab[self.symbol_table.current_block].vsze
        return 0
    
    def types_compatible(self, type1, type2):
        if type1 == type2:
            return True
        if {type1, type2} == {SymbolTable.TYPE_INTEGER, SymbolTable.TYPE_REAL}:
            return True
        # Allow integer to boolean (for 1/0 as true/false)
        if {type1, type2} == {SymbolTable.TYPE_INTEGER, SymbolTable.TYPE_BOOLEAN}:
            return True
        return False
