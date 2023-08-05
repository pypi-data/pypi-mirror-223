from typing import List

from tablate.type.primitives import FrameNameList
from tablate.type.type_input import FrameDict, FrameDictList
from tablate.type.type_store import FrameStoreList
from tablate.type.type_global import Globals


class TablateBase:

    _globals_dict: dict

    _frame_list: FrameDictList

    _name_list: FrameNameList
