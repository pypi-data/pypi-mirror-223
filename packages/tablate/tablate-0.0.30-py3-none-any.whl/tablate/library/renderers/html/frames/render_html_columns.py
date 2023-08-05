from tablate.classes.options.html.style.subclasses.ElementStyler import ElementStyler
from tablate.library.calcs.get_row_colspan import get_row_colspans
from tablate.library.formatters.html.element.column import html_column_head_formatter, html_column_foot_formatter
from tablate.library.formatters.html.element.frame import html_frame_head_formatter, html_frame_foot_formatter
from tablate.library.formatters.html.element.row import html_row_head_formatter, html_row_foot_formatter
from tablate.library.formatters.html.element.text import html_text_formatter
from tablate.library.formatters.html.style.elements.style_column import style_column_dict
from tablate.library.formatters.html.style.elements.style_frame import style_frame
from tablate.type.primitives import HtmlRowGroupElement, HtmlCellElement, HtmlFrameType
from tablate.type.type_store import BaseFrameStore, FrameStoreUnion
from tablate.type.type_global import Globals


def render_html_column(frame_dict: FrameStoreUnion, global_options: Globals, frame_styler: ElementStyler, frame_type: HtmlFrameType = "body") -> str:

    frame_element: HtmlRowGroupElement
    column_element: HtmlCellElement

    if frame_type == "head":
        frame_element = "tbody"
        column_element = 'th'
    else:
        frame_element = "tbody"
        column_element = 'td'

    column_baselines = global_options.html.column_baselines
    html_px = global_options.html.html_outer_styles.html_px_multiplier

    colspans = get_row_colspans(frame_dict.column_list, column_baselines)

    style_frame(frame_store=frame_dict, frame_styler=frame_styler)

    return_html = html_frame_head_formatter(frame_styler=frame_styler, frame_element=frame_element)

    return_html += html_row_head_formatter(frame_styler.row(0))

    for column_index, column_item in enumerate(frame_dict.column_list):

        column_styler = frame_styler.column(column_index)

        style_column_dict(column_dict=column_item,
                          column_styler=column_styler,
                          html_px_multiplier=frame_dict.html_frame_styles.html_px_multiplier)

        return_html += html_column_head_formatter(column_styler=column_styler,
                                                  column_index=column_index,
                                                  colspans=colspans,
                                                  column_element=column_element)

        text_styler = column_styler.text

        return_html += html_text_formatter(text_styler=text_styler, string=column_item["string"])

        return_html += html_column_foot_formatter(column_element=column_element)
    return_html += html_row_foot_formatter()
    return_html += html_frame_foot_formatter(frame_element=frame_element)

    return return_html
