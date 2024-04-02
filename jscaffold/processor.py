from jscaffold.task.runtask import RunTask
import asyncio
from inspect import signature


class Processor:
    """
    Run output(s) from input(s) and instance value(s)
    """

    def __init__(self, context=None):
        self.context = context

    def __call__(self, input, output, value):
        return self.process(input, output, value)

    async def process(self, input, output, value):
        if self.context is not None:
            self.context.clear_output()
        if isinstance(output, list):
            outputs = output
        else:
            outputs = [output]

        for target in outputs:
            if isinstance(target, str):
                script = target
                # TODO Handle list type
                env = {
                    "JS_VALUE": str(value),
                }
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
