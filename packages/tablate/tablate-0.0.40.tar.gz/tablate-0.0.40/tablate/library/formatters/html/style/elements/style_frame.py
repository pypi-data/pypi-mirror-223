from tablate.classes.options.html.style.subclasses.ElementStyler import ElementStyler
from tablate.library.formatters.html.style.attributes.divider import divider_attr
from tablate.library.formatters.html.style.elements.style_column import style_column
from tablate.library.formatters.html.style.elements.style_text import style_text

from tablate.type.type_store import FrameStore


def style_frame(frame_store: FrameStore, frame_styler: ElementStyler, is_last_element: bool) -> None:

    divider_style = frame_store.html_frame_styles.html_frame_divider_style
    divider_weight = frame_store.html_frame_styles.html_frame_divider_weight
    divider_color = frame_store.html_frame_styles.html_frame_divider_color
    background = frame_store.html_frame_styles.html_background

    frame_styler.add_style_attribute("padding", "0", " tr")
    frame_styler.add_style_attribute("padding", "0", " th")
    frame_styler.add_style_attribute("padding", "0", " td")


    if not is_last_element:
        frame_styler.add_style_attribute("border-bottom",
                                         divider_attr(divider_style=divider_style,
                                                      divider_weight=divider_weight,
                                                      divider_color=divider_color))
    if background is not None:
        frame_styler.add_style_attribute("background-color", background)

    multiline = frame_store.html_frame_styles.html_multiline
    max_lines = frame_store.html_frame_styles.html_max_lines

    text_styler = frame_styler.text

    if multiline is False or max_lines is not None:
        text_styler.add_style_attribute("display", "-webkit-box")
    text_styler.add_style_attribute("-webkit-box-orient", "vertical")
    text_styler.add_style_attribute("overflow", "hidden")
    if multiline is False:
        text_styler.add_style_attribute("-webkit-line-clamp", 1)
    elif max_lines is not None:
        text_styler.add_style_attribute("-webkit-line-clamp", max_lines)

    style_column(column_store=frame_store.html_column_styles,
                 column_styler=frame_styler.column(),
                 html_px_multiplier=frame_store.html_frame_styles.html_px_multiplier)
    style_text(text_store=frame_store.html_text_styles,
               text_styler=text_styler,
               html_px_multiplier=frame_store.html_frame_styles.html_px_multiplier)





