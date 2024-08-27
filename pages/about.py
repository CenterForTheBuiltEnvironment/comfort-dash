import dash
from dash import html

from utils.my_config_file import (
    URLS,
)

dash.register_page(__name__, path=URLS.ABOUT.value)


layout = html.Div(
    "About page",
)
