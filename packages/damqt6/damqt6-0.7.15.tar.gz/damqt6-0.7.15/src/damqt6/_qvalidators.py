import re

from PyQt6.QtGui import QValidator


class QBaseValidator(QValidator):
    _re_dup_spaces = re.compile(' +')

    def validate(self, text: str, pos: int) -> tuple['QValidator.State', str, int]:
        valid_text = ''
        valid_pos = pos
        for ix, char in enumerate(text):
            if char != ' ':
                valid_text += char
            elif valid_text and not valid_text.endswith(' '):
                valid_text += char
            elif ix < pos:
                valid_pos -= 1

        state = QValidator.State.Intermediate if valid_text.endswith(' ') else QValidator.State.Acceptable
        return state, valid_text, valid_pos
