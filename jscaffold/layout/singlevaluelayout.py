from jscaffold.services.changedispatcher import (
    change_dispatcher,
    Listener,
)
from ..decorators import preset_iot_class_method
from ipywidgets import widgets
from ..widgets.widgetfactory import WidgetFactory
from ..processor import Processor


class SingleValueLayout:
    """
    SingleValueLayout is a internal class that creates a layout for a single input value.
    """

    class State:
        def __init__(self):
            self.instant_write = False
            self.title = None
            self.action_label = "Confirm"

    @preset_iot_class_method
    def __init__(
        self,
        input=None,
        output=None,
        title=None,
        context=None,
        instant_write=False,
    ):
        self.input = input
        self.output = output
        self.context = context
        self.confirm_button = None

        self.state = SingleValueLayout.State()
        self.state.title = title
        self.state.instant_write = instant_write
        self.create_widget()
        self.update_widget()

    def focus(self):
        if self.input_widget is not None:
            self.input_widget.focus()

    # pylama:ignore=C901
    def create_widget(self):
        layout = []
        factory = WidgetFactory()
        self.input_widget = None

        def on_change(value):
            try:
                if self.input_widget.value != value:
                    self.input_widget.value = value
            except Exception as e:
                self.context.print_line(str(e))
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

        # TODO: Update title style
        self.title_widget = widgets.Label(value=self.state.title)
        layout.append(self.title_widget)

        if self.input is None:
            (submit_area, confirm_button) = factory.create_submit_area(
                self.output, on_submit=on_submit, default_label=self.state.action_label
            )
            self.confirm_button = confirm_button
            widgets_box = widgets.VBox(layout + [submit_area])
            self.widget = widgets_box
            return

        input_widget = factory.create_input(self.input)
        self.input_widget = input_widget

        listener = Listener(self.input._get_id(), on_change)
        change_dispatcher.add_listener(listener)

        self.confirm_button = None
        if self.state.instant_write is False:
            (submit_area, confirm_button) = factory.create_submit_area(
                self.output, on_submit=on_submit, default_label=self.state.action_label
            )
            self.confirm_button = confirm_button
            widgets_box = widgets.VBox(layout + [input_widget.widget, submit_area])
        else:

            def on_change(change):
                if change["type"] == "change" and change["name"] == "value":
                    on_submit()

            self.input_widget.widget.observe(on_change)
            widgets_box = widgets.VBox(layout + [input_widget.widget])

        self.widget = widgets_box

    def update_widget(self):
        self.title_widget.value = self.state.title if self.state.title else ""
        self.title_widget.layout.visibility = (
            "visible" if self.state.title else "hidden"
        )
        if self.confirm_button is not None:
            self.confirm_button.description = self.state.action_label

    def title(self, value):
        self.state.title = value
        self.update_widget()
        return self

    def action_label(self, value):
        self.state.action_label = value
        self.update_widget()
        return self
