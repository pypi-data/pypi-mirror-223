from tablate.library.checkers.set_key_resolver import set_key_resolver
from tablate.type.type_input import HtmlRowsStylesInput
from tablate.type.type_style import HtmlTableRowsStyles


def html_row_input_to_style(html_row_styles_input: HtmlRowsStylesInput) -> HtmlTableRowsStyles:

    html_row_styles_input = html_row_styles_input if html_row_styles_input is not None else {}

    html_row_line_divider_weight = set_key_resolver(instance=html_row_styles_input, key="html_row_line_divider_weight", default=None)
    html_row_line_divider_style = set_key_resolver(instance=html_row_styles_input, key="html_row_line_divider_style", default=None)
    html_row_line_divider_color = set_key_resolver(instance=html_row_styles_input, key="html_row_line_divider_color", default=None)
    html_odds_background = set_key_resolver(instance=html_row_styles_input, key="html_odds_background", default=None)
    html_evens_background = set_key_resolver(instance=html_row_styles_input, key="html_evens_background", default=None)

    return HtmlTableRowsStyles(
        html_row_line_divider_weight=html_row_line_divider_weight,
        html_row_line_divider_style=html_row_line_divider_style,
        html_row_line_divider_color=html_row_line_divider_color,
        html_odds_background=html_odds_background,
        html_evens_background=html_evens_background
    )