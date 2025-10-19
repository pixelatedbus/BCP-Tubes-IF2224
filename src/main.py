from rule_reader import RuleReader
from automata import Automata
def main():
    sm = RuleReader.from_file("../test/milestone-1/input.json")
    automata = Automata(sm)
    test_code = "../test/milestone-1/"
    filename = input("Enter test file name (e.g., test.pas): ")
    test_code += filename
    with open(test_code, 'r') as f:
        test_code = f.read()

    
    for char in test_code:
        automata.process_char(char)
    automata.finalize()
    automata.print_tokens()
    for error in automata.errors:
        print("LEXICAL ERROR:", error)
    automata.save_tokens()

if __name__ == "__main__":
    main()
