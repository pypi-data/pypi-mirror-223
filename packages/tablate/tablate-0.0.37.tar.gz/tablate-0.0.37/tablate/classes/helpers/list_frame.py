from tablate.library.ascii.chars.line_h import h_line
from tablate.library.ascii.chars.line_v import v_line
from tablate.library.ascii.chars.matrix_cross import cross_matrix
from tablate.library.checkers.set_key_resolver import set_key_resolver
from tablate.library.formatters.console.ascii_styler import ascii_text_styler, ascii_terminator
from tablate.library.formatters.console.concat_string import concat_string
from tablate.type.type_global import Globals
from tablate.type.type_store import FrameDictList


def list_frames(frame_list: FrameDictList, global_options: Globals):
    print()
    # top_index = f"{' '}{h_line['thin'] * ((len(frame_list) // 10) + 3)}{cross_matrix['blank']['thin']['thin']}"
    # top_name = f"{h_line['thin'] * 22}{cross_matrix['blank']['thin']['thin']}"
    # top_type = f"{h_line['thin'] * 8}{cross_matrix['blank']['thin']['thin']}"
    # top_cols = f"{h_line['thin'] * 7}{cross_matrix['blank']['thin']['thin']}"
    # top_rows = f"{h_line['thin'] * 7}{cross_matrix['blank']['thin']['thin']}"
    # top_globals = f"{h_line['thin'] * 42}"
    # print(f"{top_index}{top_name}{top_type}{top_cols}{top_rows}{top_globals}")
    divider = v_line["thin"]
    padding = " "
    header_string = f"{padding} {' ' * ((len(frame_list) // 10) + 1)}{padding}"
    frame_name, name_ws = concat_string(string="Name",
                                        width=20,
                                        padding=0,
                                        trunc_value="")
    frame_name = ascii_text_styler(string=frame_name, column_dict={"text_style": "bold"}) + ascii_terminator()
    header_string += f"{divider}{padding}{frame_name}{' ' * name_ws}{padding}"
    frame_type, type_ws = concat_string(string="Type",
                                        width=6,
                                        padding=0,
                                        trunc_value="")
    frame_type = ascii_text_styler(string=frame_type, column_dict={"text_style": "bold"}) + ascii_terminator()
    header_string += f"{divider}{padding}{frame_type}{' ' * type_ws}{padding}"
    frame_cols, cols_ws = concat_string(string="Cols.",
                                        width=5,
                                        padding=0,
                                        trunc_value="")
    frame_cols = ascii_text_styler(string=frame_cols, column_dict={"text_style": "bold"}) + ascii_terminator()
    header_string += f"{divider}{padding}{frame_cols}{' ' * cols_ws}{padding}"
    frame_rows, rows_ws = concat_string(string="Rows",
                                        width=5,
                                        padding=0,
                                        trunc_value="")
    frame_rows = ascii_text_styler(string=frame_rows, column_dict={"text_style": "bold"}) + ascii_terminator()
    header_string += f"{divider}{padding}{' ' * rows_ws}{frame_rows}{padding}"
    frame_options = ascii_text_styler(string="Options", column_dict={"text_style": "bold"}) + ascii_terminator()
    header_string += f"{divider}{padding}{frame_options}{padding}"
    default_options = ascii_text_styler(string="[defaults]", column_dict={"text_style": "bold"}) + ascii_terminator()
    header_string += default_options
    print(header_string)
    divider_index = f"{padding}{h_line['thin'] * ((len(frame_list) // 10) + 3)}{cross_matrix['thin']['thin']['thin']}"
    divider_name = f"{h_line['thin'] * 22}{cross_matrix['thin']['thin']['thin']}"
    divider_type = f"{h_line['thin'] * 8}{cross_matrix['thin']['thin']['thin']}"
    divider_cols = f"{h_line['thin'] * 7}{cross_matrix['thin']['thin']['thin']}"
    divider_rows = f"{h_line['thin'] * 7}{cross_matrix['thin']['thin']['thin']}"
    divider_globals = f"{h_line['thin'] * 42}"
    print(f"{divider_index}{divider_name}{divider_type}{divider_cols}{divider_rows}{divider_globals}")
    ####################################################################################################################
    # global_options = globals_init(**global_options)
    processed_frame_list = []
    for _, frame_item in frame_list.items():
        if frame_item.type == "table":
            if frame_item.args["hide_header"] is not True:
                processed_frame_list.append(frame_item.store[0])
            processed_frame_list.append(frame_item.store[1])
        else:
            processed_frame_list.append(frame_item.store)
    processed_frame_index = 0
    ####################################################################################################################

    for frame_index, (frame_key, frame_item) in enumerate(frame_list.items()):
        item_string = f"{padding}"
        index, index_ws = concat_string(string=frame_index,
                                        width=(len(frame_list) // 10) + 1,
                                        padding=0,
                                        trunc_value="")
        item_string += f"{padding}{' ' * index_ws}{index}{padding}"
        item_name, name_ws = concat_string(string=frame_item.name,
                                           width=20,
                                           padding=0,
                                           trunc_value="...")
        item_string += f"{divider}{padding}{item_name}{' ' * name_ws}{padding}"
        item_type = frame_item.type.capitalize() if frame_item.type != "table_body" else "Table"
        item_type, type_ws = concat_string(string=item_type,
                                           width=6,
                                           padding=0,
                                           trunc_value="")
        item_string += f"{divider}{padding}{item_type}{' ' * type_ws}{padding}"
        item_cols, cols_ws = concat_string(string=len(frame_item.args["columns"]),
                                           width=5,
                                           padding=0,
                                           trunc_value="")
        item_cols = item_cols if frame_item.type != "text" else "-"
        item_string += f"{divider}{padding}{' ' * cols_ws}{item_cols}{padding}"
        item_rows_list = set_key_resolver(instance=frame_item.args, key="row_list", default=[])
        item_rows, rows_ws = concat_string(string=len(item_rows_list),
                                           width=5,
                                           padding=0,
                                           trunc_value="")
        item_rows = item_rows if frame_item.type == "table" else "-"
        item_string += f"{divider}{padding}{' ' * rows_ws}{item_rows}{padding}"
        item_options_list = []
        default_options_list = []
        item_options_list.append("hide_header") if "hide_header" in frame_item.args and frame_item.args["hide_header"] is True else None
        default_options_list.append("hide_header") if hasattr(processed_frame_list[processed_frame_index].frame_styles, "hide_header") and processed_frame_list[processed_frame_index].frame_styles.hide_header is True else None
        item_options_list.append("multiline") if frame_item.args["multiline"] is True else None
        default_options_list.append("multiline") if processed_frame_list[processed_frame_index].frame_styles.multiline is True else None
        item_options_list.append(f"max_lines: {frame_item.args['max_lines']}") if frame_item.args["max_lines"] is not None else None
        default_options_list.append("max_lines") if processed_frame_list[processed_frame_index].frame_styles.max_lines is not None else None
        duplicate_options_list = []
        for default_option_index, default_option_item in enumerate(default_options_list):
            if default_option_item in item_options_list:
                duplicate_options_list.append(default_option_index)
        duplicate_options_list.reverse()
        for duplicate_option in duplicate_options_list:
            default_options_list.pop(duplicate_option)
        item_options_string = f"{', '.join(item_options_list)}{padding}" if len(item_options_list) > 0 else ""
        duplicate_option_string = f"[{', '.join(default_options_list)}]" if len(default_options_list) > 0 else ""
        item_string += f"{divider}{padding}{item_options_string}{duplicate_option_string}"
        print(item_string)
        processed_frame_index += 1 if processed_frame_list[processed_frame_index].type != "table_header" else 2
    print()

    # todo: please fix this!!!