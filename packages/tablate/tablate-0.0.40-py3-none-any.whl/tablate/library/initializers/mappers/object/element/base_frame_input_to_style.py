from tablate.library.checkers.set_key_resolver import set_key_resolver
from tablate.type.type_input import FrameStylesInput
from tablate.type.type_style import FrameStyles


def base_frame_input_to_style(frame_styles_input: FrameStylesInput) -> FrameStyles:

    frame_styles_input = frame_styles_input if frame_styles_input is not None else {}

    frame_divider = set_key_resolver(instance=frame_styles_input, key="frame_divider", default=None)
    max_lines = set_key_resolver(instance=frame_styles_input, key="max_lines", default=None)
    multiline = set_key_resolver(instance=frame_styles_input, key="multiline", default=None)
    background = set_key_resolver(instance=frame_styles_input, key="background", default=None)
    trunc_value = set_key_resolver(instance=frame_styles_input, key="trunc_value", default=None)

    return FrameStyles(
        frame_divider=frame_divider,
        max_lines=max_lines,
        multiline=multiline,
        background=background,
        trunc_value=trunc_value
    )
