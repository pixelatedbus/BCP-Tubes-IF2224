from automata import Automata, StateMachine
import json

class RuleReader:
    @staticmethod
    def expand_char_range(char_range: str) -> list[str]:
        list_chars: list[str] = []
        i = 0
        while i < len(char_range):
            if i + 2 < len(char_range) and char_range[i + 1] == '-':
                start_char, end_char = char_range[i], char_range[i + 2]
                
                list_chars.extend([chr(c) for c in range(ord(start_char), ord(end_char) + 1)])
                
                i += 3
            else:
                list_chars.append(char_range[i])
                i += 1

        return list_chars

    @staticmethod
    def from_file(file_path: str) -> StateMachine:
        with open(file_path, 'r') as file:
            rules: dict = json.load(file)
        state_machine = StateMachine()
        state_machine.set_start_state(rules.get("start_state"))
        for final_state, token_type in rules.get("final_states", {}).items():
            state_machine.add_final_state(final_state, token_type)

        for keyword, token_type in rules.get("keywords", {}).items():
            state_machine.add_reserved_keyword(keyword, token_type)

        for state, transitions in rules.items():
            if state in ["start_state", "final_states", "keywords"]:
                continue
            for input_char, next_state in transitions.items():
                if len(input_char) > 1:
                    expanded_chars = RuleReader.expand_char_range(input_char)
                    for char in expanded_chars:
                        state_machine.add_transition(state, char, next_state)
                else:
                    state_machine.add_transition(state, input_char, next_state)
        
        return state_machine
    
# if __name__ == "__main__":
#     sm = RuleReader.from_file("../test/milestone-1/input.json")
#     automata = Automata(sm)
#     test_code = "../test/milestone-1/"
#     filename = input("Enter test file name (e.g., test.pas): ")
#     test_code += filename
#     with open(test_code, 'r') as f:
#         test_code = f.read()

    
#     for char in test_code:
#         automata.process_char(char)
#     automata.finalize()
#     automata.print_tokens()
#     automata.errors and print("Errors:", automata.errors)
#     automata.save_tokens()
