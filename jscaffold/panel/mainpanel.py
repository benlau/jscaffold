from jscaffold.panel.formpanel import FormPanel
from jscaffold.utils import args_to_list
from jscaffold.views.logview.logview import LogViewWidget
from jscaffold.widgets.ipywidgetwrapper import IPYWidgetWrapper
from ..contexts.context import Context
from ipywidgets import widgets


class MainPanel(IPYWidgetWrapper):
    class State:
        def __init__(self):
            self.forms = []

    def __init__(self):
        self.log_view = LogViewWidget()
        self.context = Context(log_view=self.log_view, main_panel=self)
        self.create_widget()
        self.state = MainPanel.State()

    def create_widget(self):
        self.form_box = widgets.VBox([])
        self.widget = widgets.VBox([self.form_box, self.log_view])

    def update_widget(self):
        self.form_box.children = [form.widget for form in self.state.forms]

    def get_widget(self):
        return self.widget

    def form(self, *args):
        input = args_to_list(args, defaults=[])
        form = FormPanel(input, log_view=self.log_view, context=self.context)
        self.state.forms.append(form)
        self.update_widget()

        return form
