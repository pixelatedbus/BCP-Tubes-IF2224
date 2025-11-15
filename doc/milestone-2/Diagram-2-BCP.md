**program:**

![program](diagram/program.svg)

```
program  ::= program_header declaration_part compound_statement '.'
```

**program_header:**

![program_header](diagram/program_header.svg)

```
program_header
         ::= 'program' IDENTIFIER ';'
```

referenced by:

* program

**declaration_part:**

![declaration_part](diagram/declaration_part.svg)

```
declaration_part
         ::= ( const_declaration | type_declaration | var_declaration | subprogram_declaration )*
```

referenced by:

* function_declaration
* procedure_declaration
* program

**const_declaration:**

![const_declaration](diagram/const_declaration.svg)

```
const_declaration
         ::= 'konstanta' ( IDENTIFIER '=' expression ';' )+
```

referenced by:

* declaration_part

**type_declaration:**

![type_declaration](diagram/type_declaration.svg)

```
type_declaration
         ::= 'tipe' ( IDENTIFIER '=' type_spec ';' )+
```

referenced by:

* declaration_part

**var_declaration:**

![var_declaration](diagram/var_declaration.svg)

```
var_declaration
         ::= 'variabel' ( identifier_list ':' type ';' )+
```

referenced by:

* declaration_part

**identifier_list:**

![identifier_list](diagram/identifier_list.svg)

```
identifier_list
         ::= IDENTIFIER ( ',' IDENTIFIER )*
```

referenced by:

* parameter_group
* var_declaration

**type_spec:**

![type_spec](diagram/type_spec.svg)

```
type_spec
         ::= simple_type
           | array_type
           | record_type
           | range
```

referenced by:

* record_type
* type_declaration

**simple_type:**

![simple_type](diagram/simple_type.svg)

```
simple_type
         ::= 'integer'
           | 'real'
           | 'boolean'
           | 'char'
```

referenced by:

* type
* type_spec

**type:**

![type](diagram/type.svg)

```
type     ::= simple_type
```

referenced by:

* array_type
* function_declaration
* parameter_group
* var_declaration

**array_type:**

![array_type](diagram/array_type.svg)

```
array_type
         ::= 'larik' '[' range ']' 'dari' type
```

referenced by:

* type_spec

**record_type:**

![record_type](diagram/record_type.svg)

```
record_type
         ::= 'rekaman' ( IDENTIFIER ':' type_spec ';' )* 'selesai'
```

referenced by:

* type_spec

**range:**

![range](diagram/range.svg)

```
range    ::= expression '..' expression
```

referenced by:

* array_type
* type_spec

**subprogram_declaration:**

![subprogram_declaration](diagram/subprogram_declaration.svg)

```
subprogram_declaration
         ::= function_declaration
           | procedure_declaration
```

referenced by:

* declaration_part

**function_declaration:**

![function_declaration](diagram/function_declaration.svg)

```
function_declaration
         ::= 'fungsi' IDENTIFIER formal_parameter_list? ':' type ';' declaration_part compound_statement ';'
```

referenced by:

* subprogram_declaration

**procedure_declaration:**

![procedure_declaration](diagram/procedure_declaration.svg)

```
procedure_declaration
         ::= 'prosedur' IDENTIFIER formal_parameter_list? ';' declaration_part compound_statement ';'
```

referenced by:

* subprogram_declaration

**formal_parameter_list:**

![formal_parameter_list](diagram/formal_parameter_list.svg)

```
formal_parameter_list
         ::= '(' parameter_group ( ';' parameter_group )* ')'
```

referenced by:

* function_declaration
* procedure_declaration

**parameter_group:**

![parameter_group](diagram/parameter_group.svg)

```
parameter_group
         ::= identifier_list ':' type
```

referenced by:

* formal_parameter_list

**compound_statement:**

![compound_statement](diagram/compound_statement.svg)

```
compound_statement
         ::= 'mulai' statement_list 'selesai'
```

referenced by:

* function_declaration
* procedure_declaration
* program
* single_statement

**statement_list:**

![statement_list](diagram/statement_list.svg)

```
statement_list
         ::= single_statement ( ';' single_statement )*
```

referenced by:

* compound_statement

**single_statement:**

![single_statement](diagram/single_statement.svg)

```
single_statement
         ::= compound_statement
           | if_statement
           | while_statement
           | for_statement
           | assignment_statement
           | procedure_call_statement
```

referenced by:

* for_statement
* if_statement
* statement_list
* while_statement

**assignment_statement:**

![assignment_statement](diagram/assignment_statement.svg)

```
assignment_statement
         ::= IDENTIFIER ':=' expression
```

referenced by:

* single_statement

**procedure_call_statement:**

![procedure_call_statement](diagram/procedure_call_statement.svg)

```
procedure_call_statement
         ::= IDENTIFIER '(' parameter_list ')'
```

referenced by:

* single_statement

**parameter_list:**

![parameter_list](diagram/parameter_list.svg)

```
parameter_list
         ::= expression ( ',' expression )*
```

referenced by:

* procedure_call_statement

**if_statement:**

![if_statement](diagram/if_statement.svg)

```
if_statement
         ::= 'jika' expression 'maka' single_statement ( 'selain_itu' single_statement )?
```

referenced by:

* single_statement

**while_statement:**

![while_statement](diagram/while_statement.svg)

```
while_statement
         ::= 'selama' expression 'lakukan' single_statement
```

referenced by:

* single_statement

**for_statement:**

![for_statement](diagram/for_statement.svg)

```
for_statement
         ::= 'untuk' IDENTIFIER ':=' expression ( 'ke' | 'turun-ke' ) expression 'lakukan' single_statement
```

referenced by:

* single_statement

**relational_operator:**

![relational_operator](diagram/relational_operator.svg)

```
relational_operator
         ::= '='
           | '<>'
           | '<'
           | '<='
           | '>'
           | '>='
```

**additive_operator:**

![additive_operator](diagram/additive_operator.svg)

```
additive_operator
         ::= '+'
           | '-'
           | 'atau'
```

**multiplicative_operator:**

![multiplicative_operator](diagram/multiplicative_operator.svg)

```
multiplicative_operator
         ::= '*'
           | '/'
           | 'bagi'
           | 'mod'
           | 'dan'
```

## 
![Railroad-Diagram-Generator](diagram/Railroad-Diagram-Generator.svg) <sup>generated by [RR - Railroad Diagram Generator][RR]</sup>

[RR]: https://www.bottlecaps.de/rr/ui