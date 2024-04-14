class Context:
    def __init__(
        self,
        shared_storage=None,
        input=None,
        output=None,
        main_layout=None,
        log=None,
        clear_log=None,
        save_changes=True,
    ):
        # Shared storage between input and output
        self.shared_storage = shared_storage
        self.input = input
        self.output = output
        self.save_changes = save_changes
        self.main_layout = main_layout

        # For reporting the progress
        self._log = log
        self._clear_log = clear_log

    def log(self, *args):
        if self._log is not None:
            self._log(*args)

    def clear_output(self):
        if self._clear_log is not None:
            self._clear_log()

    def create_next_context(self, input, output):
        """
        Create a new context for the next block
        """
        return Context(
            shared_storage=self.shared_storage,
            input=input,
            output=output,
            main_layout=self.main_layout,
            log=self.log,
            clear_output=self.clear_output,
        )
