from typing import List, Union

from tablate.classes.bases.TablateApiBase import TablateApiBase
from tablate.classes.bases.TablateApiItem import TablateApiItem
from tablate.library.initializers.processors.process_frame import process_frame
from tablate.type.primitives import FrameDivider, ColumnDivider, OuterBorder, OuterPadding, OuterWidth, Background, \
    BackgroundPadding, HtmlPxMultiplier, Multiline, MaxLines, ColumnPadding, TextStyle, TextAlign, TextColor, FrameName, \
    HtmlDefaultColors
from tablate.type.type_input import GridColumnInput, HtmlOuterStylesInput, HtmlGridStylesInput


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
                 html_styles: HtmlGridStylesInput = None,
                 # TablateApi args
                 html_default_colors: HtmlDefaultColors = None,
                 outer_border: OuterBorder = None,
                 outer_padding: OuterPadding = None,
                 outer_width: OuterWidth = None,
                 html_outer_styles: HtmlOuterStylesInput = None) -> None:

        TablateApiBase.__init__(self=self,
                                outer_border=outer_border,
                                outer_padding=outer_padding,
                                frame_divider=frame_divider,
                                outer_width=outer_width,
                                html_outer_styles=html_outer_styles,
                                html_default_colors=html_default_colors)

        frame_dict = process_frame(frame_name=name,
                                   frame_type="grid",
                                   frame_args=locals(),
                                   frame_list=self._frame_list,
                                   global_options=self._globals_store.store)

        self._frame_list[frame_dict.name] = frame_dict
