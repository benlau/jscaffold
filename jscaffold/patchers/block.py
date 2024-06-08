class PatchBlock:
    def __init__(self, begin_divider: str, end_divider: str):
        self.begin_divider = begin_divider
        self.end_divider = end_divider

    def _process(self, content: str):
        lines = content.split("\n")
        begin_index = None
        end_index = None
        for i, line in enumerate(lines):
            if begin_index is None and line.strip() == self.begin_divider:
                begin_index = i
                continue
            if begin_index is not None and line.strip() == self.end_divider:
                end_index = i
                break

        return begin_index, end_index, lines

    def read(self, content: str):
        begin_index, end_index, lines = self._process(content)
        if begin_index is not None and end_index is not None:
            return "\n".join(lines[begin_index + 1 : end_index])

        return None

    def write(self, content: str, value: str):
        begin_index, end_index, lines = self._process(content)

        if begin_index is not None and end_index is not None:
            lines[begin_index + 1 : end_index] = value.split("\n")
            return "\n".join(lines)

        lines = lines + [self.begin_divider] + value.split("\n") + [self.end_divider]
        return "\n".join(lines)
