from unittest import TestCase
from unittest.mock import Mock, patch
from jscaffold.iounit.envvar import EnvVar
from jscaffold.panel.formpanel import FormPanel


@patch("jscaffold.services.changedispatcher.ChangeDispatcher.dispatch", Mock())
class TestFormPanel(TestCase):
    def test_no_input(self):
        """
        No input object can be allowed
        """

        script = "ls"
        FormPanel(output=script)

    def test_form(self):
        """
        FormPanel can be created
        """
        v = EnvVar("test")
        form1 = FormPanel()
        form2 = form1.form(v)
        assert form1.log_view == form2.log_view

    def test_output_only_form(self):
        """ """
        form = FormPanel(output="ls")
        assert form.layout is not None
