class StateMachine:
    def __init__(self):
        self.transition: dict[tuple[str, str], str] = {} 
        self.final_states: dict[str, str] = {} # state -> token type
        self.start_state: str = "start"
        self.reserved_keywords: dict[str, str] = {}

    def add_transition(self, from_state: str, input_char: str, to_state: str):
        input_char = input_char.lower()
        if (from_state, input_char) in self.transition:
            return
        self.transition[(from_state, input_char)] = to_state

    def add_final_state(self, state: str, token_type: str = "IDENTIFIER"):
        self.final_states[state] = token_type

    def set_start_state(self, start_state: str):
        self.start_state = start_state

    def add_reserved_keyword(self, keyword: str, token_type: str = "KEYWORD"):
        self.reserved_keywords[keyword] = token_type

    def get_next_state(self, current_state: str, input_char: str) -> str | None:
        return self.transition.get((current_state, input_char))

    def get_reserved_keywords(self) -> dict[str, str]:
        return self.reserved_keywords
    
    def is_accepting_state(self, state: str) -> bool:
        return state in self.final_states
    
    def get_token_type(self, state: str) -> str | None:
        return self.final_states.get(state)
    
    def get_start_state(self) -> str:
        return self.start_state
    
class Automata:
    def __init__(self, state_machine: StateMachine):
        self.state_machine: StateMachine = state_machine
        self.current_state: str = state_machine.start_state
        self.buffer: str = ""
        self.token_type: str = ""
        self.tokens: list[tuple[str, str]] = [] # List of (token_type, token_value)f
        self.errors: list[str] = [] 

    def reset(self):
        self.current_state = self.state_machine.start_state
        self.buffer = ""
        self.token_type = ""

    def process_char(self, char: str) -> bool:
        char = char.lower() 
        next_state: str | None = self.state_machine.get_next_state(self.current_state, char)
        if next_state:
            # Valid transition
            self.current_state = next_state
            if next_state != self.state_machine.start_state:
                self.buffer += char # ignore chars leading to start state
            if self.state_machine.is_accepting_state(self.current_state):
                self.token_type = self.state_machine.get_token_type(self.current_state)
            return True
        elif self.state_machine.is_accepting_state(self.current_state):
            # No valid transition, but in accepting state. Record token and reset, then reprocess char
            if self.buffer:
                if self.buffer in self.state_machine.get_reserved_keywords(): 
                    self.token_type = self.state_machine.get_reserved_keywords()[self.buffer]
                self.tokens.append((self.token_type, self.buffer))
            self.reset()
            return self.process_char(char)
        # No valid transition and not in accepting state: LEXICAL ERROR
        self.errors.append(f"Unexpected character '{char}' in state '{self.current_state}' with buffer '{self.buffer}'")
        self.reset()
        return False
    
    def finalize(self):
        if self.state_machine.is_accepting_state(self.current_state) and self.buffer:
            self.tokens.append((self.token_type, self.buffer))
        elif self.buffer:
            self.errors.append(f"Incomplete token '{self.buffer}' in state '{self.current_state}' at end of input")
        self.reset()

    def print_tokens(self):
        for token_type, token_value in self.tokens:
            print(f"{token_type}({token_value})")
    
    def save_tokens(self, file_path: str = "test/milestone-2/tokens.txt"):
        with open(file_path, 'w') as file:
            for token_type, token_value in self.tokens:
                file.write(f"{token_type}({token_value})\n")

    def get_tokens(self) -> list[tuple[str, str]]:
        return self.tokens

    def get_errors(self) -> list[str]:
        return self.errors
    
    def analyze(self, input_string: str): # Use this method to process an entire string
        for char in input_string:
            self.process_char(char)
        self.finalize()
