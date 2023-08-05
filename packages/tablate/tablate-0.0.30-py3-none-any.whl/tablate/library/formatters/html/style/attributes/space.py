from typing import Optional

from tablate.type.primitives import HtmlSpacer, HtmlPxMultiplier


def space_attr(html_spacer: Optional[HtmlSpacer], html_px_multiplier: HtmlPxMultiplier):
    space_css = "0"
    edge_space = 0
    if html_spacer is not None:
        if type(html_spacer) == int or type(html_spacer) == str:
            space_css = f"{html_spacer * html_px_multiplier}px"
            edge_space = int(html_spacer) * 2
        if type(html_spacer) == list:
            if len(html_spacer) == 1:
                space_css = f"{html_spacer[0] * html_px_multiplier}px"
                edge_space = int(html_spacer[0]) * 2
            if len(html_spacer) == 2:
                space_css = f"{html_spacer[0] * html_px_multiplier}px {html_spacer[1] * html_px_multiplier}px"
                edge_space = int(html_spacer[1]) * 2
            if len(html_spacer) == 4:
                space_css = f"{html_spacer[0] * html_px_multiplier}px {html_spacer[1] * html_px_multiplier}px {html_spacer[2] * html_px_multiplier}px {html_spacer[3] * html_px_multiplier}px"
                edge_space = int(html_spacer[1]) + int(html_spacer[3])
    return space_css, edge_space
