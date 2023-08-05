import copy
from typing import List, Union, Any

from tablate.library.calcs.calc_column_widths import calc_column_widths
from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.library.initializers.mappers.element.style_mapper import style_mapper
from tablate.library.initializers.mappers.attribute.column_attr import column_attr
from tablate.type.defaults import background_padding_default, frame_name_default
from tablate.type.type_global import Globals
from tablate.type.type_store import GridFrameStore, GridColumnStore, FrameStore, ColumnStore, TextStore
from tablate.type.type_input import GridColumnInput, BaseStylesInput, HtmlGridFrameStylesInput, HtmlStylesInput
from tablate.type.primitives import FrameDivider, ColumnDivider, Background, Multiline, MaxLines, ColumnPadding, \
    TextStyle, TextAlign, TextColor, HtmlPxMultiplier, BackgroundPadding, FrameName


def grid_init(columns: List[Union[str, GridColumnInput]],
              name: FrameName,
              frame_divider: FrameDivider,
              background: Background,
              background_padding: BackgroundPadding,
              multiline: Multiline,
              max_lines: MaxLines,

              column_divider: ColumnDivider,
              column_padding: ColumnPadding,

              text_style: TextStyle,
              text_align: TextAlign,
              text_color: TextColor,

              html_px_multiplier: HtmlPxMultiplier,
              html_styles: HtmlGridFrameStylesInput,

              global_options: Globals) -> GridFrameStore:
    columns = copy.deepcopy(columns)

    background_padding = background_padding if background_padding is not None else set_attr_resolver(
        instance=global_options.console.outer_styles,
        attr="background_padding",
        default=background_padding_default)

    name = name if name is not None else frame_name_default

    grid_styles = style_mapper(base_input=BaseStylesInput(frame_styles=FrameStore(frame_divider=frame_divider,
                                                                                  max_lines=max_lines,
                                                                                  multiline=multiline,
                                                                                  background=background),
                                                          column_styles=ColumnStore(divider=column_divider,
                                                                                    padding=column_padding,
                                                                                    background_padding=background_padding),
                                                          text_styles=TextStore(text_style=text_style,
                                                                                text_align=text_align,
                                                                                text_color=text_color)),
                               html_input=html_styles,
                               base_defaults=BaseStylesInput(),
                               html_defaults=HtmlStylesInput(),
                               html_px_multiplier=html_px_multiplier,
                               global_options=global_options)

    columns = calc_column_widths(columns=columns, global_options=global_options)

    grid_column_list: List[GridColumnStore] = []

    for column_item in columns:

        if type(column_item) == str:
            column_item = {"string": column_item}

        grid_column_dict = column_attr(column_dict=column_item,
                                       frame_styles=grid_styles.frame_styles,
                                       column_styles=grid_styles.column_styles,
                                       text_styles=grid_styles.text_styles,
                                       background_padding=background_padding)
        grid_column_list.append(grid_column_dict)

    grid_frame_store = GridFrameStore(type="grid",
                                      name=name,
                                      column_list=grid_column_list,
                                      frame_styles=grid_styles.frame_styles,
                                      column_styles=grid_styles.column_styles,
                                      text_styles=grid_styles.text_styles,
                                      html_frame_styles=grid_styles.html_frame_styles,
                                      html_column_styles=grid_styles.html_column_styles,
                                      html_text_styles=grid_styles.html_text_styles)

    return grid_frame_store
