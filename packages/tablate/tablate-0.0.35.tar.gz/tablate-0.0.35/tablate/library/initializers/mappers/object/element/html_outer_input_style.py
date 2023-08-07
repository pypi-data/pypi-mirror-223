from tablate.library.checkers.set_key_resolver import set_key_resolver
from tablate.type.type_input import HtmlOuterStylesInput
from tablate.type.type_style import HtmlOuterStyles


def html_outer_input_to_style(html_outer_styles_input: HtmlOuterStylesInput) -> HtmlOuterStyles:

    html_outer_styles_input = html_outer_styles_input if html_outer_styles_input is not None else {}

    html_outer_border_weight = set_key_resolver(instance=html_outer_styles_input, key="html_frame_divider_style", default=None)
    html_outer_border_style = set_key_resolver(instance=html_outer_styles_input, key="html_outer_border_style", default=None)
    html_outer_border_color = set_key_resolver(instance=html_outer_styles_input, key="html_outer_border_color", default=None)
    html_outer_padding = set_key_resolver(instance=html_outer_styles_input, key="html_outer_padding", default=None)
    html_outer_width = set_key_resolver(instance=html_outer_styles_input, key="html_outer_width", default=None)
    html_px_multiplier = set_key_resolver(instance=html_outer_styles_input, key="html_px_multiplier", default=None)
    html_default_colors = set_key_resolver(instance=html_outer_styles_input, key="html_default_colors", default=None)

    return HtmlOuterStyles(
        html_outer_border_weight=html_outer_border_weight,
        html_outer_border_style=html_outer_border_style,
        html_outer_border_color=html_outer_border_color,
        html_outer_padding=html_outer_padding,
        html_outer_width=html_outer_width,
        html_px_multiplier=html_px_multiplier,
        html_default_colors=html_default_colors
    )