from tablate.library.ascii.chars.corners import bottom_left, bottom_right
from tablate.library.formatters.console.row_line_divider import row_line_divider
from tablate.type.type_store import FrameStoreList
from tablate.type.type_global import Globals


def render_console_foot(frame_list: FrameStoreList, global_options: Globals) -> str:

    return_string = ""

    outer_padding = global_options.console.outer_styles.outer_padding
    frame_border = global_options.console.outer_styles.outer_border

    bottom_border_inner = row_line_divider(column_list_top=frame_list[-1].column_list,
                                           column_list_bottom=[],
                                           divider=frame_border)
    return_string += f"{' ' * outer_padding}{bottom_left[frame_border]}{bottom_border_inner}{bottom_right[frame_border]}\n"

    return return_string
