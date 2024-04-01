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
        self.title = title
        self.output = output
        self.action_label = "Confirm"
        self.context = context
        self.instant_write = instant_write
        self.confirm_button = None
        self.widget = self._create_ipywidget()
        self.is_running = False

    def focus(self):
        if self.input_widget is not None:
            self.input_widget.focus()

    # pylama:ignore=C901
    def _create_ipywidget(self):
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

        title_widget = None
        if self.title is not None:
            # TODO: Update title style
            title_widget = widgets.Label(value=self.title)
            layout.append(title_widget)

        if self.input is None:
            (submit_area, confirm_button) = factory.create_submit_area(
                self.output, on_submit=on_submit, default_label=self.action_label
            )
            self.confirm_button = confirm_button
            widgets_box = widgets.VBox(layout + [submit_area])
            return widgets_box

        input_widget = factory.create_input(self.input)
        self.input_widget = input_widget

        listener = Listener(self.input.get_id(), on_change)
        change_dispatcher.add_listener(listener)

        if self.instant_write is False:
            (submit_area, confirm_button) = factory.create_submit_area(
                self.output, on_submit=on_submit, default_label=self.action_label
            )
            self.confirm_button = confirm_button
            widgets_box = widgets.VBox(layout + [input_widget.widget, submit_area])
        else:

            def on_change(change):
                if change["type"] == "change" and change["name"] == "value":
                    on_submit()

            self.input_widget.widget.observe(on_change)
            widgets_box = widgets.VBox(layout + [input_widget.widget])

        return widgets_box
