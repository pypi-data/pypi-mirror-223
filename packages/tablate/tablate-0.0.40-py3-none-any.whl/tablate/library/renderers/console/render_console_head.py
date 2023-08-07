from tablate.library.ascii.chars.corners import top_left, top_right
from tablate.library.formatters.console.row_line_divider import row_line_divider
from tablate.type.type_store import FrameStoreList
from tablate.type.type_global import Globals


def render_console_head(frame_list: FrameStoreList, global_options: Globals) -> str:

    return_string = ""

    frame_border = global_options.console.outer_styles.outer_border
    outer_padding = global_options.console.outer_styles.outer_padding

    top_border_inner = row_line_divider(column_list_top=[],
                                        column_list_bottom=frame_list[0].column_list,
                                        divider=frame_border)


    return_string += f"{' ' * outer_padding}{top_left[frame_border]}{top_border_inner}{top_right[frame_border]}\n"

    return return_string