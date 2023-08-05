from copy import copy
from typing import List, Union

from tablate.classes.bases.TablateApiItem import TablateApiItem
from tablate.library.calcs.gen_frame_name import gen_frame_name
from tablate.type.primitives import FrameDivider, ColumnDivider, OuterBorder, OuterPadding, OuterWidth, Background, \
    BackgroundPadding, HtmlPxMultiplier, Multiline, MaxLines, ColumnPadding, TextStyle, TextAlign, TextColor, FrameName
from tablate.type.type_input import GridColumnInput, HtmlOuterStylesInput, HtmlGridFrameStylesInput


class Grid(TablateApiItem):

    def __init__(self,
                 # TablateGrid args
                 columns: List[Union[str, GridColumnInput]],
                 name: FrameName = None,
                 frame_divider: FrameDivider = None,
                 background: Background = None,
                 background_padding: BackgroundPadding = None,
                 multiline: Multiline = None,
                 max_lines: MaxLines = None,
                 column_divider: ColumnDivider = None,
                 column_padding: ColumnPadding = None,
                 text_style: TextStyle = None,
                 text_align: TextAlign = None,
                 text_color: TextColor = None,
                 html_px_multiplier: HtmlPxMultiplier = None,
                 html_styles: HtmlGridFrameStylesInput = None,
                 # TablateApi args
                 outer_border: OuterBorder = None,
                 outer_padding: OuterPadding = None,
                 outer_width: OuterWidth = None,
                 html_outer_styles: HtmlOuterStylesInput = None) -> None:

        super().__init__(outer_border=outer_border,
                         outer_padding=outer_padding,
                         frame_divider=frame_divider,
                         outer_width=outer_width,
                         html_styles=html_outer_styles)

        name = gen_frame_name(name=name, type="grid", frame_dict=self._frame_list)

        args = copy(locals())
        del args["self"]

        self._frame_list[name] = {
            "name": name,
            "type": "grid",
            "options": args
        }
