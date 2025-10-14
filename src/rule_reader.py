from automata import Automata, StateMachine
import json

class RuleReader:
    @staticmethod
    def from_file(file_path: str) -> StateMachine:
        with open(file_path, 'r') as file:
            rules: dict = json.load(file)
        state_machine = StateMachine()
        state_machine.set_start_state(rules.get("start_state"))
        for final_state, token_type in rules.get("final_states", {}).items():
            state_machine.add_final_state(final_state, token_type)
        
        for keyword in rules.get("keywords", []):
            keyword = keyword.lower()
            state_machine.add_reserved_keyword(keyword)
        
        for state, transitions in rules.items():
            if state in ["start_state", "final_states", "keywords"]:
                continue
            for input_char, next_state in transitions.items():
                state_machine.add_transition(state, input_char, next_state)
        
        return state_machine
    
# TESTING, gunakan 'uv run ./rule_reader.py' di terminal
if __name__ == "__main__":
    sm = RuleReader.from_file("../test/milestone-1/input.json") # INI INPUT RULES MASI DARI AI YA
    automata = Automata(sm)
    test_string = """
program test;
var x, y: integer;
begin
    x := 10;
    y := x + 5;
    writeln(x, y);
end
"""
    
    for char in test_string:
        automata.process_char(char)
    automata.finalize()
    automata.print_tokens()
    automata.errors and print("Errors:", automata.errors) # perlu ignore whitespace secara eksplisit
    automata.save_tokens()
