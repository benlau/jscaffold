from jscaffold.decorators.iot import preset_iot
from jscaffold.panel.formpanel import FormPanel


@preset_iot
def form(
    input=None,
    output=None,
    title=None,
):
    return FormPanel(input, output, title).show()
