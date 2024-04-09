from .iounit import InputUnit, OutputUnit


class ApplyToSource(OutputUnit):
    """
    An OutputUnit that writes the value to the source input.
    """

    def __call__(self, value, context):
        values = []
        sources = []
        if isinstance(value, list):
            values = value
            sources = context.input
        else:
            values = [value]
            sources = [context.input]

        for index, value in enumerate(values):
            source = sources[index]
            if isinstance(source, InputUnit):
                if source.format.readonly:
                    continue
            if isinstance(source, OutputUnit):
                source.write(value, context)
