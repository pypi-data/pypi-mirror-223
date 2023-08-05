class Anwser:
    promt: str = "[ > ] "
    stop_word: str = "exit"

    def __init__(self) -> None:
        self.anwser_var = None

    def return_anwser(self) -> str:
        return self.anwser_var

    def geting(self, description: str, func = None):
        print(description)
        while True:
            anwser = input(self.promt)
            
            if anwser == self.stop_word:
                anwser = None
                break
            else:
                self.anwser_var = anwser
                break

        if func is not None:
            func(anwser)
