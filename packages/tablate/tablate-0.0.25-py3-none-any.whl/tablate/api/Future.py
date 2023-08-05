from copy import copy
from typing import List, Union

from tablate.api.functions import concat

from tablate.classes.bases.TablateApiSet import TablateApiSet
from tablate.library.calcs.gen_frame_name import gen_frame_name
from tablate.library.calcs.random_string import random_string
from tablate.type.primitives import FrameDivider, Multiline, TextColor, \
    TextAlign, TextStyle, MaxLines, HideHeader, Background, ColumnDivider, ColumnPadding, HtmlPxMultiplier, \
    BackgroundPadding, FrameName, OuterBorder, OuterPadding, OuterWidth
from tablate.type.type_input import GridColumnInput, TableHeaderFrameStylesInput, \
    TableBodyFrameStylesInput, HtmlTableBodyFrameStylesInput, HtmlTableHeaderFrameStylesInput, \
    HtmlTableFrameStylesInput, TableColumnInput, \
    TableRowsDataInputDict, \
    HtmlTextFrameStylesInput, \
    HtmlGridFrameStylesInput, HtmlOuterStylesInput, ColumnStylesInput, TextStylesInput, HtmlFrameStylesInput, \
    HtmlColumnStylesInput, HtmlTextStylesInput


class Tablate(TablateApiSet):
    # todo: reintroduce __init__ to all APIs... perhaps remove from parent classes so no need to call super() (copy/paste) > there are a few things which will need to be copied around... pull together... make a list or something... if very ambitious make a program to automate copy/paste on build...
    # def __init__(self,
    #              outer_border: OuterBorder = None,
    #              outer_padding: OuterPadding = None,
    #              outer_width: OuterWidth = None,
    #
    #              frame_divider: FrameDivider = None,
    #              background: Background = None,
    #              background_padding: BackgroundPadding = None,
    #
    #              html_px_multiplier: HtmlPxMultiplier = None,
    #              html_styles: HtmlOuterStylesInput = None,
    #
    #              column_styles: ColumnStylesInput = None,
    #              text_styles: TextStylesInput = None,
    #
    #              html_frame_styles: HtmlFrameStylesInput = None,
    #
    #              html_column_styles: HtmlColumnStylesInput = None,
    #              html_text_styles: HtmlTextStylesInput = None) -> None:
    #
    #     args = copy(locals())
    #     del args["self"]
    #
    #     super().__init__(**args)

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

        # self._frame_list.append({
        #     "name": name,
        #     "type": "text",
        #     "options": locals()
        # })

        # text_frame_store = text_init(text=text,
        #                              name=name,
        #                              frame_divider=frame_divider,
        #                              frame_padding=frame_padding,
        #                              background=background,
        #                              background_padding=background_padding,
        #                              multiline=multiline,
        #                              max_lines=max_lines,
        #                              text_style=text_style,
        #                              text_align=text_align,
        #                              text_color=text_color,
        #                              html_px_multiplier=html_px_multiplier,
        #                              html_styles=html_styles,
        #                              globals=self._globals)

        name = gen_frame_name(name=name, type="text", frame_dict=self._frame_list)

        args = copy(locals())
        del args["self"]
        args["columns"] = [{"string":text}]

        self._frame_list[name] = {
            "name": name,
            "type": "text",
            "options": args
        }
        # self._frame_list.append(text_frame_store)

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
                       html_styles: HtmlGridFrameStylesInput = None) -> None:

        name = gen_frame_name(name=name, type="grid", frame_dict=self._frame_list)

        args = copy(locals())
        del args["self"]

        self._frame_list[name] = {
            "name": name,
            "type": "grid",
            "options": args
        }

        # grid_frame_store = grid_init(columns=columns,
        #                              name=name,
        #                              frame_divider=frame_divider,
        #                              background=background,
        #                              background_padding=background_padding,
        #                              multiline=multiline,
        #                              max_lines=max_lines,
        #                              column_divider=column_divider,
        #                              column_padding=column_padding,
        #                              text_style=text_style,
        #                              text_align=text_align,
        #                              text_color=text_color,
        #                              html_styles=html_styles,
        #                              html_px_multiplier=html_px_multiplier,
        #                              globals=self._globals)
        #
        # self._frame_list.append(grid_frame_store)

    def add_table_frame(self,
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
                        html_body_styles: HtmlTableBodyFrameStylesInput = None) -> None:

        name = gen_frame_name(name=name, type="table", frame_dict=self._frame_list)

        args = copy(locals())
        del args["self"]

        self._frame_list[name] = {
            "name": name,
            "type": "table",
            "options": args
        }

        # table_header_store, table_body_store = table_init(columns=columns,
        #                                                   rows=rows,
        #                                                   name=name,
        #                                                   frame_divider=frame_divider,
        #                                                   multiline=multiline,
        #                                                   max_lines=max_lines,
        #                                                   background=background,
        #                                                   background_padding=background_padding,
        #                                                   multiline_header=multiline_header,
        #                                                   max_lines_header=max_lines_header,
        #                                                   hide_header=hide_header,
        #                                                   column_divider=column_divider,
        #                                                   column_padding=column_padding,
        #                                                   header_base_divider=header_base_divider,
        #                                                   row_line_divider=row_line_divider,
        #                                                   odd_row_background=odd_row_background,
        #                                                   even_row_background=even_row_background,
        #                                                   text_style=text_style,
        #                                                   text_align=text_align,
        #                                                   text_color=text_color,
        #                                                   header_styles=header_styles,
        #                                                   body_styles=body_styles,
        #                                                   html_px_multiplier=html_px_multiplier,
        #                                                   html_styles=html_styles,
        #                                                   html_header_styles=html_header_styles,
        #                                                   html_body_styles=html_body_styles,
        #                                                   globals=self._globals)
        #
        # if table_header_store:
        #     self._frame_list.append(table_header_store)
        #
        # self._frame_list.append(table_body_store)


########################################################################################################################
########################################################################################################################
########################################################################################################################

#
# column_list: List[Union[GridColumnInput, TableColumnInput]] = [
#     {
#         "string": "Column One",
#         "key": "Key One",
#         "width": "50%",
#         "divider": "thick",
#         "background": "blue"
#     },
#     {
#         "string": "Column Two",
#         "key": "Key Two",
#         "text_align": "right",
#         "divider": "double"
#
#     },
#     {
#         "string": "Column Three",
#         "key": "Key Three",
#         "text_align": "right"
#     }
# ]
#
# column_list2: List[Union[GridColumnInput, TableColumnInput]] = [
#     {
#         "string": "Column One",
#         "key": "Key One",
#         "width": "25%",
#         "divider": "thick",
#         "background": "blue"
#     },
#     {
#         "string": "Column Two",
#         "key": "Key Two",
#         "text_align": "right",
#         "divider": "double"
#
#     },
#     {
#         "string": "Column Three",
#         "key": "Key Three",
#         "text_align": "right"
#     }
# ]
#
# row_list = [
#     {
#         "Key One": "Some string value",
#         "Key Two": 4,
#         "Key Three": 9.6,
#         "divider": "thick"
#     },
#     {
#         "Key One": "Some other string value",
#         "Key Two": 5,
#         "Key Three": 4.6
#
#     },
#     {
#         "Key One": "Some final string value",
#         "Key Two": 100,
#         "Key Three": 328.832
#
#     }
# ]
# ########################################################################################################################
# html_global_styles_input = HtmlOuterBase(html_outer_border_style="thick",
#                                          html_outer_padding=16,
#                                          html_outer_width="100%")
# ########################################################################################################################
# frame_styles_input = FrameStylesInput(frame_divider="thick",
#                                       max_lines=None,
#                                       multiline=True,
#                                       background="yellow",
#                                       trunc_value="...")
# column_styles_input = ColumnStylesInput(divider="thick",
#                                         padding=1)
# text_styles_input = TextStylesInput(text_style="bold",
#                                     text_align="left",
#                                     text_color="green")
# ########################################################################################################################
# html_frame_styles_input = HtmlFrameStylesInput(html_frame_divider_style="thick",
#                                                html_max_lines=5,
#                                                html_multiline=True,
#                                                html_background="green")
# html_column_styles_input = HtmlColumnStylesInput(html_divider_style="thin",
#                                                  html_padding=6)
# html_text_styles_input = HtmlTextStylesInput(html_text_style="normal",
#                                              html_text_align="left",
#                                              html_text_color="red",
#                                              html_text_size=16)
# ########################################################################################################################
# table_rows_frame_styles_input = TableBodyFrameStylesInput(frame_styles=frame_styles_input,
#                                                           column_styles=column_styles_input,
#                                                           text_styles=text_styles_input,
#                                                           row_styles=TableRowsBase(row_line_divider="thin",
#                                                                                    odds_background="grey",
#                                                                                    evens_background="green"))
# header_frame_styles_input = TableHeaderFrameStylesInput(frame_styles=frame_styles_input,
#                                                         column_styles=column_styles_input,
#                                                         text_styles=text_styles_input)
# html_header_styles_input = HtmlTableHeaderFrameStylesInput(html_frame_styles=html_frame_styles_input,
#                                                            html_column_styles=html_column_styles_input,
#                                                            html_text_styles=html_text_styles_input)
# html_rows_styles_input = HtmlTableBodyFrameStylesInput(html_frame_styles=html_frame_styles_input,
#                                                        html_column_styles=html_column_styles_input,
#                                                        html_text_styles=html_text_styles_input,
#                                                        html_row_styles=HtmlTableRowsBase(
#                                                            html_row_line_divider_style="none"
#                                                        ))
# ########################################################################################################################
#
# start = time.perf_counter_ns()
# test = Tablate()
# # test = Tablate(outer_border="thin",
# #                      outer_padding=6,
# #                      outer_width=120,
# #                      html_outer_styles=html_global_styles_input,
# #                      frame_divider="double",
# #                      background="blue",
# #                      column_styles=column_styles_input,
# #                      text_styles=text_styles_input,
# #                      html_frame_styles=html_frame_styles_input,
# #                      html_column_styles=html_column_styles_input,
# #                      html_text_styles=html_text_styles_input)
#
# test.add_text_frame(text="Some String...",
#                     text_style="bold",
#                     text_align="left",
#                     text_color="red",
#                     frame_divider="thick",
#                     background="blue",
#                     multiline=True,
#                     max_lines=5)
#
# test.add_grid_frame(columns=column_list,
#                     frame_divider="thick",
#                     text_color="white",
#                     text_style="bold_underlined",
#                     background="dark_red",
#                     multiline=True,
#                     max_lines=5)
#
# test.add_table_frame(columns=column_list,
#                      rows=row_list,
#                      odd_row_background="red",
#                      text_color="yellow")
#
# test.add_grid_frame(columns=column_list)
#
# test.add_table_frame(columns=column_list,
#                      rows=row_list,
#                      name="Some Table",
#                      frame_divider="thick",
#                      background="blue",
#                      multiline=True,
#                      max_lines=5,
#                      multiline_header=False,
#                      max_lines_header=None,
#                      hide_header=False,
#
#                      column_divider="thin",
#                      column_padding=1,
#                      header_base_divider="thick",
#                      row_line_divider="thin",
#                      even_row_background="magenta",
#                      odd_row_background="blue",
#
#                      text_style="bold",
#                      text_align="center",
#                      text_color="blue",
#
#                      header_styles=header_frame_styles_input,
#                      body_styles=table_rows_frame_styles_input,
#
#                      html_styles=html_rows_styles_input,
#
#                      html_header_styles=html_header_styles_input,
#                      html_body_styles=html_rows_styles_input)
#
#
# test.add_text_frame(text="Some String...")
#
# test.add_grid_frame(columns=column_list)
#
# test.add_table_frame(columns=column_list2,
#                      rows=row_list,
#                      hide_header=True)
#
# test.add_grid_frame(columns=column_list, html_px_multiplier=3, text_color="blue")
#
# test.add_table_frame(columns=column_list,
#                      rows=row_list,
#                      text_color="grey")
#
#
# string = test.to_string()
# html = test.to_html()
# print(string)
# print(html)
#
# test.list_frames()
#
# test.get_frame(9).print()

column_list = [
    {
        "string": "Column One",
        "key": "one",
        "width": "50%",
        "divider": "thick",
    },
    {
        "string": "Column Two",
        "key": "two",
        "text_align": "right",

    },
    {
        "string": "Column Three",
        "key": "three",
        "text_align": "right"
    }
]

row_list = [
    {
        "one": "Some string value",
        "two": 4,
        "three": 9.6,
    },
    {
        "one": "Some other string value",
        "two": 5,
        "three": 4.6

    },
    {
        "one": "Some final string value",
        "two": 100,
        "three": 328.832

    }
]

tab = Tablate(outer_border="thin")

tab.add_table_frame(columns=column_list, rows=row_list, background="red", multiline=True)
tab.add_text_frame("one")
tab.add_table_frame(columns=column_list, rows=row_list, background="green")
tab.add_text_frame("two")
tab.add_table_frame(columns=column_list, rows=row_list, background="blue")
tab.add_text_frame("three", multiline=True)
tab.add_table_frame(columns=column_list, rows=row_list, background="cyan", hide_header=True, multiline=True)
tab.add_text_frame("four")
tab.add_table_frame(columns=column_list, rows=row_list, background="yellow")
tab.add_table_frame(columns=column_list, rows=row_list, background="magenta", name="Test")
tab.add_table_frame(columns=column_list, rows=row_list, background="magenta", name="Test")
tab.add_table_frame(columns=column_list, rows=row_list, background="magenta", name="Test")
tab.add_table_frame(columns=column_list, rows=row_list, background="magenta", name="Test")
tab.add_table_frame(columns=column_list, rows=row_list, background="magenta", name="Test")
tab.add_table_frame(columns=column_list, rows=row_list, background="magenta", name="Test")
tab.add_table_frame(columns=column_list, rows=row_list, background="magenta", name="Test")
tab.add_grid_frame(columns=column_list)





tab.print()
tab.list_frames()
print(tab.to_html())
tab.get_frame(3).print()
tab.get_frame(3, apply_globals=True).print()
tab.list_frames()
got_frame = tab.get_frame(4, apply_globals=True)
tab.replace_frame(3, got_frame, "cat")
tab.list_frames()

tab.apply_style(".tablate_frame_3.tablate_row", "background-color:pink", ":hover")
print(tab.to_html())
# tab.remove_frame(0)
# tab.print()

# got_frame.name()
# got_frame.rename("lala")
# got_frame.name()
#
# new_frame = concat.concat([tab, got_frame], outer_border="thin")
#
# new_frame.print()
#
# new_frame.list_frames()
#
# # for item_key, item_name in new_frame._frame_list.items():
# #     print(item_key, item_name["name"])
#
# test_frame = new_frame.get_frame("Test", apply_globals=True)
#
# test_frame.print()
#
# # test_frame.apply(lambda x, y: print(x,y))
#
# # print(tab.get_frame(9).to_dict())
#
# import pandas as pd
#
#
# arrays = [[1, 1, 2, 2], ['red', 'blue', 'red', 'blue']]
#
# mul = pd.MultiIndex.from_arrays(arrays)
# df3 = pd.DataFrame({"one": ["sdfsdfsdfs sd  fsd f sd fsdfsdfsdf  sdfsdfff sd f sd fsd fsdf sdf sd f sd f sd f sd f s sd f sdfsdfkjsdf ds f dsf sdfsdfsdf sdf sdfsdfdsfdsf dsfsdfsdf",2,3,4], "two": [1,2,3,4]}, index=mul)
# tab.from_dict(df3.to_dict(), row_line_divider="blank")
#
# tab.print()