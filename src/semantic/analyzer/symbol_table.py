"""
Symbol Table Implementation
Three-table system: tab (identifiers), atab (arrays), btab (blocks)
"""


class SymbolTableEntry:
    def __init__(self, name, obj, typ, ref=0, nrm=1, lev=0, adr=0, link=0):
        self.name = name        # Identifier name
        self.link = link        # Pointer to previous identifier in same scope
        self.obj = obj          # Object class (constant, variable, type, procedure, function)
        self.type = typ         # Basic type (integer, boolean, char, real, array, record)
        self.ref = ref          # Pointer to atab/btab if composite type
        self.nrm = nrm          # 1 = normal variable, 0 = var parameter (by reference)
        self.lev = lev          # Lexical level (0 = global, 1+ = local)
        self.adr = adr          # Address/offset/value depending on obj type
    
    def __str__(self):
        return (f"Entry(name={self.name}, obj={self.obj}, type={self.type}, "
                f"ref={self.ref}, nrm={self.nrm}, lev={self.lev}, adr={self.adr}, link={self.link})")


class ArrayTableEntry:
    def __init__(self, xtyp, etyp, eref=0, low=0, high=0, elsz=1, size=0):
        self.xtyp = xtyp    # Index type
        self.etyp = etyp    # Element type
        self.eref = eref    # Element reference if composite
        self.low = low      # Lower bound
        self.high = high    # Upper bound
        self.elsz = elsz    # Element size
        self.size = size    # Total array size
    
    def __str__(self):
        return (f"Array(xtyp={self.xtyp}, etyp={self.etyp}, eref={self.eref}, "
                f"low={self.low}, high={self.high}, elsz={self.elsz}, size={self.size})")


class BlockTableEntry:
    def __init__(self, last=0, lpar=0, psze=0, vsze=0):
        self.last = last    # Last identifier in block
        self.lpar = lpar    # Last parameter
        self.psze = psze    # Parameter size
        self.vsze = vsze    # Variable size
    
    def __str__(self):
        return f"Block(last={self.last}, lpar={self.lpar}, psze={self.psze}, vsze={self.vsze})"


class SymbolTable:
    # Object types (obj field)
    OBJ_CONSTANT = 1
    OBJ_VARIABLE = 2
    OBJ_TYPE = 3
    OBJ_PROCEDURE = 4
    OBJ_FUNCTION = 5
    OBJ_PROGRAM = 6
    
    # Basic types (type field) - starting after reserved words (index 29+)
    TYPE_NOTYPE = 0
    TYPE_INTEGER = 1
    TYPE_REAL = 2
    TYPE_BOOLEAN = 3
    TYPE_CHAR = 4
    TYPE_ARRAY = 5
    TYPE_RECORD = 6
    
    # Type sizes
    TYPE_SIZES = {
        TYPE_INTEGER: 4,
        TYPE_REAL: 8,
        TYPE_BOOLEAN: 1,
        TYPE_CHAR: 1,
    }
    
    def __init__(self):
        self.tab = []   # Main identifier table
        self.atab = []  # Array table
        self.btab = []  # Block table
        
        self.current_level = 0
        self.current_block = 0
        self.display = [0]  # Display register for scope management
        self.global_data_size = 0  # Track global variable offsets
        
        # Initialize with reserved words and built-in types (indices 0-28)
        self._init_reserved_words()
        
    def _init_reserved_words(self):
        """Initialize reserved words (indices 0-28)"""
        reserved = [
            "program", "variabel", "var", "mulai", "selesai", "jika", "maka",
            "selain_itu", "selama", "lakukan", "untuk", "ke", "turun-ke",
            "integer", "real", "boolean", "char", "larik", "dari", "prosedur",
            "fungsi", "konstanta", "tipe", "rekaman", "sampai", "ulangi",
            "bagi", "mod", "dan", "atau", "tidak"
        ]
        
        for i, word in enumerate(reserved):
            # Reserved words have special obj type
            self.tab.append(SymbolTableEntry(
                name=word,
                obj=0,  # Reserved word
                typ=self.TYPE_NOTYPE,
                lev=0
            ))
        
        # Add predefined procedures
        predefined_procs = ['write', 'writeln', 'read', 'readln']
        for proc in predefined_procs:
            self.tab.append(SymbolTableEntry(
                name=proc,
                obj=self.OBJ_PROCEDURE,
                typ=self.TYPE_NOTYPE,
                lev=0,
                link=0
            ))
    
    def enter_scope(self):
        """Enter a new scope (procedure/function)"""
        self.current_level += 1
        block_idx = len(self.btab)
        self.btab.append(BlockTableEntry())
        self.display.append(len(self.tab))
        self.current_block = block_idx
        return block_idx
    
    def exit_scope(self):
        """Exit current scope"""
        if self.current_level > 0:
            self.current_level -= 1
            self.display.pop()
            if len(self.display) > 0:
                # Find previous block
                for i in range(len(self.btab) - 1, -1, -1):
                    if i < len(self.btab):
                        self.current_block = i
                        break
    
    def lookup(self, name, level=None):
        if level is None:
            level = self.current_level
        
        # Search from current level backwards
        for lev in range(level, -1, -1):
            if lev < len(self.display):
                start_idx = self.display[lev]
                for i in range(len(self.tab) - 1, start_idx - 1, -1):
                    if self.tab[i].name == name and self.tab[i].lev == lev:
                        return i, self.tab[i]
        
        return None, None
    
    def lookup_current_scope(self, name):
        """Look up identifier only in current scope"""
        if self.current_level < len(self.display):
            start_idx = self.display[self.current_level]
            for i in range(len(self.tab) - 1, start_idx - 1, -1):
                if self.tab[i].name == name and self.tab[i].lev == self.current_level:
                    return i, self.tab[i]
        return None, None
    
    def enter(self, name, obj, typ, ref=0, nrm=1, adr=0, lev=None):
        # Use provided level or current level
        level = lev if lev is not None else self.current_level
        
        # Get link to previous identifier in this scope
        link = 0
        
        # Only create links for identifiers within the same block/scope
        # Link points to previous identifier of similar kind (not programs)
        if level < len(self.display):
            start_idx = self.display[level]
            if len(self.tab) > start_idx:
                # For Level 0: only link variables/constants/types (not program name)
                # For Level > 0: link all identifiers in that block
                if level == 0:
                    # At global level, only link identifiers of the same category (exclude OBJ_PROGRAM)
                    for i in range(len(self.tab) - 1, start_idx - 1, -1):
                        if (self.tab[i].lev == level and i >= 35 and 
                            self.tab[i].obj != self.OBJ_PROGRAM):  # Don't link to program
                            link = i
                            break
                else:
                    # In nested scopes, link to the most recent entry in this scope
                    for i in range(len(self.tab) - 1, start_idx - 1, -1):
                        if self.tab[i].lev == level:
                            link = i
                            break
        
        entry = SymbolTableEntry(
            name=name,
            obj=obj,
            typ=typ,
            ref=ref,
            nrm=nrm,
            lev=level,
            adr=adr,
            link=link
        )
        
        self.tab.append(entry)
        idx = len(self.tab) - 1
        
        # Update block table's last pointer
        # Only update if the identifier's level is > 0 (i.e., it's inside a procedure/function)
        if level > 0:
            # If lev was explicitly provided and is less than current_level,
            # we're declaring something in parent scope (like a nested procedure/function name)
            # In that case, update the parent block's last pointer
            if lev is not None and level < self.current_level:
                # This identifier belongs to parent scope, update parent block
                # The parent block is current_block - 1 (we just entered a new scope)
                parent_block = self.current_block - 1
                if parent_block >= 0 and parent_block < len(self.btab):
                    self.btab[parent_block].last = idx
            elif self.current_block < len(self.btab):
                # Normal case: update current block
                self.btab[self.current_block].last = idx
        
        return idx
    
    def enter_array(self, xtyp, etyp, eref, low, high):
        """
        Enter array type into atab
        Returns index of new entry
        """
        elsz = self.TYPE_SIZES.get(etyp, 1)
        if eref > 0:  # Composite element type
            if eref < len(self.atab):
                elsz = self.atab[eref].size
        
        size = (high - low + 1) * elsz
        
        entry = ArrayTableEntry(
            xtyp=xtyp,
            etyp=etyp,
            eref=eref,
            low=low,
            high=high,
            elsz=elsz,
            size=size
        )
        
        self.atab.append(entry)
        return len(self.atab) - 1
    
    def enter_record(self, fields):
        # Create block entry for record
        btab_idx = len(self.btab)
        self.btab.append(BlockTableEntry())
        
        offset = 0
        last_field_idx = 0
        
        for field in fields:
            field_name = field.get("name", "")
            field_type = field.get("type", "integer")
            
            # Get type code
            if field_type in ['integer', 'real', 'boolean', 'char']:
                type_map = {
                    'integer': self.TYPE_INTEGER,
                    'real': self.TYPE_REAL,
                    'boolean': self.TYPE_BOOLEAN,
                    'char': self.TYPE_CHAR
                }
                type_code = type_map.get(field_type, self.TYPE_INTEGER)
            else:
                type_code = self.TYPE_INTEGER  # Default
            
            field_size = self.TYPE_SIZES.get(type_code, 4)
            
            # Enter field into tab as a special variable
            # Fields have obj=OBJ_VARIABLE, but are linked through btab
            # Use lev=current_level+1 so they don't interfere with normal identifier lookup
            # (fields are conceptually in a nested scope within the record type)
            idx = len(self.tab)
            entry = SymbolTableEntry(
                name=field_name,
                obj=self.OBJ_VARIABLE,
                typ=type_code,
                ref=0,
                nrm=1,
                lev=self.current_level + 1,  # Fields at level beyond current (not searchable via normal lookup)
                adr=offset,
                link=last_field_idx if last_field_idx > 0 else 0
            )
            self.tab.append(entry)
            
            last_field_idx = idx
            offset += field_size
        
        # Update btab entry
        self.btab[btab_idx].last = last_field_idx
        self.btab[btab_idx].lpar = 0  # No parameters
        self.btab[btab_idx].psze = 0  # No parameter size
        self.btab[btab_idx].vsze = offset  # Total record size
        
        return btab_idx
    
    def get_type_size(self, typ, ref=0):
        """Get size of a type"""
        if typ in self.TYPE_SIZES:
            return self.TYPE_SIZES[typ]
        elif typ == self.TYPE_ARRAY and ref < len(self.atab):
            return self.atab[ref].size
        elif typ == self.TYPE_RECORD and ref < len(self.btab):
            return self.btab[ref].vsze  # Record size stored in vsze
        return 1
    
    def to_string(self):
        """Generate formatted string representation of symbol tables"""
        result = []
        
        # Main symbol table (tab)
        result.append("=" * 120)
        result.append("SYMBOL TABLE (tab)")
        result.append("=" * 120)
        result.append(f"{'Index':<6} {'Name':<15} {'Obj':<6} {'Type':<6} {'Ref':<6} {'Nrm':<6} {'Lev':<6} {'Adr':<6} {'Link':<6}")
        result.append("-" * 120)
        
        for i, entry in enumerate(self.tab):
            result.append(
                f"{i:<6} {entry.name:<15} {entry.obj:<6} {entry.type:<6} "
                f"{entry.ref:<6} {entry.nrm:<6} {entry.lev:<6} {entry.adr:<6} {entry.link:<6}"
            )
        
        # Array table (atab)
        if self.atab:
            result.append("\n" + "=" * 120)
            result.append("ARRAY TABLE (atab)")
            result.append("=" * 120)
            result.append(f"{'Index':<6} {'XTyp':<10} {'ETyp':<10} {'ERef':<6} {'Low':<6} {'High':<6} {'ElSz':<6} {'Size':<6}")
            result.append("-" * 120)
            
            for i, entry in enumerate(self.atab):
                xtyp_name = self._type_to_string(entry.xtyp)
                etyp_name = self._type_to_string(entry.etyp)
                result.append(
                    f"{i:<6} {xtyp_name:<10} {etyp_name:<10} {entry.eref:<6} "
                    f"{entry.low:<6} {entry.high:<6} {entry.elsz:<6} {entry.size:<6}"
                )
        
        # Block table (btab)
        if self.btab:
            result.append("\n" + "=" * 120)
            result.append("BLOCK TABLE (btab)")
            result.append("=" * 120)
            result.append(f"{'Index':<6} {'Last':<6} {'LPar':<6} {'PSize':<6} {'VSize':<6}")
            result.append("-" * 120)
            
            for i, entry in enumerate(self.btab):
                result.append(
                    f"{i:<6} {entry.last:<6} {entry.lpar:<6} {entry.psze:<6} {entry.vsze:<6}"
                )
        
        return "\n".join(result)
    
    def _obj_to_string(self, obj):
        """Convert object type to string"""
        obj_map = {
            0: "RESV",
            self.OBJ_CONSTANT: "CONST",
            self.OBJ_VARIABLE: "VAR",
            self.OBJ_TYPE: "TYPE",
            self.OBJ_PROCEDURE: "PROC",
            self.OBJ_FUNCTION: "FUNC",
            self.OBJ_PROGRAM: "PROG",
        }
        return obj_map.get(obj, str(obj))
    
    def _type_to_string(self, typ):
        """Convert type to string"""
        type_map = {
            self.TYPE_NOTYPE: "NONE",
            self.TYPE_INTEGER: "INT",
            self.TYPE_REAL: "REAL",
            self.TYPE_BOOLEAN: "BOOL",
            self.TYPE_CHAR: "CHAR",
            self.TYPE_ARRAY: "ARRAY",
            self.TYPE_RECORD: "REC",
        }
        return type_map.get(typ, str(typ))
    
    def save_to_file(self, filepath):
        """Save symbol table to file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_string())
