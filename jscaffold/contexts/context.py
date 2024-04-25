from jscaffold.services.sharedstorage import shared_storage


class Context:
    def __init__(
        self,
        shared_storage=shared_storage,
        log_view=None,
    ):
        # Shared storage between input and output
        self.shared_storage = shared_storage
        self.log_view = log_view

    def to_kwargs(self):
        return {
            "log": self.log,
            "clear_log": self.clear_log,
            "shared_storage": self.shared_storage,
        }

    def log(self, *args):
        if self.log_view is not None:
            self.log_view.append_stdout(*args)
        else:
            print(*args)

    def clear_log(self):
        if self.log_view is not None:
            self.log_view.clear_output()


class FormContext(Context):
    def __init__(self, input=None, save_changes=True, parent=None, form=None, **kwargs):
        super().__init__(**kwargs)
        self.input = input
        self.save_changes = save_changes
        self.parent = parent
        self.form = form

    @staticmethod
    def from_base_context(base_context, **kwargs):
        return FormContext(
            log_view=base_context.log_view,
            shared_storage=base_context.shared_storage,
            parent=base_context,
            **kwargs
        )

    def refresh_form(self):
        if self.form is not None:
            self.form.refresh()

    def to_kwargs(self):
        kwargs = super().to_kwargs()
        kwargs.update(
            {
                "input": self.input,
                "refresh_form": self.refresh_form,
            }
        )
        return kwargs
