from tablate.library.checkers.is_last_element import is_last_element
from tablate.library.formatters.console.row_line_divider import row_line_divider
from tablate.library.formatters.console.row_outer_border import row_outer_border
from tablate.library.renderers.console.frames.render_console_frame_grid import render_console_single_line_grid, \
    render_console_multi_line_grid
from tablate.library.renderers.console.frames.render_console_frame_table import render_console_table_frame
from tablate.type.type_store import FrameStoreList
from tablate.type.type_global import Globals


def render_console_frames(frame_list: FrameStoreList, global_options: Globals) -> str:

    return_string = ""

    for frame_index, frame_item in enumerate(frame_list):

        if frame_item.type == "grid" or frame_item.type == "table_header" or frame_item.type == "text":
            if frame_item.frame_styles.multiline is False or frame_item.frame_styles.max_lines == 1:
                return_string += render_console_single_line_grid(grid_frame_dict=frame_item, global_options=global_options)
            else:
                return_string += render_console_multi_line_grid(grid_frame_dict=frame_item, global_options=global_options)

        if frame_item.type == "table_body":
            return_string += render_console_table_frame(table_frame_store=frame_item, global_options=global_options)

        if not is_last_element(frame_index, frame_list):
            if frame_list[frame_index].frame_styles.frame_divider != 'none':
                frame_divider_inner = row_line_divider(column_list_top=frame_list[frame_index].column_list,
                                                       column_list_bottom=frame_list[frame_index + 1].column_list,
                                                       divider=frame_list[frame_index].frame_styles.frame_divider)
                return_string += row_outer_border(row_string=frame_divider_inner,
                                                  global_options=global_options,
                                                  row_divider=frame_item.frame_styles.frame_divider)

    return return_string
