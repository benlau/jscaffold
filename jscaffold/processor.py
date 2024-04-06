from jscaffold.task.runtask import RunTask
import asyncio
from inspect import signature


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
            self.context.clear_output()

        outputs = [output] if not isinstance(output, list) else output

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
                    await run_task(print=self.context.print, env=env)
                elif callable(target):
                    sig = signature(target)
                    arg_count = len(sig.parameters)

                    args = [value, self.context][:arg_count]
                    target(*args)
            except Exception as e:
                if self.context is not None:
                    self.context.print(str(e))

    def create_task(self, input, output, value):
        async def run():
            return await self.process(input, output, value)

        return asyncio.get_event_loop().create_task(run())
