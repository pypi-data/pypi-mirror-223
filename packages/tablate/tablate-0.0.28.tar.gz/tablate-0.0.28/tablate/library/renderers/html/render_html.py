from tablate.classes.options.html.style.CssStyler import CssStyler
from tablate.library.calcs.calc_column_percent import calc_column_percent
from tablate.library.initializers.append.append import process_frame_list
from tablate.library.initializers.globals_init import globals_init
from tablate.library.renderers.html.render_html_foot import render_html_foot
from tablate.library.renderers.html.render_html_frames import render_html_frames
from tablate.library.renderers.html.render_html_head import render_html_head
from tablate.type.type_store import FrameStoreList
from tablate.type.type_global import Globals


def render_html(frame_list: dict, globals_dict: dict, css_injection: list) -> str:
    global_options = globals_init(**globals_dict)
    processed_frame_list = process_frame_list(frame_list=frame_list, global_options=global_options)

    global_options.html.styler = CssStyler()

    for css_injection in css_injection:
        global_options.html.styler.inject_scoped_css(css_injection["selector"], css_injection["css"], css_injection["sub_selector"])

    global_options.html.styler.inject_css_block(global_options.html.css_injection)

    return_html = ""

    if len(processed_frame_list) > 0:
        processed_frame_list, column_baselines = calc_column_percent(frame_list=processed_frame_list,
                                                                     outer_width=global_options.console.outer_styles.outer_width)
        global_options.html.column_baselines = column_baselines
        return_html += render_html_head(global_options=global_options)
        return_html += render_html_frames(frame_list=processed_frame_list, global_options=global_options)
        return_html += render_html_foot()

    css_head = global_options.html.styler.return_head_styles()
    css_foot = global_options.html.styler.return_foot_styles()

    return_html = f"{css_head}{return_html}{css_foot}"

    return return_html
