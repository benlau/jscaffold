from jscaffold.iounit.var import Var
from jscaffold.panel.formpanel import FormPanel
from jscaffold.utils import args_to_list


def form(*args):
    input = args_to_list(args, defaults=[])
    input = list(map(lambda x: Var(x) if isinstance(x, str) else x, input))

    return FormPanel(input).show()
