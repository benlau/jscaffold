class Context:
    def __init__(
        self,
        current_block_index=None,
        shared_storage=None,
        input=None,
        output=None,
        main_layout=None,
        print=None,
        clear_output=None,
        processor=None,
        save_changes=True,
    ):
        self.current_block_index = current_block_index
        # Shared storage between input and output
        self.shared_storage = shared_storage
        self.input = input
        self.output = output
        self.save_changes = save_changes
        self.main_layout = main_layout

        # For reporting the progress
        self.print = print
        self.processor = processor
        self._clear_output = clear_output

    def clear_output(self):
        if self._clear_output is not None:
            self._clear_output()

    def create_next_context(self, input, output):
        """
        Create a new context for the next block
        """
        return Context(
            current_block_index=self.current_block_index + 1,
            shared_storage=self.shared_storage,
            input=input,
            output=output,
            main_layout=self.main_layout,
            print=self.print,
            clear_output=self.clear_output,
        )
