from tablate.library.ascii.chars.line_v import v_line
from tablate.library.checkers.is_last_element import is_last_element
from tablate.library.formatters.console.cell_string import cell_string_single_line, cell_string_multi_line
from tablate.library.formatters.console.row_line_color import row_colors
from tablate.library.renderers.console.frames.render_console_columns import column_console_multiline
from tablate.library.formatters.console.row_line_divider import row_line_divider
from tablate.library.formatters.console.row_outer_border import row_outer_border
from tablate.type.type_store import TableBodyFrameStore
from tablate.type.type_global import Globals


def render_console_table_frame(table_frame_store: TableBodyFrameStore, global_options: Globals) -> str:
    return_string = ""
    line_divider_string = None

    if table_frame_store.row_styles.row_line_divider != "none":
        line_divider_row_string = row_line_divider(divider=table_frame_store.row_styles.row_line_divider,
                                                   column_list_top=table_frame_store.column_list,
                                                   column_list_bottom=table_frame_store.column_list)
        line_divider_string = row_outer_border(row_string=line_divider_row_string,
                                               global_options=global_options,
                                               row_divider=table_frame_store.row_styles.row_line_divider)
    for row_index, row_item in enumerate(table_frame_store.row_list):
        if table_frame_store.frame_styles.multiline is False or table_frame_store.frame_styles.max_lines == 1:
            row_line_string = ""
            for column_index, column_item in enumerate(table_frame_store.column_list):
                row_column_item = row_colors(column_item=column_item,
                                             row_index=row_index,
                                             table_frame_store=table_frame_store)
                row_line_string += cell_string_single_line(string=row_item[column_item["key"]],
                                                           column_item=row_column_item,
                                                           column_styles=table_frame_store.column_styles,
                                                           trunc_value=table_frame_store.frame_styles.trunc_value)
                if not is_last_element(column_index, table_frame_store.column_list):
                    row_line_string += v_line[column_item["divider"]]
            return_string += row_outer_border(row_string=row_line_string, global_options=global_options)
        else:
            formatted_columns_array = []

            for column_item in table_frame_store.column_list:
                row_column_item = row_colors(column_item=column_item,
                                             row_index=row_index,
                                             table_frame_store=table_frame_store)

                column_string_array = cell_string_multi_line(string=row_item[row_column_item["key"]],
                                                             column_item=row_column_item,
                                                             column_styles=table_frame_store.column_styles,
                                                             trunc_value=table_frame_store.frame_styles.trunc_value,
                                                             max_lines=table_frame_store.frame_styles.max_lines)
                formatted_columns_array.append(column_string_array)
            return_string += column_console_multiline(formatted_columns_array=formatted_columns_array,
                                                      frame_dict=table_frame_store,
                                                      global_options=global_options)
        if not is_last_element(row_index, table_frame_store.row_list) and line_divider_string:
            return_string += line_divider_string
    # todo: if background maybe blank doesn't add first and last line spacing (maybe remove even if no background)
    if table_frame_store.row_styles.row_line_divider == "blank":
        return_string = f"{line_divider_string}{return_string}{line_divider_string}"
    return return_string
