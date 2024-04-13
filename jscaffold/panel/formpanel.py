from ..context import Context
from jscaffold.layout.singlevaluelayout import SingleValueLayout
from jscaffold.layout.formlayout import FormLayout
from jscaffold.decorators.iot import preset_iot_class_method
from IPython.display import display
from jscaffold.views.logview.logview import LogViewWidget
from ipywidgets import widgets


class FormPanel:
    class State:
        """
        The State object hold the properties
        that may need to refresh the UI when
        changed
        """

        def __init__(self):
            self.instant_write = False
            self.title = None
            self.action_label = "Confirm"
            self.save_changes = True

    @preset_iot_class_method
    def __init__(
        self,
        input=None,
        output=None,
        title=None,
        logger=None,
        context=None,
        instant_write=False,  # TODO
    ):
        self.input = input
        self.output = output
        self.widget = None
        self.context = context
        self.logger = logger
        self.is_setup_completed = False
        self.state = FormPanel.State()
        self.state.title = title
        self.state.instant_write = instant_write

        if self.logger is None:
            self.logger = LogViewWidget()

        if self.context is None:
            self.context = Context(
                input=self.input,
                output=self.output,
                log=self.logger.append_stdout,
                clear_log=self.logger.clear_output,
            )

        self.create_widget()

    def create_widget(self):
        input = self.input
        output = self.output
        title = self.state.title

        if isinstance(input, list):
            layout = FormLayout(
                input,
                output,
                title,
                context=self.context,
                instant_write=self.state.instant_write,
            )
        else:
            layout = SingleValueLayout(
                input,
                output,
                title,
                context=self.context,
                instant_write=self.state.instant_write,
            )
        self.layout = layout

        self.widget = widgets.VBox([self.layout.widget, self.logger])

    def update_widget(self):
        self.layout.title(self.state.title).action_label(self.state.action_label)

    def __repr__(self):
        return ""

    def show(self):
        display(self.widget)
        self.focus()
        return self

    def focus(self):
        if self.layout is not None:
            self.layout.focus()
        return self

    def title(self, new_title: str):
        self.state.title = new_title
        self.update_widget()
        return self

    def action_label(self, new_label: str):
        self.state.action_label = new_label
        self.update_widget()
        return self

    def save_changes(self, value):
        self.context.save_changes = value
        return self
