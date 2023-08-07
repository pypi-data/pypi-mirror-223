from typing import Union

from tablate.library.checkers.set_key_resolver import set_key_resolver
from tablate.library.initializers.mappers.object.element.base_column_input_to_style import base_column_input_to_style
from tablate.library.initializers.mappers.object.element.base_frame_input_to_style import base_frame_input_to_style
from tablate.library.initializers.mappers.object.element.base_row_input_to_style import base_row_input_to_style
from tablate.library.initializers.mappers.object.element.base_text_input_to_style import base_text_input_to_style
from tablate.type.type_input import BaseStylesInput, TableBodyFrameStylesInput
from tablate.type.type_store import BaseFrameStore, TableFrameStore, FrameStore


def base_frame_input_to_store(frame_input: Union[BaseStylesInput, TableBodyFrameStylesInput],
                              frame_type: str) -> BaseFrameStore:

    if frame_type == "table":
        return TableFrameStore(
            frame_styles=base_frame_input_to_style(
                set_key_resolver(instance=frame_input, key="frame_styles",
                                 default={})),
            column_styles=base_column_input_to_style(
                set_key_resolver(instance=frame_input, key="column_styles",
                                 default={})),
            row_styles=base_row_input_to_style(
                set_key_resolver(instance=frame_input, key="row_styles",
                                 default={})),
            text_styles=base_text_input_to_style(
                set_key_resolver(instance=frame_input, key="text_styles",
                                 default={})))
    else:
        return FrameStore(
            frame_styles=base_frame_input_to_style(
                set_key_resolver(instance=frame_input, key="frame_styles",
                                 default={})),
            column_styles=base_column_input_to_style(
                set_key_resolver(instance=frame_input, key="column_styles",
                                 default={})),
            text_styles=base_text_input_to_style(
                set_key_resolver(instance=frame_input, key="text_styles",
                                 default={})))
