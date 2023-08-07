from tablate.library.checkers.set_key_resolver import set_key_resolver
from tablate.type.type_input import HtmlFrameStylesInput
from tablate.type.type_style import HtmlFrameStyles


def html_frame_input_to_style(html_frame_styles_input: HtmlFrameStylesInput) -> HtmlFrameStyles:

    html_frame_styles_input = html_frame_styles_input if html_frame_styles_input is not None else {}

    html_frame_divider_style = set_key_resolver(instance=html_frame_styles_input, key="html_frame_divider_style", default=None)
    html_frame_divider_weight = set_key_resolver(instance=html_frame_styles_input, key="html_frame_divider_weight", default=None)
    html_frame_divider_color = set_key_resolver(instance=html_frame_styles_input, key="html_frame_divider_color", default=None)
    html_max_lines = set_key_resolver(instance=html_frame_styles_input, key="html_max_lines", default=None)
    html_multiline = set_key_resolver(instance=html_frame_styles_input, key="html_multiline", default=None)
    html_background = set_key_resolver(instance=html_frame_styles_input, key="html_background", default=None)
    html_px_multiplier = set_key_resolver(instance=html_frame_styles_input, key="html_px_multiplier", default=None)

    return HtmlFrameStyles(
        html_frame_divider_style=html_frame_divider_style,
        html_frame_divider_weight=html_frame_divider_weight,
        html_frame_divider_color=html_frame_divider_color,
        html_max_lines=html_max_lines,
        html_multiline=html_multiline,
        html_background=html_background,
        html_px_multiplier=html_px_multiplier
    )
