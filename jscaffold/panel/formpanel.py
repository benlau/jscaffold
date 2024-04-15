from ..contexts.context import IOContext
from jscaffold.layout.singlevaluelayout import SingleValueLayout
from jscaffold.layout.multivaluelayout import MultiValueLayout
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
            self.instant_update = False
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
        instant_update=False,  # TODO
    ):
        self.input = input
        self.output = output
        self.widget = None
        self.logger = logger
        self.is_setup_completed = False
        self.state = FormPanel.State()
        self.state.title = title
        self.state.instant_update = instant_update

        if self.logger is None:
            self.logger = LogViewWidget()

        if context is None:
            self.context = IOContext(
                input=self.input,
                output=self.output,
                log_view=self.logger,
            )
        else:
            self.context = IOContext.from_base_context(
                context,
                input=self.input,
                output=self.output,
            )

        self.create_widget()

    def create_widget(self):
        input = self.input
        output = self.output
        title = self.state.title

        if input is None:
            self.widget = widgets.VBox([self.logger])
            return

        if isinstance(input, list):
            layout = MultiValueLayout(
                input,
                output,
                title,
                context=self.context,
                instant_update=self.state.instant_update,
            )
        else:
            layout = SingleValueLayout(
                input,
                output,
                title,
                context=self.context,
                instant_update=self.state.instant_update,
            )
        self.layout = layout

        self.widget = widgets.VBox([self.layout.widget, self.logger])

    def update_widget(self):
        if self.layout is not None:
            self.layout.title(self.state.title).action_label(self.state.action_label)
            self.layout.instant_update(self.state.instant_update)
            self.layout.update_widget()

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

    def instant_update(self, value: bool = True):
        self.state.instant_update = value
        self.update_widget()
        return self

    def save_changes(self, value: bool):
        self.context.save_changes = value
        return self
