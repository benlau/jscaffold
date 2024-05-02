from unittest import TestCase
from jscaffold.form import form
from jscaffold.iounit.var import Var


class TestForm(TestCase):
    def test_form_normalize_str(self):
        """
        Form can be created
        """
        created_form = form("VAR")
        assert created_form is not None
        assert isinstance(created_form.input[0], Var) is True
