import copy
import math
from typing import List, TypeVar

from tablate.type.type_store import FrameStoreUnion

T = TypeVar("T")


def calc_column_percent(frame_list: List[FrameStoreUnion], outer_width: int) -> (List[T], List[int]):
    frame_list = copy.deepcopy(frame_list)
    baseline_width_set = set()
    outer_width = outer_width - 1
    for frame_item in frame_list:
        outer_width_total = 0
        for column_item in frame_item.column_list:
            outer_width_total += column_item["width"] + 1
            acc_column_width = math.floor((100 / outer_width) * outer_width_total)
            baseline_width_set.add(math.floor(acc_column_width))
            column_item["baseline_width_percent"] = acc_column_width
    sorted_baseline_array = sorted(baseline_width_set)
    return frame_list, sorted_baseline_array



