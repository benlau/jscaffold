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
        inputs = [input] if not isinstance(input, list) else input
        inputs = [input for input in inputs if input is not None]
        for target in outputs:
            if isinstance(target, str):
                script = target
                env = dict(
                    [
                        (input.key, str(input.value) if input.value is not None else "")
                        for input in inputs
                    ]
                )
                run_task = RunTask()
                run_task.script = script
                await run_task(print_line=self.context.print_line, env=env)
            elif callable(target):
                sig = signature(target)
                arg_count = len(sig.parameters)

                args = [value, self.context][:arg_count]
                target(*args)

    def create_task(self, input, output, value):
        async def run():
            return await self.process(input, output, value)

        return asyncio.get_event_loop().create_task(run())
