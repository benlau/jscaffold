import anywidget
import traitlets
import pathlib


class LogViewWidget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "index.js"
    _css = pathlib.Path(__file__).parent / "style.css"

    value = traitlets.Unicode("").tag(sync=True)
    is_running = traitlets.Bool(False).tag(sync=True)

    def append_stdout(self, *args):
        message = " ".join(str(arg) for arg in args)
        self.value = self.value + message

    def clear_output(self):
        self.value = ""
