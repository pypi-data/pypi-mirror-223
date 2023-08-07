from tablate.classes.options.html.style.subclasses.ElementStyler import ElementStyler
from tablate.library.checkers.set_attr_resolver import set_attr_resolver
from tablate.library.formatters.html.style.attributes.divider import divider_attr
from tablate.type.type_style import HtmlTableRowsStyles


def style_row(row_store: HtmlTableRowsStyles, row_styler: ElementStyler):
    row_divider_style = set_attr_resolver(instance=row_store, attr="html_row_line_divider_style", default=None)
    row_line_divider_color = set_attr_resolver(instance=row_store, attr="html_row_line_divider_color", default=None)
    row_divider_weight = set_attr_resolver(instance=row_store, attr="html_row_line_divider_weight", default=None)
    odds_background = set_attr_resolver(instance=row_store, attr="html_odds_background", default=None)
    evens_background = set_attr_resolver(instance=row_store, attr="html_evens_background", default=None)
    if row_divider_style is not None and row_divider_weight is not None:
        row_styler.add_style_attribute("border-bottom",
                                       divider_attr(divider_style=row_divider_style,
                                                    divider_weight=row_divider_weight,
                                                    divider_color=row_line_divider_color),
                                       sub_selector=":not(:last-child)")
    if odds_background is not None:
        row_styler.add_style_attribute("background-color",
                                       odds_background,
                                       sub_selector=":nth-child(odd)")
    if evens_background is not None:
        row_styler.add_style_attribute("background-color",
                                       evens_background,
                                       sub_selector=":nth-child(even)")