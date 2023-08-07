from typing import Union

from tablate.classes.bases.TablateApiBase import TablateApiBase
from tablate.classes.bases.TablateApiItem import TablateApiItem
from tablate.library.initializers.processors.process_frame import process_frame
from tablate.type.primitives import TextAlign, FrameDivider, OuterBorder, FrameName, TextStyle, TextColor, Background, \
    BackgroundPadding, Multiline, MaxLines, HtmlPxMultiplier, OuterPadding, OuterWidth, ColumnPadding, HtmlDefaultColors
from tablate.type.type_input import HtmlTextFrameStylesInput, HtmlOuterStylesInput


class Text(TablateApiItem):

    def __init__(self,
                 # TablateText args
                 text: Union[str, int, float],

                 name: FrameName = None,

                 text_style: TextStyle = None,
                 text_align: TextAlign = None,
                 text_color: TextColor = None,
                 frame_padding: ColumnPadding = None,
                 frame_divider: FrameDivider = None,
                 background: Background = None,
                 background_padding: BackgroundPadding = None,
                 multiline: Multiline = None,
                 max_lines: MaxLines = None,

                 html_default_colors: HtmlDefaultColors = None,

                 html_px_multiplier: HtmlPxMultiplier = None,
                 html_styles: HtmlTextFrameStylesInput = None,
                 # TablateApi arge
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
                                   frame_type="text",
                                   frame_args=locals(),
                                   frame_list=self._frame_list,
                                   global_options=self._globals_store.store)

        self._frame_list[frame_dict.name] = frame_dict
