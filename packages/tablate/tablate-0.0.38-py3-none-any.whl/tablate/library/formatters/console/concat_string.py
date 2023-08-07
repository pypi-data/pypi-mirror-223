from typing import Union


def concat_string(string: Union[str, int], width: int, padding: int, trunc_value: str):
    string = str(string)
    if len(string) + (padding * 2) > width:
        slice_outer_index = width - ((padding * 2) + len(trunc_value))
        if slice_outer_index < 1:
            trunc_value = trunc_value[0:len(trunc_value) - abs(slice_outer_index - 1)]
            slice_outer_index = 1
        string = f"{string[0:slice_outer_index]}{trunc_value}"

    white_space = width - ((padding * 2) + len(string))

    return string, white_space