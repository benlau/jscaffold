from jscaffold.panel.configpanel import ConfigPanel


def test_no_input():
    """
    No input object should be allowed
    """

    script = "ls"
    ConfigPanel(output=script).show()
