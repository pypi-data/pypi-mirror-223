from typing import List

from tablate.classes.options.html.style.subclasses.ElementStyler import ElementStyler
from tablate.type.primitives import HtmlCellElement


def html_column_head_formatter(column_styler: ElementStyler,
                               column_index: int,
                               colspans: List[int],
                               column_element: HtmlCellElement = 'td'):

    return_html = ''

    column_classnames = column_styler.generate_class_names()

    return_html += f'<{column_element} colspan="{colspans[column_index]}" class="{column_classnames}">'

    return return_html


def html_column_foot_formatter(column_element: HtmlCellElement = 'td'):
    return f'</{column_element}>'
