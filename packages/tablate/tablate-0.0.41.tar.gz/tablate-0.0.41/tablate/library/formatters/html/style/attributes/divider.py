def divider_attr(divider_style: str, divider_weight: int, divider_color: str) -> str:
    if divider_style == "none":
        border_string = "none"
    elif divider_style == "blank":
        border_string = "none"
    elif divider_style == "thin":
        border_string = f"{divider_weight}px solid {divider_color}"
    elif divider_style == "thick":
        border_string = f"{divider_weight * 2}px solid {divider_color}"
    elif divider_style == "double":
        border_string = f"{divider_weight * 3}px double {divider_color}"
    else:
        border_string = f"{divider_weight}px solid {divider_color}"
    return border_string

# todo: seems not inheriting base styles
