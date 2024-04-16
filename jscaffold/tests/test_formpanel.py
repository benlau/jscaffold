from jscaffold.iounit.envvar import EnvVar
from jscaffold.panel.formpanel import FormPanel


def test_no_input():
    """
    No input object can be allowed
    """

    script = "ls"
    FormPanel(output=script)


def test_form():
    """
    FormPanel can be created
    """
    v = EnvVar("test")
    form1 = FormPanel()
    form2 = form1.form(v)
    assert form1.log_view == form2.log_view


def test_output_only_form():
    """ """
    form = FormPanel(output="ls")
    assert form.layout is not None
