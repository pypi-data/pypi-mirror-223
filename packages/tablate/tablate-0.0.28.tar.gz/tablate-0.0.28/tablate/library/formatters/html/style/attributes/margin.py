from typing import Optional

from tablate.library.formatters.html.style.attributes.space import space_attr
from tablate.type.primitives import HtmlSpacer, HtmlPxMultiplier


def margin_attr(margin: Optional[HtmlSpacer], html_px_multiplier: HtmlPxMultiplier):
    return space_attr(html_spacer=margin, html_px_multiplier=html_px_multiplier)[0]
