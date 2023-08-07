from tablate.library.checkers.set_key_resolver import set_key_resolver
from tablate.type.type_input import TextStylesInput
from tablate.type.type_style import TextStyles


def base_text_input_to_style(text_input: TextStylesInput) -> TextStyles:

    text_input = text_input if text_input is not None else {}

    text_style = set_key_resolver(instance=text_input, key="text_style", default=None)
    text_align = set_key_resolver(instance=text_input, key="text_align", default=None)
    text_color = set_key_resolver(instance=text_input, key="text_color", default=None)

    return TextStyles(
        text_style=text_style,
        text_align=text_align,
        text_color=text_color
    )
