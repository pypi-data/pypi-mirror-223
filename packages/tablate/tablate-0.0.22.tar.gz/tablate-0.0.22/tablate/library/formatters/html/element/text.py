from tablate.classes.options.html.style.subclasses.TextStyler import TextStyler


def html_text_formatter(text_styler: TextStyler, string: str) -> str:

    text_classnames = text_styler.generate_class_names()

    return f'<div><p class="{text_classnames}">{string}</p></div>'
