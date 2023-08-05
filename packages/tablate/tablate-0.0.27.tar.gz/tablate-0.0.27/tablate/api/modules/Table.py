from copy import copy
from typing import List

from tablate.classes.bases.TablateApiBase import TablateApiBase
from tablate.classes.bases.TablateApiItem import TablateApiItem
from tablate.library.calcs.gen_frame_name import gen_frame_name
from tablate.type.primitives import FrameDivider, ColumnDivider, OuterBorder, \
    FrameName, Multiline, MaxLines, Background, BackgroundPadding, HideHeader, ColumnPadding, TextAlign, TextStyle, \
    TextColor, HtmlPxMultiplier, OuterPadding, OuterWidth
from tablate.type.type_input import TableColumnInput, TableRowsDataInputDict, TableBodyFrameStylesInput, \
    TableHeaderFrameStylesInput, HtmlTableFrameStylesInput, HtmlTableHeaderFrameStylesInput, \
    HtmlTableBodyFrameStylesInput, HtmlOuterStylesInput


class Table(TablateApiItem):

    def __init__(self,
                 # TablateTable args
                 columns: List[TableColumnInput],
                 rows: List[TableRowsDataInputDict],

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

                 html_px_multiplier: HtmlPxMultiplier = None,
                 html_styles: HtmlTableFrameStylesInput = None,

                 html_header_styles: HtmlTableHeaderFrameStylesInput = None,
                 html_body_styles: HtmlTableBodyFrameStylesInput = None,

                 outer_border: OuterBorder = None,
                 outer_padding: OuterPadding = None,
                 outer_width: OuterWidth = None,
                 html_outer_styles: HtmlOuterStylesInput = None) -> None:

        TablateApiBase.__init__(self=self,
                                outer_border=outer_border,
                                outer_padding=outer_padding,
                                frame_divider=frame_divider,
                                outer_width=outer_width,
                                html_styles=html_outer_styles)

        name = gen_frame_name(name=name, type="table", frame_dict=self._frame_list)

        args = copy(locals())
        del args["self"]

        self._frame_list[name] = {
            "name": name,
            "type": "table",
            "options": args
        }