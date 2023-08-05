from copy import deepcopy, copy
from typing import Union, Callable, Tuple

from tablate.api.modules.Table import Table
from tablate.classes.bases.TablateApiBase import TablateApiBase
from tablate.classes.classes import TablateUnion
from tablate.classes.helpers.get_frame import get_frame
from tablate.classes.helpers.list_frame import list_frames
from tablate.library.calcs.gen_frame_name import gen_frame_name
from tablate.type.primitives import FrameName, FrameDivider, Multiline, MaxLines, Background, BackgroundPadding, \
    HideHeader, ColumnDivider, ColumnPadding, TextStyle, TextAlign, TextColor, HtmlPxMultiplier, OuterBorder, \
    OuterPadding, OuterWidth
from tablate.type.type_input import TableHeaderFrameStylesInput, TableBodyFrameStylesInput, HtmlTableFrameStylesInput, \
    HtmlTableHeaderFrameStylesInput, HtmlTableBodyFrameStylesInput, HtmlOuterStylesInput


class TablateApiSet(TablateApiBase):

    def list_frames(self):
        list_frames(self._frame_list, self._globals_dict)

    def get_frame(self, selector: Union[int, str], apply_globals: bool = False):
        if apply_globals:
            return deepcopy(get_frame(frame_list=self._frame_list, selector=selector, global_options=self._globals_dict))
        else:
            return deepcopy(get_frame(frame_list=self._frame_list, selector=selector))

    def from_dict(self,
                  dict_object: dict,
                  name: FrameName = None,
                  capitalize_keys: bool = True,
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
                  html_body_styles: HtmlTableBodyFrameStylesInput = None):

        name = gen_frame_name(name=name, type="table", frame_dict=self._frame_list)

        args = deepcopy(locals())
        del args["self"]
        del args["dict_object"]
        del args["capitalize_keys"]

        columns = []
        rows = []
        for col_index, (col_key, col_value) in enumerate(dict_object.items()):
            for row_index, (value_index, value) in enumerate(col_value.items()):
                if col_index == 0:
                    rows.append({})
                    if type(value_index) == tuple:
                        for i in range(0, len(value_index)):
                            if row_index == 0:
                                columns.append({"key": f"i{i}", "width": "10%", "text_align": "right"})
                            rows[row_index][f"i{i}"] = value_index[i]
                    else:
                        if row_index == 0:
                            columns.append({"key": "i", "width": "10%", "text_align": "right"})
                        rows[row_index]["i"] = value_index
                rows[row_index][col_key.title() if capitalize_keys else col_key] = value
            columns.append({"key": col_key.title() if capitalize_keys else col_key})
        new_table = Table(columns=columns, rows=rows, **args)
        # todo: fix column widths... ensure no bugs if millions of index columns
        # todo: for later allow specific column widths
        self._frame_list[name] = {"name": name, "type": "table", "options": {"columns":columns, "rows":rows, **args}}




    def remove_frame(self, selector: Union[int, str]):
        for frame_index, (frame_key, frame_item) in enumerate(self._frame_list.items()):
            if (type(selector) == int and selector == frame_index) or (type(selector) == str and selector == frame_key):
                del self._frame_list[frame_key]
                break

    def replace_frame(self, selector: Union[int, str], new_frame: TablateUnion, new_name: str = None):
        new_frame = deepcopy(new_frame)
        for frame_index, (frame_key, frame_item) in enumerate(self._frame_list.items()):
            if (type(selector) == int and selector == frame_index) or (type(selector) == str and selector == frame_key):
                for new_frame_key, new_frame_item in new_frame._frame_list.items():
                    new_name = new_name if new_name is not None else new_frame_key
                    new_name = gen_frame_name(name=new_name, type=new_frame_item["type"], frame_dict=self._frame_list, ensure_unique=True)
                    new_frame_item["name"] = new_name
                    new_frame_item["options"]["name"] = new_name
                    self._frame_list = {key if key != frame_key else new_name: value for key, value in self._frame_list.items()}
                    self._frame_list[new_name] = new_frame_item
                    break
