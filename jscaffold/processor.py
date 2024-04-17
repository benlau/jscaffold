from jscaffold.task.runtask import RunTask
from jscaffold.iounit.applytosource import ApplyToSource
import asyncio
from inspect import signature
import traceback


class Processor:
    """
    Run output(s) from input(s) and instance value(s)
    """

    def __init__(self, context=None):
        self.context = context

    async def __call__(self, input, output, value):
        return await self.process(input, output, value)

    async def process(self, input, output, value):
        if self.context is not None:
            self.context.clear_log()

        outputs = [output] if not isinstance(output, list) else output[:]

        if self.context is not None and self.context.save_changes is True:
            outputs.insert(0, ApplyToSource())

        if input is None:
            inputs = []
            values = []
        else:
            inputs = [input] if not isinstance(input, list) else input
            values = [value] if not isinstance(value, list) else value

        env = dict(
            [
                (
                    i.key,
                    str(v) if v is not None else "",
                )
                for (i, v) in zip(inputs, values)
            ]
        )

        for target in outputs:
            try:
                if isinstance(target, str):
                    script = target
                    run_task = RunTask()
                    run_task.script = script
                    await run_task(print=self.context.log, env=env)
                elif callable(target):
                    self.invoke(target, value, self.context)
            except Exception:
                if self.context is not None:
                    self.context.log(traceback.format_exc())

    def create_task(self, input, output, value):
        async def run():
            return await self.process(input, output, value)

        return asyncio.get_event_loop().create_task(run())

    def invoke(self, callable, value, context):
        sig = signature(callable)
        args = {}
        context_kwargs = context.to_kwargs()
        for key in context_kwargs:
            if key in sig.parameters:
                args[key] = context_kwargs[key]
        if "value" in sig.parameters:
            args["value"] = value
        if "context" in sig.parameters:
            args["context"] = context
        return callable(**args)
