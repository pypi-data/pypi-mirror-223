from tablate.library.initializers.grid_init import grid_init
from tablate.library.initializers.table_init import table_init
from tablate.library.initializers.text_init import text_init
from tablate.type.primitives import FrameNameList
from tablate.type.type_global import Globals
from tablate.type.type_store import FrameStoreUnion, FrameStoreList


def process_frame_list(frame_list: dict, global_options: Globals) -> FrameStoreList:
    processed_frame_list: FrameStoreList = []
    for frame_key, frame_item in frame_list.items():
        if frame_item["type"] == "text":
            processed_frame_list.append(text_init(**frame_item["options"], global_optiona=global_options))
        if frame_item["type"] == "grid":
            processed_frame_list.append(grid_init(**frame_item["options"], global_options=global_options))
        if frame_item["type"] == "table":
            table_header, table_body = table_init(**frame_item["options"], global_options=global_options)
            if table_header:
                processed_frame_list.append(table_header)
            processed_frame_list.append(table_body)
    return processed_frame_list
