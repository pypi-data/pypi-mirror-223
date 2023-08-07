from tablate.classes.options.html.style.subclasses.ElementStyler import ElementStyler
from tablate.library.formatters.html.element.column import html_column_head_formatter, html_column_foot_formatter
from tablate.library.formatters.html.element.frame import html_frame_head_formatter, html_frame_foot_formatter
from tablate.library.formatters.html.element.row import html_row_head_formatter, html_row_foot_formatter
from tablate.library.formatters.html.element.text import html_text_formatter
from tablate.library.formatters.html.style.elements.style_column import style_column_dict
from tablate.library.formatters.html.style.elements.style_frame import style_frame
from tablate.library.formatters.html.style.elements.style_rows import style_row
from tablate.type.type_global import Globals

from tablate.library.calcs.get_row_colspan import get_row_colspans
from tablate.type.type_store import TableBodyFrameStore


def render_html_table_body(table_body_frame_store: TableBodyFrameStore, global_options: Globals, frame_styler: ElementStyler):

    column_baselines = global_options.html.column_baselines

    colspans = get_row_colspans(table_body_frame_store.column_list, column_baselines)

    # style_frame(frame_store=table_body_frame_store, frame_styler=frame_styler)
    style_row(row_store=table_body_frame_store.html_row_styles, row_styler=frame_styler.row())

    return_html = html_frame_head_formatter(frame_styler=frame_styler)

    for column_index, column_item in enumerate(table_body_frame_store.column_list):
        style_column_dict(column_dict=column_item, column_styler=frame_styler.column(column_index=column_index), html_px_multiplier=table_body_frame_store.html_frame_styles.html_px_multiplier)

    for row_index, row_item in enumerate(table_body_frame_store.row_list):

        row_styler = frame_styler.row(row_index)

        return_html += html_row_head_formatter(row_styler=row_styler)

        for row_column_index, row_column_item in enumerate(table_body_frame_store.column_list):

            column_styler = row_styler.column(row_column_index)

            return_html += html_column_head_formatter(column_styler=column_styler,
                                                      column_index=row_column_index,
                                                      colspans=colspans)

            text_styler = column_styler.text

            return_html += html_text_formatter(text_styler=text_styler,
                                               string=row_item[row_column_item["key"]])

            return_html += html_column_foot_formatter()

        return_html += html_row_foot_formatter()
    return_html += html_frame_foot_formatter()

    return return_html



