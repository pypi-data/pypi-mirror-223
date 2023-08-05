class State:
    current_state: str = ''

    def __init__(self) -> None:
        self.states = []

    def current_state_func(self): return self.current_state
    def current_state_list(self): return self.states

    def new_state(self, *states):
        for state in states:
            self.states.append(state)
            
        self.current_state = self.states[0]
    
    def clear_state(self, *states):
        for state in states:
            self.states.remove(state)
    
    def switch_state(self, state):
        if state in self.states:
            self.current_state = state
        else: print("this state is not in statelist")
