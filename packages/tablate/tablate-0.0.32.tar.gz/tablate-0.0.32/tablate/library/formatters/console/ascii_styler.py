from tablate.library.ascii.colors.background import ascii_background_colors
from tablate.library.ascii.colors.characters import ascii_character_colors
from tablate.library.ascii.styles.styles import ascii_text_styles
from tablate.library.checkers.set_key_resolver import set_key_resolver
from tablate.type.type_input import BaseColumnStyles


def ascii_background_styler(string: str, column_dict: BaseColumnStyles):
    background = ascii_background_colors[column_dict["background"]]
    return f"\033[{background}m{string}"


def ascii_text_styler(string: str, column_dict: BaseColumnStyles):
    text_style = ascii_text_styles[set_key_resolver(instance=column_dict, key="text_style", default="normal")]
    text_color = ascii_character_colors[set_key_resolver(instance=column_dict, key="text_color", default="default")]
    if text_color != "" or text_style != "":
        return f"\033[{text_style}{';' if text_color != '' and text_style != '' else ''}{text_color}m{string}\033[24m"
    else:
        return string

def ascii_terminator():
    return "\033[0m"

