__all__ = ["Select", "SelectMap"]

class Select:
    def __init__(self, option, description, action):
        self.option = option
        self.description = description
        self.action = action

    def execute(self):
        self.action()


class SelectMap:
    select_promt: str = "[ ? ] "
    invalid_opt: str = "Invalid option. Please select a valid option."
    select_exit: str = "exit"
    valueErrorExcept: str = f"Invalid input. Please enter a number or exit-command to quit."
    
    def __init__(self, *selects):
        self.selects = {select.option: select for select in selects}

    def print_options(self):
        for select in self.selects.values():
            print(f"[ {select.option} ] {select.description}")

    def process_selection(self, option):
        if option in self.selects:
            self.selects[option].execute()
        else:
            print(self.invalid_opt)

    def handle_select(self):
        self.print_options()
        while True:
            user_input = input(self.select_promt)
            if user_input == self.select_exit:
                break
            try:
                option = int(user_input)
                self.process_selection(option)
                break
            except ValueError:
                print(self.valueErrorExcept)
