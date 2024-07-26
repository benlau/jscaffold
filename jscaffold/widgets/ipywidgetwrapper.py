from abc import ABC
import ipywidgets


class IPYWidgetWrapper(ABC):
    """
    IPython widget wrapper
    """

    def create_widget(self):
        raise NotImplementedError()

    def update_widget(self):
        raise NotImplementedError()

    def get_widget(self) -> "ipywidgets.Widget":
        raise NotImplementedError()

    def focus(self):
        widget = self.get_widget()

        if widget is not None:
            widget.focus()
