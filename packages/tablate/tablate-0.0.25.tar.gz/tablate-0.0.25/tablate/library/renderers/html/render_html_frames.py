from tablate.library.renderers.html.frames.render_html_columns import render_html_column
from tablate.library.renderers.html.frames.render_html_table_body import render_html_table_body
from tablate.type.type_store import FrameStoreList
from tablate.type.type_global import Globals


def render_html_frames(frame_list: FrameStoreList, global_options: Globals) -> str:

    return_html = ''

    for frame_index, frame_item in enumerate(frame_list):
        frame_item.html_frame_styles.html_px_multiplier = frame_item.html_frame_styles.html_px_multiplier * global_options.html.html_outer_styles.html_px_multiplier
        frame_styler = global_options.html.styler.frame(frame_index)
        if frame_item.type == "grid" or frame_item.type == "text":
            return_html += render_html_column(frame_dict=frame_item,
                                              global_options=global_options,
                                              frame_styler=frame_styler)
        if frame_item.type == "table_header":
            return_html += render_html_column(frame_dict=frame_item,
                                              global_options=global_options,
                                              frame_styler=frame_styler,
                                              frame_type="head")
        if frame_item.type == "table_body":
            return_html += render_html_table_body(table_body_frame_store=frame_item,
                                                  global_options=global_options,
                                                  frame_styler=frame_styler)

    return return_html
