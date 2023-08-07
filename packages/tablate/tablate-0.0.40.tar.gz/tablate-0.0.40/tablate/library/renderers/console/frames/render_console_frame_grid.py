
from tablate.library.ascii.chars.line_v import v_line
from tablate.library.checkers.is_last_element import is_last_element
from tablate.library.formatters.console.cell_string import cell_string_single_line, cell_string_multi_line
from tablate.library.renderers.console.frames.render_console_columns import column_console_multiline
from tablate.library.formatters.console.row_outer_border import row_outer_border
from tablate.type.type_store import GridFrameStore
from tablate.type.type_global import Globals


def render_console_single_line_grid(grid_frame_dict: GridFrameStore, global_options: Globals):

    grid_line_string = ""
    for column_index, column_item in enumerate(grid_frame_dict.column_list):
        grid_line_string += cell_string_single_line(string=column_item["string"],
                                                    column_item=column_item,
                                                    column_styles=grid_frame_dict.column_styles,
                                                    trunc_value=grid_frame_dict.frame_styles.trunc_value)
        if not is_last_element(column_index, grid_frame_dict.column_list):
            grid_line_string += v_line[column_item["divider"]]

    return row_outer_border(row_string=grid_line_string, global_options=global_options)


def render_console_multi_line_grid(grid_frame_dict: GridFrameStore, global_options: Globals):

    formatted_columns_array = []

    for column_item in grid_frame_dict.column_list:
        column_string_array = cell_string_multi_line(string=column_item["string"],
                                                     column_item=column_item,
                                                     column_styles=grid_frame_dict.column_styles,
                                                     trunc_value=grid_frame_dict.frame_styles.trunc_value,
                                                     max_lines=grid_frame_dict.frame_styles.max_lines)
        formatted_columns_array.append(column_string_array)

    return column_console_multiline(formatted_columns_array=formatted_columns_array,
                                    frame_dict=grid_frame_dict,
                                    global_options=global_options)
