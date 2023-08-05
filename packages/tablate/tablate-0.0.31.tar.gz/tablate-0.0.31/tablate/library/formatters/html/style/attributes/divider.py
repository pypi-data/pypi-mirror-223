def divider_attr(divider_style: str, divider_weight) -> str:
    if divider_style == "none":
        border_string = "none"
    elif divider_style == "blank":
        border_string = "none"
    elif divider_style == "thin":
        border_string = f"{divider_weight}px solid"
    elif divider_style == "thick":
        border_string = f"{divider_weight * 2}px solid"
    elif divider_style == "double":
        border_string = f"{divider_weight * 3}px double"
    else:
        border_string = f"{divider_weight}px solid"
    return border_string