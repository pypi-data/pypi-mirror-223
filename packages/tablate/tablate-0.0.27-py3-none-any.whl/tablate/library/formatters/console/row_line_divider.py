from typing import List

from tablate.library.ascii.chars.line_h import h_line
from tablate.library.ascii.chars.matrix_cross import cross_matrix
from tablate.type.primitives import FrameDivider
from tablate.type.type_store import BaseColumnStore


def row_line_divider(column_list_top: List[BaseColumnStore], column_list_bottom: List[BaseColumnStore], divider: FrameDivider) -> str:

    # todo: fix this!
    #  are both the 'col_width' and the 'sum_width' needed ??
    #  (sum_width is used for if checks... col_width are used for iterative calculations..)

    return_string = ""

    upper_frame_sum_width = 0
    upper_frame = []
    for v_line_index in range(0, len(column_list_top)):
        upper_frame_sum_width += column_list_top[v_line_index]["width"]
        upper_frame.append({
            "col_width": column_list_top[v_line_index]["width"],
            "sum_width": upper_frame_sum_width,
            "divider": column_list_top[v_line_index]["divider"]
        })
    upper_frame.reverse()
    
    lower_frame_sum_width = 0
    lower_frame = []
    for v_line_index in range(0, len(column_list_bottom)):
        lower_frame_sum_width += column_list_bottom[v_line_index]["width"]
        lower_frame.append({
            "col_width": column_list_bottom[v_line_index]["width"], 
            "sum_width": lower_frame_sum_width,              
            "divider": column_list_bottom[v_line_index]["divider"]
        })
    lower_frame.reverse()

    current_v_line_index = len(column_list_top) + len(column_list_bottom)

    while current_v_line_index > 0:
        if len(upper_frame) > 0 and len(lower_frame) > 0:
            if upper_frame[-1]["sum_width"] > lower_frame[-1]["sum_width"]:
                return_string += f"{h_line[divider] * lower_frame[-1]['col_width']}{cross_matrix['blank'][divider][lower_frame[-1]['divider']]}"
                upper_frame[-1]["col_width"] = upper_frame[-1]["col_width"] - lower_frame[-1]["col_width"] - 1
                lower_frame.pop()
            elif upper_frame[-1]["sum_width"] == lower_frame[-1]["sum_width"]:
                return_string += f"{h_line[divider] * lower_frame[-1]['col_width']}{cross_matrix[upper_frame[-1]['divider']][divider][lower_frame[-1]['divider']]}"
                upper_frame.pop()
                lower_frame.pop()
            elif upper_frame[-1]["sum_width"] < lower_frame[-1]["sum_width"]:
                return_string += f"{h_line[divider] * upper_frame[-1]['col_width']}{cross_matrix[upper_frame[-1]['divider']][divider]['blank']}"
                lower_frame[-1]["col_width"] = lower_frame[-1]["col_width"] - upper_frame[-1]["col_width"] - 1
                upper_frame.pop()
        else:
            if len(upper_frame) > 0:
                return_string += f"{h_line[divider] * upper_frame[-1]['col_width']}{cross_matrix[upper_frame[-1]['divider']][divider]['blank']}"
                if upper_frame[-1]["col_width"] < 0:
                    return_string = return_string[0:upper_frame[-1]["col_width"]]
                upper_frame.pop()
            if len(lower_frame) > 0:
                return_string += f"{h_line[divider] * lower_frame[-1]['col_width']}{cross_matrix['blank'][divider][lower_frame[-1]['divider']]}"
                if lower_frame[-1]["col_width"] < 0:
                    return_string = return_string[0:lower_frame[-1]["col_width"]]
                lower_frame.pop()
        current_v_line_index -= 1

    return return_string[0:-1]
