from typing import Union, Any, List

from tablate.library.calcs.calc_column_widths import calc_column_widths
from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.library.initializers.mappers.element.style_mapper import style_mapper
from tablate.library.initializers.mappers.attribute.column_attr import column_attr
from tablate.type.defaults import column_padding_default, background_padding_default, frame_name_default
from tablate.type.type_base import HtmlColumnBase, HtmlFrameBase, HtmlTextBase
from tablate.type.type_global import Globals
from tablate.type.type_input import BaseStylesInput, \
    HtmlStylesInput, HtmlTextFrameStylesInput, BaseColumnInput, GridColumnInput
from tablate.type.primitives import FrameDivider, TextAlign, TextStyle, TextColor, Background, Multiline, MaxLines, \
    ColumnPadding, HtmlPxMultiplier, BackgroundPadding, FrameName
from tablate.type.type_store import GridFrameStore, FrameStore, TextStore


def text_init(text: Union[str, int, float],
              columns: List[Union[str, GridColumnInput]],
              name: FrameName,
              text_style: TextStyle,
              text_align: TextAlign,
              text_color: TextColor,

              frame_divider: FrameDivider,
              frame_padding: ColumnPadding,
              background: Background,
              background_padding: BackgroundPadding,
              multiline: Multiline,
              max_lines: MaxLines,

              html_px_multiplier: HtmlPxMultiplier,
              html_styles: HtmlTextFrameStylesInput,

              global_optiona: Globals) -> GridFrameStore:
    background_padding = background_padding if background_padding is not None else set_attr_resolver(
        instance=global_optiona.console.outer_styles,
        attr="background_padding",
        default=background_padding_default)

    name = name if name is not None else frame_name_default

    html_frame_styles = html_styles.html_frame_styles if hasattr(html_styles, 'html_frame_styles') else HtmlFrameBase()
    html_column_styles = HtmlColumnBase()
    html_text_styles = html_styles.html_text_styles if hasattr(html_styles, 'html_text_styles') else HtmlTextBase()

    text_styles = style_mapper(base_input=BaseStylesInput(frame_styles=FrameStore(frame_divider=frame_divider,
                                                                                  max_lines=max_lines,
                                                                                  multiline=multiline,
                                                                                  background=background),
                                                          text_styles=TextStore(text_style=text_style,
                                                                                text_align=text_align,
                                                                                text_color=text_color)),
                               html_input=HtmlStylesInput(html_frame_styles=html_frame_styles,
                                                          html_column_styles=html_column_styles,
                                                          html_text_styles=html_text_styles),
                               base_defaults=BaseStylesInput(),
                               html_defaults=HtmlStylesInput(),
                               html_px_multiplier=html_px_multiplier,
                               global_options=global_optiona)

    text_column: BaseColumnInput = {
        "string": text,
        "padding": frame_padding if frame_padding else global_optiona.console.column_styles.padding if global_optiona.console.column_styles.padding is not None else column_padding_default,
        "divider": "thin"
    }

    columns = calc_column_widths(columns=[text_column], global_options=global_optiona)
    # todo: pesky warning
    column = column_attr(column_dict=columns[0],
                         frame_styles=text_styles.frame_styles,
                         column_styles=text_styles.column_styles,
                         text_styles=text_styles.text_styles,
                         background_padding=background_padding)

    text_frame_store = GridFrameStore(type="text",
                                      name=name,
                                      column_list=[column],
                                      frame_styles=text_styles.frame_styles,
                                      column_styles=text_styles.column_styles,
                                      text_styles=text_styles.text_styles,
                                      html_frame_styles=text_styles.html_frame_styles,
                                      html_column_styles=text_styles.html_column_styles,
                                      html_text_styles=text_styles.html_text_styles)

    return text_frame_store
