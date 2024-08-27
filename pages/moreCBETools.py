import dash
from dash import html

from utils.my_config_file import (
    URLS,
)

dash.register_page(__name__, path=URLS.Tools.value)


layout = html.Div(
    "More CBE tools can be found here",
)
