import string
from .utils.hooks import Hooks
from .utils.register import AutoRegisterCommandsMeta
from .utils.detector import Detector

IDENTCHARS = string.ascii_letters + string.digits + '_'

__all__ = ["YveCMD"]

class YveCMD(metaclass=AutoRegisterCommandsMeta):
    identchars = IDENTCHARS
    ruler = '='
    lastcmd = ''
    relative_prompt = '[ cmd ] '
    admin = False

    def __init__(self):
        self.cmdqueue = []

        self.hook = Hooks()
        self.detect = Detector()

    @classmethod
    def register_handler(cls, cmd_handler):
        cls.register_handler_method(cmd_handler)

    def cmdloop(self, intro=None):
        self.hook.preloop()
        try:
            stop = None
            while not stop:
                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                else:
                    line = input(self.relative_prompt)
                line = self.hook.precmd(line)
                stop = self.onecmd(line)  # Use the Detector object to handle commands
                stop = self.hook.postcmd(stop, line)
            self.hook.postloop()
        except KeyboardInterrupt:
            self.hook.postloop()

    def onecmd(self, line):
        cmd, args, line = self.detect.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if line == 'EOF':
            self.lastcmd = ''
        if cmd == '':
            return self.default(line)
        else:
            try:
                func = getattr(self, 'do_' + cmd)
                func(*args)  # Call the do_ method with arguments
            except AttributeError:
                try:
                    func = getattr(self, 'void_' + cmd)
                    func()  # Call the void_ method without arguments
                except AttributeError:
                    return self.default(line)
            except TypeError as e:
                if not self.admin:
                    print("Error: Invalid number of arguments.")
                    print("Type 'help {}' for more information.".format(cmd))
                else:
                    print(e)
            except Exception as e:
                print("Error:", e)

    def emptyline(self):
        if self.lastcmd:
            return self.onecmd(self.lastcmd)

    def default(self, line):
        print('[ e r r o r  > %s' % line)

