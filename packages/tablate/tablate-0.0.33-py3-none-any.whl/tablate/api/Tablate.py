from copy import copy
from typing import List, Union

from tablate.classes.bases.TablateApiSet import TablateApiSet
from tablate.library.calcs.gen_frame_name import gen_frame_name
from tablate.library.initializers.grid_init import grid_init
from tablate.library.initializers.table_init import table_init
from tablate.library.initializers.text_init import text_init
from tablate.type.primitives import FrameDivider, Multiline, TextColor, \
    TextAlign, TextStyle, MaxLines, HideHeader, Background, ColumnDivider, ColumnPadding, HtmlPxMultiplier, \
    BackgroundPadding, FrameName
from tablate.type.type_input import GridColumnInput, TableHeaderFrameStylesInput, \
    TableBodyFrameStylesInput, HtmlTableBodyStylesInput, HtmlTableHeaderStylesInput, \
    HtmlTableStylesInput, TableColumnInput, \
    TableRowsInput, \
    HtmlTextFrameStylesInput, \
    HtmlGridStylesInput
from tablate.type.type_store import FrameDict


class Tablate(TablateApiSet):

    def add_text_frame(self,
                       text: Union[str, int, float],

                       name: FrameName = None,

                       text_style: TextStyle = None,
                       text_align: TextAlign = None,
                       text_color: TextColor = None,

                       frame_divider: FrameDivider = None,
                       frame_padding: ColumnPadding = None,
                       background: Background = None,
                       background_padding: BackgroundPadding = None,
                       multiline: Multiline = None,
                       max_lines: MaxLines = None,

                       html_px_multiplier: HtmlPxMultiplier = None,
                       html_styles: HtmlTextFrameStylesInput = None) -> None:

        name = gen_frame_name(name=name, type="text", frame_dict=self._frame_list)

        args = copy(locals())
        del args["self"]
        args["columns"] = [{"string":text}]

        self._frame_list[name] = FrameDict(name=name, type="text", args=args, store=text_init(**args))

    def add_grid_frame(self,
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
                       html_styles: HtmlGridStylesInput = None) -> None:

        name = gen_frame_name(name=name, type="grid", frame_dict=self._frame_list)

        args = copy(locals())
        del args["self"]

        self._frame_list[name] = FrameDict(name=name, type="grid", args=args, store=grid_init(**args))
    def add_table_frame(self,
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

                        html_px_multiplier: HtmlPxMultiplier = None,
                        html_styles: HtmlTableStylesInput = None,

                        html_header_styles: HtmlTableHeaderStylesInput = None,
                        html_body_styles: HtmlTableBodyStylesInput = None) -> None:

        name = gen_frame_name(name=name, type="table", frame_dict=self._frame_list)

        args = copy(locals())
        del args["self"]

        self._frame_list[name] = FrameDict(name=name, type="table", args=args, store=table_init(**args))