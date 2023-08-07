from typing import Union

from tablate.type.type_store import FrameDict, FrameDictList


def select_frame(frame_list: FrameDictList, selector: Union[int, str]) -> FrameDict:
    for frame_index, (frame_key, frame_item) in enumerate(frame_list.items()):
        if (type(selector) == int and selector == frame_index) or (type(selector) == str and selector == frame_key):
            return frame_item
