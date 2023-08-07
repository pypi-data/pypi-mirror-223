from tablate.library.checkers.set_key_resolver import set_key_resolver
from tablate.type.type_input import HtmlColumnStylesInput
from tablate.type.type_style import HtmlColumnStyles


def html_column_input_to_style(html_column_styles_input: HtmlColumnStylesInput) -> HtmlColumnStyles:

    html_column_styles_input = html_column_styles_input if html_column_styles_input is not None else {}

    html_column_divider_style = set_key_resolver(instance=html_column_styles_input, key="html_column_divider_style", default=None)
    html_column_divider_weight = set_key_resolver(instance=html_column_styles_input, key="html_column_divider_weight", default=None)
    html_column_divider_color = set_key_resolver(instance=html_column_styles_input, key="html_column_divider_color", default=None)
    html_padding = set_key_resolver(instance=html_column_styles_input, key="html_padding", default=None)

    return HtmlColumnStyles(
        html_column_divider_style=html_column_divider_style,
        html_column_divider_weight=html_column_divider_weight,
        html_column_divider_color=html_column_divider_color,
        html_padding=html_padding
    )
