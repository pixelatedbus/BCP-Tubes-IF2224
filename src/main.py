from lexer.rule_reader import RuleReader
from lexer.automata import Automata
from parser.parser import Parser
from semantic.builder.ast_builder import build_ast
from semantic.analyzer.decorator import ASTDecorator
import os
import sys

def main():
    sm = RuleReader.from_file("../test/milestone-1/input_indo.json")
    automata = Automata(sm)
    
    if len(sys.argv) > 1:
        test_code = sys.argv[1]
    else:
        test_code = "../test/milestone-3/"
        filename = input("Enter test file name (e.g., test.pas): ")
        test_code += filename
    
    with open(test_code, 'r') as f:
        test_code = f.read()

    
    for char in test_code:
        automata.process_char(char)
    automata.finalize()
    for error in automata.errors:
        print("LEXICAL ERROR:", error)
    automata.save_tokens("../test/milestone-3/tokens.txt")
    
    parser = Parser(automata.tokens)
    parse_tree = parser.parse_program()

    # print("\nAST:")
    ast = build_ast(parse_tree)

    ast.save_to_file("../test/milestone-3/output_ast.txt")
    
    print("\nSEMANTIC ANALYSIS:")
    decorator = ASTDecorator()
    symbol_table, errors = decorator.decorate(ast)
    
    if errors:
        print(f"Found {len(errors)} semantic error(s):")
        for error in errors:
            print(f"  {error}")
    else:
        print("No semantic errors found.")
    
    print("\nSYMBOL TABLE:")
    print(symbol_table.to_string())
    
    symbol_table.save_to_file("../test/milestone-3/symbol_table.txt")
    print("\nSymbol table saved to ../test/milestone-3/symbol_table.txt")
    
    # Save decorated AST
    decorator.save_decorated_ast(ast, "../test/milestone-3/decorated_ast.txt")
    print("Decorated AST saved to ../test/milestone-3/decorated_ast.txt")

if __name__ == "__main__":
    main()
