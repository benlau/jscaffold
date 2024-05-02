from jscaffold.iounit.var import Var
from jscaffold.utils import inspect_arg_name


def _normalize_input(input):
    if isinstance(input, str):
        return Var(input)
    return input


def _setup_iot(input, output, title):
    if isinstance(input, list):
        input = [_normalize_input(i) for i in input]
    else:
        input = _normalize_input(input)

    return (input, output, title)


def preset_iot(func):
    """
    A decorator that preset the input, output, title arguments
    """

    def inner(input=None, output=None, title=None, *args, **kwargs):
        if title is None:
            if input is not None:
                title = inspect_arg_name(0, "input")
            elif output is not None:
                title = inspect_arg_name(1, "output")
        (input, output, title) = _setup_iot(input, output, title)
        return func(input, output, title, *args, **kwargs)

    return inner


def preset_iot_class_method(func):
    """
    A decorator that preset the input, output, title arguments
    """

    def inner(self, input=None, output=None, title=None, *args, **kwargs):
        if title is None:
            if input is not None:
                title = inspect_arg_name(0, "input")
            elif output is not None:
                title = inspect_arg_name(1, "output")
        (input, output, title) = _setup_iot(input, output, title)
        return func(self, input, output, title, *args, **kwargs)

    return inner
