from copy import deepcopy
from typing import List

from tablate.classes.bases.TablateSet import TablateSet
from tablate.classes.classes import TablateUnion
from tablate.type.primitives import FrameDivider, OuterBorder, OuterPadding, OuterWidth, Background, BackgroundPadding, \
    HtmlPxMultiplier
from tablate.type.type_input import HtmlOuterStylesInput, ColumnStylesInput, TextStylesInput, HtmlFrameStylesInput, \
    HtmlColumnStylesInput, HtmlTextStylesInput, FrameDictList


def concat(frame_list: List[TablateUnion],
           outer_border: OuterBorder = None,
           outer_padding: OuterPadding = None,
           outer_width: OuterWidth = None,

           frame_divider: FrameDivider = None,
           background: Background = None,
           background_padding: BackgroundPadding = None,

           html_px_multiplier: HtmlPxMultiplier = None,
           html_styles: HtmlOuterStylesInput = None,

           column_styles: ColumnStylesInput = None,
           text_styles: TextStylesInput = None,

           html_frame_styles: HtmlFrameStylesInput = None,

           html_column_styles: HtmlColumnStylesInput = None,
           html_text_styles: HtmlTextStylesInput = None):

    input_dict_list: List[FrameDictList] = []

    for frame_set in frame_list:
        input_dict_list.append(deepcopy(frame_set._frame_list))

    args = deepcopy(locals())

    args["frame_list"] = input_dict_list
    del args["input_dict_list"]
    del args["frame_set"]

    return TablateSet(**args)
