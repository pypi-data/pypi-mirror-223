from tablate.classes.options.html.style.subclasses.ElementStyler import ElementStyler


def html_row_head_formatter(row_styler: ElementStyler) -> str:
    return f'<tr class="{row_styler.generate_class_names()}">'


def html_row_foot_formatter() -> str:
    return '</tr>'
