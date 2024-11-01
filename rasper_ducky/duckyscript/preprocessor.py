import re


class Preprocessor:
    def __init__(self):
        self.define_table = {}

    def process(self, code: str) -> str:
        lines = code.split("\n")
        processed_lines = []

        for line in lines:
            if line.strip().startswith("DEFINE"):
                self._handle_define(line)
                # Appends an line to remove defines from the code once consumed
                processed_lines.append("")
            else:
                processed_lines.append(self._apply_substitutions(line))

        return "\n".join(processed_lines)

    def _handle_define(self, line: str):
        parts = line.split(None, 2)
        if len(parts) == 3:
            _, key, value = parts
            self.define_table[key.strip()] = value.strip()

    def _apply_substitutions(self, line: str) -> str:
        for key, value in self.define_table.items():
            if key in line:
                line = line.replace(key, value)

        return line
