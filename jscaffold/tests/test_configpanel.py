from jscaffold.panel.formpanel import FormPanel


def test_no_input():
    """
    No input object can be allowed
    """

    script = "ls"
    FormPanel(output=script)
