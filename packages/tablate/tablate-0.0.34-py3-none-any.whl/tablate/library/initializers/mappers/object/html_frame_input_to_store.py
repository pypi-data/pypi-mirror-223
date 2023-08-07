from typing import Union

from tablate.library.checkers.set_key_resolver import set_key_resolver
from tablate.library.initializers.mappers.object.element.html_column_input_to_style import html_column_input_to_style
from tablate.library.initializers.mappers.object.element.html_frame_input_to_style import html_frame_input_to_style
from tablate.library.initializers.mappers.object.element.html_row_input_style import html_row_input_to_style
from tablate.library.initializers.mappers.object.element.html_text_input_to_style import html_text_input_to_style
from tablate.type.type_input import HtmlTableStylesInput, HtmlGridStylesInput
from tablate.type.type_store import HtmlFrameStore, HtmlTableFrameStore


def html_frame_input_to_store(html_frame_input: Union[HtmlGridStylesInput, HtmlTableStylesInput],
                              frame_type: str) -> Union[HtmlFrameStore, HtmlTableFrameStore]:
    if frame_type == "table":
        return HtmlTableFrameStore(
            html_frame_styles=html_frame_input_to_style(
                set_key_resolver(instance=html_frame_input, key="html_frame_styles",
                                 default={})),
            html_column_styles=html_column_input_to_style(
                set_key_resolver(instance=html_frame_input, key="html_column_styles",
                                 default={})),
            html_row_styles=html_row_input_to_style(
                set_key_resolver(instance=html_frame_input, key="html_row_styles",
                                 default={})),
            html_text_styles=html_text_input_to_style(
                set_key_resolver(instance=html_frame_input, key="html_text_styles",
                                 default={})))
    else:
        return HtmlFrameStore(
            html_frame_styles=html_frame_input_to_style(
                set_key_resolver(instance=html_frame_input, key="html_frame_styles",
                                 default={})),
            html_column_styles=html_column_input_to_style(
                set_key_resolver(instance=html_frame_input, key="html_column_styles",
                                 default={})),
            html_text_styles=html_text_input_to_style(
                set_key_resolver(instance=html_frame_input, key="html_text_styles",
                                 default={})))
