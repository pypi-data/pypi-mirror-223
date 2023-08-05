import string

class Detector:
    identchars = string.ascii_letters + string.digits + '_'

    def __init__(self):
        pass

    def parseline(self, line):
        line = line.strip()
        if not line:
            return None, None, line

        elif line[0] == '?':
            line = 'help ' + line[1:]

        i, n = 0, len(line)
        while i < n and line[i] in self.identchars:
            i += 1
        cmd, arg = line[:i], line[i:].strip().split()
        return cmd, arg, line
    

