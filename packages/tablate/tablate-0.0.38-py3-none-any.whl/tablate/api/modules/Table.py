from typing import List

from tablate.classes.bases.TablateApiBase import TablateApiBase
from tablate.classes.bases.TablateApiItem import TablateApiItem
from tablate.library.initializers.processors.process_frame import process_frame
from tablate.type.primitives import FrameDivider, ColumnDivider, OuterBorder, \
    FrameName, Multiline, MaxLines, Background, BackgroundPadding, HideHeader, ColumnPadding, TextAlign, TextStyle, \
    TextColor, HtmlPxMultiplier, OuterPadding, OuterWidth, HtmlDefaultColors
from tablate.type.type_input import TableColumnInput, TableRowsInput, TableBodyFrameStylesInput, \
    TableHeaderFrameStylesInput, HtmlTableStylesInput, HtmlTableHeaderStylesInput, \
    HtmlTableBodyStylesInput, HtmlOuterStylesInput


class Table(TablateApiItem):

    def __init__(self,
                 # TablateTable args
                 columns: List[TableColumnInput],
                 rows: List[TableRowsInput],

                 name: FrameName = None,

                 frame_divider: FrameDivider = None,
                 multiline: Multiline = None,
                 max_lines: MaxLines = None,
                 background: Background = None,
                 background_padding: BackgroundPadding = None,

                 multiline_header: Multiline = None,
                 max_lines_header: MaxLines = None,
                 hide_header: HideHeader = None,

                 column_divider: ColumnDivider = None,
                 column_padding: ColumnPadding = None,
                 header_base_divider: FrameDivider = None,

                 row_line_divider: FrameDivider = None,
                 odd_row_background: Background = None,
                 even_row_background: Background = None,

                 text_style: TextStyle = None,
                 text_align: TextAlign = None,
                 text_color: TextColor = None,

                 header_styles: TableHeaderFrameStylesInput = None,
                 body_styles: TableBodyFrameStylesInput = None,

                 html_default_colors: HtmlDefaultColors = None,

                 html_px_multiplier: HtmlPxMultiplier = None,
                 html_styles: HtmlTableStylesInput = None,

                 html_header_styles: HtmlTableHeaderStylesInput = None,
                 html_body_styles: HtmlTableBodyStylesInput = None,

                 outer_border: OuterBorder = None,
                 outer_padding: OuterPadding = None,
                 outer_width: OuterWidth = None,
                 html_outer_styles: HtmlOuterStylesInput = None) -> None:

        TablateApiBase.__init__(self=self,
                                outer_border=outer_border,
                                outer_padding=outer_padding,
                                frame_divider=frame_divider,
                                outer_width=outer_width,
                                html_default_colors=html_default_colors,
                                html_outer_styles=html_outer_styles)

        frame_dict = process_frame(frame_name=name,
                                   frame_type="table",
                                   frame_args=locals(),
                                   frame_list=self._frame_list,
                                   global_options=self._globals_store.store)

        self._frame_list[frame_dict.name] = frame_dict
