class AutoRegisterCommandsMeta(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        cls.handlers = {}

    def register_handler_method(cls, cmd_handler):
        cmd_methods = [method for method in dir(cmd_handler) if method.startswith("do_") or method.startswith("void_")]
        for method in cmd_methods:
            if method.startswith("do_"):
                cmd_name = method[3:]
                handler_method = getattr(cmd_handler, method)
                setattr(cls, 'do_' + cmd_name, handler_method)
                cls.handlers[cmd_name] = handler_method
            elif method.startswith("void_"):
                cmd_name = method[5:]
                handler_method = getattr(cmd_handler, method)
                setattr(cls, 'void_' + cmd_name, handler_method)
                cls.handlers[cmd_name] = handler_method

    def __getattr__(cls, name):
        if name.startswith("do_"):
            def missing_method(*args, **kwargs):
                print(f"Error: Command '{name[3:]}' requires arguments.")
            return missing_method
        elif name.startswith("void_"):
            def missing_method(*args, **kwargs):
                print(f"Error: Command '{name[5:]}' does not require arguments.")
            return missing_method
        raise AttributeError(f"type object '{cls.__name__}' has no attribute '{name}'")
