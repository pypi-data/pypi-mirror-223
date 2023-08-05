def text_align_attr(text_align: str):
    pass


def text_style_attr(text_style: str):
    pass


def text_color_attr(text_color: str):
    pass


def text_size_attr(text_size: str, px_multiplier: int = None):
    if text_size is None:
        text_size = html_text_size_default
    if px_multiplier is not None:
        text_size = text_size * px_multiplier
    return f"{text_size}px"
