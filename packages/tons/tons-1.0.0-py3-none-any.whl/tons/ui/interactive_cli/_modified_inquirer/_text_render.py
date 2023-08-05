from typing import Optional

from inquirer import errors, Text
from inquirer.render.console.base import BaseConsoleRender
from readchar import key

from ._utils import text_to_not_formatted_displayed_lines


class ModifiedTextRender(BaseConsoleRender):
    title_inline = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current = self.question.default or ""
        self.cursor_offset = 0

    def get_current_value(self, console_render: 'ModifiedConsoleRender'):
        current = self.current
        message = f"[?] {self.question._message}: {self.current}"
        message_lines = text_to_not_formatted_displayed_lines(message, self.terminal.width)
        cursor_x0 = cursor_x = len(message_lines[-1])
        cursor_y0 = cursor_y = len(message_lines) - 1
        cursor_offset = self.cursor_offset
        while cursor_offset > 0:
            cursor_x -= 1
            if cursor_x < 0:
                cursor_y -= 1
                cursor_x = len(message_lines[cursor_y])-1
            cursor_offset -= 1

        cursor_delta_x = cursor_x - cursor_x0
        cursor_delta_y = cursor_y - cursor_y0

        if cursor_delta_x > 0:
            current += self.terminal.move_right * cursor_delta_x
        else:
            current += self.terminal.move_left * (-cursor_delta_x)

        if cursor_delta_y > 0:
            current += self.terminal.move_down * cursor_delta_y
        else:
            current += self.terminal.move_up * (-cursor_delta_y)
        console_render._position += cursor_delta_y

        return current

    def process_input(self, pressed):
        if pressed == key.CTRL_C:
            raise KeyboardInterrupt()

        if pressed in (key.CR, key.LF, key.ENTER):
            raise errors.EndOfInput(self.current)

        if pressed == key.BACKSPACE:
            if self.current and self.cursor_offset != len(self.current):
                if self.cursor_offset > 0:
                    n = -self.cursor_offset
                    self.current = self.current[: n - 1] + self.current[n:]
                else:
                    self.current = self.current[:-1]
        elif pressed == key.LEFT:
            if self.cursor_offset < len(self.current):
                self.cursor_offset += 1
        elif pressed == key.RIGHT:
            self.cursor_offset = max(self.cursor_offset - 1, 0)
        elif len(pressed) != 1:
            return
        else:
            if self.cursor_offset == 0:
                self.current += pressed
            else:
                n = -self.cursor_offset
                self.current = "".join((self.current[:n], pressed, self.current[n:]))


class TempTextRender(ModifiedTextRender):
    pass


class TempText(Text):
    kind = "temp_text"
