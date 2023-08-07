from tablate.library.checkers.set_key_resolver import set_key_resolver
from tablate.type.type_input import HtmlTextStylesInput
from tablate.type.type_style import HtmlTextStyles


def html_text_input_to_style(html_text_styles_input: HtmlTextStylesInput) -> HtmlTextStyles:

    html_text_styles_input = html_text_styles_input if html_text_styles_input is not None else {}

    html_text_style = set_key_resolver(instance=html_text_styles_input, key="html_text_style", default=None)
    html_text_align = set_key_resolver(instance=html_text_styles_input, key="html_text_align", default=None)
    html_text_color = set_key_resolver(instance=html_text_styles_input, key="html_text_color", default=None)
    html_text_size = set_key_resolver(instance=html_text_styles_input, key="html_text_size", default=None)

    return HtmlTextStyles(
        html_text_style=html_text_style,
        html_text_align=html_text_align,
        html_text_color=html_text_color,
        html_text_size=html_text_size
    )
