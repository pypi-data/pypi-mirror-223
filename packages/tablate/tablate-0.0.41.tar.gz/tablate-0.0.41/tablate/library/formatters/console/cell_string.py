import math
from typing import List, Optional

from tablate.library.formatters.console.ascii_styler import ascii_background_styler, \
    ascii_text_styler, ascii_terminator
from tablate.library.formatters.console.concat_string import concat_string
from tablate.type.type_input import BaseColumnInput
from tablate.type.type_style import ColumnStyles


def cell_string_single_line(string: str,
                            column_item: BaseColumnInput,
                            column_styles: ColumnStyles,
                            trunc_value: str = "...") -> str:
    string = str(string)
    string = string.split("\n")[0]
    string = " ".join(string.split("\t"))

    padding = column_item["padding"]

    if hasattr(column_styles, "background_padding") and "background" in column_item \
            and column_styles.background_padding is not None and column_item["background"] is not None:
        padding = padding + column_styles.background_padding

    string, white_space = concat_string(string=string,
                                        width=column_item["width"],
                                        padding=padding,
                                        trunc_value=trunc_value)

    if hasattr(column_styles, "background_padding") and "background" in column_item \
            and column_styles.background_padding is not None and column_item["background"] is not None:
        string = f"{' ' * column_styles.background_padding}{string}{' ' * column_styles.background_padding}"

    return_string = ""

    if column_item["text_color"] is not None or column_item["text_style"] is not None:
        if len(string.strip()) > 0:
            fore_space = len(string) - len(string.lstrip())
            back_space = len(string) - len(string.rstrip())
            string = (" " * fore_space) + ascii_text_styler(string=string.strip(), column_dict=column_item) + (
                        " " * back_space)

    if column_item["text_align"] == "left":
        return_string += string
        return_string += " " * white_space
    if column_item["text_align"] == "center":
        if white_space % 2 != 0:
            left_space = int(math.floor(white_space / 2))
            right_space = int(math.floor(white_space / 2) + 1)
        else:
            left_space = int(white_space / 2)
            right_space = int(white_space / 2)
        return_string += " " * left_space
        return_string += string
        return_string += " " * right_space
    if column_item["text_align"] == "right":
        return_string += " " * white_space
        return_string += string

    if column_item["background"] is not None:
        return_string = ascii_background_styler(string=return_string, column_dict=column_item)
    padding = " " * column_item["padding"]
    return_string = f"{padding}{return_string}{ascii_terminator()}{padding}"

    return return_string


def cell_string_multi_line(string: str,
                           column_item: BaseColumnInput,
                           column_styles: ColumnStyles,
                           max_lines: Optional[int] = None,
                           trunc_value: str = "...") -> List[str]:
    return_string_array = []

    string = str(string)

    clean_string = " ".join(string.split("\t"))
    initial_string_array = clean_string.split("\n")

    reached_max_lines = False

    for initial_string_item in initial_string_array:
        word_string_array = initial_string_item.split(" ")
        character_count = 0
        current_line_array = []
        for word_string_index, word_string_item in enumerate(word_string_array):
            last_line = max_lines is not None and len(return_string_array) == max_lines - 1
            character_count += len(word_string_item)
            if (character_count + (column_item["padding"] * 2) < column_item["width"]) or (
                    last_line and character_count + (column_item["padding"] * 2) < column_item["width"] + len(
                    trunc_value)):
                current_line_array.append(word_string_item)
            else:
                if last_line:
                    current_line_array.append(word_string_item)
                    current_line_string = " ".join(current_line_array)
                    return_string_array.append(cell_string_single_line(string=current_line_string,
                                                                       column_item=column_item,
                                                                       column_styles=column_styles,
                                                                       trunc_value=trunc_value))
                    reached_max_lines = True
                    break
                else:
                    current_line_string = " ".join(current_line_array)
                    return_string_array.append(cell_string_single_line(string=current_line_string,
                                                                       column_item=column_item,
                                                                       column_styles=column_styles,
                                                                       trunc_value=trunc_value))
                    current_line_array = [word_string_item]
                    character_count = len(word_string_item)
            character_count += 1
        if reached_max_lines:
            break
        current_line_string = " ".join(current_line_array)
        return_string_array.append(cell_string_single_line(string=current_line_string,
                                                           column_item=column_item,
                                                           column_styles=column_styles,
                                                           trunc_value=trunc_value))
    return return_string_array
