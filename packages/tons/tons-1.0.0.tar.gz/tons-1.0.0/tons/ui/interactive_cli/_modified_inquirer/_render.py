import sys

from inquirer import events, errors
from inquirer.render.console import ConsoleRender
from inquirer.render.console import List

from ._confirm_render import ModifiedConfirmRender, RemovePrevAfterEnterRender
from ._list_with_filter_render import ListWithFilterRender
from ._menu_with_hotkeys import MenuWithHotkeysRender, MenuWithHotkeys
from ._text_render import ModifiedTextRender, TempTextRender
from ._utils import displayable_line_length, text_to_not_formatted_displayed_lines
from .._exceptions import EscButtonPressed

ESC_BUTTONS = {"\x1b", "\x1b\x1b"}


class ModifiedConsoleRender(ConsoleRender):
    def render(self, question, question_idx, questions_num, answers=None):
        question.answers = answers or {}

        if question.ignore:
            return question.default

        clazz = self.render_factory(question.kind)
        render = clazz(question, terminal=self.terminal,
                       theme=self._theme, show_default=question.show_default)

        if isinstance(question, MenuWithHotkeys):
            render.current = question.starting_pos

        self.clear_eos()

        is_success = True

        try:
            ans = self._event_loop(render)
            return ans

        except EscButtonPressed:
            raise

        except Exception:
            is_success = False

        finally:
            # if question is a list and it's the last one then we should delete +1
            # if question is a list and it's not the last one then we should NOT delete +1
            if type(render) in [List, TempTextRender, RemovePrevAfterEnterRender,
                                ListWithFilterRender, MenuWithHotkeysRender]:
                if type(render) is List or type(render) is MenuWithHotkeysRender \
                        or type(render) is ListWithFilterRender:
                    self._position = len(list(render.get_options()))
                    if question_idx == questions_num - 1:
                        self._position += 1
                elif type(render) is TempTextRender:
                    pass
                elif type(render) is RemovePrevAfterEnterRender:
                    self._position += render.get_lines_count_to_erase()

                self._relocate()
                self.clear_eos()
                if (not isinstance(render, RemovePrevAfterEnterRender)) and \
                        (not isinstance(render, TempTextRender)):
                    self._print_header(render, self._get_msg_mark(is_success))
            else:
                print("")

    def _event_loop(self, render):
        try:
            while True:
                self._relocate()

                self.clear_eos()

                self._print_status_bar(render)

                self._print_header(render)
                self._print_options(render)

                self._process_input(render)

                if isinstance(render, ListWithFilterRender):
                    # TODO this is a crutch
                    self.clear_eos()

                self._force_initial_column()
        except errors.EndOfInput as e:
            # TODO FIXME this is a crutch
            if isinstance(render, RemovePrevAfterEnterRender) or isinstance(render, TempTextRender):
                self._relocate()
                self.clear_eos()
            self._go_to_end(render)
            return e.selection

    def _print_header(self, render, specific_msg_mark=None):
        header = render.get_header()
        default_value = " ({color}{default}{normal})".format(
            default=render.question.default, color=self._theme.Question.default_color,
            normal=self.terminal.normal
        )
        show_default = render.question.default and render.show_default
        header += default_value if show_default else ""

        msg_mark = "?" if specific_msg_mark is None else specific_msg_mark
        msg_template = (
                "{t.move_up}{t.clear_eol}{tq.brackets_color}[" "{tq.mark_color}" +
                msg_mark + "{tq.brackets_color}]{t.normal} {msg}"
        )

        # ensure any user input with { or } will not cause a formatting error
        # TODO FIXME crutch
        current_value = render.get_current_value(console_render=self) \
            if isinstance(render, ModifiedTextRender) \
            else render.get_current_value()

        escaped_current_value = str(current_value).replace(
            "{", "{{").replace("}", "}}")

        fit_width = isinstance(render, MenuWithHotkeysRender) or isinstance(render, ListWithFilterRender)
        self.print_str(
            f"\n{msg_template}: {escaped_current_value}",
            msg=header,
            lf=not render.title_inline,
            fit_width=False,
            tq=self._theme.Question,
        )

    def _print_options(self, render):
        fit_width = isinstance(render, MenuWithHotkeysRender) or isinstance(render, ListWithFilterRender)
        for message, symbol, color in render.get_options():
            if hasattr(message, "decode"):  # python 2
                message = message.decode("utf-8")
            self.print_line(" {color}{s} {m}{t.normal}", m=message, color=color, s=symbol, fit_width=fit_width)

    def print_str(self, base, lf=False, fit_width=False, **kwargs):
        if lf:
            self._position += 1

        text = base.format(t=self.terminal, **kwargs)
        if fit_width:
            lines = text.split('\n')
            text = '\n'.join([self._fit_line_within_terminal_width(line) for line in lines])

        # TODO FIXME this is a crutch with incorrect logic,
        #  asserting that `print_str()` is always called under these circumstances
        #  ((line feed symbol is in the beginning) XOR (`lf`==True)) AND (text doesn't contain other line feeds)
        line_count = len(text_to_not_formatted_displayed_lines(text.lstrip('\n'), self.width))
        # TODO also, this will only work under assumption that the text is printed from the beginning of the line
        self._position += line_count - 1

        print(text, end="\n" if lf else "")
        sys.stdout.flush()

    def _process_input(self, render):
        try:
            ev = self._event_gen.next()
            if isinstance(ev, events.KeyPressed):
                if ev.value in ESC_BUTTONS:
                    raise EscButtonPressed()

                render.process_input(ev.value)
        except errors.ValidationError as e:
            self._previous_error = e.value
        except errors.EndOfInput as e:
            try:
                render.question.validate(e.selection)
                raise
            except errors.ValidationError as e:
                self._previous_error = render.handle_validation_error(e)

    def _get_msg_mark(self, is_success):
        return "✓" if is_success else "✕"

    def render_factory(self, question_type):
        if question_type == 'text' or question_type == 'path':
            return ModifiedTextRender
        if question_type == 'temp_text':
            return TempTextRender
        if question_type == 'modified_confirm':
            return ModifiedConfirmRender
        if question_type == 'remove_prev_after_enter':
            return RemovePrevAfterEnterRender
        if question_type == 'list_with_filter':
            return ListWithFilterRender
        if question_type == 'menu_with_hotkeys':
            return MenuWithHotkeysRender

        return super().render_factory(question_type)

    def _fit_line_within_terminal_width(self, line: str) -> str:
        """
        Make the `line` fit within the terminal width by truncating and adding an ellipsis (...).
        """
        def with_ellipsis_at_end(_text: str) -> str:
            return _text[:-3] + self.terminal.normal + '...'

        if displayable_line_length(line) >= self.width:
            while displayable_line_length(with_ellipsis_at_end(line)) >= self.width and len(line) > 0:
                line = line[:-1]
            line = with_ellipsis_at_end(line)

        return line
