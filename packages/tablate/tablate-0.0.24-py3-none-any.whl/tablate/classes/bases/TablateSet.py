from copy import deepcopy
from typing import List

from tablate.classes.bases.TablateApiSet import TablateApiSet
from tablate.library.calcs.gen_frame_name import gen_frame_name
from tablate.type.primitives import OuterBorder, OuterPadding, OuterWidth, FrameDivider, Background, BackgroundPadding, \
    HtmlPxMultiplier
from tablate.type.type_input import HtmlOuterStylesInput, ColumnStylesInput, TextStylesInput, HtmlFrameStylesInput, \
    HtmlColumnStylesInput, HtmlTextStylesInput, FrameDictList


class TablateSet(TablateApiSet):

    def __init__(self,
                 frame_list: List[FrameDictList],
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

        super().__init__(outer_border=outer_border,
                         outer_padding=outer_padding,
                         outer_width=outer_width,
                         frame_divider=frame_divider,
                         background=background,
                         background_padding=background_padding,
                         html_px_multiplier=html_px_multiplier,
                         html_styles=html_styles,
                         column_styles=column_styles,
                         text_styles=text_styles,
                         html_frame_styles=html_frame_styles,
                         html_column_styles=html_column_styles,
                         html_text_styles=html_text_styles)

        for frame_set in frame_list:
            for frame_key, frame_item in frame_set.items():
                name = gen_frame_name(name=frame_key, type=frame_item["type"], frame_dict=self._frame_list, ensure_unique=True)
                frame_item['name'] = name
                self._frame_list[name] = deepcopy(frame_item)
