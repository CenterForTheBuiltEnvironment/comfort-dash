import dash
import dash_mantine_components as dmc
from dash import html
from utils.my_config_file import (
    URLS,
)

dash.register_page(__name__, path=URLS.HOME.value)


layout = dmc.Stack(
    [
        dmc.Title(f"Home page", order=1),
    ]
)
