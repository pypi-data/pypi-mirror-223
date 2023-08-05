import inspect


def parseFuncParams(func, args):
    args0 = {};
    if args is None:
        return args0;
    signature = inspect.signature(func)
    parameters = signature.parameters
    for param in parameters.values():
        if param.name in args:
            args0[param.name] = args[param.name]
    return args0;


def my_function(a, b, c=10, *args, **kwargs):
    pass


print(parseFuncParams(my_function, {'a': '33', 'c': 33, 'd': 1}))
print(parseFuncParams(my_function, None))
