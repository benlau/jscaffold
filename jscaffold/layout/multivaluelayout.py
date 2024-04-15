from typing import List
from jscaffold.processor import Processor
from jscaffold.services.changedispatcher import (
    Listener,
    change_dispatcher,
)
import ipywidgets as widgets
from jscaffold.iounit.variable import Variable
from ..widgets.widgetfactory import WidgetFactory


class MultiValueLayout:
    """
    FormLayout is a class that creates a layout for a form.
    """

    class State:
        def __init__(self):
            self.title = None
            self.action_label = "Confirm"
            self.instant_update = False

    # TODO:
    # - Add support for debouncer

    def __init__(
        self,
        input: List[Variable],
        output=None,
        title="Form",
        context=None,
        instant_update=False,
    ):
        if isinstance(input, list):
            self.input = input
        else:
            self.input = [input]
        self.output = output
        self.input_widgets = []
        self.context = context
        self.confirm_button = None
        self.state = MultiValueLayout.State()
        self.state.instant_update = instant_update
        self.state.title = title
        self.create_widget()
        self.update_widget()

    # pylama:ignore=C901
    def create_widget(self):
        factory = WidgetFactory()

        layout = []
        self.title_widget = widgets.HTML()
        layout.append(self.title_widget)

        grid = widgets.GridspecLayout(len(self.input), 2)

        grid._grid_template_columns = (
            "auto 1fr"  # A dirty hack to override the default value
        )
        grid._grid_template_rows = "auto"

        def create_listener(id, widget):
            def on_change(value):
                try:
                    if widget.value != value:
                        widget.value = value
                except Exception as e:
                    self.context.log(str(e))
                    raise e

            listener = Listener(id, on_change)
            return listener

        for i, input in enumerate(self.input):
            label = widgets.Label(value=input.key, layout=widgets.Layout())
            label.layout.margin = "0px 20px 0px 0px"

            input_widget = factory.create_input(input)
            grid[i, 0] = label
            grid[i, 1] = input_widget.widget
            self.input_widgets.append(input_widget)
            listener = create_listener(input._get_id(), input_widget)
            change_dispatcher.add_listener(listener)

        def on_submit():
            def enable():
                if self.confirm_button is not None:
                    self.confirm_button.disabled = False

            values = []
            for i, _ in enumerate(self.input):
                values.append(self.input_widgets[i].value)

            if self.confirm_button is not None:
                self.confirm_button.disabled = True
            processor = Processor(self.context)
            task = processor.create_task(self.input, self.output, values)
            task.add_done_callback(lambda _: enable())

        self.confirm_button = None
        (submit_area, confirm_button) = factory.create_submit_area(
            self.output, on_submit
        )
        self.confirm_button = confirm_button
        self.submit_area = submit_area
        widgets_box = widgets.VBox(layout + [grid, submit_area])
        for widget in self.input_widgets:

            def on_user_change(change):
                if (
                    change["type"] == "change"
                    and change["name"] == "value"
                    and self.state.instant_update is True
                ):
                    on_submit()

            widget.observe(on_user_change)
        self.widget = widgets_box

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

    def focus(self):
        if len(self.input_widgets) > 0:
            self.input_widgets[0].focus()

    def title(self, value):
        self.state.title = value
        self.update_widget()
        return self

    def action_label(self, value):
        self.state.action_label = value
        self.update_widget()
        return self

    def instant_update(self, value=True):
        self.state.instant_update = value
        self.update_widget()
        return self
