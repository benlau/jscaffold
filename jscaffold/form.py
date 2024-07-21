from jscaffold.panel.mainpanel import MainPanel

from jscaffold.utils import args_to_list


def form(*args):
    input = args_to_list(args, defaults=[])
    return MainPanel().form(input).show()
