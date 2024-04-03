from jscaffold.panel.configpanel import ConfigPanel


def test_no_input():
    """
    No input object can be allowed
    """

    script = "ls"
    ConfigPanel(output=script)
