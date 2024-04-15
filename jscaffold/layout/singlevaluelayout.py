from jscaffold.services.changedispatcher import (
    change_dispatcher,
    Listener,
)
from jscaffold.decorators.iot import preset_iot_class_method
from ipywidgets import widgets
from ..widgets.widgetfactory import WidgetFactory
from ..processor import Processor


class SingleValueLayout:
    """
    SingleValueLayout is a internal class that creates a layout for a single input value.
    """

    class State:
        def __init__(self):
            self.instant_update = False
            self.title = None
            self.action_label = "Confirm"

    @preset_iot_class_method
    def __init__(
        self,
        input=None,
        output=None,
        title=None,
        context=None,
        instant_update=False,
    ):
        self.input = input
        self.output = output
        self.context = context
        self.confirm_button = None

        self.state = SingleValueLayout.State()
        self.state.title = title
        self.state.instant_update = instant_update
        self.create_widget()
        self.update_widget()

    def focus(self):
        if self.input_widget is not None:
            self.input_widget.focus()

    # pylama:ignore=C901
    def create_widget(self):
        factory = WidgetFactory()
        self.input_widget = None

        def on_dispatcher_change(value):
            try:
                if self.input_widget.value != value:
                    self.input_widget.value = value
            except Exception as e:
                self.context.log(str(e))
                raise e

        def on_submit():
            def enable():
                if self.confirm_button is not None:
                    self.confirm_button.disabled = False

            processor = Processor(self.context)
            if self.confirm_button is not None:
                self.confirm_button.disabled = True
            current_input_value = (
                self.input_widget.value if self.input is not None else None
            )
            task = processor.create_task(self.input, self.output, current_input_value)
            task.add_done_callback(lambda _: enable())

        def on_user_change(change):
            if (
                change["type"] == "change"
                and change["name"] == "value"
                and self.state.instant_update is True
            ):
                on_submit()

        # TODO: Update title style
        self.title_widget = widgets.HTML(value=self.state.title)

        input_widget = factory.create_input(self.input)
        self.input_widget = input_widget

        listener = Listener(self.input._get_id(), on_dispatcher_change)
        change_dispatcher.add_listener(listener)

        (submit_area, confirm_button) = factory.create_submit_area(
            self.output, on_submit=on_submit, default_label=self.state.action_label
        )
        self.submit_area = submit_area
        self.confirm_button = confirm_button
        self.input_widget.observe(on_user_change)
        vbox = widgets.VBox([self.title_widget, self.input_widget.widget, submit_area])
        self.widget = vbox

    def update_widget(self):
        self.title_widget.value = self.state.title if self.state.title else ""
        self.title_widget.layout.visibility = (
            "visible" if self.state.title else "hidden"
        )
        if self.confirm_button is not None:
            self.confirm_button.description = self.state.action_label
        if self.state.instant_update is True:
            self.confirm_button.disabled = True
            self.confirm_button.layout.visibility = "hidden"
            self.submit_area.layout.visibility = "hidden"
        else:
            self.confirm_button.disabled = False
            self.confirm_button.layout.visibility = "visible"
            self.submit_area.layout.visibility = "visible"

    def title(self, value):
        self.state.title = value
        self.update_widget()
        return self

    def action_label(self, value):
        self.state.action_label = value
        self.update_widget()
        return self

    def instant_update(self, value: bool):
        self.state.instant_update = value
        self.update_widget()
        return self
