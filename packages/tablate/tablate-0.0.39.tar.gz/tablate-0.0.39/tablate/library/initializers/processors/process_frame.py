from copy import deepcopy
from typing import Union, Tuple

from tablate.library.calcs.gen_frame_name import gen_frame_name
from tablate.library.initializers.grid_init import grid_init
from tablate.library.initializers.table_init import table_init
from tablate.library.initializers.text_init import text_init
from tablate.type.primitives import FrameType, FrameArgs, FrameName
from tablate.type.type_global import Globals
from tablate.type.type_store import GridFrameStore, TableHeaderFrameStore, TableBodyFrameStore, FrameDictList, FrameDict


def process_frame_args(frame_args: FrameArgs,
                       frame_type: FrameType,
                       global_options: Globals) -> Union[GridFrameStore, Tuple[Union[TableHeaderFrameStore, None], TableBodyFrameStore]]:

    frame_args = deepcopy(frame_args)

    # if frame_type == "text":
    #     return text_init(**frame_args, global_options=global_options)
    if frame_type == "grid" or frame_type == "text":
        return grid_init(**frame_args, global_options=global_options)
    if frame_type == "table":
        return table_init(**frame_args, global_options=global_options)


def process_frame(frame_name: FrameName,
                  frame_type: FrameType,
                  frame_args: FrameArgs,
                  frame_list: FrameDictList,
                  global_options: Globals) -> FrameDict:
    if "self" in frame_args:
        del frame_args["self"]
    if "html_default_colors" in frame_args:
        del frame_args["html_default_colors"]
    if "outer_border" in frame_args:
        del frame_args["outer_border"]
    if "outer_padding" in frame_args:
        del frame_args["outer_padding"]
    if "outer_width" in frame_args:
        del frame_args["outer_width"]
    if "html_outer_styles" in frame_args:
        del frame_args["html_outer_styles"]

    if frame_type == "text":
        frame_args["columns"] = [{"string": frame_args["text"]}]
        del frame_args["text"]
        frame_args["column_padding"] = frame_args["frame_padding"]
        del frame_args["frame_padding"]
        frame_args["column_divider"] = "thin"

    if frame_type == "grid" and type(frame_args["columns"][0]) == str:
        grid_columns = []
        for column_item in frame_args["columns"]:
            grid_columns.append({
                "string": column_item
            })
        frame_args["columns"] = grid_columns

    name = gen_frame_name(name=frame_name, type=frame_type, frame_dict=frame_list)
    args = deepcopy(frame_args)
    args["name"] = name

    return FrameDict(name=name, type=frame_type, args=args, store=process_frame_args(frame_args=args,
                                                                                     frame_type=frame_type,
                                                                                     global_options=global_options))
