from tablate.library.renderers.console.render_console_foot import render_console_foot
from tablate.library.renderers.console.render_console_frames import render_console_frames
from tablate.library.renderers.console.render_console_head import render_console_head
from tablate.type.type_store import FrameDictList
from tablate.type.type_global import Globals


def render_console(frame_list: FrameDictList, global_options: Globals) -> str:
    processed_frame_list = []
    for _, frame_item in frame_list.items():
        if frame_item.type == "table":
            if frame_item.args["hide_header"] is not True:
                processed_frame_list.append(frame_item.store[0])
            processed_frame_list.append(frame_item.store[1])
        else:
            processed_frame_list.append(frame_item.store)
    return_string = ""
    if len(processed_frame_list) > 0:
        return_string += render_console_head(frame_list=processed_frame_list, global_options=global_options)
        return_string += render_console_frames(frame_list=processed_frame_list, global_options=global_options)
        return_string += render_console_foot(frame_list=processed_frame_list, global_options=global_options)
    return return_string
