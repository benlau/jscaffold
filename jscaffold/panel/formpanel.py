from jscaffold.utils import args_to_list
from ..contexts.context import FormContext
from IPython.display import display
from jscaffold.views.logview.logview import LogViewWidget
from ipywidgets import widgets
from jscaffold.widgets.widgetfactory import WidgetFactory
from jscaffold.processor import Processor
from jscaffold.services.changedispatcher import (
    Listener,
    change_dispatcher,
)
from jscaffold.debounce import KeyFilterDebouncer


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
            self.action_label = "Submit"
            self.save_changes = True
            self.runnables = []
            self.is_submitting = False

    def __init__(
        self,
        input=None,
        log_view=None,
        context=None,
    ):
        if input is None:
            self.input = []
        else:
            self.input = input if isinstance(input, list) else [input]

        self.widget = None
        self.state = FormPanel.State()
        self.submit_debouncer = KeyFilterDebouncer(0.1)

        has_own_log_view = False
        if log_view is None:
            has_own_log_view = True
            log_view = LogViewWidget()
        self.log_view = log_view

        if context is None:
            self.context = FormContext(
                input=self.input, log_view=self.log_view, form=self
            )
        else:
            self.context = FormContext.from_base_context(
                context, input=self.input, form=self
            )

        self.create_widget(has_own_log_view)

    def create_widget(self, has_own_log_view):
        factory = WidgetFactory()
        input = self.input

        items = []
        # TODO: Update title style
        self.title_widget = widgets.HTML(value=self.state.title)
        items.append(self.title_widget)

        self.input_widgets = []

        if len(input) > 0:
            grid = widgets.GridspecLayout(len(self.input), 2)

            grid._grid_template_columns = (
                "auto 1fr"  # A dirty hack to override the default value
            )
            grid._grid_template_rows = "auto"

            for i, item in enumerate(self.input):
                label = widgets.Label(value=item.key, layout=widgets.Layout())
                label.layout.margin = "0px 20px 0px 0px"

                input_widget = factory.create_input(item)
                grid[i, 0] = label
                grid[i, 1] = input_widget.widget
                self.input_widgets.append(input_widget)

            items.append(grid)

        (submit_area, confirm_button) = factory.create_submit_area(
            on_submit=lambda: self.submit(),
            default_label=self.state.action_label,
        )
        self.confirm_button = confirm_button
        self.submit_area = submit_area

        items.append(submit_area)
        if has_own_log_view:
            items.append(self.log_view)

        self.widget = widgets.VBox(items)
        self.listen()

    def listen(self):
        def on_user_change(change):
            if (
                change["type"] == "change"
                and change["name"] == "value"
                and self.state.instant_update is True
            ):
                self.submit()

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

        for input_widget, input_item in zip(self.input_widgets, self.input):
            listener = create_listener(input_item._get_id(), input_widget)
            change_dispatcher.add_listener(listener)
            input_widget.observe(on_user_change)

    def submit(self):
        def reenable():
            if self.confirm_button is not None:
                self.confirm_button.disabled = False
            self.state.is_submitting = False

        if self.state.is_submitting:
            self.submit_debouncer("", self.submit)
            return self
        self.state.is_submitting = True
        display_value = [input_widget.value for input_widget in self.input_widgets]
        processor = Processor(self.context)
        if self.confirm_button is not None:
            self.confirm_button.disabled = True
        task = processor.create_task(self.input, self.state.runnables, display_value)
        task.add_done_callback(lambda _: reenable())
        return self

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

    def __repr__(self):
        return ""

    def show(self):
        display(self.widget)
        self.focus()
        return self

    def focus(self):
        if len(self.input_widgets) > 0:
            self.input_widgets[0].focus()
        return self

    def title(self, new_title: str):
        self.state.title = new_title
        self.update_widget()
        return self

    def run(self, *args):
        self.state.runnables = args_to_list(args, defaults=[])
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

    def form(self, *args):
        context = self.context
        log_view = self.log_view
        input = args_to_list(args, defaults=[])
        new_form = FormPanel(input=input, context=context, log_view=log_view)

        if len(self.widget.children) == 0:
            self.widget.children = [new_form.widget]
            return new_form

        last_children = self.widget.children[-1]
        if isinstance(last_children, LogViewWidget):
            self.widget.children = tuple(
                list(self.widget.children[:-1]) + [new_form.widget, last_children]
            )
        else:
            self.widget.children = tuple(list(self.widget.children) + [new_form.widget])
        return new_form

    def refresh(self):
        for input_widget in self.input_widgets:
            input_widget.update_widget()
        return self
