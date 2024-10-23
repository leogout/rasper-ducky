import re


class Preprocessor:
    def __init__(self):
        self.define_table = {}

    def process(self, code):
        lines = code.split("\n")
        processed_lines = []

        for line in lines:
            if line.strip().startswith("DEFINE"):
                self._handle_define(line)
            else:
                processed_lines.append(self._apply_substitutions(line))

        return "\n".join(processed_lines)

    def _handle_define(self, line):
        parts = line.split(None, 2)
        if len(parts) == 3:
            _, key, value = parts
            self.define_table[key.strip()] = value.strip()

    def _apply_substitutions(self, line):
        for key, value in self.define_table.items():
            line = re.sub(r"\b" + re.escape(key) + r"\b", value, line)
        return line
