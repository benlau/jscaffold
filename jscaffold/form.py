from jscaffold.panel.formpanel import FormPanel
from jscaffold.utils import args_to_list


def form(*args):
    input = args_to_list(args, defaults=[])

    return FormPanel(input).show()
