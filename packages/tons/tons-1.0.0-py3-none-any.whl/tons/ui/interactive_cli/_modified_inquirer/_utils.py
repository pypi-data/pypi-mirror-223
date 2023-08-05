import re
from typing import List


def text_to_not_formatted_displayed_lines(text: str, terminal_width: int) -> List[str]:
    text = remove_ansi_escape_codes(text)
    lines = []
    while len(text) > 0:
        if '\n' in text[:terminal_width]:
            crop_pos = text.find('\n')
            lines.append(text[:crop_pos])
            text = text[crop_pos+1:]
        else:
            lines.append(text[:terminal_width])
            text = text[terminal_width:]
    return lines


def displayable_line_length(text: str) -> int:
    """
    Calculate the length of the displayable text by removing ANSI escape sequences and measuring the remaining
    characters.

    ANSI escape sequences are used to control text formatting and colors in terminal environments.
    These sequences do not contribute to the visual length of the text when displayed in modern systems.
    This function removes ANSI escape sequences from the input text and measures the length of the remaining characters
    (graphemes) to determine the length of the displayable text.

    Example:
        >> displayable_text_length("Hello, \x1B[1mworld!\x1B[0m")
        13
    """
    text = remove_ansi_escape_codes(text)
    return len(text)


def remove_ansi_escape_codes(text) -> str:
    """
    Remove ANSI escape codes from the input `text`.

    ANSI escape codes are used in terminal environments to add formatting and color to text.
    This function utilizes a regular expression to find and remove ANSI escape codes from the provided `text`.

    Example:
        >> remove_ansi_escape_codes("Hello, \x1B[1mworld!\x1B[0m")
        'Hello, world!'

    References:
        - ANSI Escape Sequences: https://invisible-island.net/xterm/ctlseqs/ctlseqs.html
        - Regex reference: https://stackoverflow.com/questions/38982637/regex-to-match-any-character-or-none
    """
    ansi_escape = \
        re.compile(r'''
            \x1B  # ESC
            (?:   # 7-bit C1 Fe (except CSI)
                [@-Z\\-_]
            |     # or [ for CSI, followed by a control sequence
                \[
                [0-?]*  # Parameter bytes
                [ -/]*  # Intermediate bytes
                [@-~]   # Final byte
            |
                \(  # G0 character set
                [A-Za-z0-9]
            )   
        ''', re.VERBOSE)
    return ansi_escape.sub('', text)
