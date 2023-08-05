class Hooks:
    intro = "Welcome to CMD-app. Press ctrl+C to exit"
    outro = "exit ... "

    def __init__(self):
        pass

    def preloop(self):
        """
        [Goals]
            - Runs any setup code before the command loop starts.
        """
        print(self.intro)

    def postloop(self):
        """
        [Goals]
            - Runs any cleanup code after the command loop ends.
        """
        print(self.outro)
    
    
    def precmd(self, line):
        """
        [Goals]
            - Preprocesses the command line input before parsing.

        [ForExm]
            - precmd line1
        """
        return line

    def postcmd(self, stop, line):
        """
        [Goals]
            - Postprocesses the command execution result.

        [ForExm]
            - postcmd stop1 line1
        """
        return stop
