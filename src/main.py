from lexer.rule_reader import RuleReader
from lexer.automata import Automata
from parser.parser import Parser
import os
def main():
    # sm = RuleReader.from_file("test/milestone-1/input.json")
    # automata = Automata(sm)
    # test_code = "test/milestone-1/"
    # filename = input("Enter test file name (e.g., test.pas): ")
    # test_code += filename
    # with open(test_code, 'r') as f:
    #     test_code = f.read()

    
    # for char in test_code:
    #     automata.process_char(char)
    # automata.finalize()
    # automata.print_tokens()
    # for error in automata.errors:
    #     print("LEXICAL ERROR:", error)
    # automata.save_tokens()
    
    #create dummy token to test expression parser
    tokens = [
        ("KEYWORD", "program"),
        ("IDENTIFIER", "TestProgram"),
        ("SEMICOLON", ";"),
        ("IDENTIFIER", "a"),
        ("ARITHMETIC_OPERATOR", "+"),
        ("NUMBER", "10"),
        ("SEMICOLON", ";"),
        ("DOT", ".")
    ]   

    parser = Parser(tokens)
    parse_tree = parser.parse_program()
    print(parse_tree)

if __name__ == "__main__":
    main()
