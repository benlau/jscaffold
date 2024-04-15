from .iounit import Inputable, Outputable


class ApplyToSource(Outputable):
    """
    An Outputable that writes the value to the source input.
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
            if isinstance(source, Inputable):
                if source.format.readonly:
                    continue
            if isinstance(source, Outputable):
                source.write(value, context)
