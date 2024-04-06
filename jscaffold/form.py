from jscaffold.decorators.iot import preset_iot
from jscaffold.panel.configpanel import ConfigPanel


@preset_iot
def form(
    input=None,
    output=None,
    title=None,
):
    return ConfigPanel(input, output, title).show()
