def background_color_attr(color: str):
    colors_map = {
        None: None,
        "white": "white",
        "grey": "lightgray",
        "red": "red",
        "green": "limegreen",
        "yellow": "yellow",
        "blue": "skyblue",
        "magenta": "violet",
        "cyan": "cyan",
        "dark_red": "darkred",
        "dark_green": "green",
        "dark_yellow": "khaki",
        "dark_blue": "royalblue",
        "dark_magenta": "mediumorchid",
        "dark_cyan": "darkturquoise",
        "dark_grey": "darkgray",
        "black": "black",
    }
    return colors_map[color]


def text_color_attr(color):
    colors_map = {
        None: None,
        "white": "white",
        "grey": "darkgray",
        "red": "red",
        "green": "green",
        "yellow": "gold",
        "blue": "dodgerblue",
        "magenta": "orchid",
        "cyan": "turquoise",

        "dark_red": "darkred",
        "dark_green": "darkgreen",
        "dark_yellow": "orange",
        "dark_blue": "darkblue",
        "dark_magenta": "darkviolet",
        "dark_cyan": "darkcyan",
        "dark_grey": "dimgray",

        "black": "black",

    }
    return colors_map[color]
