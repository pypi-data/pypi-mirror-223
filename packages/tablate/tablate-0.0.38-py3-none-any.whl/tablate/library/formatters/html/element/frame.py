from tablate.classes.options.html.style.subclasses.ElementStyler import ElementStyler
from tablate.type.primitives import HtmlRowGroupElement


def html_frame_head_formatter(frame_styler: ElementStyler, frame_element: HtmlRowGroupElement = "tbody") -> str:

    frame_classes = frame_styler.generate_class_names()

    return f'<{frame_element} class="{frame_classes}">'


def html_frame_foot_formatter(frame_element: HtmlRowGroupElement = "tbody") -> str:
    return f'</{frame_element}>'
