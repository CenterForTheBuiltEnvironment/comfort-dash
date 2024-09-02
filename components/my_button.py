from dash import dcc
import dash_mantine_components as dmc

from utils.my_config_file import URLS


def my_button(
    text: str,
    color: str = "blue",
    variant: str = "light",
    margin_top: str = "xs",
    full_width: bool = True,
    radius: str = "md",
    font_weight: int = 700,
    href: str = URLS.HOME.value,
    style=None,
):
    if style is None:
        style = {"text-decoration": "none"}
    return dcc.Link(
        dmc.Button(
            text,
            variant=variant,
            color=color,
            fullWidth=full_width,
            mt=margin_top,
            radius=radius,
            fw=font_weight,
        ),
        style=style,
        href=href,
    )
